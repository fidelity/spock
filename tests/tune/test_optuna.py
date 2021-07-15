# -*- coding: utf-8 -*-
from tests.tune.base_asserts_test import *
from tests.tune.attr_configs_test import *
import pytest
import sys
from spock.builder import ConfigArgBuilder
from spock.addons.tune import OptunaTunerConfig


class TestOptunaBasic(AllTypes):
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_hp.yaml'])
            optuna_config = OptunaTunerConfig(study_name="Tests", direction="maximize")
            config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)
            return config


class TestOptunaSample(SampleTypes):
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_hp.yaml'])
            optuna_config = OptunaTunerConfig(study_name="Tests", direction="maximize")
            config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)
            return config
