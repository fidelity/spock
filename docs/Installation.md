# Installation

### Requirements

* Python: 3.6+
* Dependencies: attrs, GitPython, PyYAML, toml
* Tested OS: Unix (Ubuntu 16.04, Ubuntu 18.04), OSX (10.14.6)

### Install/Upgrade

#### Pip/PyPi
```bash
pip install spock-config
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