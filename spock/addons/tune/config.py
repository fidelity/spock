# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config interface that wraps attr -- tune version for hyper-parameters"""
import sys
from typing import List, Optional, Sequence, Tuple, Union
from uuid import uuid4

import attr
import optuna
from ax.modelbridge.generation_strategy import GenerationStrategy

from spock.backend.config import _base_attr


@attr.s(auto_attribs=True)
class AxTunerConfig:
    objective_name: str
    tracking_metric_names: Optional[List[str]] = None
    name: Optional[str] = f"spock_ax_{uuid4()}"
    minimize: bool = True
    parameter_constraints: Optional[List[str]] = None
    outcome_constraints: Optional[List[str]] = None
    support_intermediate_data: bool = False
    overwrite_existing_experiment: bool = False
    immutable_search_space_and_opt_config: bool = True
    is_test: bool = False
    generation_strategy: Optional[GenerationStrategy] = None
    enforce_sequential_optimization: bool = True
    random_seed: Optional[int] = None
    verbose_logging: bool = True


@attr.s(auto_attribs=True)
class OptunaTunerConfig:
    storage: Optional[Union[str, optuna.storages.BaseStorage]] = None
    sampler: Optional[optuna.samplers.BaseSampler] = None
    pruner: Optional[optuna.pruners.BasePruner] = None
    study_name: Optional[str] = f"spock_optuna_{uuid4()}"
    direction: Optional[Union[str, optuna.study.StudyDirection]] = None
    load_if_exists: bool = False
    directions: Optional[Sequence[Union[str, optuna.study.StudyDirection]]] = None


def _spock_tune(cls):
    """Ovverides basic spock_attr decorator with another name

    Using a different name allows spock to easily determine which parameters are normal and which are
    meant to be used in a hyper-parameter tuning backend

    *Args*:

        cls: basic class def

    *Returns*:

        cls: slotted attrs class that is frozen and kw only
    """
    bases, attrs_dict = _base_attr(cls)
    # Dynamically make an attr class
    obj = attr.make_class(
        name=cls.__name__, bases=bases, attrs=attrs_dict, kw_only=True, frozen=True
    )
    # For each class we dynamically create we need to register it within the system modules for pickle to work
    setattr(sys.modules["spock"].addons.tune.config, obj.__name__, obj)
    # Swap the __doc__ string from cls to obj
    obj.__doc__ = cls.__doc__
    return obj


# Make the alias for the decorator
spockTuner = _spock_tune


@attr.s
class RangeHyperParameter:
    """Range based hyper-parameter that is sampled uniformly

    Attributes:
        type: type of the hyper-parameter (note: spock will attempt to autocast into this type)
        bounds: min and max of the hyper-parameter range
        log_scale: log scale the values before sampling

    """

    type = attr.ib(
        type=str,
        validator=[
            attr.validators.instance_of(str),
            attr.validators.in_(["float", "int"]),
        ],
    )
    bounds = attr.ib(
        type=Union[Tuple[float, float], Tuple[int, int]],
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of((float, int)),
            iterable_validator=attr.validators.instance_of(tuple),
        ),
    )
    log_scale = attr.ib(type=bool, validator=attr.validators.instance_of(bool))


@attr.s
class ChoiceHyperParameter:
    """Choice based hyper-parameter that is sampled uniformly

    Attributes:
        type: type of the hyper-parameter -- (note: spock will attempt to autocast into this type)
        choices: list of variable length that contains all the possible choices to select from

    """

    type = attr.ib(
        type=str,
        validator=[
            attr.validators.instance_of(str),
            attr.validators.in_(["float", "int", "str", "bool"]),
        ],
    )
    choices = attr.ib(
        type=Union[List[str], List[int], List[float], List[bool]],
        validator=attr.validators.deep_iterable(
            member_validator=attr.validators.instance_of((float, int, bool, str)),
            iterable_validator=attr.validators.instance_of(list),
        ),
    )
