# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""
Spock is a framework that helps manage complex parameter configurations for Python applications

Please refer to the documentation provided in the README.md
"""
from spock.addons.s3.utils import S3Config
from spock.addons.s3.configs import S3DownloadConfig
from spock.addons.s3.configs import S3UploadConfig

__all__ = ["s3", "S3Config", "S3DownloadConfig", "S3UploadConfig"]
