# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""I/O handlers for various file formats"""

from abc import ABC
from abc import abstractmethod
import json
import re
from spock import __version__
from spock.utils import check_path_s3
import toml
import typing
from warnings import warn
import yaml


class Handler(ABC):
    """Base class for file type loaders

    ABC for loaders

    """
    def load(self, path: str, s3_config=None) -> typing.Dict:
        """Load function for file type

        This handles s3 path conversion for all handler types pre load call

        *Args*:

            path: path to file
            s3_config: optional s3 config object if using s3 storage

        *Returns*:

            dictionary of read file

        """
        path = self._handle_possible_s3_load_path(path=path, s3_config=s3_config)
        return self._load(path=path)

    @abstractmethod
    def _load(self, path: str) -> typing.Dict:
        """Private load function for file type

        *Args*:

            path: path to file

        *Returns*:

            dictionary of read file

        """
        raise NotImplementedError

    @abstractmethod
    def save(self, out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str, s3_config=None):
        """Write function for file type

        *Args*:

            out_dict: payload to write
            info_dict: info payload to write
            path: path to write out

        *Returns*:

        """
        raise NotImplementedError

    @staticmethod
    def _handle_possible_s3_load_path(path: str, s3_config=None) -> str:
        """Handles the possibility of having to handle a S3 file

        Checks to see if it detects a S3 uri and if so triggers imports of s3 functionality and handles the file
        download

        *Args*:

            path: spock config path
            s3_config: optional s3 configuration object

        *Returns*:

            path: current path for the configuration file

        """
        is_s3 = check_path_s3(path=path)
        if is_s3:
            try:
                from spock.backend.s3.utils import handle_s3_load_path
                path = handle_s3_load_path(path=path, s3_config=s3_config)
            except ImportError:
                print('Error importing s3 utils after detecting s3:// path')
        return path

    @staticmethod
    def write_extra_info(path, info_dict):
        """Writes extra info to commented newlines

        *Args*:

            path: path to write out
            info_dict: info payload to write

        *Returns*:

        """
        # Write the commented info as new lines
        with open(path.name, 'w+') as fid:
            # Write a spock header
            fid.write(f'# Spock Version: {__version__}\n')
            # Write info dict if not None
            if info_dict is not None:
                for k, v in info_dict.items():
                    fid.write(f'{k}: {v}\n')
            fid.write('\n')


class YAMLHandler(Handler):
    """YAML class for loading YAML config files

    Base YAML class

    """
    # override default SafeLoader behavior to correctly
    # interpret 1e1 (as opposed to 1.e+1) as 10
    # https://stackoverflow.com/questions/30458977/yaml-loads-5e-6-as-string-and-not-a-number/30462009#30462009
    yaml.SafeLoader.add_implicit_resolver(
        u'tag:yaml.org,2002:float',
        re.compile(u'''^(?:
         [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
        |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
        |\\.[0-9_]+(?:[eE][-+][0-9]+)?
        |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
        |[-+]?\\.(?:inf|Inf|INF)
        |\\.(?:nan|NaN|NAN))$''', re.X),
        list(u'-+0123456789.')
    )

    def _load(self, path: str) -> typing.Dict:
        """YAML load function

        *Args*:

            path: path to YAML file

        *Returns*:

            base_payload: dictionary of read file

        """
        file_contents = open(path, 'r').read()
        file_contents = re.sub(r'--([a-zA-Z0-9_]*)', r'\g<1>: True', file_contents)
        base_payload = yaml.safe_load(file_contents)
        return base_payload

    def save(self, out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str, s3_config=None):
        """Write function for YAML type

        *Args*:

            out_dict: payload to write
            info_dict: info payload to write
            path: path to write out

        *Returns*:

        """
        # First write the commented info
        self.write_extra_info(path=path, info_dict=info_dict)
        # Remove aliases in YAML dump
        yaml.Dumper.ignore_aliases = lambda *args: True
        with open(path.name, 'a') as yaml_fid:
            yaml.safe_dump(out_dict, yaml_fid, default_flow_style=False)


class TOMLHandler(Handler):
    """TOML class for loading TOML config files

    Base TOML class

    """
    def _load(self, path: str) -> typing.Dict:
        """TOML load function

        *Args*:

            path: path to TOML file

        Returns:

            base_payload: dictionary of read file

        """
        base_payload = toml.load(path)
        return base_payload

    def save(self, out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str, s3_config=None):
        """Write function for TOML type

        *Args*:

            out_dict: payload to write
            info_dict: info payload to write
            path: path to write out

        *Returns*:

        """
        # First write the commented info
        self.write_extra_info(path=path, info_dict=info_dict)
        with open(path.name, 'a') as toml_fid:
            toml.dump(out_dict, toml_fid)


class JSONHandler(Handler):
    """JSON class for loading JSON config files

    Base JSON class

    """
    def _load(self, path: str) -> typing.Dict:
        """JSON load function

        *Args*:

            path: path to JSON file

        Returns:

            base_payload: dictionary of read file

        """
        with open(path) as json_fid:
            base_payload = json.load(json_fid)
        return base_payload

    def save(self, out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str, s3_config=None):
        """Write function for JSON type

        *Args*:

            out_dict: payload to write
            info_dict: info payload to write
            path: path to write out

        *Returns*:

        """
        if info_dict is not None:
            warn('JSON does not support comments and thus cannot save extra info to file... removing extra info')
            info_dict = None
        with open(path.name, 'a') as json_fid:
            json.dump(out_dict, json_fid, indent=4, separators=(',', ': '))
