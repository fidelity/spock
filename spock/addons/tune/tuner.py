# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the tuner interface interface"""

from typing import Union

from spock.addons.tune.config import OptunaTunerConfig
from spock.addons.tune.optuna import OptunaInterface
from spock.backend.wrappers import Spockspace


class TunerInterface:
    """Handles the general tuner interface by creating the necessary underlying tuner class and dispatches necessary
    ops to the class instance

    *Attributes*:

        _fixed_namespace: fixed parameter namespace used for combination with a sample draw
        _lib_interface: class instance of the underlying hyper-parameter library

    """

    def __init__(
        self,
        tuner_config: Union[OptunaTunerConfig],
        tuner_namespace: Spockspace,
        fixed_namespace: Spockspace,
    ):
        """Init call to the TunerInterface

        *Args*:

            tuner_config: necessary object to determine the interface and sample correctly from the underlying library
            tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types
            fixed_namespace: namespace of fixed parameters

        """
        self._fixed_namespace = fixed_namespace
        # Todo: add ax type check here
        accept_types = OptunaTunerConfig
        if not isinstance(tuner_config, accept_types):
            raise ValueError(
                f"Passed incorrect tuner_config type of {type(tuner_config)} -- must be of type "
                f"{repr(accept_types)}"
            )
        if isinstance(tuner_config, OptunaTunerConfig):
            self._lib_interface = OptunaInterface(
                tuner_config=tuner_config, tuner_namespace=tuner_namespace
            )
        # # TODO: Add ax class logic
        # elif isinstance(tuner_config, (ax.Experiment, ax.SimpleExperiment)):
        #     pass

    def sample(self):
        """Public interface to underlying library sepcific sample that returns a single sample/draw from the
        hyper-parameter sets (e.g. ranges, choices) and combines them with the fixed parameters into a single Spockspace

        *Returns*:

            Spockspace of drawn sample of hyper-parameters and fixed parameters

        """
        curr_sample, extra_dict = self._lib_interface.sample()
        # Merge w/ fixed parameters
        return (
            Spockspace(**vars(curr_sample), **vars(self._fixed_namespace)),
            extra_dict,
        )
