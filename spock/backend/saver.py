# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles prepping and saving the Spock config"""

from abc import abstractmethod
from uuid import uuid4

import attr

from spock.backend.handler import BaseHandler
from spock.utils import add_info


class BaseSaver(BaseHandler):  # pylint: disable=too-few-public-methods
    """Base class for saving configs

    Contains methods to build a correct output payload and then writes to file based on the file
    extension

    Attributes:
        _writers: maps file extension to the correct i/o handler
        _s3_config: optional S3Config object to handle s3 access

    """

    def __init__(self, s3_config=None):
        super(BaseSaver, self).__init__(s3_config=s3_config)

    def dict_payload(self, payload):
        """Clean up the config payload so it can be returned as a dict representation

        Args:
            payload: dirty payload

        Returns:
            clean_dict: cleaned output payload

        """
        # Fix up values -- parameters
        return self._clean_up_values(payload)

    def save(
        self,
        payload,
        path,
        file_name=None,
        create_save_path=False,
        extra_info=True,
        file_extension=".yaml",
        tuner_payload=None,
        fixed_uuid=None,
    ):  # pylint: disable=too-many-arguments
        """Writes Spock config to file

        Cleans and builds an output payload and then correctly writes it to file based on the
        specified file extension

        Args:
            payload: current config payload
            path: path to save
            file_name: name of file (will be appended with .spock.cfg.file_extension) -- falls back to uuid if None
            create_save_path: boolean to create the path if non-existent
            extra_info: boolean to write extra info
            file_extension: what type of file to write
            tuner_payload: tuner level payload (unsampled)
            fixed_uuid: fixed uuid to allow for file overwrite

        Returns:
            None

        """
        # Check extension
        self._check_extension(file_extension=file_extension)
        # Make the filename -- always append a uuid for unique-ness
        uuid_str = str(uuid4()) if fixed_uuid is None else fixed_uuid
        fname = "" if file_name is None else f"{file_name}."
        name = f"{fname}{uuid_str}.spock.cfg{file_extension}"
        # Fix up values -- parameters
        out_dict = self._clean_up_values(payload)
        # Fix up the tuner values if present
        tuner_dict = (
            self._clean_tuner_values(tuner_payload)
            if tuner_payload is not None
            else None
        )
        if tuner_dict is not None:
            out_dict.update(tuner_dict)
        # Get extra info
        extra_dict = add_info() if extra_info else None
        try:
            self._supported_extensions.get(file_extension)().save(
                out_dict=out_dict,
                info_dict=extra_dict,
                path=path,
                name=name,
                create_path=create_save_path,
                s3_config=self._s3_config,
            )
        except OSError as e:
            print(f"Unable to write to given path: {path / name}")
            raise e

    @abstractmethod
    def _clean_up_values(self, payload):
        """Clean up the config payload so it can be written to file

        Args:
            payload: dirty payload

        Returns:
            clean_dict: cleaned output payload

        """

    @abstractmethod
    def _clean_tuner_values(self, payload):
        """Cleans up the base tuner payload that is not sampled

        Args:
            payload: dirty payload

        Returns:
            clean_dict: cleaned output payload

        """

    def _clean_output(self, out_dict):
        """Clean up the dictionary so it can be written to file

        Args:
            out_dict: cleaned dictionary
            extra_info: boolean to add extra info

        Returns:
            clean_dict: cleaned output payload

        """
        # Convert values
        clean_dict = {}
        for key, val in out_dict.items():
            clean_inner_dict = {}
            if isinstance(val, list):
                for idx, list_val in enumerate(val):
                    tmp_dict = {}
                    for inner_key, inner_val in list_val.items():
                        tmp_dict = self._convert_tuples_2_lists(
                            tmp_dict, inner_val, inner_key
                        )
                    val[idx] = tmp_dict
                clean_inner_dict = val
            else:
                for inner_key, inner_val in val.items():
                    clean_inner_dict = self._convert_tuples_2_lists(
                        clean_inner_dict, inner_val, inner_key
                    )
            clean_dict.update({key: clean_inner_dict})
        return clean_dict

    def _convert_tuples_2_lists(self, clean_inner_dict, inner_val, inner_key):
        """Convert tuples to lists

        Args:
            clean_inner_dict: dictionary to update
            inner_val: current value
            inner_key: current key

        Returns:
            updated dictionary where tuples are cast back to lists

        """
        # Convert tuples to lists so they get written correctly
        if isinstance(inner_val, tuple):
            clean_inner_dict.update(
                {inner_key: self._recursive_tuple_to_list(inner_val)}
            )
        elif inner_val is not None:
            clean_inner_dict.update({inner_key: inner_val})
        return clean_inner_dict

    def _recursive_tuple_to_list(self, value):
        """Recursively turn tuples into lists

        Recursively looks through tuple(s) and convert to lists

        Args:
            value: value to check and set typ if necessary
            typed: type of the generic alias to check against

        Returns:
            value: updated value with correct type casts

        """
        # Check for __args__ as it signifies a generic and make sure it's not already been cast as a tuple
        # from a composed payload
        list_v = []
        for v in value:
            if isinstance(v, tuple):
                v = self._recursive_tuple_to_list(v)
                list_v.append(v)
            else:
                list_v.append(v)
        return list_v


