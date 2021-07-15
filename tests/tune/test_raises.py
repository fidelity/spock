# -*- coding: utf-8 -*-
from tests.tune.attr_configs_test import *
import pytest
import sys
from spock.builder import ConfigArgBuilder
import optuna


class TestIncorrectTunerConfig:
    def test_incorrect_tuner_config(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_hp.yaml'])
            optuna_config = optuna.create_study(study_name="Tests", direction='minimize')
            with pytest.raises(TypeError):
                config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)


class TestInvalidCastChoice:
    def test_invalid_cast_choice(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_hp_cast.yaml'])
            optuna_config = optuna.create_study(study_name="Tests", direction='minimize')
            with pytest.raises(TypeError):
                config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)


class TestInvalidCastRange:
    def test_invalid_cast_range(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test_hp_cast_bounds.yaml'])
            optuna_config = optuna.create_study(study_name="Tests", direction='minimize')
            with pytest.raises(ValueError):
                config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)
