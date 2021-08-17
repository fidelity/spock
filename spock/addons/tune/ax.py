# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the ax backend"""

from ax.service.ax_client import AxClient

from spock.addons.tune.config import AxTunerConfig
from spock.addons.tune.interface import BaseInterface

try:
    from typing import TypedDict
except ImportError:
    from mypy_extensions import TypedDict


class AxTunerStatus(TypedDict):
    """Tuner status return object for Ax -- supports the service style API from Ax

    *Attributes*:

        client: current AxClient instance
        trial_index: current trial index

    """

    client: AxClient
    trial_index: int


class AxInterface(BaseInterface):
    """Specific override to support the Ax backend -- supports the service style API from Ax"""

    def __init__(self, tuner_config: AxTunerConfig, tuner_namespace):
        """AxInterface init call that maps variables, creates a map to fnc calls, and constructs the necessary
        underlying objects

        *Args*:

            tuner_config: configuration object for the ax backend
            tuner_namespace: tuner namespace that has attr classes that maps to an underlying library types
        """
        super(AxInterface, self).__init__(tuner_config, tuner_namespace)
        self._tuner_obj = AxClient(
            generation_strategy=self._tuner_config.generation_strategy,
            enforce_sequential_optimization=self._tuner_config.enforce_sequential_optimization,
            random_seed=self._tuner_config.random_seed,
            verbose_logging=self._tuner_config.verbose_logging,
        )
        # Some variables to use later
        self._trial_index = None
        self._sample_hash = None
        # Mapping spock underlying classes to ax distributions (search space)
        self._map_type = {
            "RangeHyperParameter": {
                "int": self._ax_range,
                "float": self._ax_range,
            },
            "ChoiceHyperParameter": {
                "int": self._ax_choice,
                "float": self._ax_choice,
                "str": self._ax_choice,
                "bool": self._ax_choice,
            },
        }
        # Build the correct underlying dictionary object for Ax client create experiment
        self._param_obj = self._construct()
        # Create the AxClient experiment
        self._tuner_obj.create_experiment(
            parameters=self._param_obj,
            name=self._tuner_config.name,
            objective_name=self._tuner_config.objective_name,
            minimize=self._tuner_config.minimize,
            parameter_constraints=self._tuner_config.parameter_constraints,
            outcome_constraints=self._tuner_config.outcome_constraints,
            overwrite_existing_experiment=self._tuner_config.overwrite_existing_experiment,
            tracking_metric_names=self._tuner_config.tracking_metric_names,
            immutable_search_space_and_opt_config=self._tuner_config.immutable_search_space_and_opt_config,
            is_test=self._tuner_config.is_test,
        )

    @property
    def tuner_status(self) -> AxTunerStatus:
        return AxTunerStatus(client=self._tuner_obj, trial_index=self._trial_index)

    @property
    def best(self):
        best_obj = self._tuner_obj.get_best_parameters()
        rollup_dict, _ = self._sample_rollup(best_obj[0])
        return (
            self._gen_spockspace(rollup_dict),
            best_obj[1][0][self._tuner_obj.objective_name],
        )

    @property
    def _get_sample(self):
        return self._tuner_obj.get_next_trial()

    def sample(self):
        parameters, self._trial_index = self._get_sample
        # Roll this back out into a Spockspace so it can be merged into the fixed parameter Spockspace
        # Also need to un-dot the param names to rebuild the nested structure
        rollup_dict, sample_hash = self._sample_rollup(parameters)
        self._sample_hash = sample_hash
        return self._gen_spockspace(rollup_dict)

    def _construct(self):
        param_list = []
        # These will only be nested one level deep given the tuner syntax
        for k, v in vars(self._tuner_namespace).items():
            for ik, iv in vars(v).items():
                param_fn = self._map_type[type(iv).__name__][iv.type]
                param_list.append(param_fn(name=f"{k}.{ik}", val=iv))
        return param_list

    def _ax_range(self, name, val):
        """Assemble the dictionary for ax range parameters

        *Args*:

            name: parameter name
            val: current attr val

        *Returns*:

            dictionary that can be added to a parameter list

        """
        low, high = self._try_range_cast(val, type_string="RangeHyperParameter")
        return {
            "name": name,
            "type": "range",
            "bounds": [low, high],
            "value_type": val.type,
            "log_scale": val.log_scale,
        }

    def _ax_choice(self, name, val):
        """Assemble the dictionary for ax choice parameters

        *Args*:

            name: parameter name
            val: current attr val

        *Returns*:

            dictionary that can be added to a parameter list

        """
        val = self._try_choice_cast(val, type_string="ChoiceHyperParameter")
        return {
            "name": name,
            "type": "choice",
            "values": val.choices,
            "value_type": val.type,
        }
