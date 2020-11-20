# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Utility functions for Spock"""

import ast
from enum import EnumMeta
import os
import subprocess
import sys
from time import localtime
from time import strftime
from warnings import warn
import git
minor = sys.version_info.minor
if minor < 7:
    from typing import GenericMeta as _GenericAlias
else:
    from typing import _GenericAlias


def convert_save_dict(clean_inner_dict, inner_val, inner_key):
    """Convert tuples in save dictionary

    *Args*:

        clean_inner_dict: inner dictionary that is clean
        inner_val: inner value
        inner_key:  inner key

    *Returns*:

        clean_inner_dict: updated with cleaned values

    """
    # Convert tuples to lists so they get written correctly
    if isinstance(inner_val, tuple):
        clean_inner_dict.update({inner_key: list(inner_val)})
    elif inner_val is not None:
        clean_inner_dict.update({inner_key: inner_val})
    return clean_inner_dict


def make_argument(arg_name, arg_type, parser):
    """Make argparser argument based on type

    Based on the type passed in handle the creation of the argparser argument so that overrides will have the correct
    behavior when set

    *Args*:

        arg_name: name for the argument
        arg_type: type of the argument
        parser: current parser

    Returns:

        parser: updated argparser

    """
    # For generic alias we take the input string and use a custom type callable to convert
    if isinstance(arg_type, _GenericAlias):
        parser.add_argument(arg_name, required=False, type=_handle_generic_type_args)
    # For choice enums we need to check a few things first
    elif isinstance(arg_type, EnumMeta):
        type_set = list({type(val.value) for val in arg_type})[0]
        parser.add_argument(arg_name, required=False, type=type_set)
    # For booleans we map to store true
    elif arg_type == bool:
        parser.add_argument(arg_name, required=False, action='store_true')
    # Else we are a simple base type which we can cast to
    else:
        parser.add_argument(arg_name, required=False, type=arg_type)
    return parser


def _handle_generic_type_args(val):
    return ast.literal_eval(val)


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


def make_blank_git(out_dict):
    """Adds blank git info

    *Args*:

        out_dict: current output dictionary

    Returns:

        out_dict: output dictionary with added git info

    """
    for key in ('BRANCH', 'COMMIT SHA', 'STATUS', 'ORIGIN'):
        out_dict.update({f'# Git {key}': 'UNKNOWN'})
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
        # Check if we are really in a detached head state as this will fail
        if minor < 7:
            head_result = subprocess.run('git rev-parse --abbrev-ref --symbolic-full-name HEAD', stdout=subprocess.PIPE,
                                         shell=True, check=False)
        else:
            head_result = subprocess.run('git rev-parse --abbrev-ref --symbolic-full-name HEAD', capture_output=True,
                                         shell=True, check=False)
        if head_result.stdout.decode().rstrip('\n') == 'HEAD':
            out_dict = make_blank_git(out_dict)
        else:
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
        out_dict = make_blank_git(out_dict)

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


def deep_payload_update(source, updates):
    """Deeply updates a dictionary

    Iterates through a dictionary recursively to update individual values within a possibly nested dictionary
    of dictionaries -- creates a dictionary if empty and trying to recurse

    *Args*:

        source: source dictionary
        updates: updates to the dictionary

    *Returns*:

        source: updated version of the source dictionary

    """

    for k, v in updates.items():
        if isinstance(v, dict) and v:
            source_dict = {} if source.get(k) is None else source.get(k)
            updated_dict = deep_payload_update(source_dict, v)
            if updated_dict:
                source[k] = updated_dict
        else:
            source[k] = v
    return source


def check_payload_overwrite(payload, updates, configs, overwrite=''):
    """Warns when parameters are overwritten across payloads as order will matter

    *Args*:

        payload: current payload
        payload_update: update to add to payload
        configs: config path
        overwrite: name of parent

    *Returns*:

    """
    for k, v in updates.items():
        if isinstance(v, dict) and v:
            overwrite += (k + ":")
            current_payload = {} if payload.get(k) is None else payload.get(k)
            check_payload_overwrite(current_payload, v, configs, overwrite=overwrite)
        else:
            if k in payload.keys():
                warn(f'Overriding an already set parameter {overwrite + k} from {configs}\n'
                     f'Be aware that value precedence is set by the order of the config files (last to load)...',
                     SyntaxWarning)
