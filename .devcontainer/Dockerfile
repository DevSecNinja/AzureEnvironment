#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

# Update the VARIANT arg in devcontainer.json to pick a Python version: 3, 3.8, 3.7, 3.6
# To fully customize the contents of this image, use the following Dockerfile instead:
# https://github.com/microsoft/vscode-dev-containers/tree/v0.128.0/containers/python-3/.devcontainer/base.Dockerfile
ARG VARIANT="3"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

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