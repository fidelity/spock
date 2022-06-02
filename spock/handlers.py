# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""I/O handlers for various file formats"""

import json
import os
import re
from abc import ABC, abstractmethod
from pathlib import Path, PurePosixPath
from typing import ByteString, Dict, Optional, Tuple, Union
from warnings import warn

import pytomlpp
import yaml

from spock._version import get_versions
from spock.utils import _T, check_path_s3, path_object_to_s3path

__version__ = get_versions()["version"]


class Handler(ABC):
    """Base class for file type loaders

    ABC for loaders

    """

    def load(self, path: Path, s3_config: Optional[_T] = None) -> Dict:
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
    def _load(self, path: str) -> Dict:
        """Private load function for file type

        Args:
            path: path to file

        Returns:
            dictionary of read file

        """
        raise NotImplementedError

    def _write_crypto(
        self,
        value: Union[str, ByteString],
        path: Path,
        name: str,
        crypto_name: str,
        create_path: bool,
        s3_config: Optional[_T],
    ):
        """Write values of the underlying cryptography data used to encode some spock values

        Args:
            value: current crypto attribute
            path: path to write out
            name: spock generated file name
            create_path: boolean to create the path if non-existent (for non S3)
            s3_config: optional s3 config object if using s3 storage
            crypto_name: name of the crypto attribute

        Returns:
            None

        """
        # Convert ByteString to str
        value = value.decode("utf-8") if isinstance(value, ByteString) else value
        write_path, is_s3 = self._handle_possible_s3_save_path(
            path=path, name=name, create_path=create_path, s3_config=s3_config
        )
        # We need to shim in the crypto value name into the name used for S3
        name_root, name_extension = os.path.splitext(name)
        name = f"{name_root}.{crypto_name}.yaml"
        # Also need to shim the crypto name into the full path
        root, extension = os.path.splitext(write_path)
        full_name = f"{root}.{crypto_name}.yaml"
        YAMLHandler.write({crypto_name: value}, full_name)
        # After write check if it needs to be pushed to S3
        if is_s3:
            self._check_s3_write(write_path, path, name, s3_config)

    def save(
        self,
        out_dict: Dict,
        info_dict: Optional[Dict],
        library_dict: Optional[Dict],
        path: Path,
        name: str,
        create_path: bool = False,
        s3_config: Optional[_T] = None,
        salt: Optional[str] = None,
        key: Optional[ByteString] = None,
    ):
        """Write function for file type

        This will handle local or s3 writes with the boolean is_s3 flag. If detected it will conditionally import
        the necessary addons to handle the upload

        Args:
            out_dict: payload to write
            info_dict: info payload to write
            library_dict: package info to write
            path: path to write out
            name: spock generated file name
            create_path: boolean to create the path if non-existent (for non S3)
            s3_config: optional s3 config object if using s3 storage
            salt: string of the salt used for crypto
            key: ByteString of the key used for crypto

        Returns:
        """
        write_path, is_s3 = self._handle_possible_s3_save_path(
            path=path, name=name, create_path=create_path, s3_config=s3_config
        )
        write_path = self._save(
            out_dict=out_dict,
            info_dict=info_dict,
            library_dict=library_dict,
            path=write_path,
        )
        # After write check if it needs to be pushed to S3
        if is_s3:
            self._check_s3_write(write_path, path, name, s3_config)
        # Write the crypto files if needed
        if (salt is not None) and (key is not None):
            # If the values are not none then write the salt and key into individual files
            self._write_crypto(salt, path, name, "salt", create_path, s3_config)
            self._write_crypto(key, path, name, "key", create_path, s3_config)

    @staticmethod
    def _check_s3_write(
        write_path: str, path: Path, name: str, s3_config: Optional[_T]
    ):
        """Handles writing to S3 if necessary

        Args:
            write_path: path the file was written to locally
            path: original path specified
            name: original file name
            s3_config: optional s3 config object if using s3 storage

        Returns:

        """
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
        self,
        out_dict: Dict,
        info_dict: Optional[Dict],
        library_dict: Optional[Dict],
        path: str,
    ) -> str:
        """Write function for file type

        Args:
            out_dict: payload to write
            info_dict: info payload to write
            library_dict: package info to write
            path: path to write out

        Returns:
        """
        raise NotImplementedError

    @staticmethod
    def _handle_possible_s3_load_path(
        path: Path, s3_config: Optional[_T] = None
    ) -> Union[str, Path]:
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
        path: Path, name: str, create_path: bool, s3_config: Optional[_T] = None
    ) -> Tuple[str, bool]:
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
    def write_extra_info(
        path: str,
        info_dict: Dict,
        version: bool = True,
        write_mode: str = "w+",
        newlines: Optional[int] = None,
        header: Optional[str] = None,
    ):
        """Writes extra info to commented newlines

        Args:
            path: path to write out
            info_dict: info payload to write
            version: write the spock version string first
            write_mode: write mode for the file
            newlines: number of new lines to add to start

        Returns:
        """
        # Write the commented info as new lines
        with open(path, write_mode) as fid:
            if newlines is not None:
                for _ in range(newlines):
                    fid.write("\n")
            if header is not None:
                fid.write(header)
            # Write a spock header
            if version:
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

    def _load(self, path: str) -> Dict:
        """YAML load function

        Args:
            path: path to YAML file

        Returns:
            base_payload: dictionary of read file

        """
        file_contents = open(path, "r").read()
        base_payload = yaml.safe_load(file_contents)
        return base_payload

    def _save(
        self,
        out_dict: Dict,
        info_dict: Optional[Dict],
        library_dict: Optional[Dict],
        path: str,
    ) -> str:
        """Write function for YAML type

        Args:
            out_dict: payload to write
            info_dict: info payload to write
            library_dict: package info to write
            path: path to write out
        Returns:
        """
        # First write the commented info
        self.write_extra_info(path=path, info_dict=info_dict)
        # Remove aliases in YAML dump
        yaml.Dumper.ignore_aliases = lambda *args: True
        self.write(out_dict, path)
        # Write the library info at the bottom
        self.write_extra_info(
            path=path,
            info_dict=library_dict,
            version=False,
            write_mode="a",
            newlines=2,
            header="################\n# Package Info #\n################\n",
        )
        return path

    @staticmethod
    def write(write_dict: Dict, path: str):
        # Remove aliases in YAML dump
        yaml.Dumper.ignore_aliases = lambda *args: True
        with open(path, "a") as yaml_fid:
            yaml.safe_dump(write_dict, yaml_fid, default_flow_style=False)


