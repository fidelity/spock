# -*- coding: utf-8 -*-
import sys
import os

import attr
import pytest

from spock import spock
from spock import SpockBuilder
from spock.exceptions import _SpockResolverError
from typing import Optional


@spock
class EnvClass:
    # Basic types no defaults
    env_int: int = "${spock.env:INT}"
    env_float: float = "${spock.env:FLOAT}"
    env_bool: bool = "${spock.env:BOOL}"
    env_str: str = "${spock.env:STRING}"
    # Basic types w/ defaults
    env_int_def: int = "${spock.env:INT_DEF, 3}"
    env_float_def: float = "${spock.env:FLOAT_DEF, 3.0}"
    env_bool_def: bool = "${spock.env:BOOL_DEF, True}"
    env_str_def: str = "${spock.env:STRING_DEF, hello}"
    # Basic types allowing None as default
    env_int_def_opt: Optional[int] = "${spock.env:INT_DEF, None}"
    env_float_def_opt: Optional[float] = "${spock.env:FLOAT_DEF, None}"
    env_bool_def_opt: Optional[bool] = "${spock.env:BOOL_DEF, False}"
    env_str_def_opt: Optional[str] = "${spock.env:STRING_DEF, None}"
    # Basic types w/ defaults -- inject
    env_int_def_inject: int = "${spock.env.inject:INT_DEF, 30}"
    env_float_def_inject: float = "${spock.env.inject:FLOAT_DEF, 30.0}"
    env_bool_def_inject: bool = "${spock.env.inject:BOOL_DEF, False}"
    env_str_def_inject: str = "${spock.env.inject:STRING_DEF, hola}"
    # Basic types w/ defaults -- to crypto
    env_int_def_crypto: int = "${spock.env.crypto:INT_DEF, 300}"
    env_float_def_crypto: float = "${spock.env.crypto:FLOAT_DEF, 300.0}"
    env_bool_def_crypto: bool = "${spock.env.crypto:BOOL_DEF, True}"
    env_str_def_crypto: str = "${spock.env.crypto:STRING_DEF, yikes}"


@spock
class FromCrypto:
    # Basic types from crypto
    env_int_def_from_crypto: int = "${spock.crypto:gAAAAABigpYHrKffEQ203V6L5YEikgAfuzOU6i0xigLinKlXeR7seWHji4aHyoQ-H9IGaXcCns65AZq-cSyXcUFtQ_9w43RUraUM-tqDdCXeiDygeA_BEC0=}"
    env_float_def_from_crypto: float = "${spock.crypto:gAAAAABigpYHuJndgXM8wQ17uDblBfgm256VzXNjCiblpPfL08LndRWSG4E8v7rSPB7AmfoUwmvTW91b1qn1O1UL2aTNdNz-pmkmf6ZrOpxNnSgOF7TSpE8=}"
    env_bool_def_from_crypto: bool = "${spock.crypto:gAAAAABigpYHfzExxlvyFcIjzOMn25Gj-2luN0tGQ1dpDb8lInCY3C5PNTlaV4xLxekQ6x2SJli37dpaRNB4vXBqE1MLU5V9Rth9dlu6olmEuomIzx8V_Nw=}"
    env_str_def_from_crypto: str = "${spock.crypto:gAAAAABigpYH8mqVr8LCATnJBHyTAhnoO6nDXAjzyVlxiXSPSqlmYMp9h4i2S552DC_xQHgUiN11dbyD2psroKUxF_uPDRzhPfvG9mkZvbTEpMpb5JPqJxs=}"


@spock
class CastRaise:
    cast_miss: int = "${spock.env:CAST_MISS}"


@spock
class AnnotationNotInSetRaise:
    annotation_miss: int = "${spock.env.foobar:INT}"


@spock
class AnnotationNotAllowedRaise:
    annotation_miss: int = "${spock.crypto.foobar:INT}"


@spock
class MultipleDefaults:
    multi_def: int = "${spock.env:INT,one,two}"


@spock
class NoDefAllowed:
    no_def: int = "${spock.crypto:INT,one}"


@spock
class NoEnv:
    no_env: int = "${spock.env:PEEKABOO}"


