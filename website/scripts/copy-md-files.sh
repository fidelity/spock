#!/bin/bash

# Borrowed from here: https://github.com/facebook/docusaurus/issues/3475

readme_file='../README.md'
index_file='./docs/index.md'

# README
cat << EOF > $index_file
---
slug: /
title: spock
---

<h1 align="center">
    <a href="https://fidelity.github.io/spock/"><img width="200" height="208" src="https://raw.githubusercontent.com/fidelity/spock/master/resources/images/logo_small.png"/></a>
    <h6 align="center">Managing complex configurations any other way would be highly illogical...</h6>
</h1>
EOF

tail -n +3 $readme_file >> $index_file

contrib_file='../CONTRIBUTING.md'
to_contrib_file='./docs/contributing.md'

# Contributing
cat $contrib_file > $to_contrib_file

