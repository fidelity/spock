# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""
Spock is a framework that helps manage complex parameter configurations for Python applications

Please refer to the documentation provided in the README.md
"""
from spock.addons.s3.configs import S3DownloadConfig, S3UploadConfig
from spock.addons.s3.utils import S3Config
from spock.addons.tune.config import spockTuner

__all__ = ["s3", "S3Config", "S3DownloadConfig", "S3UploadConfig", "spockTuner"]
