# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles prepping and saving the Spock config"""

import attr
from spock.backend.base import BaseSaver


class AttrSaver(BaseSaver):
    """Base class for saving configs for the attrs backend

    Contains methods to build a correct output payload and then writes to file based on the file
    extension

    *Attributes*:

        _writers: maps file extension to the correct i/o handler

    """
    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        return AttrSaver()

    def _clean_up_values(self, payload, file_extension):
        # Dictionary to recursively write to
        out_dict = {}
        # All of the classes are defined at the top level
        all_spock_cls = set(vars(payload).keys())
        out_dict = self._recursively_handle_clean(payload, out_dict, all_cls=all_spock_cls)
        # Convert values
        clean_dict = self._clean_output(out_dict)
        return clean_dict

    def _recursively_handle_clean(self, payload, out_dict, parent_name=None, all_cls=None):
        """Recursively works through spock classes and adds clean data to a dictionary

        Given a payload (Spockspace) work recursively through items that don't have parents to catch all
        parameter definitions while correctly mapping nested class definitions to their base level class thus
        allowing the output markdown to be a valid input file

        *Args*:

            payload: current payload (namespace)
            out_dict: output dictionary
            parent_name: name of the parent spock class if nested
            all_cls: all top level spock class definitions

        *Returns*:

            out_dict: modified dictionary with the cleaned data

        """
        for key, val in vars(payload).items():
            val_name = type(val).__name__
            # This catches basic lists and list of classes
            if isinstance(val, list):
                # Check if each entry is a spock class
                clean_val = []
                repeat_flag = False
                for l_val in val:
                    cls_name = type(l_val).__name__
                    # For those that are a spock class and are repeated (cls_name == key) simply convert to dict
                    if (cls_name in all_cls) and (cls_name == key):
                        clean_val.append(attr.asdict(l_val))
                    # For those whose cls is different than the key just append the cls name
                    elif cls_name in all_cls:
                        # Change the flag as this is a repeated class -- which needs to be compressed into a single
                        # k:v pair
                        repeat_flag = True
                        clean_val.append(cls_name)
                    # Fall back to the passed in values
                    else:
                        clean_val.append(l_val)
                # Handle repeated classes
                if repeat_flag:
                    clean_val = list(set(clean_val))[-1]
                out_dict.update({key: clean_val})
            # If it's a spock class but has a parent then just use the class name to reference the values
            elif(val_name in all_cls) and parent_name is not None:
                out_dict.update({key: val_name})
            # Check if it's a spock class without a parent -- iterate the values and recurse to catch more lists
            elif val_name in all_cls:
                new_dict = self._recursively_handle_clean(val, {}, parent_name=key, all_cls=all_cls)
                out_dict.update({key: new_dict})
            # Either base type or no nested values that could be Spock classes
            else:
                out_dict.update({key: val})
        return out_dict
