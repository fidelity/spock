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
        """Handles making a clean dict to hind the salt and key on print"""
        return {
            k: v for k, v in self.__dict__.items() if k not in {"__key__", "__salt__"}
        }

    def __repr__(self):
        """Overloaded repr to pretty print the spock object"""
        # Remove aliases in YAML print
        yaml.Dumper.ignore_aliases = lambda *args: True
        # yaml.emitter.Emitter.process_tag = lambda self, *args, **kw: None
        return yaml.dump(self.__repr_dict__, default_flow_style=False)

    def __iter__(self):
        """Iter for the underlying dictionary"""
        for k, v in self.__dict__.items():
            yield k, v
