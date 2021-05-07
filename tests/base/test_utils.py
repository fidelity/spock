# -*- coding: utf-8 -*-
from spock.config import isinstance_spock
from tests.base.attr_configs_test import *


class TestIsInstance:
    def test_isinstance(self):
        """Test that isinstance is behaving correctly"""
        assert isinstance_spock(TypeConfig) is True
        assert isinstance_spock(object) is False
        assert isinstance_spock(StrChoice) is False
