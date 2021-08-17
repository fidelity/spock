# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Spock Setup"""

import setuptools
import sys
from platform import python_version
from pkg_resources import parse_requirements

import versioneer

with open("README.md", "r") as fid:
    long_description = fid.read()

with open("REQUIREMENTS.txt", "r") as fid:
    install_reqs = [str(req) for req in parse_requirements(fid)]

with open("./requirements/S3_REQUIREMENTS.txt", "r") as fid:
    s3_reqs = [str(req) for req in parse_requirements(fid)]

with open("./requirements/TUNE_REQUIREMENTS.txt", "r") as fid:
    tune_reqs = [str(req) for req in parse_requirements(fid)]


def _get_tune_reqs():
    if sys.version_info.minor >= 7:
        with open("./requirements/TUNE_REQUIREMENTS.txt", "r") as fid:
            return [str(req) for req in parse_requirements(fid)]
    else:
        raise RuntimeError(f'Installation of the [tune] add-on requires Python 3.7+ -- current Python version is {python_version()}')


setuptools.setup(
    name="spock-config",
    description="Spock is a framework designed to help manage complex parameter configurations for Python applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="FMR LLC",
    url="https://github.com/fidelity/spock",
    download_url="https://github.com/fidelity/spock",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    project_urls={
        "Source": "https://github.com/fidelity/spock",
        "Documentation": "https://fidelity.github.io/spock/",
        "Bug Tracker": "https://fidelity.github.io/spock/issues",
    },
    keywords=[
        "configuration",
        "argparse",
        "parameters",
        "machine learning",
        "deep learning",
        "reproducibility",
    ],
    packages=setuptools.find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    python_requires=">=3.6",
    install_requires=install_reqs,
    extras_require={"s3": s3_reqs, "tune": _get_tune_reqs()},
)
