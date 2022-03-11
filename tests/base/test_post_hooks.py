# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import sys

import pytest

from spock import spock
from spock import SpockBuilder
from spock.utils import within, gt, ge, lt, le
from spock.exceptions import _SpockInstantiationError


@spock
class WithinLowFailConfig:
    other: float = 0.9

    def __post_hook__(self):
        within(self.other, 0.9, 1.1, inclusive_lower=False, inclusive_upper=False)


@spock
class WithinHighFailConfig:
    other: float = 1.1

    def __post_hook__(self):
        within(self.other, 0.9, 1.1, inclusive_lower=False, inclusive_upper=False)


@spock
class GTFailConfig:
    other: float = 1.0

    def __post_hook__(self):
        gt(self.other, bound=1.1)


@spock
class GEFailConfig:
    other: float = 0.9

    def __post_hook__(self):
        ge(self.other, bound=1.0)


@spock
class LTFailConfig:
    other: float = 1.0

    def __post_hook__(self):
        lt(self.other, bound=0.9)


@spock
class LEFailConfig:
    other: float = 0.9

    def __post_hook__(self):
        le(self.other, bound=0.8)


class TestPostHooks:
    def test_within_low(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    WithinLowFailConfig,
                    desc="Test Builder",
                )
                config.generate()

    def test_within_high(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    WithinHighFailConfig,
                    desc="Test Builder",
                )
                config.generate()

    def test_gt(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    GTFailConfig,
                    desc="Test Builder",
                )
                config.generate()

    def test_ge(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    GEFailConfig,
                    desc="Test Builder",
                )
                config.generate()

    def test_lt(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    LTFailConfig,
                    desc="Test Builder",
                )
                config.generate()

    def test_le(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    LEFailConfig,
                    desc="Test Builder",
                )
                config.generate()