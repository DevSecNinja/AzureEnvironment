#!/bin/bash

# Alias & Environment Variables
echo '' >> ~/.bashrc
echo '### Start config by postCreateCommand.sh' >> ~/.bashrc

alias pulprev='pulumi preview'
echo 'export pulprev=pulumi preview' >> ~/.bashrc

alias python='/opt/python/latest/bin/python'
echo 'export python=/opt/python/latest/bin/python' >> ~/.bashrc

alias PULUMI_PYTHON_CMD='/opt/python/latest/bin/python'
echo 'export PULUMI_PYTHON_CMD=/opt/python/latest/bin/python' >> ~/.bashrc

echo 'export PATH=$PATH:$HOME/.pulumi/bin' >> ~/.bashrc

echo '### End config by postCreateCommand.sh' >> ~/.bashrc

# Installations
## General
sudo apt-get update -y
sudo apt-get install -y \
	python3-setuptools \
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
curl -fsSL https://get.pulumi.com/ | bash

## Python pip packages
pip3 install -r ./platform/infrastructure/pulumi/requirements.txt
pip3 install -r ./platform/compute/pulumi/requirements.txt

## Prepare Python venv for Pulumi
/opt/python/latest/bin/python -m venv ./platform/compute/pulumi/venv
./platform/compute/pulumi/venv/bin/python -m pip install --upgrade pip setuptools wheel
./platform/compute/pulumi/venv/bin/python -m pip install -r ./platform/compute/pulumi/requirements.txt

/opt/python/latest/bin/python -m venv ./platform/infrastructure/pulumi/venv
./platform/infrastructure/pulumi/venv/bin/python -m pip install --upgrade pip setuptools wheel
./platform/infrastructure/pulumi/venv/bin/python -m pip install -r ./platform/infrastructure/pulumi/requirements.txt

# Finalize
uname -a
