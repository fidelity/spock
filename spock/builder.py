# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the building/saving of the configurations from the Spock config classes"""

from pathlib import Path
import attr
from spock.backend.builder import AttrBuilder
from spock.backend.payload import AttrPayload
from spock.backend.saver import AttrSaver
from spock.utils import check_payload_overwrite
from spock.utils import deep_payload_update
import typing


class ConfigArgBuilder:
    """Automatically generates dataclass instances from config file(s)

    This class builds out necessary arguments from *args classes, reads
    the arguments from specified config file(s), and subsequently (via chained
    call to generate) generates each class instance based on the necessary
    field values for each backend class instance

    *Attributes*:

        _arg_namespace: generated argument namespace
        _builder_obj: instance of a BaseBuilder class
        _dict_args: dictionary args from the command line
        _payload_obj: instance of a BasePayload class
        _saver_obj: instance of a BaseSaver class

    """
    def __init__(self, *args, configs: typing.Optional[typing.List] = None,
                 desc: str = '', no_cmd_line: bool = False, s3_config=None, **kwargs):
        """Init call for ConfigArgBuilder

        *Args*:

            *args: tuple of spock decorated classes to process
            configs: list of config paths
            desc: description for help
            no_cmd_line: turn off cmd line args
            s3_config: s3Config object for S3 support
            **kwargs: keyword args

        """
        backend = self._set_backend(args)
        fixed_args, tune_args = self._strip_tune_parameters(args)
        self._builder_obj = backend.get('builder')(
            *fixed_args, configs=configs, desc=desc, no_cmd_line=no_cmd_line, **kwargs
        )
        if len(tune_args) > 0:
            try:
                from spock.addons.tune.optuna import OptunaBuilder
                self._tuner_obj = OptunaBuilder(
                    *tune_args, configs=configs, no_cmd_line=no_cmd_line
                )
            except ImportError:
                print(
                    'Missing libraries to support tune functionality. Please re-install with the extra tune '
                    'dependencies -- pip install spock-config[tune]')
        self._payload_obj = backend.get('payload')(s3_config=s3_config)
        self._saver_obj = backend.get('saver')(s3_config=s3_config)
        try:
            self._dict_args = self._get_payload(ignore_args=tune_args)
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

    def generate(self):
        """Generate method that returns the actual argument namespace


        *Returns*:

            argument namespace consisting of all config classes

        """
        return self._arg_namespace

    @staticmethod
    def _set_backend(args: typing.Tuple):
        """Determines which backend class to use

        *Args*:

            args: tuple of classes passed to the builder

        *Returns*:

            backend: class of backend

        """
        # Gather if all attr backend
        type_attrs = all([attr.has(arg) for arg in args])
        if not type_attrs:
            which_idx = [attr.has(arg) for arg in args].index(False)
            if hasattr(args[which_idx], '__name__'):
                raise TypeError(f"*args must be of all attrs backend -- missing a @spock decorator on class "
                                f"{args[which_idx].__name__}")
            else:
                raise TypeError(f"*args must be of all attrs backend -- invalid type "
                                f"{type(args[which_idx])}")
        else:
            backend = {'builder': AttrBuilder, 'payload': AttrPayload, 'saver': AttrSaver}
        return backend

    @staticmethod
    def _strip_tune_parameters(args: typing.Tuple):
        """Separates the fixed arguments from any hyper-parameter arguments

        *Args*:

            args: tuple of classes passed to the builder

        *Returns*:

            fixed_args: list of fixed args
            tune_args: list of args destined for a tuner backend

        """
        fixed_args = []
        tune_args = []
        for arg in args:
            if arg.__module__ == 'spock.backend.config':
                fixed_args.append(arg)
            elif arg.__module__ == 'spock.addons.tune.config':
                tune_args.append(arg)
        return fixed_args, tune_args

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

    def _get_payload(self, ignore_args: typing.List):
        """Get the parameter payload from the config file(s)

        Calls the various ways to get configs and then parses to retrieve the parameter payload - make sure to call
        deep update so as to not lose some parameters when only partially updating the payload

        *Args*:

            ignore_args: args that were decorated for hyper-parameter tuning

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
            payload_update = self._payload_obj.payload(
                self._builder_obj.input_classes, ignore_args, configs, args, dependencies
            )
            check_payload_overwrite(payload, payload_update, configs)
            deep_payload_update(payload, payload_update)
        return payload

    def save(self, file_name: str = None, user_specified_path: str = None, create_save_path: bool = True,
             extra_info: bool = True, file_extension: str = '.yaml'):
        """Saves the current config setup to file with a UUID

        *Args*:

            file_name: name of file (will be appended with .spock.cfg.file_extension) -- falls back to uuid if None
            user_specified_path: if user provides a path it will be used as the path to write
            create_save_path: bool to create the path to save if called
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
        self._saver_obj.save(
            self._arg_namespace, save_path, file_name, create_save_path, extra_info, file_extension
        )
        return self
