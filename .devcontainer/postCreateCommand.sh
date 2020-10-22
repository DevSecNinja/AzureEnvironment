#!/bin/bash

# Prepare Python venv for Pulumi
python -m venv ./.virtualenvs/compute
./.virtualenvs/compute/bin/python -m pip install --upgrade pip setuptools wheel
./.virtualenvs/compute/bin/python -m pip install -r ./platform/compute/pulumi/requirements.txt

python -m venv ./.virtualenvs/infrastructure
./.virtualenvs/infrastructure/bin/python -m pip install --upgrade pip setuptools wheel
./.virtualenvs/infrastructure/bin/python -m pip install -r ./platform/infrastructure/pulumi/requirements.txt

python -m venv ./.virtualenvs/applications
./.virtualenvs/applications/bin/python -m pip install --upgrade pip setuptools wheel
./.virtualenvs/applications/bin/python -m pip install -r ./platform/applications/pulumi/requirements.txt
