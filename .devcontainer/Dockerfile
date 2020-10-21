FROM pulumi/pulumi-python:latest

# Installations
## General
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# hadolint ignore=DL3008
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
		wget \
	&& rm -rf /var/lib/apt/lists/*

## Pulumi
RUN curl -fsSL https://get.pulumi.com/ | bash