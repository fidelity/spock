# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import sys

import pytest

from spock.addons.tune import OptunaTunerConfig
from spock.builder import ConfigArgBuilder
from tests.tune.attr_configs_test import *


class TestOptunaCmdLineOverride:
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [
                    "",
                    "--config",
                    "./tests/conf/yaml/test_hp.yaml",
                    "--HPOne.hp_int.bounds",
                    "(1, 1000)",
                    "--HPOne.hp_int_log.bounds",
                    "(1, 1000)",
                    "--HPOne.hp_float.bounds",
                    "(1.0, 1000.0)",
                    "--HPOne.hp_float_log.bounds",
                    "(1.0, 1000.0)",
                    "--HPTwo.hp_choice_int.choices",
                    "[1, 2, 4, 8]",
                    "--HPTwo.hp_choice_float.choices",
                    "[1.0, 2.0, 4.0, 8.0]",
                    "--HPTwo.hp_choice_str.choices",
                    "['is', 'it ', 'me', 'youre', 'looking', 'for']",
                ],
            )
            optuna_config = OptunaTunerConfig(study_name="Tests", direction="maximize")
            config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)
            return config

    def test_hp_one(self, arg_builder):
        assert arg_builder._tune_namespace.HPOne.hp_int.bounds == (1, 1000)
        assert arg_builder._tune_namespace.HPOne.hp_int.type == "int"
        assert arg_builder._tune_namespace.HPOne.hp_int.log_scale is False
        assert arg_builder._tune_namespace.HPOne.hp_int_log.bounds == (1, 1000)
        assert arg_builder._tune_namespace.HPOne.hp_int_log.type == "int"
        assert arg_builder._tune_namespace.HPOne.hp_int_log.log_scale is True
        assert arg_builder._tune_namespace.HPOne.hp_float.bounds == (1.0, 1000.0)
        assert arg_builder._tune_namespace.HPOne.hp_float.type == "float"
        assert arg_builder._tune_namespace.HPOne.hp_float.log_scale is False
        assert arg_builder._tune_namespace.HPOne.hp_float_log.bounds == (1.0, 1000.0)
        assert arg_builder._tune_namespace.HPOne.hp_float_log.type == "float"
        assert arg_builder._tune_namespace.HPOne.hp_float_log.log_scale is True

    def test_hp_two(self, arg_builder):
        assert arg_builder._tune_namespace.HPTwo.hp_choice_int.type == "int"
        assert arg_builder._tune_namespace.HPTwo.hp_choice_int.choices == [1, 2, 4, 8]
        assert arg_builder._tune_namespace.HPTwo.hp_choice_float.type == "float"
        assert arg_builder._tune_namespace.HPTwo.hp_choice_float.choices == [
            1.0,
            2.0,
            4.0,
            8.0,
        ]
        assert arg_builder._tune_namespace.HPTwo.hp_choice_bool.type == "bool"
        assert arg_builder._tune_namespace.HPTwo.hp_choice_bool.choices == [True, False]
        assert arg_builder._tune_namespace.HPTwo.hp_choice_str.type == "str"
        assert arg_builder._tune_namespace.HPTwo.hp_choice_str.choices == [
            "is",
            "it ",
            "me",
            "youre",
            "looking",
            "for",
        ]

    def test_sampling(self, arg_builder):
        # Draw 100 random samples and make sure all fall within all of the bounds or sets
        for _ in range(100):
            hp_attrs = arg_builder.sample()
            assert 1 <= hp_attrs.HPOne.hp_int <= 1000
            assert isinstance(hp_attrs.HPOne.hp_int, int) is True
            assert 1 <= hp_attrs.HPOne.hp_int_log <= 1000
            assert isinstance(hp_attrs.HPOne.hp_int_log, int) is True
            assert 1.0 <= hp_attrs.HPOne.hp_float <= 1000.0
            assert isinstance(hp_attrs.HPOne.hp_float, float) is True
            assert 1.0 <= hp_attrs.HPOne.hp_float_log <= 1000.0
            assert isinstance(hp_attrs.HPOne.hp_float_log, float) is True
            assert hp_attrs.HPTwo.hp_choice_int in [1, 2, 4, 8]
            assert isinstance(hp_attrs.HPTwo.hp_choice_int, int) is True
            assert hp_attrs.HPTwo.hp_choice_float in [1.0, 2.0, 4.0, 8.0]
            assert isinstance(hp_attrs.HPTwo.hp_choice_float, float) is True
            assert hp_attrs.HPTwo.hp_choice_bool in [True, False]
            assert isinstance(hp_attrs.HPTwo.hp_choice_bool, bool) is True
            assert hp_attrs.HPTwo.hp_choice_str in [
                "is",
                "it ",
                "me",
                "youre",
                "looking",
                "for",
            ]
            assert isinstance(hp_attrs.HPTwo.hp_choice_str, str) is True
