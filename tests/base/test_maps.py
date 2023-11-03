# -*- coding: utf-8 -*-
import sys

from typing import List, Tuple, Optional

import pytest

from spock import spock
from spock import SpockBuilder
from spock.exceptions import _SpockInstantiationError


class DummyClass:
    def __init__(self, value):
        self.value = value


class TestMaps:
    def test_return_raise(self, monkeypatch, tmp_path):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )
            with pytest.raises(_SpockInstantiationError):

                @spock
                class FailReturnConfig:
                    val_1: float = 0.5

                    def __maps__(self):
                        print(self.val_1)

                config = SpockBuilder(
                    FailReturnConfig,
                    desc="Test Builder",
                )
                config.generate()

    def test_map_return(self, monkeypatch, tmp_path):
        with monkeypatch.context() as m:
            m.setattr(
                sys,
                "argv",
                [""],
            )

            @spock
            class ReturnConfig:
                val_1: float = 0.5

                def __maps__(self):
                    return DummyClass(value=self.val_1)

            config = SpockBuilder(
                ReturnConfig,
                desc="Test Builder",
            )
            configs = config.generate()
            assert configs.ReturnConfig._maps.value == configs.ReturnConfig.val_1
