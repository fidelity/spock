---
sidebar_label: utils
title: addons.s3.utils
---

Handles all S3 related ops -- allows for s3 functionality to be optional to keep req deps light

#### handle\_s3\_load\_path

```python
def handle_s3_load_path(path: str, s3_config: S3Config) -> str
```

Handles loading from S3 uri

Handles downloading file from a given s3 uri to a local temp location and passing the path back to the handler
load call

*Args*:

    path: s3 uri path
    s3_config: s3_config object

*Returns*:

    temp_path: the temporary path of the config file downloaded from s3

#### handle\_s3\_save\_path

```python
def handle_s3_save_path(temp_path: str, s3_path: str, name: str, s3_config: S3Config)
```

Handles saving to S3 uri

Points to the local spock configuration file and handles getting it up to S3

*Args*:

    temp_path: the temporary path the spock config was written out to locally
    s3_path: base s3 uri
    name: spock generated filename
    s3_config: s3_config object

*Returns*:

#### get\_s3\_bucket\_object\_name

```python
def get_s3_bucket_object_name(s3_path: str) -> typing.Tuple[str, str, str]
```

Splits a S3 uri into bucket, object, name

*Args*:

    s3_path: s3 uri

*Returns*:

    bucket
    object
    name

#### download\_s3

```python
def download_s3(bucket: str, obj: str, temp_path: str, s3_session: BaseClient, download_config: S3DownloadConfig) -> str
```

Attempts to download the file from the S3 uri to a temp location using any extra arguments to the download

*Args*:

    bucket: s3 bucket
    obj: s3 object
    temp_path: local temporary path to write file
    s3_session: current s3 session
    download_config: S3DownloadConfig with extra options for the file transfer

*Returns*:

    temp_path: the temporary path of the config file downloaded from s3

#### upload\_s3

```python
def upload_s3(bucket: str, obj: str, temp_path: str, s3_session: BaseClient, upload_config: S3UploadConfig)
```

Attempts to upload the local file to the S3 uri using any extra arguments to the upload

*Args*:

    bucket: s3 bucket
    obj: s3 object
    temp_path: temporary path of the config file
    s3_session: current s3 session
    upload_config: S3UploadConfig with extra options for the file transfer

*Returns*:

