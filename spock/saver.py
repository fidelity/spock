# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles prepping and saving the Spock config"""

import os
from uuid import uuid1
from spock._dataclasses import asdict
from spock.handlers import JSONHandler
from spock.handlers import TOMLHandler
from spock.handlers import YAMLHandler
from spock.utils import add_info


class Saver:
    """Base class for saving configs

    Contains methods to build a correct output payload and then writes to file based on the file
    extension

    *Attributes*:

        _writers: maps file extension to the correct i/o handler

    """
    def __init__(self):
        self._writers = {'.yaml': YAMLHandler, '.toml': TOMLHandler, '.json': JSONHandler}

    def __call__(self, *args, **kwargs):
        return Saver()

    def save(self, payload, path, create_save_path=False, extra_info=True, file_extension='.yaml'):  #pylint: disable=too-many-arguments
        """Writes Spock config to file

        Cleans and builds an output payload and then correctly writes it to file based on the
        specified file extension

        *Args*:

            payload: current config payload
            path: path to save
            create_save_path: boolean to create the path if non-existent
            extra_info: boolean to write extra info
            file_extension: what type of file to write

        *Returns*:

            None

        """
        supported_extensions = list(self._writers.keys())
        if file_extension not in list(self._writers.keys()):
            raise ValueError(f'Invalid fileout extension. Expected a fileout from {supported_extensions}')
        # Make the filename
        name = str(uuid1()) + '.spck.cfg' + file_extension
        fid = path / name
        # Fix up values
        out_dict = self._clean_up_values(payload, extra_info, file_extension)
        try:
            if not os.path.exists(path) and create_save_path:
                os.makedirs(path)
            with open(fid, 'w') as file_out:
                self._writers.get(file_extension)().save(out_dict, file_out)
                # yaml.dump(out_dict, file_out, default_flow_style=False)
        except OSError:
            print('Not a valid file path to write to: {}'.format(fid))

    @staticmethod
    def _clean_up_values(payload, extra_info, file_extension):
        """Clean up the config payload so it can be written to file

        *Args*:

            payload: dirty payload
            extra_info: boolean to add extra info
            file_extension: type of file to write

        *Returns*:

            clean_dict: cleaned output payload

        """
        out_dict = {}
        for key, val in vars(payload).items():
            # Append comment tag to the base class and convert the spock class to a dict
            if file_extension == '.json':
                out_dict.update({key: asdict(val)})
            else:
                out_dict.update({('# ' + key): asdict(val)})
        # Convert values
        clean_dict = {}
        for key, val in out_dict.items():
            clean_inner_dict = {}
            for inner_key, inner_val in val.items():
                # Convert tuples to lists so they get written correctly
                if type(inner_val) == tuple:
                    clean_inner_dict.update({inner_key: list(inner_val)})
                elif inner_val is not None:
                    clean_inner_dict.update({inner_key: inner_val})
            clean_dict.update({key: clean_inner_dict})
        if extra_info:
            clean_dict = add_info(clean_dict)
        return clean_dict
