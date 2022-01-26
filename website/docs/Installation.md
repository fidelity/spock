# Installation

### Requirements

* Python: 3.6+ (`[tune]` extension requires 3.7+)
* Base Dependencies: attrs, GitPython, PyYAML, toml
* Tested OS: Ubuntu (16.04, 18.04), OSX (10.14.6, 11.3.1)

### Install/Upgrade

#### PyPi
```shell
pip install spock-config
```

#### w/ S3 Extension

Extra Dependencies: boto3, botocore, hurry.filesize, s3transfer

```shell
pip install spock-config[s3]
```

#### w/ Hyper-Parameter Tuner Extension

Requires Python 3.7+

Extra Dependencies: optuna, ax-platform, torch, torchvision, mypy_extensions (Python < 3.8)

```shell
pip install spock-config[tune]
```

#### Pip From Source
```shell
pip install git+https://github.com/fidelity/spock
```

#### Build From Source
```shell
git clone https://github.com/fidelity/spock
cd spock
pip install setuptools wheel
python setup.py bdist_wheel
pip install /dist/spock-config-X.X.XxX-py3-none-any.whl
```