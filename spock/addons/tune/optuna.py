# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the optuna backend"""

import hashlib
import json
from warnings import warn

import attr
import optuna

from spock.addons.tune.config import OptunaTunerConfig
from spock.addons.tune.interface import BaseInterface


class OptunaInterface(BaseInterface):
    """Specific override to support the optuna backend

    *Attributes*:

        _map_type: dictionary that maps class names and types to fns that create optuna distributions
        _tuner_obj: necessary object to determine the interface and sample correctly from the underlying library
        _tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types
        _param_obj: underlying object that optuna study can sample from (flat dictionary)

    """

    def __init__(self, tuner_config: OptunaTunerConfig, tuner_namespace):
        """OptunaInterface init call that maps variables, creates a map to fnc calls, and constructs the necessary
        underlying objects

        *Args*:

            tuner_config: necessary object to determine the interface and sample correctly from the underlying library
            tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types

        """
        super(OptunaInterface, self).__init__(tuner_config, tuner_namespace)
        self._tuner_obj = optuna.create_study(**self._tuner_config)
        self._trial = None
        self._sample_hash = None
        self._trial_status_hash = None
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
    def tuner_status(self):
        return {"trial": self._trial, "study": self._tuner_obj}

    @property
    def best(self):
        rollup_dict, _ = self._trial_rollup(self._tuner_obj.best_trial)
        return (
            self._to_spockspace(self._gen_attr_classes(rollup_dict)),
            self._tuner_obj.best_value,
        )

    def sample(self):
        self._trial = self._tuner_obj.ask(self._param_obj)
        # Roll this back out into a Spockspace so it can be merged into the fixed parameter Spockspace
        # Also need to un-dot the param names to rebuild the nested structure
        rollup_dict, sample_hash = self._trial_rollup(self._trial)
        self._sample_hash = sample_hash
        return self._to_spockspace(self._gen_attr_classes(rollup_dict))

    @staticmethod
    def _trial_rollup(trial):
        """Rollup the trial into a dictionary that can be converted to a spockspace with the correct names and roots

        *Returns*:

            dictionary of rolled up sampled parameters
            md5 hash of the dictionary contents

        """
        key_set = {k.split(".")[0] for k in trial.params.keys()}
        rollup_dict = {val: {} for val in key_set}
        for k, v in trial.params.items():
            split_names = k.split(".")
            rollup_dict[split_names[0]].update({split_names[1]: v})
        dict_hash = hashlib.md5(
            json.dumps(rollup_dict, sort_keys=True).encode("utf-8")
        ).digest()
        return rollup_dict, dict_hash

    def _construct(self):
        """Constructs the base object needed by the underlying library to construct the correct object that allows
        for hyper-parameter sampling

        *Returns*:

            flat dictionary of all hyper-parameters named with dot notation (class.param_name)

        """
        optuna_dict = {}
        # These will only be nested one level deep given the tuner syntax
        for k, v in vars(self._tuner_namespace).items():
            for ik, iv in vars(v).items():
                param_fn = self._map_type[type(iv).__name__][iv.type]
                optuna_dict.update({f"{k}.{ik}": param_fn(iv)})
        return optuna_dict

    @staticmethod
    def _uniform_float_dist(val):
        """Assemble the optuna.distributions.(Log)UniformDistribution object

        https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.UniformDistribution.html
        https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.LogUniformDistribution.html

        *Args*:

            val: current attr val

        *Returns*:

            optuna.distributions.UniformDistribution or optuna.distributions.LogUniformDistribution

        """
        try:
            low = float(val.bounds[0])
            high = float(val.bounds[1])
        except TypeError:
            print(
                f"Attempted to cast into type: {val.type} but failed -- check the inputs to RangeHyperParameter"
            )
        log_scale = val.log_scale
        return (
            optuna.distributions.LogUniformDistribution(low=low, high=high)
            if log_scale
            else optuna.distributions.UniformDistribution(low=low, high=high)
        )

    @staticmethod
    def _uniform_int_dist(val):
        """Assemble the optuna.distributions.Int(Log)UniformDistribution object

        https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntUniformDistribution.html
        https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.IntLogUniformDistribution.html

        *Args*:

            val: current attr val

        *Returns*:

            optuna.distributions.IntUniformDistribution or optuna.distributions.IntLogUniformDistribution

        """
        try:
            low = int(val.bounds[0])
            high = int(val.bounds[1])
        except TypeError:
            print(
                f"Attempted to cast into type: {val.type} but failed -- check the inputs to RangeHyperParameter"
            )
        log_scale = val.log_scale
        return (
            optuna.distributions.IntLogUniformDistribution(low=low, high=high)
            if log_scale
            else optuna.distributions.IntUniformDistribution(low=low, high=high)
        )

    def _categorical_dist(self, val):
        """Assemble the optuna.distributions.CategoricalDistribution object

        https://optuna.readthedocs.io/en/stable/reference/generated/optuna.distributions.CategoricalDistribution.html

        *Args*:

            val: current attr val

        *Returns*:

            optuna.distributions.CategoricalDistribution

        """
        caster = self._get_caster(val)
        # Just attempt to cast in a try except
        try:
            val.choices = [caster(v) for v in val.choices]
        except TypeError:
            print(
                f"Attempted to cast into type: {val.type} but failed -- check the inputs to ChoiceHyperParameter"
            )
        return optuna.distributions.CategoricalDistribution(choices=val.choices)
