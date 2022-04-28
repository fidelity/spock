# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import sys

from typing import List, Tuple, Optional

import pytest

from spock import spock
from spock import SpockBuilder
from spock.utils import within, gt, ge, lt, le, eq_len, sum_vals
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
class WithinNoneFailConfig:
    other: Optional[float] = None

    def __post_hook__(self):
        within(self.other, 0.9, 1.1, inclusive_lower=False, inclusive_upper=False, allow_optional=False)


@spock
class GTFailConfig:
    other: float = 1.0

    def __post_hook__(self):
        gt(self.other, bound=1.1)


@spock
class GTFailNoneConfig:
    other: Optional[float] = None

    def __post_hook__(self):
        gt(self.other, bound=1.1, allow_optional=False)


@spock
class GEFailConfig:
    other: float = 0.9

    def __post_hook__(self):
        ge(self.other, bound=1.0)


@spock
class GEFailNoneConfig:
    other: Optional[float] = None

    def __post_hook__(self):
        ge(self.other, bound=1.1, allow_optional=False)


@spock
class LTFailConfig:
    other: float = 1.0

    def __post_hook__(self):
        lt(self.other, bound=0.9)


@spock
class LTFailNoneConfig:
    other: Optional[float] = None

    def __post_hook__(self):
        lt(self.other, bound=0.9, allow_optional=False)


@spock
class LEFailConfig:
    other: float = 0.9

    def __post_hook__(self):
        le(self.other, bound=0.8)


@spock
class LEFailNoneConfig:
    other: Optional[float] = None

    def __post_hook__(self):
        le(self.other, bound=0.9, allow_optional=False)


@spock
class EqLenNoneFailConfig:
    val_1: List[int] = [10, 12, 14]
    val_2: Optional[Tuple[int]] = None
    val_3: Tuple[int, int, int] = (1, 2, 3)

    def __post_hook__(self):
        eq_len([self.val_1, self.val_2, self.val_3], allow_optional=False)


@spock
class EqLenNoneConfig:
    val_1: List[int] = [10, 12, 14]
    val_2: Optional[Tuple[int]] = None
    val_3: Tuple[int, int, int] = (1, 2, 3)

    def __post_hook__(self):
        eq_len([self.val_1, self.val_2, self.val_3], allow_optional=True)


@spock
class EqLenNoneTwoLenConfig:
    val_1: List[int] = [10, 12]
    val_2: Optional[Tuple[int]] = None
    val_3: Tuple[int, int, int] = (1, 2, 3)

    def __post_hook__(self):
        eq_len([self.val_1, self.val_2, self.val_3], allow_optional=True)


@spock
class SumNoneFailConfig:
    val_1: float = 0.5
    val_2: float = 0.5
    val_3: Optional[float] = None

    def __post_hook__(self):
        sum_vals([self.val_1, self.val_2, self.val_3], sum_val=1.0, allow_optional=False)


@spock
class SumNoneNotEqualConfig:
    val_1: float = 0.5
    val_2: float = 0.5
    val_3: Optional[float] = None

    def __post_hook__(self):
        sum_vals([self.val_1, self.val_2, self.val_3], sum_val=0.75)


class TestPostHooks:

    def test_sum_none_fail_config(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    SumNoneFailConfig,
                    desc="Test Builder",
                )
                config.generate()

    def test_sum_not_equal_config(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    SumNoneNotEqualConfig,
                    desc="Test Builder",
                )
                config.generate()



    def test_eq_len_two_len_fail(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    EqLenNoneTwoLenConfig,
                    desc="Test Builder",
                )
                config.generate()

    def test_eq_len_none_fail(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    EqLenNoneFailConfig,
                    desc="Test Builder",
                )
                config.generate()

    def test_eq_len_none(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            config = SpockBuilder(
                EqLenNoneConfig,
                desc="Test Builder",
            )
            config.generate()

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

    def test_within_none(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    WithinNoneFailConfig,
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

    def test_gt_none(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    GTFailNoneConfig,
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

    def test_ge_none(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    GEFailNoneConfig,
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

    def test_lt_none(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    LTFailNoneConfig,
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

    def test_le_none(self, monkeypatch, tmp_path):
        """Test serialization/de-serialization"""
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):
                config = SpockBuilder(
                    LEFailNoneConfig,
                    desc="Test Builder",
                )
                config.generate()