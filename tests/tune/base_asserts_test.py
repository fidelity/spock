# -*- coding: utf-8 -*-
from spock.addons.tune.ax import AxInterface


class AllTypes:
    def test_hp_one(self, arg_builder):
        assert arg_builder._tune_namespace.HPOne.hp_int.bounds == (10, 100)
        assert arg_builder._tune_namespace.HPOne.hp_int.type == "int"
        assert arg_builder._tune_namespace.HPOne.hp_int.log_scale is False
        assert arg_builder._tune_namespace.HPOne.hp_int_log.bounds == (10, 100)
        assert arg_builder._tune_namespace.HPOne.hp_int_log.type == "int"
        assert arg_builder._tune_namespace.HPOne.hp_int_log.log_scale is True
        assert arg_builder._tune_namespace.HPOne.hp_float.bounds == (10.0, 100.0)
        assert arg_builder._tune_namespace.HPOne.hp_float.type == "float"
        assert arg_builder._tune_namespace.HPOne.hp_float.log_scale is False
        assert arg_builder._tune_namespace.HPOne.hp_float_log.bounds == (10.0, 100.0)
        assert arg_builder._tune_namespace.HPOne.hp_float_log.type == "float"
        assert arg_builder._tune_namespace.HPOne.hp_float_log.log_scale is True

    def test_hp_two(self, arg_builder):
        assert arg_builder._tune_namespace.HPTwo.hp_choice_int.type == "int"
        assert arg_builder._tune_namespace.HPTwo.hp_choice_int.choices == [
            10,
            20,
            40,
            80,
        ]
        assert arg_builder._tune_namespace.HPTwo.hp_choice_float.type == "float"
        assert arg_builder._tune_namespace.HPTwo.hp_choice_float.choices == [
            10.0,
            20.0,
            40.0,
            80.0,
        ]
        assert arg_builder._tune_namespace.HPTwo.hp_choice_bool.type == "bool"
        assert arg_builder._tune_namespace.HPTwo.hp_choice_bool.choices == [True, False]
        assert arg_builder._tune_namespace.HPTwo.hp_choice_str.type == "str"
        assert arg_builder._tune_namespace.HPTwo.hp_choice_str.choices == [
            "hello",
            "ciao",
            "bonjour",
        ]


class SampleTypes:
    def test_sampling(self, arg_builder):
        # Draw random samples and make sure all fall within all of the bounds or sets
        if isinstance(arg_builder._tuner_interface._lib_interface, AxInterface):
            max_draws = arg_builder._tuner_interface.tuner_status[
                "client"
            ].generation_strategy.current_generator_run_limit()[0]
        else:
            max_draws = 25
        for _ in range(max_draws):
            hp_attrs = arg_builder.sample()
            assert 10 <= hp_attrs.HPOne.hp_int <= 100
            assert isinstance(hp_attrs.HPOne.hp_int, int) is True
            assert 10 <= hp_attrs.HPOne.hp_int_log <= 100
            assert isinstance(hp_attrs.HPOne.hp_int_log, int) is True
            assert 10.0 <= hp_attrs.HPOne.hp_float <= 100.0
            assert isinstance(hp_attrs.HPOne.hp_float, float) is True
            assert 10.0 <= hp_attrs.HPOne.hp_float_log <= 100.0
            assert isinstance(hp_attrs.HPOne.hp_float_log, float) is True
            assert hp_attrs.HPTwo.hp_choice_int in [10, 20, 40, 80]
            assert isinstance(hp_attrs.HPTwo.hp_choice_int, int) is True
            assert hp_attrs.HPTwo.hp_choice_float in [10.0, 20.0, 40.0, 80.0]
            assert isinstance(hp_attrs.HPTwo.hp_choice_float, float) is True
            assert hp_attrs.HPTwo.hp_choice_bool in [True, False]
            assert isinstance(hp_attrs.HPTwo.hp_choice_bool, bool) is True
            assert hp_attrs.HPTwo.hp_choice_str in ["hello", "ciao", "bonjour"]
            assert isinstance(hp_attrs.HPTwo.hp_choice_str, str) is True
