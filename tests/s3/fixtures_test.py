# -*- coding: utf-8 -*-
import os

import boto3
import pytest
from moto import mock_s3, mock_sts


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="function")
def sts(aws_credentials):
    with mock_sts():
        yield boto3.client("sts", region_name="us-east-1")


@pytest.fixture(scope="function")
def s3(aws_credentials):
    with mock_s3():
        aws_s3_client = boto3.client("s3", region_name="us-east-1")
        aws_session = boto3.Session(region_name="us-east-1")
        yield aws_session, aws_s3_client
