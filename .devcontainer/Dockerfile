#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

# Update the VARIANT arg in devcontainer.json to pick a Python version: 3, 3.8, 3.7, 3.6
# To fully customize the contents of this image, use the following Dockerfile instead:
# https://github.com/microsoft/vscode-dev-containers/tree/v0.128.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
#
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional packages.
#
# RUN apt-get update \
#     && export DEBIAN_FRONTEND=noninteractive \
#    && apt-get -y install --no-install-recommends <your-package-list-here>

#!/bin/bash

# Alias & Environment Variables
RUN echo '' >> ~/.bashrc \
	&& echo '### Start config by postCreateCommand.sh' >> ~/.bashrc \

	&& alias pulprev='pulumi preview' \
	&& echo 'export pulprev=pulumi preview' >> ~/.bashrc \

# && alias python='/opt/python/latest/bin/python' \
# && echo 'export python=/opt/python/latest/bin/python' >> ~/.bashrc \

# && alias PULUMI_PYTHON_CMD='/opt/python/latest/bin/python' \
# && echo 'export PULUMI_PYTHON_CMD=/opt/python/latest/bin/python' >> ~/.bashrc \

# && echo 'export PATH=$PATH:$HOME/.pulumi/bin' >> ~/.bashrc \

	&& echo '### End config by postCreateCommand.sh' >> ~/.bashrc

# Installations
## General

RUN apt-get update -y \
    && export DEBIAN_FRONTEND=noninteractive \
	&& apt-get -y install --no-install-recommends python3-setuptools \
		python3-venv \
		python3-pip \
		apt-transport-https \
		build-essential \
		ca-certificates \
		curl \
		git \
		gnupg \
		software-properties-common \
		wget

## Pulumi
RUN curl -fsSL https://get.pulumi.com/ | bash

## Prepare Python venv for Pulumi
RUN python3 -m venv ./platform/compute/pulumi/venv \
	&& ./platform/compute/pulumi/venv/bin/python -m pip install --upgrade pip setuptools wheel \
	&& ./platform/compute/pulumi/venv/bin/python -m pip install -r ./platform/compute/pulumi/requirements.txt

RUN python3 -m venv ./platform/infrastructure/pulumi/venv \
	&& ./platform/infrastructure/pulumi/venv/bin/python -m pip install --upgrade pip setuptools wheel \
	&& ./platform/infrastructure/pulumi/venv/bin/python -m pip install -r ./platform/infrastructure/pulumi/requirements.txt

RUN python3 -m venv ./platform/applications/pulumi/venv \
	&& ./platform/applications/pulumi/venv/bin/python -m pip install --upgrade pip setuptools wheel \
	&& ./platform/applications/pulumi/venv/bin/python -m pip install -r ./platform/infrastructure/pulumi/requirements.txt
