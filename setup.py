#!/usr/bin/env python3

# Copyright (c) 2019 Anton Semjonov
# Licensed under the MIT License

# metadata
NAME = "randomart"
AUTHOR = "Anton Semjonov"
EMAIL = "anton@semjonov.de"
URL = "https://github.com/ansemjo/randomart"
LICENSE = "MIT"
DESCRIPTION = "Generate ASCII randomart by hashing input and using an adapted drunken bishop alogirthm."
KEYWORDS = "randomart drunken bishop openssh hash comparison"
SCRIPTS = [NAME + ".py"]
PYTHON = ">3.5"
REQUIREMENTS = ["numpy"]

# imports
from os import environ
from pathlib import Path as path
from subprocess import check_output as cmd
from setuptools import setup, find_packages

# read current version
environ["REVISION_SEPERATOR"] = "-dev"
VERSION = cmd(["sh", "version.sh", "version"]).strip().decode()

# embed package metadata subset
with (path(NAME) / "__metadata__.py").open("w") as v:
    v.write(f'VERSION = "{VERSION}"\n')
    v.write(f'AUTHOR = "{AUTHOR}"\n')
    v.write(f'URL = "{URL}"\n')
    v.write(f'DESCRIPTION = "{DESCRIPTION}"\n')

setup(
    name=NAME,
    description=DESCRIPTION,
    keywords=KEYWORDS,
    version=VERSION,
    license=LICENSE,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    scripts=SCRIPTS,
    packages=find_packages(),
    python_requires=PYTHON,
    install_requires=REQUIREMENTS,
)
