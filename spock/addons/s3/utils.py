# -*- coding: utf-8 -*-

# Copyright 2019 FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles all S3 related ops -- allows for s3 functionality to be optional to keep req deps light"""

import attr
try:
    import boto3
    from botocore.client import BaseClient
except ImportError:
    print('Missing libraries to support S3 functionality. Please re-install spock with the extra s3 dependencies -- '
          'pip install spock-config[s3]')
from hurry.filesize import size
import os
from urllib.parse import urlparse
import sys
import typing


@attr.s(auto_attribs=True)
class S3Config:
    """Configuration class for S3 support

    *Attributes*:

        session: instantiated boto3 session object
        s3_session: automatically generated s3 client from the boto3 session
        kms_arn: AWS KMS key ARN (optional)
        temp_folder: temporary working folder to write/read spock configuration(s) (optional: defaults to /tmp)

    """
    session: boto3.Session
    s3_session: BaseClient = attr.ib(init=False)
    kms_arn: typing.Optional[str] = None
    temp_folder: typing.Optional[str] = '/tmp/'

    def __attrs_post_init__(self):
        self.s3_session = self.session.client('s3')


def handle_s3_load_path(path: str, s3_config: S3Config) -> str:
    """Handles loading from S3 uri

    Handles downloading file from a given s3 uri to a local temp location and passing the path back to the handler
    load call

    *Args*:

        path: s3 uri path
        s3_config: s3_config object

    *Returns*:

        temp_path: the temporary path of the config file downloaded from s3

    """
    if s3_config is None:
        raise ValueError('Missing S3Config object which is necessary to handle S3 style paths')
    bucket, obj, fid = get_s3_bucket_object_name(s3_path=path)
    # Construct the full temp path
    temp_path = f'{s3_config.temp_folder}/{fid}'
    # Strip double slashes if exist
    temp_path = temp_path.replace(r'//', r'/')
    temp_path = download_s3(bucket=bucket, obj=obj, temp_path=temp_path, s3_session=s3_config.s3_session)
    return temp_path


def get_s3_bucket_object_name(s3_path: str) -> typing.Tuple[str, str, str]:
    """Splits a S3 uri into bucket, object, name

    *Args*:

        s3_path: s3 uri

    *Returns*:

        bucket
        object
        name

    """
    parsed = urlparse(s3_path)
    return parsed.netloc, parsed.path.lstrip('/'), os.path.basename(parsed.path)


def download_s3(bucket: str, obj: str, temp_path: str, s3_session: BaseClient) -> str:
    """Attempts to download the file from the S3 uri to a temp location

    *Args*:

        bucket: s3 bucket
        obj: s3 object
        temp_path: local temporary path to write file
        s3_session: current s3 session

    *Returns*:

        temp_path: the temporary path of the config file downloaded from s3

    """
    try:
        file_size = s3_session.head_object(Bucket=bucket, Key=obj)['ContentLength']
        print(f'Attempting to download s3://{bucket}/{obj} (size: {size(file_size)})')
        current_progress = 0
        n_ticks = 50

        def _s3_progress_bar(chunk):
            nonlocal current_progress
            # Increment progress
            current_progress += chunk
            done = int(n_ticks * (current_progress / file_size))
            sys.stdout.write(f"\r[%s%s] "
                             f"{int(current_progress/file_size) * 100}%%" % ('=' * done, ' ' * (n_ticks - done)))
            sys.stdout.flush()
            sys.stdout.write('\n\n')
        # Download with the progress callback
        s3_session.download_file(bucket, obj, temp_path, Callback=_s3_progress_bar)
        return temp_path
    except IOError:
        print(f'Failed to download file from S3 '
              f'(bucket: {bucket}, object: {obj}) '
              f'and write to {temp_path}')


def upload_s3(self):
    # Here it should upload to S3 from the written path (/tmp?)
    # How to manage KMS or if file is encrypted? Config obj? Would the session have it already
    pass