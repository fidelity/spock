# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles prepping and saving the Spock config"""
from abc import abstractmethod
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from uuid import uuid4

import attr

from spock.backend.handler import BaseHandler
from spock.backend.utils import _callable_2_str, _get_iter, _recurse_callables
from spock.backend.wrappers import Spockspace
from spock.utils import _T, add_info, get_packages


class BaseSaver(BaseHandler):  # pylint: disable=too-few-public-methods
    """Base class for saving configs

    Contains methods to build a correct output payload and then writes to file based on the file
    extension

    Attributes:
        _writers: maps file extension to the correct i/o handler
        _s3_config: optional S3Config object to handle s3 access

    """

    def __init__(self, s3_config: Optional[_T] = None):
        """Init function for base class

        Args:
            s3_config: optional s3Config object for S3 support
        """
        super(BaseSaver, self).__init__(s3_config=s3_config)

    def dict_payload(self, payload: Spockspace) -> Dict:
        """Clean up the config payload so that it can be returned as a dict representation

        Args:
            payload: dirty payload

        Returns:
            clean_dict: cleaned output payload

        """
        # Fix up values -- parameters
        return self._clean_up_values(payload)

    def save(
        self,
        payload: Spockspace,
        path: str,
        file_name: Optional[str] = None,
        create_save_path: bool = False,
        extra_info: bool = True,
        file_extension: str = ".yaml",
        tuner_payload: Optional[Spockspace] = None,
        fixed_uuid: Optional[str] = None,
    ) -> None:  # pylint: disable=too-many-arguments
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
        # Make the filename -- always append uuid for unique-ness
        uuid_str = str(uuid4()) if fixed_uuid is None else fixed_uuid
        fname = "" if file_name is None else f"{file_name}."
        name = f"{fname}{uuid_str}.spock.cfg{file_extension}"
        # Fix up values -- parameters
        out_dict = self.dict_payload(payload)
        # Handle any env annotations that are present
        # Just stuff them into the dictionary
        crypto_flag = False
        for k, v in payload:
            if hasattr(v, "__resolver__"):
                for key, val in v.__resolver__.items():
                    out_dict[k][key] = val
            if hasattr(v, "__crypto__"):
                crypto_flag = True
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
        library_dict = get_packages() if extra_info else None
        try:
            self._supported_extensions.get(file_extension)().save(
                out_dict=out_dict,
                info_dict=extra_dict,
                library_dict=library_dict,
                path=path,
                name=name,
                create_path=create_save_path,
                s3_config=self._s3_config,
                salt=payload.__salt__ if crypto_flag else None,
                key=payload.__key__ if crypto_flag else None,
            )
        except OSError as e:
            print(f"Unable to write to given path: {path / name}")
            raise e

    @abstractmethod
    def _clean_up_values(self, payload: Spockspace, remove_crypto: bool = True) -> Dict:
        """Clean up the config payload so it can be written to file

        Args:
            payload: dirty payload
            remove_crypto: try and remove crypto values if present

        Returns:
            clean_dict: cleaned output payload

        """

    @abstractmethod
    def _clean_tuner_values(self, payload: Spockspace) -> Dict:
        """Cleans up the base tuner payload that is not sampled

        Args:
            payload: dirty payload

        Returns:
            clean_dict: cleaned output payload

        """

    def _clean_output(self, out_dict: Dict) -> Dict:
        """Clean up the dictionary such that it can be written to file

        Args:
            out_dict: pre-cleaned dictionary

        Returns:
            clean_dict: cleaned output payload

        """
        clean_dict = {}
        for k, v in out_dict.items():
            if v is not None:
                clean_dict.update({k: self._recursive_tuple_2_list(v)})
        return clean_dict

    def _recursive_tuple_2_list(self, val: Any) -> Any:
        """Recursively find tuples and cast them to lists

        Args:
            val: current value of various types

        Returns:
            modified version of val

        """
        # If it is a tuple then we need to cast back -- do this first
        # so we can assign by idx unlike tuples
        if isinstance(val, (tuple, Tuple)):
            val = list(val)
        if isinstance(val, (list, List)):
            for idx, v in _get_iter(val):
                if isinstance(v, (dict, Dict, list, List, tuple, Tuple)):
                    val[idx] = self._recursive_tuple_2_list(v)
        elif isinstance(val, (dict, Dict)):
            new_dict = {}
            for k, v in _get_iter(val):
                if isinstance(v, (dict, Dict, list, List, tuple, Tuple)):
                    new_dict[k] = self._recursive_tuple_2_list(v)
                elif v is not None:
                    new_dict[k] = v
            val = new_dict
        return val


