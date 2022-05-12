# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles Spock data type wrappers"""

import argparse

import yaml


class Spockspace(argparse.Namespace):
    """Inherits from Namespace to implement a pretty print on the obj

    Overwrites the __repr__ method with a pretty version of printing

    """

    def __init__(self, **kwargs):
        super(Spockspace, self).__init__(**kwargs)

    @property
    def __repr_dict__(self):
        return {k: v for k, v in self.__dict__.items() if k not in {"__key__", "__salt__"}}

    def __repr__(self):
        # Remove aliases in YAML print
        yaml.Dumper.ignore_aliases = lambda *args: True
        return yaml.dump(self.__repr_dict__, default_flow_style=False)

    def __iter__(self):
        for k, v in self.__dict__.items():
            yield k, v
