# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles all S3 related configurations"""

import attr

try:
    import boto3
    from botocore.client import BaseClient
    from s3transfer.manager import TransferManager
except ImportError:
    print(
        "Missing libraries to support S3 functionality. Please re-install spock with the extra s3 dependencies -- "
        "pip install spock-config[s3]"
    )
from typing import Optional

# Iterate through the allowed download args for S3 and map into optional attr.ib
download_attrs = {
    val: attr.ib(
        default=None,
        type=str,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    for val in TransferManager.ALLOWED_DOWNLOAD_ARGS
}


# Make the class dynamically
S3DownloadConfig = attr.make_class(
    name="S3DownloadConfig", attrs=download_attrs, kw_only=True, frozen=True
)

# Iterate through the allowed upload args for S3 and map into optional attr.ib
upload_attrs = {
    val: attr.ib(
        default=None,
        type=str,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    for val in TransferManager.ALLOWED_UPLOAD_ARGS
}


# Make the class dynamically
S3UploadConfig = attr.make_class(
    name="S3UploadConfig", attrs=upload_attrs, kw_only=True, frozen=True
)


@attr.s(auto_attribs=True)
class S3Config:
    """Configuration class for S3 support

    Attributes:
        session: instantiated boto3 session object
        s3_session: automatically generated s3 client from the boto3 session if not provided
        kms_arn: AWS KMS key ARN (optional)
        temp_folder: temporary working folder to write/read spock configuration(s) (optional: defaults to /tmp)
        download_config: S3DownloadConfig for extra download configs (optional)
        upload_config: S3UploadConfig for extra upload configs (optional)

    """

    session: boto3.Session
    # s3_session: BaseClient = attr.ib(init=False)
    s3_session: Optional[BaseClient] = None
    temp_folder: Optional[str] = "/tmp/"
    download_config: S3DownloadConfig = S3DownloadConfig()
    upload_config: S3UploadConfig = S3UploadConfig()

    def __attrs_post_init__(self):
        if self.s3_session is None:
            self.s3_session = self.session.client("s3")
