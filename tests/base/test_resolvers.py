# -*- coding: utf-8 -*-
import datetime
import os
import re
import sys

import pytest

from spock import spock
from spock import SpockBuilder
from spock.exceptions import (
    _SpockEnvResolverError,
    _SpockFieldHandlerError,
    _SpockResolverError,
    _SpockVarResolverError,
    _SpockInstantiationError,
)
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
class Lastly:
    ooooyah: int = 12
    tester: int = 1
    hiyah: bool = True


@spock
class BarFoo:
    newval: Optional[int] = 2
    moreref: int = "${spock.var:Lastly.ooooyah}"


@spock
class FooBar:
    val: int = 12


@spock
class OtherRef:
    other_str: str = "yes"


@spock
class RefClass:
    a_float: float = 12.1
    a_int: int = 3
    a_bool: bool = True
    a_string: str = "helloo"


@spock
class RefClassFile:
    ref_float: float
    ref_int: int
    ref_bool: bool
    ref_string: str
    ref_nested_to_str: str
    ref_nested_to_float: float
    ref_self: float


@spock
class RefClassOptionalFile:
    ref_float: Optional[float]
    ref_int: Optional[int]
    ref_bool: Optional[bool]
    ref_string: Optional[str]
    ref_nested_to_str: Optional[str]
    ref_nested_to_float: Optional[float]
    ref_self: Optional[float]


@spock
class RefClassDefault:
    ref_float: float = "${spock.var:RefClass.a_float}"
    ref_int: int = "${spock.var:RefClass.a_int}"
    ref_bool: bool = "${spock.var:RefClass.a_bool}"
    ref_string: str = "${spock.var:RefClass.a_string}"
    ref_nested_to_str: str = "${spock.var:FooBar.val}.${spock.var:Lastly.tester}"
    ref_nested_to_float: float = "${spock.var:FooBar.val}.${spock.var:Lastly.tester}"
    ref_self: float = "${spock.var:RefClassDefault.ref_float}"
    ref_self_nested: str = (
        "${spock.var:RefClassDefault.ref_string}-${spock.var:OtherRef.other_str}"
    )


class TestRefResolver:
    def test_from_config(self, monkeypatch):
        """Test reading from config to set vars works"""
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test_variable.yaml"]
            )
            config = SpockBuilder(
                RefClassFile, RefClass, Lastly, BarFoo, FooBar
            ).generate()

            assert config.RefClassFile.ref_float == 12.1
            assert config.RefClassFile.ref_int == 3
            assert config.RefClassFile.ref_bool is True
            assert config.RefClassFile.ref_string == "helloo"
            assert config.RefClassFile.ref_nested_to_str == "12.1"
            assert config.RefClassFile.ref_nested_to_float == 12.1
            assert config.RefClassFile.ref_self == config.RefClassFile.ref_float

    def test_from_config_optional(self, monkeypatch):
        """Test reading from config to set vars works"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                ["", "--config", "./tests/conf/yaml/test_variable_opt.yaml"],
            )
            config = SpockBuilder(
                RefClassOptionalFile, RefClass, Lastly, BarFoo, FooBar
            ).generate()

            assert config.RefClassOptionalFile.ref_float == 12.1
            assert config.RefClassOptionalFile.ref_int == 3
            assert config.RefClassOptionalFile.ref_bool is True
            assert config.RefClassOptionalFile.ref_string == "helloo"
            assert config.RefClassOptionalFile.ref_nested_to_str == "12.1"
            assert config.RefClassOptionalFile.ref_nested_to_float == 12.1
            assert (
                config.RefClassOptionalFile.ref_self
                == config.RefClassOptionalFile.ref_float
            )

    def test_from_def(self, monkeypatch):
        """Test reading from config to set vars works"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])
            config = SpockBuilder(
                RefClassDefault, RefClass, Lastly, BarFoo, FooBar, OtherRef
            ).generate()

            assert config.RefClassDefault.ref_float == 12.1
            assert config.RefClassDefault.ref_int == 3
            assert config.RefClassDefault.ref_bool is True
            assert config.RefClassDefault.ref_string == "helloo"
            assert config.RefClassDefault.ref_nested_to_str == "12.1"
            assert config.RefClassDefault.ref_nested_to_float == 12.1
            assert config.RefClassDefault.ref_self == config.RefClassDefault.ref_float
            assert config.RefClassDefault.ref_self_nested == "helloo-yes"


@spock
class RefCastRaise:
    failed: float = "${spock.var:RefClass.a_string}"


@spock
class RefInvalid:
    failed: float = "${spock.var:RefClass.a_str}"


@spock
class RefNotSpockClsRef:
    failed: float = "${spock.var:RefClassier.a_string}"


@spock
class RefCycle1:
    we: int = "${spock.var:RefCycle2.make}"


@spock
class RefCycle2:
    make: float = "${spock.var:RefCycle3.sense}"


@spock
class RefCycle3:
    no: int = 2
    sense: float = "${spock.var:RefCycle1.we}"


@spock
class SelfCycle:
    hi: str = "${spock.var:SelfCycle.my}"
    my: str = "${spock.var:SelfCycle.name}"
    name: str = "${spock.var:SelfCycle.hi}"


