# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""I/O handlers for various file formats"""

import json
import os
import re
import typing
from abc import ABC, abstractmethod
from pathlib import Path, PurePosixPath
from warnings import warn

import pytomlpp
import yaml

from spock._version import get_versions
from spock.utils import check_path_s3, path_object_to_s3path

__version__ = get_versions()["version"]


class Handler(ABC):
    """Base class for file type loaders

    ABC for loaders

    """

    def load(self, path: Path, s3_config=None) -> typing.Dict:
        """Load function for file type

        This handles s3 path conversion for all handler types pre load call

        Args:
            path: path to file
            s3_config: optional s3 config object if using s3 storage

        Returns:
            dictionary of read file

        """
        path = self._handle_possible_s3_load_path(path=path, s3_config=s3_config)
        return self._post_process_config_paths(self._load(path=path))

    @staticmethod
    def _post_process_config_paths(payload):
        """
        Transform path string into path object
        """
        if (payload is not None) and "config" in payload:
            payload["config"] = [Path(c) for c in payload["config"]]

        return payload

    @abstractmethod
    def _load(self, path: str) -> typing.Dict:
        """Private load function for file type

        Args:
            path: path to file

        Returns:
            dictionary of read file

        """
        raise NotImplementedError

    def save(
        self,
        out_dict: typing.Dict,
        info_dict: typing.Optional[typing.Dict],
        path: Path,
        name: str,
        create_path: bool = False,
        s3_config=None,
    ):
        """Write function for file type

        This will handle local or s3 writes with the boolean is_s3 flag. If detected it will conditionally import
        the necessary addons to handle the upload

        Args:
            out_dict: payload to write
            info_dict: info payload to write
            path: path to write out
            name: spock generated file name
            create_path: boolean to create the path if non-existent (for non S3)
            s3_config: optional s3 config object if using s3 storage

        Returns:
        """
        write_path, is_s3 = self._handle_possible_s3_save_path(
            path=path, name=name, create_path=create_path, s3_config=s3_config
        )
        write_path = self._save(out_dict=out_dict, info_dict=info_dict, path=write_path)
        # After write check if it needs to be pushed to S3
        if is_s3:
            try:
                from spock.addons.s3.utils import handle_s3_save_path

                handle_s3_save_path(
                    temp_path=write_path,
                    s3_path=str(PurePosixPath(path)),
                    name=name,
                    s3_config=s3_config,
                )
            except ImportError:
                print("Error importing spock s3 utils after detecting s3:// save path")

    @abstractmethod
    def _save(
        self, out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str
    ) -> str:
        """Write function for file type

        Args:
            out_dict: payload to write
            info_dict: info payload to write
            path: path to write out

        Returns:
        """
        raise NotImplementedError

    @staticmethod
    def _handle_possible_s3_load_path(
        path: Path, s3_config=None
    ) -> typing.Union[str, Path]:
        """Handles the possibility of having to handle loading from a S3 path

        Checks to see if it detects a S3 uri and if so triggers imports of s3 functionality and handles the file
        download

        Args:
            path: spock config path
            s3_config: optional s3 configuration object

        Returns:
            path: current path for the configuration file

        """
        is_s3 = check_path_s3(path=path)
        if is_s3:
            try:
                from spock.addons.s3.utils import handle_s3_load_path

                s3_path = path_object_to_s3path(path)
                path = handle_s3_load_path(path=s3_path, s3_config=s3_config)
            except ImportError:
                print("Error importing spock s3 utils after detecting s3:// load path")
        return path

    @staticmethod
    def _handle_possible_s3_save_path(
        path: Path, name: str, create_path: bool, s3_config=None
    ) -> typing.Tuple[str, bool]:
        """Handles the possibility of having to save to a S3 path

        Checks to see if it detects a S3 uri and if so generates a tmp location to write the file to pre-upload

        Args:
            path: save path
            name: spock generated file name
            create_path: create the path for non s3 data
            s3_config: s3 config object

        Returns:
        """
        is_s3 = check_path_s3(path=path)
        if is_s3:
            if s3_config is None:
                raise ValueError(
                    "Save to S3 -- Missing S3Config object which is necessary to handle S3 style paths"
                )
            write_path = f"{s3_config.temp_folder}/{name}"
            # Strip double slashes if exist
            write_path = write_path.replace(r"//", r"/")
        else:
            # Handle the path logic for non S3
            if not os.path.exists(path) and create_path:
                os.makedirs(path)
            write_path = f"{path}/{name}"
        return write_path, is_s3

    @staticmethod
    def write_extra_info(path, info_dict):
        """Writes extra info to commented newlines

        Args:
            path: path to write out
            info_dict: info payload to write

        Returns:
        """
        # Write the commented info as new lines
        with open(path, "w+") as fid:
            # Write a spock header
            fid.write(f"# Spock Version: {__version__}\n")
            # Write info dict if not None
            if info_dict is not None:
                for k, v in info_dict.items():
                    fid.write(f"{k}: {v}\n")
            fid.write("\n")


