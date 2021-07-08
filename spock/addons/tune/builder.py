# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the tuner builder backend"""

from spock.backend.builder import BaseBuilder
from spock.utils import make_argument


class TunerBuilder(BaseBuilder):
    def __init__(self, *args, **kwargs):
        """OptunaBuilder init

        Args:
            *args: list of input classes that link to a backend
            configs: None or List of configs to read from
            desc: description for the arg parser
            no_cmd_line: flag to force no command line reads
            **kwargs: any extra keyword args
        """
        super().__init__(*args, module_name='spock.addons.tune.config',  **kwargs)

    def _handle_arguments(self, args, class_obj):
        """Ovverides base -- Handles all argument mapping

        Creates a dictionary of named parameters that are mapped to the final type of object

        *Args*:

            args: read file arguments
            class_obj: instance of a class obj

        *Returns*:

            fields: dictionary of mapped parameters

        """
        attr_name = class_obj.__name__
        fields = {val.name: val.type(**args[attr_name][val.name]) for val in class_obj.__attrs_attrs__}
        return fields

    #
    # def _handle_repeated(self, args, check_value, class_names):
    #     """Handles repeated classes as lists
    #
    #     *Args*:
    #
    #         args: dictionary of arguments from the configs
    #         check_value: value to check classes against
    #         class_names: current class names
    #
    #     *Returns*:
    #
    #         list of input_class[match)idx[0]] types filled with repeated values
    #
    #     """
    #     # Check to see if the value trying to be set is actually an input class
    #     match_idx = [idx for idx, val in enumerate(class_names) if val == check_value]
    #     return [self.input_classes[match_idx[0]](**val) for val in args]
    #
    # def _handle_nested_class(self, args, check_value, class_names):
    #     """Handles passing another class to the field dictionary
    #
    #     *Args*:
    #         args: dictionary of arguments from the configs
    #         check_value: value to check classes against
    #         class_names: current class names
    #
    #     *Returns*:
    #
    #         either the check_value or the necessary class
    #
    #     """
    #     # Check to see if the value trying to be set is actually an input class
    #     match_idx = [idx for idx, val in enumerate(class_names) if val == check_value]
    #     # If so then create the needed class object by unrolling the args to **kwargs and return it
    #     if len(match_idx) > 0:
    #         if len(match_idx) > 1:
    #             raise ValueError('Match error -- multiple classes with the same name definition')
    #         else:
    #             if args.get(self.input_classes[match_idx[0]].__name__) is None:
    #                 raise ValueError(f'Missing config file definition for the referenced class '
    #                                  f'{self.input_classes[match_idx[0]].__name__}')
    #             current_arg = args.get(self.input_classes[match_idx[0]].__name__)
    #             if isinstance(current_arg, list):
    #                 class_value = [self.input_classes[match_idx[0]](**val) for val in current_arg]
    #             else:
    #                 class_value = self.input_classes[match_idx[0]](**current_arg)
    #         return_value = class_value
    #     # else return the expected value
    #     else:
    #         return_value = check_value
    #     return return_value

    @staticmethod
    def _make_group_override_parser(parser, class_obj, class_name):
        """Makes a name specific override parser for a given class obj

        Takes a class object of the backend and adds a new argument group with argument names given with name
        Class.val.(unrolled config parameters) so that individual parameters specific to a class can be overridden.

        *Args*:

            parser: argument parser
            class_obj: instance of a backend class
            class_name: used for module matching

        *Returns*:

            parser: argument parser with new class specific overrides

        """
        attr_name = class_obj.__name__
        group_parser = parser.add_argument_group(title=str(attr_name) + " Specific Overrides")
        for val in class_obj.__attrs_attrs__:
            val_type = val.metadata['type'] if 'type' in val.metadata else val.type
            for arg in val_type.__attrs_attrs__:
                arg_name = f"--{str(attr_name)}.{val.name}.{arg.name}"
                group_parser = make_argument(arg_name, arg.type, group_parser)
        return parser

    def _extract_fnc(self, val, module_name):
        return self._extract_other_types(val.type, module_name)
