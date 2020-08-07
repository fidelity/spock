# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""I/O handlers for various file formats"""

from abc import ABC
from abc import abstractmethod
import json
import re
import toml
import yaml


class Handler(ABC):
    """Base class for file type loaders

    ABC for loaders

    """
    @abstractmethod
    def load(self, path):
        """Load function for file type

        *Args*:

            path: path to file

        *Returns*:


        """
        raise NotImplementedError

    @abstractmethod
    def save(self, out_dict, path):
        """Write function for file type

        *Args*:

            out_dict: payload to write
            path: path to write out

        *Returns*:

        """
        raise NotImplementedError


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

    def load(self, path):
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

    def save(self, out_dict, path):
        """Write function for YAML type

        *Args*:

            out_dict: payload to write
            path: path to write out

        *Returns*:

        """
        yaml.dump(out_dict, path, default_flow_style=False)


class TOMLHandler(Handler):
    """TOML class for loading TOML config files

    Base TOML class

    """
    def load(self, path):
        """TOML load function

        *Args*:

            path: path to TOML file

        Returns:

            base_payload: dictionary of read file

        """
        base_payload = toml.load(path)
        return base_payload

    def save(self, out_dict, path):
        """Write function for TOML type

        *Args*:

            out_dict: payload to write
            path: path to write out

        *Returns*:

        """
        toml.dump(out_dict, path)


class JSONHandler(Handler):
    """JSON class for loading JSON config files

    Base JSON class

    """
    def load(self, path):
        """JSON load function

        *Args*:

            path: path to JSON file

        Returns:

            base_payload: dictionary of read file

        """
        with open(path) as json_fid:
            base_payload = json.load(json_fid)
        return base_payload

    def save(self, out_dict, path):
        """Write function for JSON type

        *Args*:

            out_dict: payload to write
            path: path to write out

        *Returns*:

        """
        with open(path.name, 'w') as json_fid:
            json.dump(out_dict, json_fid, indent=4, separators=(',', ': '))