class AttrSaver(BaseSaver):
    """Base class for saving configs for the attrs backend

    Contains methods to build a correct output payload and then writes to file based on the file
    extension

    Attributes:
        _writers: maps file extension to the correct i/o handler

    """

    def __init__(self, s3_config=None):
        super().__init__(s3_config=s3_config)

    def __call__(self, *args, **kwargs):
        return AttrSaver(*args, **kwargs)

    def _clean_up_values(self, payload):
        # Dictionary to recursively write to
        out_dict = {}
        # All of the classes are defined at the top level
        all_spock_cls = set(vars(payload).keys())
        out_dict = self._recursively_handle_clean(
            payload, out_dict, all_cls=all_spock_cls
        )
        # Convert values
        clean_dict = self._clean_output(out_dict)
        # Clip any empty dictionaries
        clean_dict = {k: v for k, v in clean_dict.items() if len(v) > 0}
        return clean_dict

    def _clean_tuner_values(self, payload):
        # Just a double nested dict comprehension to unroll to dicts
        out_dict = {
            k: {ik: vars(iv) for ik, iv in vars(v).items()}
            for k, v in vars(payload).items()
        }
        # Convert values
        clean_dict = self._clean_output(out_dict)
        return clean_dict

    def _recursively_handle_clean(
        self, payload, out_dict, parent_name=None, all_cls=None
    ):
        """Recursively works through spock classes and adds clean data to a dictionary

        Given a payload (Spockspace) work recursively through items that don't have parents to catch all
        parameter definitions while correctly mapping nested class definitions to their base level class thus
        allowing the output markdown to be a valid input file

        Args:
            payload: current payload (namespace)
            out_dict: output dictionary
            parent_name: name of the parent spock class if nested
            all_cls: all top level spock class definitions

        Returns:
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
            # Catch any callables -- convert back to the str representation
            elif callable(val):
                call_2_str = f"{val.__module__}.{val.__name__}"
                out_dict.update({key: call_2_str})
            # If it's a spock class but has a parent then just use the class name to reference the values
            elif (val_name in all_cls) and parent_name is not None:
                out_dict.update({key: val_name})
            # Check if it's a spock class without a parent -- iterate the values and recurse to catch more lists
            elif val_name in all_cls:
                new_dict = self._recursively_handle_clean(
                    val, {}, parent_name=key, all_cls=all_cls
                )
                out_dict.update({key: new_dict})
            # Either base type or no nested values that could be Spock classes
            else:
                out_dict.update({key: val})
        return out_dict
