import pulumi
from pulumi_azure_nextgen.resources import latest as resources
from pulumi_azure_nextgen.network import latest as network
from pulumi_azure_nextgen.compute import latest as compute

import json
from pprint import pprint

import os

import random
import string

stackName = pulumi.get_stack()
infrastructure = pulumi.StackReference(f"DevSecNinja/infrastructure/{stackName}")

# Check if the stackName is either develop or production
if stackName == "develop":
    print("Pulumi Stack is develop")
elif stackName == "production":
    print("Pulumi Stack is production - be careful")
else:
    raise AssertionError("We can only serve the develop and production Pulumi stack")

# Print the current directory
currentDirectory = os.getcwd()
print("Current directory is:", str(currentDirectory))

# Import generic variables from JSON
with open("../../generic/json/generic.json") as generic_params_file:
    generic_params_data = json.load(generic_params_file)
    print("Generic parameter file contents:")
    pprint(generic_params_data)

# Import environment-specific variables from JSON
env_params_file_location = str("../../generic/json/compute-" + stackName + ".json")
with open(env_params_file_location) as env_params_file:
    env_params_data = json.load(env_params_file)
    print("Environment parameter file contents:")
    pprint(env_params_data)

# Gather infrastructure details
# fmt: off
outputName = "platformVirtualNetworkSubnets-devsecninjaplatform" + generic_params_data["environments"][stackName]["shortName"] + "-vnet"
platformVirtualNetworkSubnetsOutput = infrastructure.get_output(outputName)

platformVirtualNetworkSubnet = network.Subnet.get(
    "platformVirtualNetworkSubnet",
    id=platformVirtualNetworkSubnetsOutput[0]["id"]
)

# Create an Azure Resource Group
computeResourceGroup = resources.ResourceGroup(
    env_params_data["resourceGroups"]["platform"]["name"],
    resource_group_name=env_params_data["resourceGroups"]["platform"]["name"],
    location=generic_params_data["regions"]["primaryRegion"]["name"],
)

# Create a network interface and Virtual Machine
for virtualMachine in env_params_data["virtualMachines"]["windowsServer"]["resources"]:
    print(
        "Creating virtual machine",
        virtualMachine["name"]
    )

    vmNetworkInterface = network.NetworkInterface(
        (virtualMachine["name"] + "nic01"),
        location=computeResourceGroup.location,
        network_interface_name=(virtualMachine["name"] + "-NIC01"),
        resource_group_name=computeResourceGroup.name,
        ip_configurations=[{
            "name": "ipconfig1",
            "subnet": {
                "id": platformVirtualNetworkSubnet.id
            },
        }],
    )

    def get_random_password_string(length):
        password_characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(password_characters) for i in range(length))
        return password

    vmResource = compute.VirtualMachine(
        virtualMachine["name"],
        vm_name=virtualMachine["name"],
        location=computeResourceGroup.location,
        resource_group_name=computeResourceGroup.name,
        diagnostics_profile=env_params_data["virtualMachines"]["windowsServer"]["settings"]["diagnosticsProfile"],
        hardware_profile={
            "vmSize": virtualMachine["size"],
        },
        network_profile={
            "networkInterfaces": [{
                "id": vmNetworkInterface.id,
                "primary": True,
            }]
        },
        os_profile={
            "adminUsername": env_params_data["virtualMachines"]["windowsServer"]["settings"]["osProfile"]["adminUsername"],
            "adminPassword": get_random_password_string(20),
            "computerName": virtualMachine["name"],
            "windowsConfiguration": env_params_data["virtualMachines"]["windowsServer"]["settings"]["osProfile"]["windowsConfiguration"],
        },
        storage_profile={
            "imageReference": env_params_data["virtualMachines"]["windowsServer"]["settings"]["storageProfile"]["imageReference"],
            "osDisk": {
                "caching": env_params_data["virtualMachines"]["windowsServer"]["settings"]["storageProfile"]["osDisk"]["caching"],
                "createOption": env_params_data["virtualMachines"]["windowsServer"]["settings"]["storageProfile"]["osDisk"]["createOption"],
                "managedDisk": env_params_data["virtualMachines"]["windowsServer"]["settings"]["storageProfile"]["osDisk"]["managedDisk"],
                "name": (virtualMachine["name"] + "-OSDISK")
            }
        }
    )

# fmt: on

# Export relevant data to Pulumi output
pulumi.export("computeResourceGroupName", computeResourceGroup.name)
