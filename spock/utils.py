# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Utility functions for Spock"""

from copy import copy
import os
from time import localtime
from time import strftime
from typing import List
from typing import Tuple
import git
from spock._dataclasses import field


def add_info(out_dict):
    """Adds extra information to the output dictionary

    *Args*:

        out_dict: output dictionary

    *Returns*:

        out_dict: output dictionary
    """
    out_dict = add_date_info(out_dict)
    out_dict = add_repo_info(out_dict)
    return out_dict


def add_repo_info(out_dict):
    """Adds GIT information to the output dictionary

    *Args*:

        out_dict: output dictionary

    *Returns*:

        out_dict: output dictionary
    """
    try:
        # Assume we are working out of a repo
        repo = git.Repo(os.getcwd())
        out_dict.update({'# Git BRANCH': repo.active_branch.name})
        out_dict.update({'# Git COMMIT SHA': repo.head.object.hexsha})
        if len(repo.untracked_files) > 0 or len(repo.head.commit.diff(None)) > 0:
            git_status = 'DIRTY'
        else:
            git_status = 'CLEAN'
        out_dict.update({'# Git STATUS': git_status})
        out_dict.update({'# Git ORIGIN': repo.remotes.origin.url})
    except git.InvalidGitRepositoryError:
        # But it's okay if we are not
        for key in ('BRANCH', 'COMMIT SHA', 'STATUS', 'ORIGIN'):
            out_dict.update({f'# Git {key}': 'UNKNOWN'})

    return out_dict


def add_date_info(out_dict):
    """Adds date information to the output dictionary

    *Args*:

        out_dict: output dictionary

    *Returns*:

        out_dict: output dictionary
    """
    out_dict.update({'# Run Date': strftime('%Y_%m_%d_%H_%M_%S', localtime())})
    return out_dict


def cast(x):
    """Recasts lists as tuples

    *Args*:

        x: object

    *Returns*:

        x: object or object recast as Tuple
    """
    if isinstance(x, list):
        x = tuple(x)
    return x


def _def_list(values: List):
    """Creates a list of default values for List datatype that is mutable

    *Args*:

        values: default list

    Returns:

        list built from default factory

    """
    return field(default_factory=lambda: copy(values))


def _def_tuple(values: Tuple):
    """Creates a tuple of default values for Tuple datatype that is mutable

        *Args*:

            values: default tuple

        Returns:

            tuple built from default factory

        """
    return field(default_factory=lambda: copy(values))
