# -*- coding: utf-8 -*-
import datetime
import glob
import os
import re
import sys

import pytest

from spock.builder import ConfigArgBuilder
from tests.base.attr_configs_test import *


class TestDefaultWriter:
    def test_default_file_writer(self, monkeypatch, tmp_path):
        """Test the default writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                desc="Test Builder",
            )
            # Test the chained version
            config.save(user_specified_path=tmp_path).generate()
            assert len(list(tmp_path.iterdir())) == 1


class TestYAMLWriter:
    def test_yaml_file_writer(self, monkeypatch, tmp_path):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                desc="Test Builder",
            )
            # Test the chained version
            config.save(user_specified_path=tmp_path, file_extension=".yaml").generate()
            check_path = f"{str(tmp_path)}/*.yaml"
            fname = glob.glob(check_path)[0]
            with open(fname, "r") as fin:
                print(fin.read())
            assert len(list(tmp_path.iterdir())) == 1


class TestYAMLWriterCreate:
    def test_yaml_file_writer_create(self, monkeypatch, tmp_path):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                desc="Test Builder",
            )
            # Test the chained version
            config.save(
                user_specified_path=f"{tmp_path}/tmp",
                create_save_path=True,
                file_extension=".yaml",
            ).generate()
            check_path = f"{str(tmp_path)}/tmp/*.yaml"
            fname = glob.glob(check_path)[0]
            with open(fname, "r") as fin:
                print(fin.read())
            assert len(list(tmp_path.iterdir())) == 1


class TestYAMLWriterSavePath:
    def test_yaml_file_writer_save_path(self, monkeypatch):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test_save_path.yaml"]
            )
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                desc="Test Builder",
            )
            # Test the chained version
            now = datetime.datetime.now()
            curr_int_time = int(f"{now.year}{now.month}{now.day}{now.hour}{now.second}")
            config_values = config.save(
                file_extension=".yaml", file_name=f"pytest.{curr_int_time}"
            ).generate()
            yaml_regex = re.compile(
                fr"pytest.{curr_int_time}."
                fr"[a-fA-F0-9]{{8}}-[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{4}}-"
                fr"[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{12}}.spock.cfg.yaml"
            )
            matches = [
                re.fullmatch(yaml_regex, val)
                for val in os.listdir(str(config_values.TypeConfig.save_path))
                if re.fullmatch(yaml_regex, val) is not None
            ]
            fname = f"{str(config_values.TypeConfig.save_path)}/{matches[0].string}"
            with open(fname, "r") as fin:
                print(fin.read())
            assert os.path.exists(fname)
            # Clean up if assert is good
            if os.path.exists(fname):
                os.remove(fname)


class TestYAMLWriterNoPath:
    def test_yaml_file_writer_no_path(self, monkeypatch):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            with pytest.raises(ValueError):
                config = ConfigArgBuilder(
                    TypeConfig,
                    NestedStuff,
                    NestedListStuff,
                    TypeOptConfig,
                    desc="Test Builder",
                )
                # Test the chained version
                config.save(file_extension=".yaml", file_name="pytest").generate()


class TestWritePathRaise:
    def test_yaml_file_writer(self, monkeypatch, tmp_path):
        """Test the YAML writer fails correctly when create path isn't set"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                desc="Test Builder",
            )
            # Test the chained version
            with pytest.raises(FileNotFoundError):
                config.save(
                    user_specified_path=f"{str(tmp_path)}/foo.bar/fizz.buzz/",
                    file_extension=".yaml",
                    create_save_path=False,
                ).generate()


class TestInvalidExtensionTypeRaise:
    def test_yaml_invalid_extension(self, monkeypatch, tmp_path):
        """Test the YAML writer fails correctly when create path isn't set"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                desc="Test Builder",
            )
            # Test the chained version
            with pytest.raises(TypeError):
                config.save(
                    user_specified_path=f"{str(tmp_path)}/foo.bar/fizz.buzz/",
                    file_extension=".foo",
                ).generate()


class TestTOMLWriter:
    def test_toml_file_writer(self, monkeypatch, tmp_path):
        """Check the TOML writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/toml/test.toml"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                desc="Test Builder",
            )
            # Test the chained version
            config.save(user_specified_path=tmp_path, file_extension=".toml").generate()
            check_path = f"{str(tmp_path)}/*.toml"
            fname = glob.glob(check_path)[0]
            with open(fname, "r") as fin:
                print(fin.read())
            assert len(list(tmp_path.iterdir())) == 1


class TestJSONWriter:
    def test_json_file_writer(self, monkeypatch, tmp_path):
        """Check JSON writer works correctly"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/json/test.json"])
            config = ConfigArgBuilder(
                TypeConfig,
                NestedStuff,
                NestedListStuff,
                TypeOptConfig,
                desc="Test Builder",
            )
            # Test the chained version
            config.save(user_specified_path=tmp_path, file_extension=".json").generate()
            check_path = f"{str(tmp_path)}/*.json"
            fname = glob.glob(check_path)[0]
            with open(fname, "r") as fin:
                print(fin.read())
            assert len(list(tmp_path.iterdir())) == 1
