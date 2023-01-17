# -*- coding: utf-8 -*-
import datetime
import re
import sys

from spock.addons.s3 import S3Config
from spock.builder import ConfigArgBuilder
from tests.base.attr_configs_test import *
from tests.base.base_asserts_test import *
from tests.s3.fixtures_test import *


# S3 Tests
class TestAllTypesFromS3MockYAML(AllTypes):
    """Check all required types work as expected"""

    @staticmethod
    @pytest.fixture
    def arg_builder(monkeypatch, s3):
        with monkeypatch.context() as m:
            aws_session, s3_client = s3
            # Mock a S3 bucket and object
            mock_s3_bucket = "spock-test"
            mock_s3_object = "fake/test/bucket/pytest.s3load.yaml"
            s3_client.create_bucket(Bucket=mock_s3_bucket)
            s3_client.upload_file(
                "./tests/conf/yaml/test.yaml", mock_s3_bucket, mock_s3_object
            )
            m.setattr(
                sys, "argv", ["", "--config", f"s3://{mock_s3_bucket}/{mock_s3_object}"]
            )
            config = ConfigArgBuilder(
                *all_configs,
                s3_config=S3Config(session=aws_session, s3_session=s3_client),
                desc="Test Builder",
            )
            return config.generate()


class TestS3MockYAMLWriter:
    def test_yaml_s3_mock_file_writer(self, monkeypatch, tmp_path, s3):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            aws_session, s3_client = s3
            m.setattr(sys, "argv", ["", "--config", "./tests/conf/yaml/test.yaml"])
            config = ConfigArgBuilder(
                *all_configs,
                s3_config=S3Config(session=aws_session, s3_session=s3_client),
                desc="Test Builder",
            )
            # Mock a S3 bucket and object
            mock_s3_bucket = "spock-test"
            mock_s3_object = "fake/test/bucket/"
            s3_client.create_bucket(Bucket=mock_s3_bucket)

            # Test the chained version
            now = datetime.datetime.now()
            curr_int_time = int(f"{now.year}{now.month}{now.day}{now.hour}{now.second}")

            # Test the chained version
            config.save(
                user_specified_path=f"s3://{mock_s3_bucket}/{mock_s3_object}",
                file_extension=".yaml",
                file_name=f"pytest.s3save.{curr_int_time}",
            ).generate()
            yaml_regex = re.compile(
                rf"{mock_s3_object}pytest.s3save.{curr_int_time}."
                rf"[a-fA-F0-9]{{8}}-[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{4}}-"
                rf"[a-fA-F0-9]{{4}}-[a-fA-F0-9]{{12}}.spock.cfg.yaml"
            )
            matches = [
                re.fullmatch(yaml_regex, val["Key"])
                for val in s3_client.list_objects(Bucket=mock_s3_bucket)["Contents"]
                if re.fullmatch(yaml_regex, val["Key"]) is not None
            ]
            assert len(matches) == 1
            print(f"Found file at s3://{mock_s3_bucket}/{matches[0].string}")
