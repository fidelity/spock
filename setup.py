# -*- coding: utf-8 -*-
"""Spock Setup"""

from pkg_resources import parse_requirements
import setuptools
import versioneer

with open('README.md', 'r') as fid:
    long_description = fid.read()

with open('REQUIREMENTS.txt', 'r') as fid:
    install_reqs = [str(req) for req in parse_requirements(fid)]

setuptools.setup(
    name='spock-config',
    description='Spock is a framework designed to help manage complex parameter configurations for Python applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="FMR LLC",
    url="https://github.com/fidelity/spock",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    project_urls={
        "Source": "https://github.com/fidelity/spock",
        "Documentation": "https://fidelity.github.io/spock/"
    },
    keywords="dataclass config argparser parameter configuration",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    python_requires='>=3.6',
    install_requires=install_reqs
)