class TestRefResolverExceptions:
    def test_cast_raise(self, monkeypatch):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockResolverError):
                config = SpockBuilder(
                    RefCastRaise,
                    RefClass,
                    desc="Test Builder",
                )
                config.generate()

    def test_invalid_raise(self, monkeypatch):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockVarResolverError):
                config = SpockBuilder(
                    RefInvalid,
                    RefClass,
                    desc="Test Builder",
                )
                config.generate()

    def test_not_spock(self, monkeypatch):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockVarResolverError):
                config = SpockBuilder(
                    RefNotSpockClsRef,
                    RefClass,
                    desc="Test Builder",
                )
                config.generate()

    def test_ref_cycle(self, monkeypatch):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    RefCycle1,
                    RefCycle2,
                    RefCycle3,
                    desc="Test Builder",
                )
                config.generate()

    def test_self_cycle(self, monkeypatch):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    SelfCycle,
                    desc="Test Builder",
                )
                config.generate()


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
            with pytest.raises(_SpockFieldHandlerError):
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
            with pytest.raises(_SpockFieldHandlerError):
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
            with pytest.raises(_SpockFieldHandlerError):
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
            os.environ["CAST_MISS"] = "foo"
            with pytest.raises(_SpockFieldHandlerError):
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
            with pytest.raises(_SpockFieldHandlerError):
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
            with pytest.raises(_SpockFieldHandlerError):
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
            os.environ["INT"] = "1"
            os.environ["FLOAT"] = "1.0"
            os.environ["BOOL"] = "true"
            os.environ["STRING"] = "ciao"
            config = SpockBuilder(EnvClass)
            return config.generate()

    @staticmethod
    @pytest.fixture
    def arg_builder_conf(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test_resolvers.yaml"]
            )
            os.environ["INT"] = "2"
            os.environ["FLOAT"] = "2.0"
            os.environ["BOOL"] = "true"
            os.environ["STRING"] = "boo"
            config = SpockBuilder(EnvClass)
            return config.generate(), config

    @staticmethod
    @pytest.fixture
    def crypto_builder_direct_api(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])
            config = SpockBuilder(
                FromCrypto,
                salt="D7fqSVsaFJH2dbjT",
                key=b"hXYua9l1jbadIqTYdHtM_g7RKI3WwndMYlYuwNJsMpE=",
            )
            return config.generate()

    @staticmethod
    @pytest.fixture
    def crypto_builder_env_api(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])
            os.environ["SALT"] = "D7fqSVsaFJH2dbjT"
            os.environ["KEY"] = "hXYua9l1jbadIqTYdHtM_g7RKI3WwndMYlYuwNJsMpE="
            config = SpockBuilder(
                FromCrypto, salt="${spock.env:SALT}", key="${spock.env:KEY}"
            )
            return config.generate()

    @staticmethod
    @pytest.fixture
    def crypto_builder_yaml(monkeypatch):
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])
            config = SpockBuilder(
                FromCrypto,
                salt="./tests/conf/yaml/test_salt.yaml",
                key="./tests/conf/yaml/test_key.yaml",
            )
            return config.generate()

    def test_saver_with_resolvers(self, monkeypatch, tmp_path):
        with monkeypatch.context() as m:
            m.setattr(
                sys, "argv", ["", "--config", "./tests/conf/yaml/test_resolvers.yaml"]
            )
            os.environ["INT"] = "2"
            os.environ["FLOAT"] = "2.0"
            os.environ["BOOL"] = "true"
            os.environ["STRING"] = "boo"
            config = SpockBuilder(EnvClass)
            now = datetime.datetime.now()
            curr_int_time = int(f"{now.year}{now.month}{now.day}{now.hour}{now.second}")
            config_values = config.save(
                file_extension=".yaml",
                file_name=f"pytest.crypto.{curr_int_time}",
                user_specified_path=tmp_path,
            ).generate()
            yaml_regex = re.compile(
                rf"pytest.crypto.{curr_int_time}."
                rf"[a-fA-F0-9]{{8}}-[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{4}}-"
                rf"[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{12}}.spock.cfg.yaml"
            )
            yaml_key_regex = re.compile(
                rf"pytest.crypto.{curr_int_time}."
                rf"[a-fA-F0-9]{{8}}-[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{4}}-"
                rf"[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{12}}.spock.cfg.key.yaml"
            )
            yaml_salt_regex = re.compile(
                rf"pytest.crypto.{curr_int_time}."
                rf"[a-fA-F0-9]{{8}}-[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{4}}-"
                rf"[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{12}}.spock.cfg.salt.yaml"
            )
            matches = [
                re.fullmatch(yaml_regex, val)
                for val in os.listdir(str(tmp_path))
                if re.fullmatch(yaml_regex, val) is not None
            ]

            key_matches = [
                re.fullmatch(yaml_key_regex, val)
                for val in os.listdir(str(tmp_path))
                if re.fullmatch(yaml_key_regex, val) is not None
            ]
            assert len(key_matches) == 1 and key_matches[0] is not None
            salt_matches = [
                re.fullmatch(yaml_salt_regex, val)
                for val in os.listdir(str(tmp_path))
                if re.fullmatch(yaml_salt_regex, val) is not None
            ]
            assert len(salt_matches) == 1 and salt_matches[0] is not None
            fname = f"{str(tmp_path)}/{matches[0].string}"
            keyname = f"{str(tmp_path)}/{key_matches[0].string}"
            saltname = f"{str(tmp_path)}/{salt_matches[0].string}"

            # Deserialize
            m.setattr(sys, "argv", ["", "--config", f"{fname}"])
            de_serial_config = SpockBuilder(
                EnvClass, desc="Test Builder", key=keyname, salt=saltname
            ).generate()
            assert config_values == de_serial_config

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
        arg_builder_conf, _ = arg_builder_conf
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
