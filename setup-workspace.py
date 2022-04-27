# imports
import argparse

from azureml.core import Workspace
from azureml.core.compute import ComputeTarget, AmlCompute, AksCompute

# setup argparse
parser = argparse.ArgumentParser()
parser.add_argument("--subscription-id", type=str, default=None)
parser.add_argument("--workspace-name", type=str, default="AzureWorkshop-ws")
parser.add_argument("--resource-group", type=str, default="AzureWorkshop-rg")
parser.add_argument("--location", type=str, default=None)
args = parser.parse_args()

# define aml compute target(s) to create
amlcomputes = {
    "cpu2-ram16-hdd50": {
        "vm_size": "STANDARD_E2_V3",
        "min_nodes": 0,
        "max_nodes": 1,
        "idle_seconds_before_scaledown": 1200,
    }
}

# create workspace
ws = Workspace.create(
    args.workspace_name,
    subscription_id=args.subscription_id,
    resource_group=args.resource_group,
    location=args.location,
    create_resource_group=False,
    exist_ok=True,
    show_output=True,
)
ws.write_config()

# create aml compute targets
for ct_name in amlcomputes:
    if ct_name not in ws.compute_targets:
        compute_config = AmlCompute.provisioning_configuration(**amlcomputes[ct_name])
        ct = ComputeTarget.create(ws, ct_name, compute_config)
        ct.wait_for_completion(show_output=True)