class TOMLHandler(Handler):
    """TOML class for loading TOML config files

    Base TOML class

    """

    def _load(self, path: str) -> Dict:
        """TOML load function

        Args:
            path: path to TOML file

        Returns:
            base_payload: dictionary of read file

        """
        base_payload = pytomlpp.load(path)
        return base_payload

    def _save(
        self,
        out_dict: Dict,
        info_dict: Optional[Dict],
        library_dict: Optional[Dict],
        path: str,
    ) -> str:
        """Write function for TOML type

        Args:
            out_dict: payload to write
            info_dict: info payload to write
            library_dict: package info to write
            path: path to write out

        Returns:
        """
        # First write the commented info
        self.write_extra_info(path=path, info_dict=info_dict)
        with open(path, "a") as toml_fid:
            pytomlpp.dump(out_dict, toml_fid)
        # Write the library info at the bottom
        self.write_extra_info(
            path=path, info_dict=library_dict, version=False, write_mode="a", newlines=2
        )
        return path


class JSONHandler(Handler):
    """JSON class for loading JSON config files

    Base JSON class

    """

    def _load(self, path: str) -> Dict:
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
        self,
        out_dict: Dict,
        info_dict: Optional[Dict],
        library_dict: Optional[Dict],
        path: str,
    ) -> str:
        """Write function for JSON type

        Args:
            out_dict: payload to write
            info_dict: info payload to write
            library_dict: package info to write
            path: path to write out

        Returns:
        """
        if (info_dict is not None) or (library_dict is not None):
            warn(
                "JSON does not support comments and thus cannot save extra info to file... removing extra info"
            )
        with open(path, "a") as json_fid:
            json.dump(out_dict, json_fid, indent=4, separators=(",", ": "))
        return path
