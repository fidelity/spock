# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the base interface"""
from abc import ABC, abstractmethod
from typing import Dict

import attr

from spock.backend.wrappers import Spockspace


class BaseInterface(ABC):
    def __init__(self, tuner_config, tuner_namespace: Spockspace):
        """Base init call that maps a few variables

        *Args*:

            _tuner_config: necessary object to determine the interface and sample correctly from the underlying library
            _tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types

        """

        self._tuner_config = {
            k: v for k, v in attr.asdict(tuner_config).items() if v is not None
        }
        self._tuner_namespace = tuner_namespace

    @abstractmethod
    def sample(self):
        """Calls the underlying library sample to get a single sample/draw from the hyper-parameter
        sets (e.g. ranges, choices)

        *Returns*:

            Spockspace of the current hyper-parameter draw

        """
        pass

    @abstractmethod
    def _construct(self):
        """Constructs the base object needed by the underlying library to construct the correct object that allows
        for hyper-parameter sampling

        *Returns*:

            Any typed object needed for support

        """
        pass

    @staticmethod
    def _gen_attr_classes(tune_dict: Dict):
        for k, v in tune_dict.items():
            attrs_dict = {
                ik: attr.ib(
                    validator=attr.validators.instance_of(type(iv)), type=type(iv)
                )
                for ik, iv in v.items()
            }
            obj = attr.make_class(name=k, attrs=attrs_dict, kw_only=True, frozen=True)
            tune_dict.update({k: obj(**v)})
        return tune_dict

    @staticmethod
    def _to_spockspace(tune_dict: Dict):
        """Converts a dict to a Spockspace

        *Args*:

            tune_dict: current dictionary

        *Returns*:

            Spockspace of dict

        """
        return Spockspace(**tune_dict)

    @staticmethod
    def _get_caster(val):
        """Gets a callable type object from a string type

        *Args*:

            val: current attr val:

        *Returns*:

            type class object

        """
        return __builtins__[val.type]

    @property
    @abstractmethod
    def tuner_status(self):
        """Returns a dictionary of all the necessary underlying tuner internals to report the result"""
        pass

    @property
    @abstractmethod
    def best(self):
        """Returns a Spockspace of the best hyper-parameter config and the associated metric value"""
