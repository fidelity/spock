# Installation

### Requirements

* Python: 3.6+
* Base Dependencies: attrs, GitPython, PyYAML, toml
* Tested OS: Unix (Ubuntu 16.04, Ubuntu 18.04), OSX (10.14.6)

### Install/Upgrade

#### PyPi
```bash
pip install spock-config
```

#### w/ S3 Extension

Extra Dependencies: boto3, botocore, hurry.filesize, s3transfer

```bash
pip install spock-config[s3]
```

#### w/ Hyper-Parameter Tuner Extension

Extra Dependencies: optuna

```bash
pip install spock-config[tune]
```

#### Pip From Source
```bash
pip install git+https://github.com/fidelity/spock
```

#### Build From Source
```bash
git clone https://github.com/fidelity/spock
cd spock
pip install setuptools wheel
python setup.py bdist_wheel
pip install /dist/spock-config-X.X.XxX-py3-none-any.whl
```