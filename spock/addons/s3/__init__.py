# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""
Spock is a framework that helps manage complex parameter configurations for Python applications

Please refer to the documentation provided in the README.md
"""

from spock.addons.s3.configs import S3Config, S3DownloadConfig, S3UploadConfig

__all__ = ["configs", "utils", "S3Config", "S3DownloadConfig", "S3UploadConfig"]
