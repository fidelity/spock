# -*- coding: utf-8 -*-
import datetime
from spock.builder import ConfigArgBuilder
from spock.addons import S3Config
from tests.base.attr_configs_test import *
from tests.s3.fixtures_test import *
import sys


# S3 Tests
class TestAllTypesFromS3MockYAMLMissingS3:
    """Check all required types work as expected """
    def test_missing_s3_raise(self, monkeypatch, s3):
        with monkeypatch.context() as m:
            aws_session, s3_client = s3
            # Mock a S3 bucket and object
            mock_s3_bucket = "spock-test"
            mock_s3_object = "fake/test/bucket/pytest.load.yaml"
            s3_client.create_bucket(Bucket=mock_s3_bucket)
            s3_client.upload_file('./tests/conf/yaml/test.yaml', mock_s3_bucket, mock_s3_object)
            m.setattr(sys, 'argv', ['', '--config', f's3://{mock_s3_bucket}/{mock_s3_object}'])
            with pytest.raises(ValueError):
                config = ConfigArgBuilder(
                    TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig,
                    desc='Test Builder')


class TestAllTypesFromS3MockYAMLNoObject:
    """Check all required types work as expected """
    def test_missing_s3_object_raise(self, monkeypatch, s3):
        with monkeypatch.context() as m:
            aws_session, s3_client = s3
            # Mock a S3 bucket and object
            mock_s3_bucket = "spock-test"
            mock_s3_object = "fake/test/bucket/pytest.load.yaml"
            s3_client.create_bucket(Bucket=mock_s3_bucket)
            s3_client.upload_file('./tests/conf/yaml/test.yaml', mock_s3_bucket, mock_s3_object)
            m.setattr(sys, 'argv', ['', '--config', f's3://foo/bar.yaml'])
            with pytest.raises(ValueError):
                config = ConfigArgBuilder(
                    TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig,
                    s3_config=S3Config(
                        session=aws_session,
                        s3_session=s3_client
                    ),
                    desc='Test Builder')


class TestS3MockYAMLWriterMissingS3:
    def test_yaml_s3_mock_file_writer_missing_s3(self, monkeypatch, tmp_path, s3):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            aws_session, s3_client = s3
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(
                TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig,
                desc='Test Builder')
            # Mock a S3 bucket and object
            mock_s3_bucket = "spock-test"
            mock_s3_object = "fake/test/bucket/"
            s3_client.create_bucket(Bucket=mock_s3_bucket)

            # Test the chained version
            now = datetime.datetime.now()
            curr_int_time = int(f'{now.year}{now.month}{now.day}{now.hour}{now.second}')
            with pytest.raises(ValueError):
                # Test the chained version
                config.save(
                    user_specified_path=f's3://{mock_s3_bucket}/{mock_s3_object}',
                    file_extension='.yaml',
                    file_name=f'pytest.save.{curr_int_time}'
                ).generate()


class TestS3MockYAMLWriterNoBucket:
    def test_yaml_s3_mock_file_writer_missing_s3(self, monkeypatch, tmp_path, s3):
        """Test the YAML writer works correctly"""
        with monkeypatch.context() as m:
            aws_session, s3_client = s3
            m.setattr(sys, 'argv', ['', '--config',
                                    './tests/conf/yaml/test.yaml'])
            config = ConfigArgBuilder(
                TypeConfig, NestedStuff, NestedListStuff, TypeOptConfig,
                desc='Test Builder')
            # Mock a S3 bucket and object
            mock_s3_bucket = "spock-test"
            mock_s3_object = "fake/test/bucket/"
            s3_client.create_bucket(Bucket=mock_s3_bucket)

            # Test the chained version
            now = datetime.datetime.now()
            curr_int_time = int(f'{now.year}{now.month}{now.day}{now.hour}{now.second}')
            with pytest.raises(ValueError):
                # Test the chained version
                config.save(
                    user_specified_path=f's3://foo/{mock_s3_object}',
                    file_extension='.yaml',
                    file_name=f'pytest.save.{curr_int_time}'
                ).generate()
