#!/usr/bin/env python3

# Copyright (c) 2019 Anton Semjonov
# Licensed under the MIT License

# metadata
meta = {
    "name": "randomart",
    "author": "Anton Semjonov",
    "author_email": "anton@semjonov.de",
    "url": "https://github.com/ansemjo/randomart",
    "license": "MIT",
    "description": "Generate ASCII randomart by hashing input and using an adapted drunken bishop alogirthm.",
    "keywords": "randomart drunken bishop openssh hash comparison",
}

# package requirements
SCRIPTS = [meta["name"] + ".py"]
PYTHON = ">3.5"
REQUIREMENTS = ["numpy"]

# imports
from os import environ
from pathlib import Path as path
from subprocess import check_output as cmd
from setuptools import setup, find_packages

# read current version
environ["REVISION_SEPERATOR"] = "-dev"
meta["version"] = cmd(["sh", "version.sh", "version"]).strip().decode()

# embed package metadata
with (path(meta["name"]) / "__metadata__.py").open("w") as v:
    v.write("metadata = %s" % str(meta))

setup(
    **meta,
    scripts=SCRIPTS,
    packages=find_packages(),
    python_requires=PYTHON,
    install_requires=REQUIREMENTS,
)
