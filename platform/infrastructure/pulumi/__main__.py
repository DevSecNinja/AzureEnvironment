import pulumi
from pulumi_azure_nextgen.resources import latest as resources
from pulumi_azure_nextgen.storage import latest as storage
from pulumi_azure_nextgen.network import latest as network

import json
from pprint import pprint

import os

stackName = pulumi.get_stack()

# Check if the stackName is either develop or production
if stackName == "develop":
    print("Pulumi Stack is develop")
elif stackName == "production":
    print("Pulumi Stack is production - be careful")
else:
    raise AssertionError("We can only serve the develop and production Pulumi stack")

# Import generic variables from JSON
with open("../../generic/json/generic.json") as generic_params_file:
    generic_params_data = json.load(generic_params_file)
    print("Generic parameter file contents:")
    pprint(generic_params_data)

# Import environment-specific variables from JSON
env_params_file_location = str(
    "../../generic/json/infrastructure-" + stackName + ".json"
)
with open(env_params_file_location) as env_params_file:
    env_params_data = json.load(env_params_file)
    print("Environment parameter file contents:")
    pprint(env_params_data)

# Create an Azure Resource Group
platformResourceGroup = resources.ResourceGroup(
    env_params_data["resourceGroups"]["platform"]["name"],
    resource_group_name=env_params_data["resourceGroups"]["platform"]["name"],
    location=generic_params_data["regions"]["primaryRegion"]["name"],
)

# Create an Azure Storage Account
print(
    "Creating or updating storage account in resource group: ",
    str(platformResourceGroup.name),
)
platformStorageAccount = storage.StorageAccount(
    env_params_data["storageAccounts"]["platform"]["name"],
    account_name=env_params_data["storageAccounts"]["platform"]["name"],
    kind=env_params_data["storageAccounts"]["settings"]["kind"],
    location=platformResourceGroup.location,
    resource_group_name=platformResourceGroup.name,
    sku=storage.SkuArgs(
        name=env_params_data["storageAccounts"]["settings"]["accountReplicationType"],
    ),
)

# Create the platform virtual networks
for virtualNetwork in env_params_data["virtualNetworks"]["resources"]:
    print(
        "Creating or updating virtual network",
        virtualNetwork["name"],
        "in resource group",
        str(platformResourceGroup.name),
    )

    platformVirtualNetwork = network.VirtualNetwork(
        virtualNetwork["name"],
        virtual_network_name=virtualNetwork["name"],
        location=platformResourceGroup.location,
        resource_group_name=platformResourceGroup.name,
        address_space=virtualNetwork["addressSpace"],
        subnets=virtualNetwork["subnets"],
    )

    # Export relevant outputs for other projects
    outputFormatId = "platformVirtualNetworkId-" + str(virtualNetwork["name"])
    pulumi.export(outputFormatId, platformVirtualNetwork.id)

    outputFormatName = "platformVirtualNetworkName-" + str(virtualNetwork["name"])
    pulumi.export(outputFormatName, platformVirtualNetwork.name)

    outputFormatSubnets = "platformVirtualNetworkSubnets-" + str(virtualNetwork["name"])
    pulumi.export(outputFormatSubnets, platformVirtualNetwork.subnets)


# Export relevant data to Pulumi output
pulumi.export("platformResourceGroupName", platformResourceGroup.name)
pulumi.export("platformStorageAccountId", platformStorageAccount.id)
