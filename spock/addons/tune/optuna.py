# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles the optuna backend"""


try:
    import optuna
except ImportError:
    print('Missing libraries to support tune functionality. Please re-install with the extra tune dependencies -- '
          'pip install spock-config[tune]')


class OptunaInterface:
    def __init__(self):
        pass

    def sample(self):
        pass