class TestResolverExceptions:
    def test_no_env(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockResolverError):
                config = SpockBuilder(
                    NoEnv,
                    desc="Test Builder",
                )
                config.generate()

    def test_no_def_allowed(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockResolverError):
                config = SpockBuilder(
                    NoDefAllowed,
                    desc="Test Builder",
                )
                config.generate()

    def test_multiple_defaults(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockResolverError):
                config = SpockBuilder(
                    MultipleDefaults,
                    desc="Test Builder",
                )
                config.generate()


    def test_cast_fail(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            os.environ['CAST_MISS'] = "foo"
            with pytest.raises(_SpockResolverError):
                config = SpockBuilder(
                    CastRaise,
                    desc="Test Builder",
                )
                config.generate()

    def test_annotation_not_in_set(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockResolverError):
                config = SpockBuilder(
                    AnnotationNotInSetRaise,
                    desc="Test Builder",
                )
                config.generate()

    def test_annotation_not_allowed(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockResolverError):
                config = SpockBuilder(
                    AnnotationNotAllowedRaise,
                    desc="Test Builder",
                )
                config.generate()


class TestResolvers:
    """Testing resolvers functionality"""
    @staticmethod
    @pytest.fixture
    def arg_builder_no_conf(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])
            os.environ['INT'] = "1"
            os.environ['FLOAT'] = "1.0"
            os.environ["BOOL"] = "true"
            os.environ["STRING"] = "ciao"
            config = SpockBuilder(EnvClass)
            return config.generate()

    @staticmethod
    @pytest.fixture
    def arg_builder_conf(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test_resolvers.yaml"])
            os.environ['INT'] = "2"
            os.environ['FLOAT'] = "2.0"
            os.environ["BOOL"] = "true"
            os.environ["STRING"] = "boo"
            config = SpockBuilder(EnvClass)
            return config.generate()

    @staticmethod
    @pytest.fixture
    def crypto_builder_direct_api(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])
            config = SpockBuilder(FromCrypto, salt='D7fqSVsaFJH2dbjT', key=b'hXYua9l1jbadIqTYdHtM_g7RKI3WwndMYlYuwNJsMpE=')
            return config.generate()

    @staticmethod
    @pytest.fixture
    def crypto_builder_env_api(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])
            os.environ['SALT'] = "D7fqSVsaFJH2dbjT"
            os.environ["KEY"] = "hXYua9l1jbadIqTYdHtM_g7RKI3WwndMYlYuwNJsMpE="
            config = SpockBuilder(FromCrypto, salt='${spock.env:SALT}',
                                  key='${spock.env:KEY}')
            return config.generate()

    @staticmethod
    @pytest.fixture
    def crypto_builder_yaml(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])
            config = SpockBuilder(FromCrypto, salt='./tests/conf/yaml/test_salt.yaml',
                                  key='./tests/conf/yaml/test_key.yaml')
            return config.generate()

    def test_crypto_from_direct_api(self, crypto_builder_direct_api):
        assert crypto_builder_direct_api.FromCrypto.env_int_def_from_crypto == 100
        assert crypto_builder_direct_api.FromCrypto.env_float_def_from_crypto == 100.0
        assert crypto_builder_direct_api.FromCrypto.env_str_def_from_crypto == "hidden"
        assert crypto_builder_direct_api.FromCrypto.env_bool_def_from_crypto is True

    def test_crypto_from_env_api(self, crypto_builder_env_api):
        assert crypto_builder_env_api.FromCrypto.env_int_def_from_crypto == 100
        assert crypto_builder_env_api.FromCrypto.env_float_def_from_crypto == 100.0
        assert crypto_builder_env_api.FromCrypto.env_str_def_from_crypto == "hidden"
        assert crypto_builder_env_api.FromCrypto.env_bool_def_from_crypto is True

    def test_crypto_from_yaml(self, crypto_builder_yaml):
        assert crypto_builder_yaml.FromCrypto.env_int_def_from_crypto == 100
        assert crypto_builder_yaml.FromCrypto.env_float_def_from_crypto == 100.0
        assert crypto_builder_yaml.FromCrypto.env_str_def_from_crypto == "hidden"
        assert crypto_builder_yaml.FromCrypto.env_bool_def_from_crypto is True

    def test_resolver_basic_no_conf(self, arg_builder_no_conf):
        # Basic types no defaults
        assert arg_builder_no_conf.EnvClass.env_int == 1
        assert arg_builder_no_conf.EnvClass.env_float == 1.0
        assert arg_builder_no_conf.EnvClass.env_bool is True
        assert arg_builder_no_conf.EnvClass.env_str == "ciao"
        # Basic types w/ defaults
        assert arg_builder_no_conf.EnvClass.env_int_def == 3
        assert arg_builder_no_conf.EnvClass.env_float_def == 3.0
        assert arg_builder_no_conf.EnvClass.env_bool_def is True
        assert arg_builder_no_conf.EnvClass.env_str_def == "hello"
        # Basic types w/ defaults -- test injection
        assert arg_builder_no_conf.EnvClass.env_int_def_inject == 30
        assert arg_builder_no_conf.EnvClass.env_float_def_inject == 30.0
        assert arg_builder_no_conf.EnvClass.env_bool_def_inject is False
        assert arg_builder_no_conf.EnvClass.env_str_def_inject == "hola"
        # Basic types w/ defaults -- test crypto
        assert arg_builder_no_conf.EnvClass.env_int_def_crypto == 300
        assert arg_builder_no_conf.EnvClass.env_float_def_crypto == 300.0
        assert arg_builder_no_conf.EnvClass.env_bool_def_crypto is True
        assert arg_builder_no_conf.EnvClass.env_str_def_crypto == "yikes"
        # Basic types optional -- None
        assert arg_builder_no_conf.EnvClass.env_int_def_opt is None
        assert arg_builder_no_conf.EnvClass.env_float_def_opt is None
        assert arg_builder_no_conf.EnvClass.env_bool_def_opt is False
        assert arg_builder_no_conf.EnvClass.env_str_def_opt is None

    def test_resolver_basic_conf(self, arg_builder_conf):
        # Basic types no defaults
        assert arg_builder_conf.EnvClass.env_int == 2
        assert arg_builder_conf.EnvClass.env_float == 2.0
        assert arg_builder_conf.EnvClass.env_bool is True
        assert arg_builder_conf.EnvClass.env_str == "boo"
        # Basic types w/ defaults
        assert arg_builder_conf.EnvClass.env_int_def == 4
        assert arg_builder_conf.EnvClass.env_float_def == 4.0
        assert arg_builder_conf.EnvClass.env_bool_def is False
        assert arg_builder_conf.EnvClass.env_str_def == "rawr"
        # Basic types optional -- None
        assert arg_builder_conf.EnvClass.env_int_def_opt is None
        assert arg_builder_conf.EnvClass.env_float_def_opt is None
        assert arg_builder_conf.EnvClass.env_bool_def_opt is False
        assert arg_builder_conf.EnvClass.env_str_def_opt is None
