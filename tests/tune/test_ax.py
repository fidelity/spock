# -*- coding: utf-8 -*-
import datetime
from tests.tune.base_asserts_test import *
from tests.tune.attr_configs_test import *
import pytest
import os
import re
import sys
from spock.builder import ConfigArgBuilder
from spock.addons.tune import AxTunerConfig
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


class TestAxBasic(AllTypes):
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_hp.yaml'])
            ax_config = AxTunerConfig(name="Basic Test", minimize=False, objective_name="None", verbose_logging=False)
            config = ConfigArgBuilder(HPOne, HPTwo).tuner(ax_config)
            return config


class TestAxCompose(AllTypes):
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_hp_compose.yaml'])
            ax_config = AxTunerConfig(name="Basic Test", minimize=False, objective_name="None", verbose_logging=False)
            config = ConfigArgBuilder(HPOne, HPTwo).tuner(ax_config)
            return config

    def test_hp_one(self, arg_builder):
        assert arg_builder._tune_namespace.HPOne.hp_int.bounds == (20, 200)
        assert arg_builder._tune_namespace.HPOne.hp_int.type == 'int'
        assert arg_builder._tune_namespace.HPOne.hp_int.log_scale is False
        assert arg_builder._tune_namespace.HPOne.hp_int_log.bounds == (10, 100)
        assert arg_builder._tune_namespace.HPOne.hp_int_log.type == 'int'
        assert arg_builder._tune_namespace.HPOne.hp_int_log.log_scale is True
        assert arg_builder._tune_namespace.HPOne.hp_float.bounds == (10.0, 100.0)
        assert arg_builder._tune_namespace.HPOne.hp_float.type == 'float'
        assert arg_builder._tune_namespace.HPOne.hp_float.log_scale is False
        assert arg_builder._tune_namespace.HPOne.hp_float_log.bounds == (10.0, 100.0)
        assert arg_builder._tune_namespace.HPOne.hp_float_log.type == 'float'
        assert arg_builder._tune_namespace.HPOne.hp_float_log.log_scale is True


class TestAxSample(SampleTypes):
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_hp.yaml'])
            ax_config = AxTunerConfig(name="Basic Test", minimize=False, objective_name="None", verbose_logging=False)
            config = ConfigArgBuilder(HPOne, HPTwo).tuner(ax_config)
            return config