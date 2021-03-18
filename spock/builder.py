# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the building/saving of the configurations from the Spock config classes"""

from pathlib import Path
import attr
from spock.backend.attr.builder import AttrBuilder
from spock.backend.attr.payload import AttrPayload
from spock.backend.attr.saver import AttrSaver
from spock.backend.base import Spockspace
from spock.utils import check_payload_overwrite
from spock.utils import deep_payload_update


class ConfigArgBuilder:
    """Automatically generates dataclass instances from config file(s)

    This class builds out necessary arguments from *args classes, reads
    the arguments from specified config file(s), and subsequently (via chained
    call to generate) generates each class instance based on the necessary
    field values for each backend class instance

    *Attributes*:

        _arg_namespace: generated argument namespace
        _builder_obj: instance of a BaseBuilder class
        _create_save_path: boolean to make the path to save to
        _dict_args: dictionary args from the command line
        _payload_obj: instance of a BasePayload class
        _saver_obj: instance of a BaseSaver class

    """
    def __init__(self, *args, configs=None, create_save_path=False, desc='', no_cmd_line=False, **kwargs):
        backend = self._set_backend(args)
        self._create_save_path = create_save_path
        self._builder_obj = backend.get('builder')(
            *args, configs=configs, create_save_path=create_save_path, desc=desc, no_cmd_line=no_cmd_line, **kwargs)
        self._payload_obj = backend.get('payload')
        self._saver_obj = backend.get('saver')()
        try:
            self._dict_args = self._get_payload()
            self._arg_namespace = self._builder_obj.generate(self._dict_args)
        except Exception as e:
            self._builder_obj.print_usage_and_exit(str(e), sys_exit=False)
            raise ValueError(e)

    def __call__(self, *args, **kwargs):
        """Call to self to allow chaining

        *Args*:

            *args: non-keyword args
            **kwargs: keyword args

        *Returns*:

            ConfigArgBuilder: self instance
        """
        return ConfigArgBuilder(*args, **kwargs)

    def generate(self, unclass=False):
        """Generate method that returns the actual argument namespace

        *Args*:

            unclass: swaps the backend attr class type for dictionaries

        *Returns*:

            argument namespace consisting of all config classes

        """
        if unclass:
            self._arg_namespace = Spockspace(**{k: Spockspace(**{
                val.name: getattr(v, val.name) for val in v.__attrs_attrs__})
                                                for k, v in self._arg_namespace.__dict__.items()})
        return self._arg_namespace

    @staticmethod
    def _set_backend(args):
        """Determines which backend class to use

        *Args*:

            args: list of classes passed to the builder

        *Returns*:

            backend: class of backend

        """
        # Gather if all attr backend
        type_attrs = all([attr.has(arg) for arg in args])
        if not type_attrs:
            raise TypeError("*args must be of all attrs backend")
        elif type_attrs:
            backend = {'builder': AttrBuilder, 'payload': AttrPayload, 'saver': AttrSaver}
        else:
            raise TypeError("*args must be of all attrs backend")
        return backend

    def _get_config_paths(self):
        """Get config paths from all methods

        Config paths can enter from either the command line or be added in the class init call
        as a kwarg (configs=[])

        *Returns*:

            args: namespace of args

        """
        # Call the objects get_config_paths function
        args = self._builder_obj.get_config_paths()
        return args

    def _get_payload(self):
        """Get the parameter payload from the config file(s)

        Calls the various ways to get configs and then parses to retrieve the parameter payload - make sure to call
        deep update so as to not lose some parameters when only partially updating the payload

        *Returns*:

            payload: dictionary of parameter values

        """
        args = self._get_config_paths()
        if args.help:
            # Call sys exit with a clean code as this is the help call which is not unexpected behavior
            self._builder_obj.print_usage_and_exit(sys_exit=True, exit_code=0)
        payload = {}
        dependencies = {'paths': [], 'rel_paths': [], 'roots': []}
        for configs in args.config:
            payload_update = self._payload_obj().payload(self._builder_obj.input_classes, configs, args, dependencies)
            check_payload_overwrite(payload, payload_update, configs)
            deep_payload_update(payload, payload_update)
        return payload

    def save(self, user_specified_path=None, extra_info=True, file_extension='.yaml'):
        """Saves the current config setup to file with a UUID

        *Args*:

            user_specified_path: if user provides a path it will be used as the path to write
            extra_info: additional info to write to saved config (run date and git info)
            file_extension: file type to write (default: yaml)

        *Returns*:

            self so that functions can be chained
        """
        if user_specified_path is not None:
            save_path = Path(user_specified_path)
        elif self._builder_obj.save_path is not None:
            save_path = Path(self._builder_obj.save_path)
        else:
            raise ValueError('Save did not receive a valid path from: (1) markup file(s) or (2) '
                             'the keyword arg user_specified_path')
        # Call the saver class and save function
        self._saver_obj.save(self._arg_namespace, save_path, self._create_save_path, extra_info, file_extension)
        return self
