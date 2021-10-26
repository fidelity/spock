# -*- coding: utf-8 -*-
import datetime
import os
import re
import sys

import pytest
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from spock.addons.tune import OptunaTunerConfig
from spock.builder import ConfigArgBuilder
from tests.tune.attr_configs_test import *
from tests.tune.base_asserts_test import *


class TestOptunaBasic(AllTypes):
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test_hp.yaml"])
            optuna_config = OptunaTunerConfig(
                study_name="Basic Tests", direction="maximize"
            )
            config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)
            return config


class TestOptunaCompose(AllTypes):
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test_hp_compose.yaml"]
            )
            optuna_config = OptunaTunerConfig(
                study_name="Basic Tests", direction="maximize"
            )
            config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)
            return config

    def test_hp_one(self, arg_builder):
        assert arg_builder._tune_namespace.HPOne.hp_int.bounds == (20, 200)
        assert arg_builder._tune_namespace.HPOne.hp_int.type == "int"
        assert arg_builder._tune_namespace.HPOne.hp_int.log_scale is False
        assert arg_builder._tune_namespace.HPOne.hp_int_log.bounds == (10, 100)
        assert arg_builder._tune_namespace.HPOne.hp_int_log.type == "int"
        assert arg_builder._tune_namespace.HPOne.hp_int_log.log_scale is True
        assert arg_builder._tune_namespace.HPOne.hp_float.bounds == (10.0, 100.0)
        assert arg_builder._tune_namespace.HPOne.hp_float.type == "float"
        assert arg_builder._tune_namespace.HPOne.hp_float.log_scale is False
        assert arg_builder._tune_namespace.HPOne.hp_float_log.bounds == (10.0, 100.0)
        assert arg_builder._tune_namespace.HPOne.hp_float_log.type == "float"
        assert arg_builder._tune_namespace.HPOne.hp_float_log.log_scale is True


class TestOptunaSample(SampleTypes):
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test_hp.yaml"])
            optuna_config = OptunaTunerConfig(
                study_name="Sample Tests", direction="maximize"
            )
            config = ConfigArgBuilder(HPOne, HPTwo).tuner(optuna_config)
            return config


class TestOptunaSaveTopLevel:
    def test_save_top_level(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test_optuna.yaml"]
            )
            # Optuna config -- this will internally spawn the study object for the define-and-run style which will be returned
            # as part of the call to sample()
            optuna_config = OptunaTunerConfig(
                study_name="Iris Logistic Regression Tests", direction="maximize"
            )
            now = datetime.datetime.now()
            curr_int_time = int(f"{now.year}{now.month}{now.day}{now.hour}{now.second}")
            config = (
                ConfigArgBuilder(LogisticRegressionHP)
                .tuner(optuna_config)
                .save(
                    user_specified_path="/tmp",
                    file_name=f"pytest.{curr_int_time}",
                )
                .sample()
            )
            # Verify the sample was written out to file
            yaml_regex = re.compile(
                fr"pytest.{curr_int_time}."
                fr"[a-fA-F0-9]{{8}}-[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{4}}-"
                fr"[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{12}}.spock.cfg.yaml"
            )
            matches = [
                re.fullmatch(yaml_regex, val)
                for val in os.listdir("/tmp")
                if re.fullmatch(yaml_regex, val) is not None
            ]
            fname = f"/tmp/{matches[0].string}"
            assert os.path.exists(fname)
            with open(fname, "r") as fin:
                print(fin.read())
            # Clean up if assert is good
            if os.path.exists(fname):
                os.remove(fname)
            return config


class TestIrisOptuna:
    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test_optuna.yaml"]
            )
            # Optuna config -- this will internally spawn the study object for the define-and-run style which will be returned
            # as part of the call to sample()
            optuna_config = OptunaTunerConfig(
                study_name="Iris Logistic Regression Tests", direction="maximize"
            )
            config = ConfigArgBuilder(LogisticRegressionHP).tuner(optuna_config)
            return config

    def test_iris(self, arg_builder):
        # Load the iris data
        X, y = load_iris(return_X_y=True)
        # Split the Iris data
        X_train, X_valid, y_train, y_valid = train_test_split(X, y)

        # Now we iterate through a bunch of optuna trials
        for _ in range(10):
            # The crux of spock support -- call save w/ the add_tuner_sample flag to write the current draw to file and
            # then call save to return the composed Spockspace of the fixed parameters and the sampled parameters
            # Under the hood spock uses the define-and-run Optuna interface -- thus it handled the underlying 'ask' call
            # and returns the necessary trial object in the return dictionary to call 'tell' with the study object
            now = datetime.datetime.now()
            curr_int_time = int(f"{now.year}{now.month}{now.day}{now.hour}{now.second}")
            hp_attrs = arg_builder.save(
                add_tuner_sample=True,
                user_specified_path="/tmp",
                file_name=f"pytest.{curr_int_time}",
            ).sample()
            # Use the currently sampled parameters in a simple LogisticRegression from sklearn
            clf = LogisticRegression(
                C=hp_attrs.LogisticRegressionHP.c,
                solver=hp_attrs.LogisticRegressionHP.solver,
            )
            clf.fit(X_train, y_train)
            val_acc = clf.score(X_valid, y_valid)
            # Get the status of the tuner -- this dict will contain all the objects needed to update
            tuner_status = arg_builder.tuner_status
            # Pull the study and trials object out of the return dictionary and pass it to the tell call using the study
            # object
            tuner_status["study"].tell(tuner_status["trial"], val_acc)
            # Always save the current best set of hyper-parameters
            arg_builder.save_best(user_specified_path="/tmp", file_name=f"pytest")
            # Verify the sample was written out to file
            yaml_regex = re.compile(
                fr"pytest.{curr_int_time}.hp.sample.[0-9]+."
                fr"[a-fA-F0-9]{{8}}-[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{4}}-"
                fr"[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{12}}.spock.cfg.yaml"
            )
            matches = [
                re.fullmatch(yaml_regex, val)
                for val in os.listdir("/tmp")
                if re.fullmatch(yaml_regex, val) is not None
            ]
            fname = f"/tmp/{matches[0].string}"
            assert os.path.exists(fname)
            with open(fname, "r") as fin:
                print(fin.read())
            # Clean up if assert is good
            if os.path.exists(fname):
                os.remove(fname)

        best_config, best_metric = arg_builder.best
        print(f"Best HP Config:\n{best_config}")
        print(f"Best Metric: {best_metric}")
        # Verify the sample was written out to file
        yaml_regex = re.compile(
            fr"pytest.hp.best."
            fr"[a-fA-F0-9]{{8}}-[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{4}}-"
            fr"[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{12}}.spock.cfg.yaml"
        )
        matches = [
            re.fullmatch(yaml_regex, val)
            for val in os.listdir("/tmp")
            if re.fullmatch(yaml_regex, val) is not None
        ]
        fname = f"/tmp/{matches[0].string}"
        assert os.path.exists(fname)
        with open(fname, "r") as fin:
            print(fin.read())
        # Clean up if assert is good
        if os.path.exists(fname):
            os.remove(fname)
