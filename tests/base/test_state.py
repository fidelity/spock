# -*- coding: utf-8 -*-
import datetime
import os
import re
import sys

from spock.builder import ConfigArgBuilder
from tests.base.attr_configs_test import *


class TestSerializedState:
    def test_serialization_deserialization(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"]
            )
            # Serialize
            config = ConfigArgBuilder(
                *all_configs,
                desc="Test Builder",
            )
            now = datetime.datetime.now()
            curr_int_time = int(f"{now.year}{now.month}{now.day}{now.hour}{now.second}")
            config_values = config.save(
                file_extension=".yaml",
                file_name=f"pytest.{curr_int_time}",
                user_specified_path=tmp_path
            ).generate()
            yaml_regex = re.compile(
                fr"pytest.{curr_int_time}."
                fr"[a-fA-F0-9]{{8}}-[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{4}}-"
                fr"[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{12}}.spock.cfg.yaml"
            )
            matches = [
                re.fullmatch(yaml_regex, val)
                for val in os.listdir(str(tmp_path))
                if re.fullmatch(yaml_regex, val) is not None
            ]
            fname = f"{str(tmp_path)}/{matches[0].string}"
            # Deserialize
            m.setattr(
                sys, "argv", ["", "--config", f"{fname}"]
            )
            de_serial_config = ConfigArgBuilder(
                *all_configs,
                desc="Test Builder",
            ).generate()
            assert config_values == de_serial_config
