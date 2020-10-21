#!/bin/bash

## Prepare Python venv for Pulumi
python -m venv ./platform/compute/pulumi/venv
./platform/compute/pulumi/venv/bin/python -m pip install --upgrade pip setuptools wheel
./platform/compute/pulumi/venv/bin/python -m pip install -r ./platform/compute/pulumi/requirements.txt

python -m venv ./platform/infrastructure/pulumi/venv
./platform/infrastructure/pulumi/venv/bin/python -m pip install --upgrade pip setuptools wheel
./platform/infrastructure/pulumi/venv/bin/python -m pip install -r ./platform/infrastructure/pulumi/requirements.txt

python -m venv ./platform/applications/pulumi/venv
./platform/applications/pulumi/venv/bin/python -m pip install --upgrade pip setuptools wheel
./platform/applications/pulumi/venv/bin/python -m pip install -r ./platform/applications/pulumi/requirements.txt
