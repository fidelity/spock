# -*- coding: utf-8 -*-
from spock import spock, SpockBuilder, directory, file

import os
import sys

import pytest

from typing import List, Tuple, Dict, Optional


class TestFileTypes:
    def test_basic_file_types(self, monkeypatch, tmp_path):
        """Test basic file types"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])

            dir = f"{str(tmp_path)}/foo"
            os.mkdir(dir)
            for i in range(3):
                f = open(f"{dir}/tmp{str(i)}.txt", "x")
                f.close()

            @spock
            class FileTypeOptConfig:
                test_file_opt: Optional[file]
                test_list_file_opt: Optional[List[file]]
                test_dict_file_opt: Optional[Dict[str, file]]
                test_tuple_file_opt: Optional[Tuple[file, file]]

            @spock
            class FileTypeDefConfig:
                test_file_def: file = f"{dir}/tmp0.txt"
                test_list_file_def: List[file] = [f"{dir}/tmp0.txt", f"{dir}/tmp1.txt"]
                test_dict_file_def: Dict[str, file] = {
                    "one": f"{dir}/tmp0.txt",
                    "two": f"{dir}/tmp1.txt",
                    "three": f"{dir}/tmp2.txt",
                }
                test_tuple_file_def: Tuple[file, file] = (
                    f"{dir}/tmp0.txt",
                    f"{dir}/tmp1.txt",
                )

            @spock
            class FileTypeOptDefConfig:
                test_file_opt_def: Optional[file] = f"{dir}/tmp0.txt"
                test_list_file_opt_def: Optional[List[file]] = [
                    f"{dir}/tmp0.txt",
                    f"{dir}/tmp1.txt",
                ]
                test_dict_file_opt_def: Optional[Dict[str, file]] = {
                    "one": f"{dir}/tmp0.txt",
                    "two": f"{dir}/tmp1.txt",
                    "three": f"{dir}/tmp2.txt",
                }
                test_tuple_file_opt_def: Optional[Tuple[file, file]] = (
                    f"{dir}/tmp0.txt",
                    f"{dir}/tmp1.txt",
                )

            config = SpockBuilder(
                FileTypeOptConfig, FileTypeDefConfig, FileTypeOptDefConfig
            ).generate()

            assert config.FileTypeOptConfig.test_file_opt is None
            assert config.FileTypeOptConfig.test_list_file_opt is None
            assert config.FileTypeOptConfig.test_dict_file_opt is None
            assert config.FileTypeOptConfig.test_tuple_file_opt is None

            assert config.FileTypeDefConfig.test_file_def == f"{dir}/tmp0.txt"
            assert config.FileTypeDefConfig.test_list_file_def == [
                f"{dir}/tmp0.txt",
                f"{dir}/tmp1.txt",
            ]
            assert config.FileTypeDefConfig.test_dict_file_def == {
                "one": f"{dir}/tmp0.txt",
                "two": f"{dir}/tmp1.txt",
                "three": f"{dir}/tmp2.txt",
            }
            assert config.FileTypeDefConfig.test_tuple_file_def == (
                f"{dir}/tmp0.txt",
                f"{dir}/tmp1.txt",
            )

            assert config.FileTypeOptDefConfig.test_file_opt_def == f"{dir}/tmp0.txt"
            assert config.FileTypeOptDefConfig.test_list_file_opt_def == [
                f"{dir}/tmp0.txt",
                f"{dir}/tmp1.txt",
            ]
            assert config.FileTypeOptDefConfig.test_dict_file_opt_def == {
                "one": f"{dir}/tmp0.txt",
                "two": f"{dir}/tmp1.txt",
                "three": f"{dir}/tmp2.txt",
            }
            assert config.FileTypeOptDefConfig.test_tuple_file_opt_def == (
                f"{dir}/tmp0.txt",
                f"{dir}/tmp1.txt",
            )


class TestDirTypes:
    def test_basic_dir_types(self, monkeypatch, tmp_path):
        """Test basic directory types"""
        with monkeypatch.context() as m:
            m.setattr(sys, "argv", [""])

            for i in range(3):
                dir = f"{str(tmp_path)}/foo{i}"
                os.mkdir(dir)

            @spock
            class DirectoryTypeOptConfig:
                test_directory_opt: Optional[directory]
                test_list_directory_opt: Optional[List[directory]]
                test_dict_directory_opt: Optional[Dict[str, directory]]
                test_tuple_directory_opt: Optional[Tuple[directory, directory]]

            @spock
            class DirectoryTypeDefConfigCreate:
                test_directory_create: directory = f"{str(tmp_path)}/foo01"
                test_list_directory_create: List[directory] = [
                    f"{str(tmp_path)}/foo01",
                    f"{str(tmp_path)}/foo11",
                ]
                test_dict_directory_create: Dict[str, directory] = {
                    "one": f"{str(tmp_path)}/foo01",
                    "two": f"{str(tmp_path)}/foo11",
                    "three": f"{str(tmp_path)}/foo21",
                }
                test_tuple_directory_create: Tuple[directory, directory] = (
                    f"{str(tmp_path)}/foo01",
                    f"{str(tmp_path)}/foo11",
                )

            @spock
            class DirectoryTypeDefConfig:
                test_directory_def: directory = f"{str(tmp_path)}/foo0"
                test_list_directory_def: List[directory] = [
                    f"{str(tmp_path)}/foo0",
                    f"{str(tmp_path)}/foo1",
                ]
                test_dict_directory_def: Dict[str, directory] = {
                    "one": f"{str(tmp_path)}/foo0",
                    "two": f"{str(tmp_path)}/foo1",
                    "three": f"{str(tmp_path)}/foo2",
                }
                test_tuple_directory_def: Tuple[directory, directory] = (
                    f"{str(tmp_path)}/foo0",
                    f"{str(tmp_path)}/foo1",
                )

            @spock
            class DirectoryTypeOptDefConfig:
                test_directory_opt_def: Optional[directory] = f"{str(tmp_path)}/foo0"
                test_list_directory_opt_def: Optional[List[directory]] = [
                    f"{str(tmp_path)}/foo0",
                    f"{str(tmp_path)}/foo1",
                ]
                test_dict_directory_opt_def: Optional[Dict[str, directory]] = {
                    "one": f"{str(tmp_path)}/foo0",
                    "two": f"{str(tmp_path)}/foo1",
                    "three": f"{str(tmp_path)}/foo2",
                }
                test_tuple_directory_opt_def: Optional[Tuple[directory, directory]] = (
                    f"{str(tmp_path)}/foo0",
                    f"{str(tmp_path)}/foo1",
                )

            config = SpockBuilder(
                DirectoryTypeOptConfig,
                DirectoryTypeDefConfig,
                DirectoryTypeOptDefConfig,
                DirectoryTypeDefConfigCreate,
            ).generate()

            assert config.DirectoryTypeOptConfig.test_directory_opt is None
            assert config.DirectoryTypeOptConfig.test_list_directory_opt is None
            assert config.DirectoryTypeOptConfig.test_dict_directory_opt is None
            assert config.DirectoryTypeOptConfig.test_tuple_directory_opt is None

            assert (
                config.DirectoryTypeDefConfigCreate.test_directory_create
                == f"{str(tmp_path)}/foo01"
            )
            assert config.DirectoryTypeDefConfigCreate.test_list_directory_create == [
                f"{str(tmp_path)}/foo01",
                f"{str(tmp_path)}/foo11",
            ]
            assert config.DirectoryTypeDefConfigCreate.test_dict_directory_create == {
                "one": f"{str(tmp_path)}/foo01",
                "two": f"{str(tmp_path)}/foo11",
                "three": f"{str(tmp_path)}/foo21",
            }
            assert config.DirectoryTypeDefConfigCreate.test_tuple_directory_create == (
                f"{str(tmp_path)}/foo01",
                f"{str(tmp_path)}/foo11",
            )

            assert (
                config.DirectoryTypeDefConfig.test_directory_def
                == f"{str(tmp_path)}/foo0"
            )
            assert config.DirectoryTypeDefConfig.test_list_directory_def == [
                f"{str(tmp_path)}/foo0",
                f"{str(tmp_path)}/foo1",
            ]
            assert config.DirectoryTypeDefConfig.test_dict_directory_def == {
                "one": f"{str(tmp_path)}/foo0",
                "two": f"{str(tmp_path)}/foo1",
                "three": f"{str(tmp_path)}/foo2",
            }
            assert config.DirectoryTypeDefConfig.test_tuple_directory_def == (
                f"{str(tmp_path)}/foo0",
                f"{str(tmp_path)}/foo1",
            )

            assert (
                config.DirectoryTypeOptDefConfig.test_directory_opt_def
                == f"{str(tmp_path)}/foo0"
            )
            assert config.DirectoryTypeOptDefConfig.test_list_directory_opt_def == [
                f"{str(tmp_path)}/foo0",
                f"{str(tmp_path)}/foo1",
            ]
            assert config.DirectoryTypeOptDefConfig.test_dict_directory_opt_def == {
                "one": f"{str(tmp_path)}/foo0",
                "two": f"{str(tmp_path)}/foo1",
                "three": f"{str(tmp_path)}/foo2",
            }
            assert config.DirectoryTypeOptDefConfig.test_tuple_directory_opt_def == (
                f"{str(tmp_path)}/foo0",
                f"{str(tmp_path)}/foo1",
            )