class YAMLHandler(Handler):
    """YAML class for loading YAML config files

    Base YAML class

    """

    # override default SafeLoader behavior to correctly
    # interpret 1e1 (as opposed to 1.e+1) as 10
    # https://stackoverflow.com/questions/30458977/yaml-loads-5e-6-as-string-and-not-a-number/30462009#30462009
    yaml.SafeLoader.add_implicit_resolver(
        "tag:yaml.org,2002:float",
        re.compile(
            """^(?:
         [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
        |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
        |\\.[0-9_]+(?:[eE][-+][0-9]+)?
        |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
        |[-+]?\\.(?:inf|Inf|INF)
        |\\.(?:nan|NaN|NAN))$""",
            re.X,
        ),
        list("-+0123456789."),
    )

    def _load(self, path: str) -> typing.Dict:
        """YAML load function

        Args:
            path: path to YAML file

        Returns:
            base_payload: dictionary of read file

        """
        file_contents = open(path, "r").read()
        file_contents = re.sub(r"--([a-zA-Z0-9_]*)", r"\g<1>: True", file_contents)
        base_payload = yaml.safe_load(file_contents)
        return base_payload

    def _save(
        self, out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str
    ):
        """Write function for YAML type

        Args:
            out_dict: payload to write
            info_dict: info payload to write
            path: path to write out

        Returns:
        """
        # First write the commented info
        self.write_extra_info(path=path, info_dict=info_dict)
        # Remove aliases in YAML dump
        yaml.Dumper.ignore_aliases = lambda *args: True
        with open(path, "a") as yaml_fid:
            yaml.safe_dump(out_dict, yaml_fid, default_flow_style=False)
        return path


class TOMLHandler(Handler):
    """TOML class for loading TOML config files

    Base TOML class

    """

    def _load(self, path: str) -> typing.Dict:
        """TOML load function

        Args:
            path: path to TOML file

        Returns:
            base_payload: dictionary of read file

        """
        base_payload = pytomlpp.load(path)
        return base_payload

    def _save(
        self, out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str
    ):
        """Write function for TOML type

        Args:
            out_dict: payload to write
            info_dict: info payload to write
            path: path to write out

        Returns:
        """
        # First write the commented info
        self.write_extra_info(path=path, info_dict=info_dict)
        with open(path, "a") as toml_fid:
            pytomlpp.dump(out_dict, toml_fid)
        return path


class JSONHandler(Handler):
    """JSON class for loading JSON config files

    Base JSON class

    """

    def _load(self, path: str) -> typing.Dict:
        """JSON load function

        Args:
            path: path to JSON file

        Returns:
            base_payload: dictionary of read file

        """
        with open(path) as json_fid:
            base_payload = json.load(json_fid)
        return base_payload

    def _save(
        self, out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str
    ):
        """Write function for JSON type

        Args:
            out_dict: payload to write
            info_dict: info payload to write
            path: path to write out

        Returns:
        """
        if info_dict is not None:
            warn(
                "JSON does not support comments and thus cannot save extra info to file... removing extra info"
            )
        with open(path, "a") as json_fid:
            json.dump(out_dict, json_fid, indent=4, separators=(",", ": "))
        return path
