import pulumi
from pulumi_azure_nextgen.resources import latest as resources
from pulumi_azure_nextgen.web import latest as web

from azure.common.client_factory import get_client_from_cli_profile
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient

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
env_params_file_location = str("../../generic/json/applications-" + stackName + ".json")
with open(env_params_file_location) as env_params_file:
    env_params_data = json.load(env_params_file)
    print("Environment parameter file contents:")
    pprint(env_params_data)


# Create an Azure Resource Group
applicationsResourceGroup = resources.ResourceGroup(
    env_params_data["resourceGroups"]["applications"]["name"],
    resource_group_name=env_params_data["resourceGroups"]["applications"]["name"],
    location=generic_params_data["regions"]["primaryRegion"]["name"],
)

# Create an app service
for appService in env_params_data["resources"]:
    print("Creating or updating app service", appService["name"])

    appServicePlanResource = web.AppServicePlan(
        appService["servicePlanName"],
        name=appService["servicePlanName"],
        kind=appService["kind"],
        reserved=appService["reserved"],
        location=applicationsResourceGroup.location,
        resource_group_name=applicationsResourceGroup.name,
        sku=appService["svcSku"],
    )

    appResource = web.WebApp(
        appService["name"],
        name=appService["name"],
        location=applicationsResourceGroup.location,
        resource_group_name=applicationsResourceGroup.name,
        server_farm_id=appServicePlanResource.id,
        site_config=appService["appConfig"],
    )

    ## TODO: Convert this to a dynamic provider
    # Get client from Azure CLI profile
    app_service_client = get_client_from_cli_profile(WebSiteManagementClient)

    # Set source control configuration on web app
    poller = app_service_client.web_apps.create_or_update_source_control(
        resource_group_name=env_params_data["resourceGroups"]["applications"]["name"],
        name=appService["name"],
        site_source_control=appService["sourceControlConfig"],
    )

    sc_result = poller.result()

    print(
        f"Set source control on web app to {sc_result.branch} branch of {sc_result.repo_url}"
    )
    ##


# Export relevant data to Pulumi output
pulumi.export("applicationsResourceGroupName", applicationsResourceGroup.name)