class AttrSaver(BaseSaver):
    """Base class for saving configs for the attrs backend

    Contains methods to build a correct output payload and then writes to file based on the file
    extension

    Attributes:
        _writers: maps file extension to the correct i/o handler

    """

    def __init__(self, s3_config: Optional[_T] = None):
        """Init for AttrSaver class

        Args:
            s3_config: s3Config object for S3 support
        """
        super().__init__(s3_config=s3_config)

    def __call__(self, *args, **kwargs):
        return AttrSaver(*args, **kwargs)

    def _clean_up_values(self, payload: Spockspace, remove_crypto: bool = True) -> Dict:
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
        if remove_crypto:
            if "__salt__" in clean_dict:
                _ = clean_dict.pop("__salt__")
            if "__key__" in clean_dict:
                _ = clean_dict.pop("__key__")
        return clean_dict

    def _clean_tuner_values(self, payload: Spockspace) -> Dict:
        # Just a double nested dict comprehension to unroll to dicts
        out_dict = {
            k: {ik: vars(iv) for ik, iv in vars(v).items()}
            for k, v in vars(payload).items()
        }
        # Convert values
        clean_dict = self._clean_output(out_dict)
        return clean_dict

    @staticmethod
    def _check_list_of_spock_classes(val: List, key: str, all_cls: Set) -> List:
        """Finds lists of spock classes and handles changing them to a writeable format

        Args:
            val: current value that is a list
            key: current dictionary key in the payload
            all_cls: set of all spock classes

        Returns:

        """
        # Check if each entry is a spock class
        clean_val = []
        repeat_flag = False
        for v in val:
            cls_name = type(v).__name__
            # For those that are a spock class and are repeated (cls_name == key) simply convert to dict
            if (cls_name in all_cls) and (cls_name == key):
                clean_val.append(attr.asdict(v))
            # For those whose cls is different than the key just append the cls name
            elif cls_name in all_cls:
                # Change the flag as this is a repeated class -- which needs to be compressed into a single
                # k:v pair
                repeat_flag = True
                clean_val.append(cls_name)
            # Fall back to the passed in values
            else:
                clean_val.append(v)
        # Handle repeated classes
        if repeat_flag:
            clean_val = list(set(clean_val))[-1]
        return clean_val

    def _recursively_handle_clean(
        self,
        payload: Spockspace,
        out_dict: Dict,
        parent_name: Optional[str] = None,
        all_cls: Optional[Set] = None,
    ) -> Dict:
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
            # If v is any iterable we need to step into the nested structure
            if isinstance(val, (dict, Dict, list, List, tuple, Tuple)):
                # Need to inspect list type for lists of spock classes which must be handled differently
                mod_val = (
                    self._check_list_of_spock_classes(val, key, all_cls)
                    if isinstance(val, (list, List))
                    else val
                )
                # Recurses all iterables to find all callables and casts them to strings
                clean_val = _recurse_callables(
                    mod_val, _callable_2_str, check_type=Callable
                )
                out_dict.update({key: clean_val})
            # Catch any callables -- convert back to the str representation
            elif callable(val):
                out_dict.update({key: _callable_2_str(val)})
            # If it's a spock class but has a parent then just use the class name to reference the values
            elif (val_name in all_cls) and parent_name is not None:
                out_dict.update({key: val_name})
            # Check if it's a spock class without a parent -- iterate the values and recurse to catch more iterables
            elif val_name in all_cls:
                new_dict = self._recursively_handle_clean(
                    val, {}, parent_name=key, all_cls=all_cls
                )
                out_dict.update({key: new_dict})
            # Either base type or no nested values that could be Spock classes
            else:
                out_dict.update({key: val})
        return out_dict
