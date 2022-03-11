# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0


class _SpockUndecoratedClass(Exception):
    """Custom exception type for non spock decorated classes and not dynamic"""

    pass


class _SpockInstantiationError(Exception):
    """Custom exception for when the spock class cannot be instantiated correctly"""

    pass


class _SpockNotOptionalError(Exception):
    """Custom exception for missing value"""

    pass


class _SpockDuplicateArgumentError(Exception):
    """Custom exception type for duplicated values"""

    pass


class _SpockEvolveError(Exception):
    """Custom exception for when evolve errors occur"""

    pass


class _SpockValueError(Exception):
    """Custom exception for throwing value errors"""

    pass
