# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles all S3 related ops -- allows for s3 functionality to be optional to keep req deps light"""

import attr

try:
    import boto3
    from botocore.client import BaseClient
except ImportError:
    print(
        "Missing libraries to support S3 functionality. Please re-install spock with the extra s3 dependencies -- "
        "pip install spock-config[s3]"
    )
import os
import sys
import typing
from urllib.parse import urlparse

from hurry.filesize import size

from spock.addons.s3.configs import S3Config, S3DownloadConfig, S3UploadConfig


def handle_s3_load_path(path: str, s3_config: S3Config) -> str:
    """Handles loading from S3 uri

    Handles downloading file from a given s3 uri to a local temp location and passing the path back to the handler
    load call

    Args:
        path: s3 uri path
        s3_config: s3_config object

    Returns:
        temp_path: the temporary path of the config file downloaded from s3

    """
    if s3_config is None:
        raise ValueError(
            "Load from S3 -- Missing S3Config object which is necessary to handle S3 style paths"
        )
    bucket, obj, fid = get_s3_bucket_object_name(s3_path=path)
    # Construct the full temp path
    temp_path = f"{s3_config.temp_folder}/{fid}"
    # Strip double slashes if exist
    temp_path = temp_path.replace(r"//", r"/")
    temp_path = download_s3(
        bucket=bucket,
        obj=obj,
        temp_path=temp_path,
        s3_session=s3_config.s3_session,
        download_config=s3_config.download_config,
    )
    return temp_path


def handle_s3_save_path(temp_path: str, s3_path: str, name: str, s3_config: S3Config):
    """Handles saving to S3 uri

    Points to the local spock configuration file and handles getting it up to S3

    Args:
        temp_path: the temporary path the spock config was written out to locally
        s3_path: base s3 uri
        name: spock generated filename
        s3_config: s3_config object

    Returns:
    """
    if s3_config is None:
        raise ValueError(
            "Save to S3 -- Missing S3Config object which is necessary to handle S3 style paths"
        )
    # Fix posix strip
    s3_path = s3_path.replace("s3:/", "s3://")
    bucket, obj, fid = get_s3_bucket_object_name(f"{s3_path}/{name}")
    upload_s3(
        bucket=bucket,
        obj=obj,
        temp_path=temp_path,
        s3_session=s3_config.s3_session,
        upload_config=s3_config.upload_config,
    )


def get_s3_bucket_object_name(s3_path: str) -> typing.Tuple[str, str, str]:
    """Splits a S3 uri into bucket, object, name

    Args:
        s3_path: s3 uri

    Returns:
        bucket
        object
        name

    """
    parsed = urlparse(s3_path)
    return parsed.netloc, parsed.path.lstrip("/"), os.path.basename(parsed.path)


def download_s3(
    bucket: str,
    obj: str,
    temp_path: str,
    s3_session: BaseClient,
    download_config: S3DownloadConfig,
) -> str:
    """Attempts to download the file from the S3 uri to a temp location using any extra arguments to the download

    Args:
        bucket: s3 bucket
        obj: s3 object
        temp_path: local temporary path to write file
        s3_session: current s3 session
        download_config: S3DownloadConfig with extra options for the file transfer

    Returns:
        temp_path: the temporary path of the config file downloaded from s3

    """
    try:
        # Unroll the extra options for those values that are not None
        extra_options = {
            k: v for k, v in attr.asdict(download_config).items() if v is not None
        }
        file_size = s3_session.head_object(Bucket=bucket, Key=obj, **extra_options)[
            "ContentLength"
        ]
        print(f"Attempting to download s3://{bucket}/{obj} (size: {size(file_size)})")
        current_progress = 0
        n_ticks = 50

        def _s3_progress_bar(chunk):
            nonlocal current_progress
            # Increment progress
            current_progress += chunk
            done = int(n_ticks * (current_progress / file_size))
            sys.stdout.write(
                f"\r[%s%s] "
                f"{int(current_progress/file_size) * 100}%%"
                % ("=" * done, " " * (n_ticks - done))
            )
            sys.stdout.flush()
            sys.stdout.write("\n\n")

        # Download with the progress callback
        s3_session.download_file(
            bucket, obj, temp_path, Callback=_s3_progress_bar, ExtraArgs=extra_options
        )
        return temp_path
    except IOError:
        print(
            f"Failed to download file from S3 "
            f"(bucket: {bucket}, object: {obj}) "
            f"and write to {temp_path}"
        )


def upload_s3(
    bucket: str,
    obj: str,
    temp_path: str,
    s3_session: BaseClient,
    upload_config: S3UploadConfig,
):
    """Attempts to upload the local file to the S3 uri using any extra arguments to the upload

    Args:
        bucket: s3 bucket
        obj: s3 object
        temp_path: temporary path of the config file
        s3_session: current s3 session
        upload_config: S3UploadConfig with extra options for the file transfer

    Returns:
    """
    try:
        # Unroll the extra options for those values that are not None
        extra_options = {
            k: v for k, v in attr.asdict(upload_config).items() if v is not None
        }
        file_size = os.path.getsize(temp_path)
        print(f"Attempting to upload s3://{bucket}/{obj} (size: {size(file_size)})")
        current_progress = 0
        n_ticks = 50

        def _s3_progress_bar(chunk):
            nonlocal current_progress
            # Increment progress
            current_progress += chunk
            done = int(n_ticks * (current_progress / file_size))
            sys.stdout.write(
                f"\r[%s%s] "
                f"{int(current_progress/file_size) * 100}%%"
                % ("=" * done, " " * (n_ticks - done))
            )
            sys.stdout.flush()
            sys.stdout.write("\n\n")

        # Upload with progress callback
        s3_session.upload_file(
            temp_path, bucket, obj, Callback=_s3_progress_bar, ExtraArgs=extra_options
        )
    except IOError:
        print(
            f"Failed to upload file to S3 "
            f"(bucket: {bucket}, object: {obj}) "
            f"from {temp_path}"
        )
