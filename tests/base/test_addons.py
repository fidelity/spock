# -*- coding: utf-8 -*-
import sys

import pytest

from spock.builder import ConfigArgBuilder
from tests.base.attr_configs_test import *
import datetime


class TestBasicBuilder:
    """Testing when builder is calling an add on functionality it shouldn't"""

    def test_raise_tuner_sample(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            # Serialize
            config = ConfigArgBuilder(
                *all_configs,
                desc="Test Builder",
            )
            now = datetime.datetime.now()
            curr_int_time = int(f"{now.year}{now.month}{now.day}{now.hour}{now.second}")
            with pytest.raises(ValueError):
                config_values = config.save(
                    file_extension=".yaml",
                    file_name=f"pytest.{curr_int_time}",
                    user_specified_path=tmp_path,
                    add_tuner_sample=True,
                )

    def test_raise_save_best(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            # Serialize
            config = ConfigArgBuilder(
                *all_configs,
                desc="Test Builder",
            )
            now = datetime.datetime.now()
            curr_int_time = int(f"{now.year}{now.month}{now.day}{now.hour}{now.second}")
            with pytest.raises(ValueError):
                config_values = config.save_best(
                    file_extension=".yaml",
                    file_name=f"pytest.{curr_int_time}",
                    user_specified_path=tmp_path,
                )
