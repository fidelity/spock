# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the base interface"""
import hashlib
import json
from abc import ABC, abstractmethod
from typing import Dict, Union

import attr

from spock.addons.tune.config import AxTunerConfig, OptunaTunerConfig
from spock.backend.wrappers import Spockspace


class BaseInterface(ABC):
    """Base interface for the various hyper-parameter tuner backends

    Attributes

        _tuner_config: spock version of the tuner configuration
        _tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types

    """

    def __init__(self, tuner_config, tuner_namespace: Spockspace):
        """Base init call that maps a few variables

        Args:
            tuner_config: necessary dict object to determine the interface and sample correctly from the underlying library
            tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types

        """
        self._tuner_config = tuner_config
        self._tuner_namespace = tuner_namespace

    @abstractmethod
    def sample(self):
        """Calls the underlying library sample to get a single sample/draw from the hyper-parameter
        sets (e.g. ranges, choices)

        Returns:
            Spockspace of the current hyper-parameter draw

        """
        pass

    @abstractmethod
    def _construct(self):
        """Constructs the base object needed by the underlying library to construct the correct object that allows
        for hyper-parameter sampling

        Returns:
            flat dictionary of all hyper-parameters named with dot notation (class.param_name)

        """
        pass

    @property
    @abstractmethod
    def _get_sample(self):
        """Gets the sample parameter dictionary from the underlying backend"""
        pass

    @property
    @abstractmethod
    def tuner_status(self):
        """Returns a dictionary of all the necessary underlying tuner internals to report the result"""
        pass

    @property
    @abstractmethod
    def best(self):
        """Returns a Spockspace of the best hyper-parameter config and the associated metric value"""

    @staticmethod
    def _sample_rollup(params):
        """Rollup the sample draw into a dictionary that can be converted to a spockspace with the correct names and
        roots -- un-dots the name structure

        Args:
            params: current parameter dictionary -- named by dot notation

        Returns:
            dictionary of rolled up sampled parameters
            md5 hash of the dictionary contents

        """
        key_set = {k.split(".")[0] for k in params.keys()}
        rollup_dict = {val: {} for val in key_set}
        for k, v in params.items():
            split_names = k.split(".")
            rollup_dict[split_names[0]].update({split_names[1]: v})
        dict_hash = hashlib.md5(
            json.dumps(rollup_dict, sort_keys=True).encode("utf-8")
        ).digest()
        return rollup_dict, dict_hash

    def _gen_spockspace(self, tune_dict: Dict):
        """Converts a dictionary of dictionaries of parameters into a valid Spockspace

        Args:
            tune_dict: dictionary of current parameters

        Returns:
            tune_dict: Spockspace

        """
        for k, v in tune_dict.items():
            attrs_dict = {
                ik: attr.ib(
                    validator=attr.validators.instance_of(type(iv)), type=type(iv)
                )
                for ik, iv in v.items()
            }
            obj = attr.make_class(name=k, attrs=attrs_dict, kw_only=True, frozen=True)
            tune_dict.update({k: obj(**v)})
        return self._to_spockspace(tune_dict)

    @staticmethod
    def _config_to_dict(tuner_config: Union[OptunaTunerConfig, AxTunerConfig]):
        """Turns an attrs config object into a dictionary

        Args:
            tuner_config: attrs config object

        Returns:
            dictionary of the attrs config object
        """
        return {k: v for k, v in attr.asdict(tuner_config).items() if v is not None}

    @staticmethod
    def _to_spockspace(tune_dict: Dict):
        """Converts a dict to a Spockspace

        Args:
            tune_dict: current dictionary

        Returns:
            Spockspace of dict

        """
        return Spockspace(**tune_dict)

    @staticmethod
    def _get_caster(val):
        """Gets a callable type object from a string type

        Args:
            val: current attr val:

        Returns:
            type class object

        """
        return __builtins__[val.type]

    def _try_choice_cast(self, val, type_string: str):
        """Try/except for casting choice parameters

        Args:
            val: current attr val
            type_string: spock hyper-parameter type name

        Returns:
            val: updated attr val

        """
        caster = self._get_caster(val)
        # Just attempt to cast in a try except
        try:
            val.choices = [caster(v) for v in val.choices]
            return val
        except TypeError:
            print(
                f"Attempted to cast into type: {val.type} but failed -- check the inputs to {type_string}"
            )

    def _try_range_cast(self, val, type_string: str):
        """Try/except for casting range parameters

        Args:
            val: current attr val
            type_string: spock hyper-parameter type name

        Returns:
            low: low bound
            high: high bound

        """
        caster = self._get_caster(val)
        try:
            low = caster(val.bounds[0])
            high = caster(val.bounds[1])
            return low, high
        except TypeError:
            print(
                f"Attempted to cast into type: {val.type} but failed -- check the inputs to {type_string}"
            )
