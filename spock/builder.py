# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the building/saving of the configurations from the Spock config classes"""

import argparse
import sys
import typing
from collections import Counter
from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import attr

from spock.backend.builder import AttrBuilder
from spock.backend.payload import AttrPayload
from spock.backend.saver import AttrSaver
from spock.backend.wrappers import Spockspace
from spock.exceptions import _SpockEvolveError, _SpockUndecoratedClass
from spock.utils import _is_spock_instance, check_payload_overwrite, deep_payload_update

_CLS = typing.TypeVar("_CLS", bound=type)


class ConfigArgBuilder:
    """Automatically generates dataclass instances from config file(s)

    This class builds out necessary arguments from *args classes, reads
    the arguments from specified config file(s), and subsequently (via chained
    call to generate) generates each class instance based on the necessary
    field values for each backend class instance

    Attributes:
        _args: all command line args
        _arg_namespace: generated argument namespace
        _builder_obj: instance of a BaseBuilder class
        _dict_args: dictionary args from the command line
        _payload_obj: instance of a BasePayload class
        _saver_obj: instance of a BaseSaver class
        _tune_payload_obj: payload for tuner related objects -- instance of TunerPayload class
        _tune_obj: instance of TunerBuilder class
        _tuner_interface: interface that handles the underlying library for sampling -- instance of TunerInterface
        _tuner_state: current state of the hyper-parameter sampler
        _tune_namespace: namespace that hold the generated tuner related parameters
        _sample_count: current call to the sample function
        _fixed_uuid: fixed uuid to write the best file to the same path
        _configs = configs if configs is None else [Path(c) for c in configs]
        _lazy: flag to lazily find @spock decorated classes registered within sys.modules["spock"].backend.config
            thus alleviating the need to pass all @spock decorated classes to *args
        _no_cmd_line: turn off cmd line args
        _desc: description for help

    """

    def __init__(
        self,
        *args,
        configs: typing.Optional[typing.List] = None,
        desc: str = "",
        lazy: bool = False,
        no_cmd_line: bool = False,
        s3_config=None,
        **kwargs,
    ):
        """Init call for ConfigArgBuilder

        Args:
            *args: tuple of spock decorated classes to process
            configs: list of config paths
            desc: description for help
            lazy: attempts to lazily find @spock decorated classes registered within sys.modules["spock"].backend.config
            as well as the parents of any lazily inherited @spock class
            thus alleviating the need to pass all @spock decorated classes to *args
            no_cmd_line: turn off cmd line args
            s3_config: s3Config object for S3 support
            **kwargs: keyword args

        """
        # Do some verification first
        self._verify_attr(args)
        self._configs = configs if configs is None else [Path(c) for c in configs]
        self._lazy = lazy
        self._no_cmd_line = no_cmd_line
        self._desc = desc
        # Build the payload and saver objects
        self._payload_obj = AttrPayload(s3_config=s3_config)
        self._saver_obj = AttrSaver(s3_config=s3_config)
        # Split the fixed parameters from the tuneable ones (if present)
        fixed_args, tune_args = self._strip_tune_parameters(args)
        # The fixed parameter builder
        self._builder_obj = AttrBuilder(*fixed_args, lazy=lazy, **kwargs)
        # The possible tunable parameter builder -- might return None
        self._tune_obj, self._tune_payload_obj = self._handle_tuner_objects(
            tune_args, s3_config, kwargs
        )
        self._tuner_interface = None
        self._tuner_state = None
        self._tuner_status = None
        self._sample_count = 0
        self._fixed_uuid = str(uuid4())
        try:
            # Get all cmd line args and build overrides
            self._args = self._handle_cmd_line()
            # Get the actual payload from the config files -- fixed configs
            self._dict_args = self._get_payload(
                payload_obj=self._payload_obj,
                input_classes=self._builder_obj.input_classes,
                ignore_args=tune_args,
            )
            # Build the Spockspace from the payload and the classes
            # Fixed configs
            self._arg_namespace = self._builder_obj.generate(self._dict_args)
            # Get the payload from the config files -- hyper-parameters -- only if the obj is not None
            if self._tune_obj is not None:
                self._tune_args = self._get_payload(
                    payload_obj=self._tune_payload_obj,
                    input_classes=self._tune_obj.input_classes,
                    ignore_args=fixed_args,
                )
                # Build the Spockspace from the payload and the classes
                # Tuneable parameters
                self._tune_namespace = self._tune_obj.generate(self._tune_args)
        except Exception as e:
            self._print_usage_and_exit(str(e), sys_exit=False)
            raise e

    def __call__(self, *args, **kwargs):
        """Call to self to allow chaining

        Args:
            *args: non-keyword args
            **kwargs: keyword args

        Returns:
            ConfigArgBuilder: self instance
        """
        return ConfigArgBuilder(*args, **kwargs)

    def generate(self):
        """Generate method that returns the actual argument namespace


        Returns:
            argument namespace consisting of all config classes

        """
        return self._arg_namespace

    @property
    def tuner_status(self):
        """Returns a dictionary of all the necessary underlying tuner internals to report the result"""
        return self._tuner_status

    @property
    def best(self):
        """Returns a Spockspace of the best hyper-parameter config and the associated metric value"""
        return self._tuner_interface.best

    def sample(self):
        """Sample method that constructs a namespace from the fixed parameters and samples from the tuner space to
        generate a Spockspace derived from both

        Returns:
            argument namespace(s) -- fixed + drawn sample from tuner backend

        """
        if self._tuner_interface is None:
            raise RuntimeError(
                f"Called sample method without first calling the tuner method that initializes the "
                f"backend library"
            )
        return_tuple = self._tuner_state
        self._tuner_status = self._tuner_interface.tuner_status
        self._tuner_state = self._tuner_interface.sample()
        self._sample_count += 1
        return return_tuple

    def tuner(self, tuner_config):
        """Chained call that builds the tuner interface for either optuna or ax depending upon the type of the tuner_obj

        Args:
            tuner_config: a class of type optuna.study.Study or AX****

        Returns:
            self so that functions can be chained

        """

        if self._tune_obj is None:
            raise RuntimeError(
                f"Called tuner method without passing any @spockTuner decorated classes"
            )

        try:
            from spock.addons.tune.tuner import TunerInterface

            self._tuner_interface = TunerInterface(
                tuner_config=tuner_config,
                tuner_namespace=self._tune_namespace,
                fixed_namespace=self._arg_namespace,
            )
            self._tuner_state = self._tuner_interface.sample()
        except Exception as e:
            raise e
        return self

    def _print_usage_and_exit(self, msg=None, sys_exit=True, exit_code=1):
        """Prints the help message and exits

        Args:
            msg: message to print pre exit

        Returns:
            None

        """
        print(f"usage: {sys.argv[0]} -c [--config] config1 [config2, config3, ...]")
        print(f'\n{self._desc if self._desc != "" else ""}\n')
        print("configuration(s):\n")
        # Call the fixed parameter help info
        self._builder_obj.handle_help_info()
        if self._tune_obj is not None:
            self._tune_obj.handle_help_info()
        if msg is not None:
            print(msg)
        if sys_exit:
            sys.exit(exit_code)

    def _handle_tuner_objects(self, tune_args, s3_config, kwargs):
        """Handles creating the tuner builder object if @spockTuner classes were passed in

        Args:
            tune_args: list of tuner classes
            s3_config: s3Config object for S3 support
            kwargs: optional keyword args

        Returns:
            tuner builder object or None

        """
        if len(tune_args) > 0:
            try:
                from spock.addons.tune.builder import TunerBuilder
                from spock.addons.tune.payload import TunerPayload

                tuner_builder = TunerBuilder(*tune_args, **kwargs, lazy=self._lazy)
                tuner_payload = TunerPayload(s3_config=s3_config)
                return tuner_builder, tuner_payload
            except ImportError:
                print(
                    "Missing libraries to support tune functionality. Please re-install with the extra tune "
                    "dependencies -- pip install spock-config[tune]"
                )
        else:
            return None, None

    @staticmethod
    def _verify_attr(args: typing.Tuple):
        """Verifies that all the input classes are attr based

        Args:
            args: tuple of classes passed to the builder

        Returns:
            None

        """
        # Gather if all attr backend
        type_attrs = all([attr.has(arg) for arg in args])
        if not type_attrs:
            which_idx = [attr.has(arg) for arg in args].index(False)
            if hasattr(args[which_idx], "__name__"):
                raise TypeError(
                    f"*args must be of all attrs backend -- missing a @spock decorator on class "
                    f"{args[which_idx].__name__}"
                )
            else:
                raise TypeError(
                    f"*args must be of all attrs backend -- invalid type "
                    f"{type(args[which_idx])}"
                )

    @staticmethod
    def _strip_tune_parameters(args: typing.Tuple):
        """Separates the fixed arguments from any hyper-parameter arguments

        Args:
            args: tuple of classes passed to the builder

        Returns:
            fixed_args: list of fixed args
            tune_args: list of args destined for a tuner backend

        """
        fixed_args = []
        tune_args = []
        for arg in args:
            if arg.__module__ == "spock.backend.config":
                fixed_args.append(arg)
            elif arg.__module__ == "spock.addons.tune.config":
                tune_args.append(arg)
        return fixed_args, tune_args

    def _handle_cmd_line(self):
        """Handle all cmd line related tasks

        Config paths can enter from either the command line or be added in the class init call
        as a kwarg (configs=[]) -- also trigger the building of the cmd line overrides for each fixed and
        tunable objects

        Returns:
            args: namespace of args

        """
        # Need to hold an overarching parser here that just gets appended to for both fixed and tunable objects
        # Check if the no_cmd_line is not flagged and if the configs are not empty
        if self._no_cmd_line and (self._configs is None):
            raise ValueError(
                "Flag set for preventing command line read but no paths were passed to the config kwarg"
            )
        # If cmd_line is flagged then build the parsers if not make any empty Namespace
        args = (
            self._build_override_parsers(desc=self._desc)
            if not self._no_cmd_line
            else argparse.Namespace(config=[], help=False)
        )
        # If configs are present from the init call then roll these into the namespace
        if self._configs is not None:
            args = self._get_from_kwargs(args, self._configs)
        return args

    def _build_override_parsers(self, desc):
        """Creates parsers for command-line overrides

        Builds the basic command line parser for configs and help then iterates through each attr instance to make
        namespace specific cmd line override parsers -- handles calling both the fixed and tunable objects

        Args:
            desc: argparser description

        Returns:
            args: argument namespace

        """
        # Highest level parser object
        parser = argparse.ArgumentParser(description=desc, add_help=False)
        parser.add_argument(
            "-c", "--config", required=False, nargs="+", default=[], type=Path
        )
        parser.add_argument("-h", "--help", action="store_true")
        # Handle the builder obj
        parser = self._builder_obj.build_override_parsers(parser=parser)
        if self._tune_obj is not None:
            parser = self._tune_obj.build_override_parsers(parser=parser)
        args = parser.parse_args()

        return args

    @staticmethod
    def _get_from_kwargs(args, configs):
        """Get configs from the configs kwarg

        Args:
            args: argument namespace
            configs: config kwarg

        Returns:
            args: arg namespace

        """
        if isinstance(configs, list):
            args.config.extend(configs)
        else:
            raise TypeError(
                f"configs kwarg must be of type list -- given {type(configs)}"
            )
        return args

    def _get_payload(self, payload_obj, input_classes, ignore_args: typing.List):
        """Get the parameter payload from the config file(s)

        Calls the various ways to get configs and then parses to retrieve the parameter payload - make sure to call
        deep update so as to not lose some parameters when only partially updating the payload

        Args:
            payload_obj: current payload object to call
            input_classes: classes to use to get payload
            ignore_args: args that were decorated for hyper-parameter tuning

        Returns:
            payload: dictionary of parameter values

        """
        if self._args.help:
            # Call sys exit with a clean code as this is the help call which is not unexpected behavior
            self._print_usage_and_exit(sys_exit=True, exit_code=0)
        payload = {}
        dependencies = {"paths": [], "rel_paths": [], "roots": []}
        if payload_obj is not None:
            # Make sure we are actually trying to map to input classes
            if len(input_classes) > 0:
                # If configs are present then iterate through them and deal with the payload
                if len(self._args.config) > 0:
                    for configs in self._args.config:
                        payload_update = payload_obj.payload(
                            input_classes,
                            ignore_args,
                            configs,
                            self._args,
                            dependencies,
                        )
                        check_payload_overwrite(payload, payload_update, configs)
                        deep_payload_update(payload, payload_update)
                # If there are no configs present we have to fall back only on cmd line args to fill out the necessary
                # data -- this is essentially using spock as a drop in replacement of arg-parser
                else:
                    payload_update = payload_obj.payload(
                        input_classes, ignore_args, None, self._args, dependencies
                    )
                    check_payload_overwrite(payload, payload_update, None)
                    deep_payload_update(payload, payload_update)
        return payload

    def _save(
        self,
        payload,
        file_name: str = None,
        user_specified_path: Path = None,
        create_save_path: bool = True,
        extra_info: bool = True,
        file_extension: str = ".yaml",
        tuner_payload=None,
        fixed_uuid=None,
    ):
        """Private interface -- saves the current config setup to file with a UUID

        Args:
            payload: Spockspace to save
            file_name: name of file (will be appended with .spock.cfg.file_extension) -- falls back to just uuid if None
            user_specified_path: if user provides a path it will be used as the path to write
            create_save_path: bool to create the path to save if called
            extra_info: additional info to write to saved config (run date and git info)
            file_extension: file type to write (default: yaml)
            tuner_payload: tuner level payload (unsampled)
            fixed_uuid: fixed uuid to allow for file overwrite

        Returns:
            self so that functions can be chained
        """
        if user_specified_path is not None:
            save_path = Path(user_specified_path)
        elif self._builder_obj.save_path is not None:
            save_path = Path(self._builder_obj.save_path)
        else:
            raise ValueError(
                "Save did not receive a valid path from: (1) markup file(s) or (2) "
                "the keyword arg user_specified_path"
            )
        # Call the saver class and save function
        self._saver_obj.save(
            payload,
            save_path,
            file_name,
            create_save_path,
            extra_info,
            file_extension,
            tuner_payload,
            fixed_uuid,
        )
        return self

    def save(
        self,
        file_name: str = None,
        user_specified_path: typing.Union[Path, str] = None,
        create_save_path: bool = True,
        extra_info: bool = True,
        file_extension: str = ".yaml",
        add_tuner_sample: bool = False,
    ):
        """Saves the current config setup to file with a UUID

        Args:
            file_name: name of file (will be appended with .spock.cfg.file_extension) -- falls back to just uuid if None
            user_specified_path: if user provides a path it will be used as the path to write
            create_save_path: bool to create the path to save if called
            extra_info: additional info to write to saved config (run date and git info)
            file_extension: file type to write (default: yaml)
            append_tuner_state: save the current tuner sample to the payload

        Returns:
            self so that functions can be chained
        """
        if user_specified_path is not None:
            user_specified_path = Path(user_specified_path)
        if add_tuner_sample:
            if self._tune_obj is None:
                raise ValueError(
                    f"Called save method with add_tuner_sample as `{add_tuner_sample}` without passing any @spockTuner "
                    f"decorated classes -- please use the add_tuner_sample flag for saving only hyper-parameter tuning "
                    f"runs"
                )
            file_name = (
                f"hp.sample.{self._sample_count+1}"
                if file_name is None
                else f"{file_name}.hp.sample.{self._sample_count+1}"
            )
            self._save(
                self._tuner_state,
                file_name,
                user_specified_path,
                create_save_path,
                extra_info,
                file_extension,
            )
        else:
            self._save(
                self._arg_namespace,
                file_name,
                user_specified_path,
                create_save_path,
                extra_info,
                file_extension,
                tuner_payload=self._tune_namespace
                if self._tune_obj is not None
                else None,
            )
        return self

    def save_best(
        self,
        file_name: str = None,
        user_specified_path: Path = None,
        create_save_path: bool = True,
        extra_info: bool = True,
        file_extension: str = ".yaml",
    ):
        """Saves the current best config setup to file

        Args:
            file_name: name of file (will be appended with .spock.cfg.file_extension) -- falls back to just uuid if None
            user_specified_path: if user provides a path it will be used as the path to write
            create_save_path: bool to create the path to save if called
            extra_info: additional info to write to saved config (run date and git info)
            file_extension: file type to write (default: yaml)

        Returns:
            self so that functions can be chained
        """
        if self._tune_obj is None:
            raise ValueError(
                f"Called save_best method without passing any @spockTuner decorated classes -- please use the `save()`"
                f" method for saving non hyper-parameter tuning runs"
            )
        file_name = f"hp.best" if file_name is None else f"{file_name}.hp.best"
        self._save(
            Spockspace(**vars(self._arg_namespace), **vars(self.best[0])),
            file_name,
            user_specified_path,
            create_save_path,
            extra_info,
            file_extension,
            fixed_uuid=self._fixed_uuid,
        )

        return self

    @property
    def config_2_dict(self):
        """Dictionary representation of the arg payload"""
        return self._saver_obj.dict_payload(self._arg_namespace)

    def spockspace_2_dict(self, payload: Spockspace):
        """Converts an input SpockSpace into a dictionary

        Args:
            payload: SpockSpace generated by the ConfigArgBuilder

        Returns:
            dictionary representation of the SpockSpace

        """
        return self._saver_obj.dict_payload(payload)

    def evolve(self, *args: typing.Type[_CLS]):
        """Function that allows a user to evolve the underlying spock classes with instantiated spock objects

        This will map the differences between the passed in instantiated objects and the underlying class definitions
        to the underlying namespace -- this essentially allows you to 'evolve' the Spockspace similar to how attrs
        allows for class evolution -- returns a new Spockspace object

        Args:
            *args: variable number of instantiated @spock decorated classes to evolve parameters with

        Returns:
            new_arg_namespace: Spockspace evolved with *arg @spock decorated classes

        Raises:
            _SpockEvolveError: if multiple of the same instance are passed as input or if the one or more of the inputs
            are not within the set of original input classes

        """
        # First check that all instances are in the underlying set of input_classes and that there are no dupes
        arg_counts = Counter([type(v).__name__ for v in args])
        for k, v in arg_counts.items():
            if v > 1:
                raise _SpockEvolveError(
                    f"Passed multiple instances (count: {v}) of class `{k}` into `evolve()` -- please pass only a "
                    f"single instance of the class in order to evolve the underlying Spockspace"
                )
            elif k not in self._builder_obj.graph.node_names:
                raise _SpockEvolveError(
                    f"Passed class `{k}` into `evolve()` but that class in not within the set of input "
                    f"classes {repr(self._builder_obj.graph.node_names)}"
                )
        # Create a new copy of the object
        new_arg_namespace = deepcopy(self._arg_namespace)
        # Determine the order of overwrite ops -- based on the topological order
        topo_idx = sorted(
            zip(
                [
                    self._builder_obj.graph.topological_order.index(type(v).__name__)
                    for v in args
                ],
                args,
            )
        )
        args = {type(v).__name__: v for _, v in topo_idx}
        # Walk through the now sorted set of evolve classes
        for k, v in args.items():
            # Get the class name from the object
            cls_name = type(v).__name__
            # Swap in the value to the new object
            # Note: we don't need to evolve here as it's a fully new obj
            setattr(new_arg_namespace, cls_name, v)
            # Recurse upwards through the deps stack and evolve all the necessary classes
            new_arg_namespace, all_cls = self._recurse_upwards(
                new_arg_namespace, cls_name, args
            )
        return new_arg_namespace

    def _recurse_upwards(
        self, new_arg_namespace: Spockspace, current_cls: str, all_cls: typing.Dict
    ):
        """Using the underlying graph work recurse upwards through the parents and swap in the correct values

        Args:
            new_arg_namespace: new Spockspace object
            current_cls: current name of the cls
            all_cls: dict of the variable number of @spock decorated classes to evolve parameters with

        Returns:
            modified new_arg_namespace and the updated evolve class dict

        """
        # Get the parent deps from the graph
        parents = self._builder_obj.dag[current_cls]
        if len(parents) > 0:
            for parent_cls in parents:
                parent_name = parent_cls.__name__
                # Change the parent classes in the Spockspace
                new_arg_namespace = self._set_matching_attrs_by_name(
                    new_arg_namespace, current_cls, parent_name
                )
                # if the parent is in the evolve classes then morph them too
                if parent_name in all_cls.keys():
                    all_cls = self._set_matching_attrs_by_name_args(
                        current_cls, parent_name, all_cls
                    )
                # then recurse to the parents
                new_arg_namespace, all_cls = self._recurse_upwards(
                    new_arg_namespace, parent_name, all_cls
                )
        return new_arg_namespace, all_cls

    @staticmethod
    def _set_matching_attrs_by_name_args(
        current_cls_name: str, parent_cls_name: str, all_cls: typing.Dict
    ):
        """Sets the value of an attribute by matching it to a spock class name

        Args:
            current_cls_name: current name of the changed class
            parent_cls_name: name of the parent class that contains a reference to the current class
            all_cls: dict of the variable number of @spock decorated classes to evolve parameters with

        Returns:
            modified all_cls dictionary

        """
        new_arg_namespace = all_cls[parent_cls_name]
        names = attr.fields_dict(type(new_arg_namespace)).keys()
        for v in names:
            if type(getattr(new_arg_namespace, v)).__name__ == current_cls_name:
                # Some evolution magic -- attr library wants kwargs so trick it by unrolling the dict
                # This creates a new object
                new_obj = attr.evolve(
                    new_arg_namespace,
                    **{v: all_cls[current_cls_name]},
                )
                all_cls[parent_cls_name] = new_obj
                print(
                    f"Evolved CLS Dependency: Parent = {parent_cls_name}, Child = {current_cls_name}, Value = {v}"
                )
        return all_cls

    @staticmethod
    def _set_matching_attrs_by_name(
        new_arg_namespace: Spockspace, current_cls_name: str, parent_cls_name: str
    ):
        """Sets the value of an attribute by matching it to a spock class name

        Args:
            new_arg_namespace: new Spockspace object
            current_cls_name: current name of the changed class
            parent_cls_name: name of the parent class that contains a reference to the current class

        Returns:
            modified new_arg_namespace

        """
        parent_attr = getattr(new_arg_namespace, parent_cls_name)
        names = attr.fields_dict(type(parent_attr)).keys()
        for v in names:
            if type(getattr(parent_attr, v)).__name__ == current_cls_name:
                # Some evolution magic -- attr library wants kwargs so trick it by unrolling the dict
                # This creates a new object
                new_obj = attr.evolve(
                    getattr(new_arg_namespace, parent_cls_name),
                    **{v: getattr(new_arg_namespace, current_cls_name)},
                )
                # Swap the new object into the existing attribute slot
                setattr(new_arg_namespace, parent_cls_name, new_obj)
                print(
                    f"Evolved: Parent = {parent_cls_name}, Child = {current_cls_name}, Value = {v}"
                )
        return new_arg_namespace
