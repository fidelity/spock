# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the optuna backend"""


import optuna

from spock.addons.tune.config import OptunaTunerConfig
from spock.addons.tune.interface import BaseInterface

try:
    from typing import TypedDict
except ImportError:
    from mypy_extensions import TypedDict


class OptunaTunerStatus(TypedDict):
    """Tuner status return object for Optuna -- supports the define-and-run style interface from Optuna

    Attributes:
        trial: current ask trial sample
        study: current optuna study object

    """

    trial: optuna.Trial
    study: optuna.Study


class OptunaInterface(BaseInterface):
    """Specific override to support the optuna backend -- supports the define-and-run style interface from Optuna

    Attributes:
        _map_type: dictionary that maps class names and types to fns that create optuna distributions
        _trial: current trial object from the optuna backend
        _tuner_obj: underlying optuna study object
        _tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types
        _param_obj: underlying object that optuna study can sample from (flat dictionary)
        _sample_hash: hash of the most recent sample draw

    """

    def __init__(self, tuner_config: OptunaTunerConfig, tuner_namespace):
        """OptunaInterface init call that maps variables, creates a map to fnc calls, and constructs the necessary
        underlying objects

        Args:
            tuner_config: configuration object for the optuna backend
            tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types

        """
        super(OptunaInterface, self).__init__(tuner_config, tuner_namespace)
        self._tuner_obj = optuna.create_study(
            **self._config_to_dict(self._tuner_config)
        )
        # Some variables to use later
        self._trial = None
        self._sample_hash = None
        # Mapping spock underlying classes to optuna distributions (define-and-run interface)
        self._map_type = {
            "RangeHyperParameter": {
                "int": self._uniform_int_dist,
                "float": self._uniform_float_dist,
            },
            "ChoiceHyperParameter": {
                "int": self._categorical_dist,
                "float": self._categorical_dist,
                "str": self._categorical_dist,
                "bool": self._categorical_dist,
            },
        }
        # Build the correct underlying dictionary object for Optuna
        self._param_obj = self._construct()

    @property
    def tuner_status(self) -> OptunaTunerStatus:
        return OptunaTunerStatus(trial=self._trial, study=self._tuner_obj)

    @property
    def best(self):
        rollup_dict, _ = self._sample_rollup(self._tuner_obj.best_trial.params)
        return (
            self._gen_spockspace(rollup_dict),
            self._tuner_obj.best_value,
        )

    @property
    def _get_sample(self):
        return self._tuner_obj.ask(self._param_obj)

    def sample(self):
        self._trial = self._get_sample
        # Roll this back out into a Spockspace so it can be merged into the fixed parameter Spockspace
        # Also need to un-dot the param names to rebuild the nested structure
        rollup_dict, sample_hash = self._sample_rollup(self._trial.params)
        self._sample_hash = sample_hash
        return self._gen_spockspace(rollup_dict)

    def _construct(self):
        optuna_dict = {}
        # These will only be nested one level deep given the tuner syntax
        for k, v in vars(self._tuner_namespace).items():
            for ik, iv in vars(v).items():
                param_fn = self._map_type[type(iv).__name__][iv.type]
                optuna_dict.update({f"{k}.{ik}": param_fn(iv)})
        return optuna_dict

    def _uniform_float_dist(self, val):
        """Assemble the optuna.distributions.(Log)UniformDistribution object

        https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.UniformDistribution.html
        https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.LogUniformDistribution.html

        Args:
            val: current attr val

        Returns:
            optuna.distributions.UniformDistribution or optuna.distributions.LogUniformDistribution

        """
        low, high = self._try_range_cast(val, type_string="RangeHyperParameter")
        log_scale = val.log_scale
        return (
            optuna.distributions.LogUniformDistribution(low=low, high=high)
            if log_scale
            else optuna.distributions.UniformDistribution(low=low, high=high)
        )

    def _uniform_int_dist(self, val):
        """Assemble the optuna.distributions.Int(Log)UniformDistribution object

        https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntUniformDistribution.html
        https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntLogUniformDistribution.html

        Args:
            val: current attr val

        Returns:
            optuna.distributions.IntUniformDistribution or optuna.distributions.IntLogUniformDistribution

        """
        low, high = self._try_range_cast(val, type_string="RangeHyperParameter")
        log_scale = val.log_scale
        return (
            optuna.distributions.IntLogUniformDistribution(low=low, high=high)
            if log_scale
            else optuna.distributions.IntUniformDistribution(low=low, high=high)
        )

    def _categorical_dist(self, val):
        """Assemble the optuna.distributions.CategoricalDistribution object

        https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html

        Args:
            val: current attr val

        Returns:
            optuna.distributions.CategoricalDistribution

        """
        val = self._try_choice_cast(val, type_string="ChoiceHyperParameter")
        return optuna.distributions.CategoricalDistribution(choices=val.choices)
