---
sidebar_label: configs
title: addons.s3.configs
---

Handles all S3 related configurations

## S3Config Objects

```python
@attr.s(auto_attribs=True)
class S3Config()
```

Configuration class for S3 support

*Attributes*:

    session: instantiated boto3 session object
    s3_session: automatically generated s3 client from the boto3 session if not provided
    kms_arn: AWS KMS key ARN (optional)
    temp_folder: temporary working folder to write/read spock configuration(s) (optional: defaults to /tmp)
    download_config: S3DownloadConfig for extra download configs (optional)
    upload_config: S3UploadConfig for extra upload configs (optional)

