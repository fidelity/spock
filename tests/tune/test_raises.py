# -*- coding: utf-8 -*-
import sys

import optuna
import pytest

from spock import spock

from spock.addons.tune import AxTunerConfig, OptunaTunerConfig
from spock.builder import ConfigArgBuilder
from spock.exceptions import _SpockFieldHandlerError
from tests.tune.attr_configs_test import *


class TestWrongPayload:
    def test_unknown_arg(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                ["", "--config", "./tests/conf/yaml/test_hp_unknown_arg.yaml"],
            )
            optuna_config = OptunaTunerConfig(
                study_name="Basic Tests", direction="maximize"
            )
            with pytest.raises(ValueError):
                config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)
                return config

    def test_unknown_class(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                ["", "--config", "./tests/conf/yaml/test_hp_unknown_class.yaml"],
            )
            optuna_config = OptunaTunerConfig(
                study_name="Basic Tests", direction="maximize"
            )
            with pytest.raises(TypeError):
                config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)
                return config


class TestNoTunerClasses:
    def test_no_tuner_classes(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])
            optuna_config = optuna.create_study(
                study_name="Tests", direction="minimize"
            )

            @spock
            class DummyClass:
                val: int = 1

            with pytest.raises(RuntimeError):
                config = ConfigArgBuilder(DummyClass).tuner(optuna_config)

    def test_sample_before_tuner(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test_hp.yaml"])
            optuna_config = OptunaTunerConfig(
                study_name="Basic Tests", direction="maximize"
            )
            with pytest.raises(RuntimeError):
                config = ConfigArgBuilder(HPOne, HPTwo).sample()


class TestIncorrectTunerConfig:
    def test_incorrect_tuner_config(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test_hp.yaml"])
            optuna_config = optuna.create_study(
                study_name="Tests", direction="minimize"
            )
            with pytest.raises(TypeError):
                config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)


class TestOptunaInvalidCastChoice:
    def test_invalid_cast_choice(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test_hp_cast.yaml"]
            )
            optuna_config = OptunaTunerConfig(
                study_name="Basic Tests", direction="maximize"
            )
            with pytest.raises(TypeError):
                config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)


class TestOptunaInvalidCastRange:
    def test_invalid_cast_range(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                ["", "--config", "./tests/conf/yaml/test_hp_cast_bounds.yaml"],
            )
            optuna_config = OptunaTunerConfig(
                study_name="Basic Tests", direction="maximize"
            )
            with pytest.raises(_SpockFieldHandlerError):
                config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)


class TestAxInvalidCastChoice:
    def test_invalid_cast_choice(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test_hp_cast.yaml"]
            )
            ax_config = AxTunerConfig(
                name="Basic Test",
                minimize=False,
                objective_name="None",
                verbose_logging=False,
            )
            with pytest.raises(TypeError):
                config = ConfigArgBuilder(HPOne, HPTwo).tuner(ax_config)


class TestAxInvalidCastRange:
    def test_invalid_cast_range(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                ["", "--config", "./tests/conf/yaml/test_hp_cast_bounds.yaml"],
            )
            ax_config = AxTunerConfig(
                name="Basic Test",
                minimize=False,
                objective_name="None",
                verbose_logging=False,
            )
            with pytest.raises(_SpockFieldHandlerError):
                config = ConfigArgBuilder(HPOne, HPTwo).tuner(ax_config)
