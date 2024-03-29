# -*- coding: utf-8 -*-

from spock.addons.tune import ChoiceHyperParameter, RangeHyperParameter, spockTuner


@spockTuner
class HPOne:
    hp_int: RangeHyperParameter
    hp_float: RangeHyperParameter
    hp_int_log: RangeHyperParameter
    hp_float_log: RangeHyperParameter


@spockTuner
class HPTwo:
    hp_choice_int: ChoiceHyperParameter
    hp_choice_float: ChoiceHyperParameter
    hp_choice_bool: ChoiceHyperParameter
    hp_choice_str: ChoiceHyperParameter


@spockTuner
class LogisticRegressionHP:
    c: RangeHyperParameter
    solver: ChoiceHyperParameter
