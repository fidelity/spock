# -*- coding: utf-8 -*-
import os
import sys

import pytest
import subprocess

from spock import directory, file
from spock.builder import ConfigArgBuilder
from spock.exceptions import _SpockInstantiationError, _SpockFieldHandlerError
from tests.base.attr_configs_test import *


class TestChoiceRaises:
    """Check choice raises correctly"""

    def test_choice_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/choice.yaml"])
            with pytest.raises(_SpockInstantiationError):
                ConfigArgBuilder(ChoiceFail, desc="Test Builder")


class TestOptionalRaises:
    """Check choice raises correctly"""

    def test_coptional_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            # m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/empty.yaml"])
            with pytest.raises(_SpockInstantiationError):
                ConfigArgBuilder(
                    OptionalFail, desc="Test Builder", configs=[], no_cmd_line=True
                )


class TestTupleRaises:
    """Check that Tuple lengths are being enforced correctly"""

    def test_tuple_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/tuple.yaml"])
            with pytest.raises(ValueError):
                ConfigArgBuilder(*all_configs, desc="Test Builder")


class TestOverrideRaise:
    """Checks that override of a specific class variable is failing gracefully"""

    def test_override_raise(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            with pytest.raises(TypeError):
                ConfigArgBuilder(
                    TypeInherited,
                    NestedStuff,
                    NestedStuffOpt,
                    NestedListStuff,
                    TypeOptConfig,
                    SingleNestedConfig,
                    FirstDoubleNestedConfig,
                    SecondDoubleNestedConfig,
                    desc="Test Builder",
                )


class TestEnumMixedFail:
    def test_enum_mixed_fail(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(TypeError):

                @spock
                class EnumFail:
                    choice_mixed: FailedEnum


class TestIncorrectType:
    def test_incorrect_type(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(TypeError):

                @spock
                class TypeFail:
                    weird_type: lambda x: x


@spock
class TupleFail:
    foo: Tuple[int, int, int] = (2, 2)


class TestTupleLen:
    def test_tuple_len_value(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(_SpockInstantiationError):
                m.setattr(
                    sys,
                    "argv",
                    [""],
                )
                config = ConfigArgBuilder(TupleFail, desc="Test Builder")
                config.generate()


@spock
class TupleFailFlip:
    foo: Tuple[int, int] = (2, 2, 3)


class TestTupleLenFlip:
    def test_tuple_len_set(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(_SpockInstantiationError):
                m.setattr(
                    sys,
                    "argv",
                    [""],
                )
                config = ConfigArgBuilder(TupleFailFlip, desc="Test Builder")
                config.generate()


@spock
class TupleMixedTypeMiss:
    foo: Tuple[List[int], str] = ([2], 2)


class TestTupleTypeMiss:
    def test_tuple_len_set(self, monkeypatch):
        with monkeypatch.context() as m:
            with pytest.raises(_SpockInstantiationError):
                m.setattr(
                    sys,
                    "argv",
                    [""],
                )
                config = ConfigArgBuilder(TupleMixedTypeMiss, desc="Test Builder")
                config.generate()


class TestEnumClassMissing:
    def test_enum_class_missing(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                ["", "--config", "./tests/conf/yaml/test_wrong_class_enum.yaml"],
            )
            with pytest.raises(_SpockFieldHandlerError):
                ConfigArgBuilder(*all_configs, desc="Test Builder")


@spock
class RepeatedDefsFailConfig:
    # Nested list configuration
    nested_list_def: List[NestedListStuff] = [NestedListStuff]


class TestMissingRepeatedDefs:
    def test_repeated_defs_fail(self, monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = ConfigArgBuilder(
                    RepeatedDefsFailConfig, NestedListStuff, desc="Test Builder"
                )
                config.generate()


class TestNotValid:
    def test_invalid_file(self, monkeypatch, tmp_path):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )

            dir = f"{str(tmp_path)}/fail_perms"
            os.mkdir(dir)

            with pytest.raises(_SpockInstantiationError):

                @spock
                class FileFail:
                    test_dir: file = dir

                config = ConfigArgBuilder(FileFail, desc="Test Builder")
                config.generate()


class TestWrongPermission:
    def test_dir_write_permission(self, monkeypatch, tmp_path):
        """Tests directory write permission check"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            dir = f"{str(tmp_path)}/fail_perms"
            os.mkdir(dir)
            subprocess.run(["chmod", "444", dir])

            with pytest.raises(_SpockInstantiationError):

                @spock
                class DirWrongPermissions:
                    test_dir: directory = dir

                config = ConfigArgBuilder(DirWrongPermissions, desc="Test Builder")
                config.generate()
        subprocess.run(["chmod", "777", dir])
        os.rmdir(dir)

    def test_dir_read_permission(self, monkeypatch, tmp_path):
        """Tests directory read permission check"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            dir = f"{str(tmp_path)}/fail_perms"
            os.mkdir(dir)
            subprocess.run(["chmod", "222", dir])

            with pytest.raises(_SpockInstantiationError):

                @spock
                class DirWrongPermissions:
                    test_dir: directory = dir

                config = ConfigArgBuilder(DirWrongPermissions, desc="Test Builder")
                config.generate()
        subprocess.run(["chmod", "777", dir])
        os.rmdir(dir)

    def test_file_write_permission(self, monkeypatch, tmp_path):
        """Tests file write permission check"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )

            dir = f"{str(tmp_path)}/fail_perms"
            os.mkdir(dir)
            f = open(f"{dir}/tmp_fail.txt", "x")
            f.close()

            subprocess.run(["chmod", "444", f"{dir}/tmp_fail.txt"])

            with pytest.raises(_SpockInstantiationError):

                @spock
                class FileWrongPermissions:
                    test_file: file = f"{dir}/tmp_fail.txt"

                config = ConfigArgBuilder(FileWrongPermissions, desc="Test Builder")
                config.generate()
        subprocess.run(["chmod", "777", f"{dir}/tmp_fail.txt"])
        os.remove(f"{dir}/tmp_fail.txt")

    def test_file_read_permission(self, monkeypatch, tmp_path):
        """Tests file read permission check"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )

            dir = f"{str(tmp_path)}/fail_perms"
            os.mkdir(dir)
            f = open(f"{dir}/tmp_fail.txt", "x")
            f.close()

            subprocess.run(["chmod", "222", f"{dir}/tmp_fail.txt"])

            with pytest.raises(_SpockInstantiationError):

                @spock
                class FileWrongPermissions:
                    test_file: file = f"{dir}/tmp_fail.txt"

                config = ConfigArgBuilder(FileWrongPermissions, desc="Test Builder")
                config.generate()
        subprocess.run(["chmod", "777", f"{dir}/tmp_fail.txt"])
        os.remove(f"{dir}/tmp_fail.txt")
