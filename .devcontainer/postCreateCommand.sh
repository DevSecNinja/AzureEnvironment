#!/bin/bash

# Prepare Python venv for Pulumi
python -m venv ./.env
./.env/bin/python -m pip install --upgrade pip setuptools wheel
./.env/bin/python -m pip install -r ./platform/compute/pulumi/requirements.txt
./.env/bin/python -m pip install -r ./platform/infrastructure/pulumi/requirements.txt
./.env/bin/python -m pip install -r ./platform/applications/pulumi/requirements.txt
