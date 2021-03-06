from os import environ
from sqlalchemy import Boolean, Integer, String, Float
from yaml import load
from typing import Dict, List

from eNMS import db


def get_custom_properties() -> dict:
    filepath = environ.get("PATH_CUSTOM_PROPERTIES")
    if not filepath:
        return {}
    with open(filepath, "r") as properties:
        return load(properties)


sql_types: dict = {
    "boolean": Boolean,
    "float": Float,
    "integer": Integer,
    "string": String,
}

custom_properties: dict = get_custom_properties()

boolean_properties: List[str] = [
    "mattermost_verify_certificate",
    "multiprocessing",
    "is_active",
    "display_only_failed_nodes",
    "send_notification",
    "use_workflow_targets",
    "push_to_git",
    "never_update",
]

list_properties: List[str] = [
    "devices",
    "pools",
    "links",
    "permissions",
    "getters",
    "import_export_types",
]

private_properties: List[str] = ["password", "enable_password"]

base_properties: List[str] = ["id", "name", "description"]

object_common_properties: List[str] = base_properties + [
    "subtype",
    "model",
    "location",
    "vendor",
]

device_subtypes: Dict[str, str] = {
    "antenna": "Antenna",
    "firewall": "Firewall",
    "host": "Host",
    "optical_switch": "Optical switch",
    "regenerator": "Regenerator",
    "router": "Router",
    "server": "Server",
    "switch": "Switch",
}

link_subtypes: Dict[str, str] = {
    "bgp_peering": "BGP peering",
    "etherchannel": "Etherchannel",
    "ethernet_link": "Ethernet link",
    "optical_channel": "Optical channel",
    "optical_link": "Optical link",
    "pseudowire": "Pseudowire",
}

link_subtype_to_color: Dict[str, str] = {
    "bgp_peering": "#77ebca",
    "etherchannel": "#cf228a",
    "ethernet_link": "#0000ff",
    "optical_link": "#d4222a",
    "optical_channel": "#ff8247",
    "pseudowire": "#902bec",
}

device_properties = list(custom_properties) + [
    "operating_system",
    "os_version",
    "netmiko_driver",
    "napalm_driver",
    "ip_address",
    "port",
    "longitude",
    "latitude",
    "username",
]

device_table_properties: List[str] = (
    object_common_properties[1:] + device_properties[:-3]
)

pool_device_properties: List[str] = (
    object_common_properties[1:] + device_properties[:-1] + ["current_configuration"]
)

device_public_properties: List[str] = object_common_properties + device_properties + [
    "last_failure",
    "last_runtime",
    "last_status",
    "last_update",
]

device_configuration_properties: List[str] = [
    "name",
    "last_failure",
    "last_runtime",
    "last_update",
    "last_status",
]

task_properties: List[str] = base_properties + [
    "job",
    "job_name",
    "next_run_time",
    "start_date",
    "end_date",
    "frequency",
    "is_active",
]

task_public_properties: List[str] = task_properties[1:]

link_properties: List[str] = object_common_properties + [
    "source_name",
    "destination_name",
    "source",
    "destination",
]

pool_link_properties: List[str] = link_properties[1:-2]

link_table_properties: List[str] = object_common_properties[1:] + [
    "source_name",
    "destination_name",
]

pool_public_properties: List[str] = base_properties + ["never_update"]

pool_table_properties: List[str] = pool_public_properties[1:]

for obj_type, properties in (
    ("device", pool_device_properties),
    ("link", pool_link_properties),
):
    for prop in properties:
        pool_public_properties.extend(
            [f"{obj_type}_{prop}", f"{obj_type}_{prop}_regex"]
        )
        boolean_properties.append(f"{obj_type}_{prop}_regex")


job_public_properties: List[str] = base_properties + [
    "mail_recipient",
    "max_processes",
    "multiprocessing",
    "vendor",
    "operating_system",
    "type",
    "creator_name",
    "credentials",
    "status",
    "state",
    "positions",
    "push_to_git",
    "waiting_time",
    "number_of_retries",
    "time_between_retries",
    "send_notification",
    "send_notification_method",
    "display_only_failed_nodes",
]

service_public_properties: List[str] = job_public_properties
workflow_public_properties: List[str] = job_public_properties + [
    "last_modified",
    "use_workflow_targets",
]

service_table_properties: List[str] = [
    "name",
    "type",
    "description",
    "creator_name",
    "number_of_retries",
    "time_between_retries",
    "status",
]

workflow_table_properties: List[str] = [
    "name",
    "description",
    "creator_name",
    "vendor",
    "operating_system",
    "number_of_retries",
    "time_between_retries",
    "status",
]

workflow_edge_properties: List[str] = [
    "id",
    "name",
    "subtype",
    "source_id",
    "destination_id",
]

user_public_properties: List[str] = ["id", "name", "email", "permissions"]

user_table_properties: List[str] = user_public_properties[1:-1]

instance_public_properties: List[str] = base_properties + [
    "ip_address",
    "weight",
    "status",
    "cpu_load",
]

instance_table_properties = instance_public_properties[1:]

user_permissions: List[str] = ["Admin", "Connect to device", "View", "Edit"]

log_public_properties: List[str] = ["id", "source_ip", "content"]

log_rule_public_properties: List[str] = log_public_properties + [
    "name",
    "source_ip_regex",
    "content_regex",
    "jobs",
]

log_rule_table_properties: List[str] = ["name"] + log_public_properties

parameters_public_properties: List[str] = [
    "cluster_scan_subnet",
    "cluster_scan_protocol",
    "cluster_scan_timeout",
    "default_longitude",
    "default_latitude",
    "default_zoom_level",
    "default_view",
    "git_configurations",
    "git_automation",
    "gotty_start_port",
    "gotty_end_port",
    "mail_sender",
    "mail_recipients",
    "mattermost_url",
    "mattermost_channel",
    "mattermost_verify_certificate",
    "opennms_rest_api",
    "opennms_devices",
    "opennms_login",
    "pool_filter",
    "slack_channel",
    "slack_token",
]

task_serialized_properties: List[str] = [
    "id",
    "name",
    "description",
    "job_name",
    "status",
    "start_date",
    "end_date",
    "frequency",
    "next_run_time",
    "time_before_next_run",
    "is_active",
    "job",
]

task_table_properties: List[str] = task_serialized_properties[1:-2]

cls_to_properties: Dict[str, List[str]] = {
    "Instance": instance_public_properties,
    "Device": device_public_properties,
    "Link": link_properties,
    "Pool": pool_public_properties,
    "Service": service_public_properties,
    "Parameters": parameters_public_properties,
    "Workflow": workflow_public_properties,
    "WorkflowEdge": workflow_edge_properties,
    "User": user_public_properties,
    "Log": log_public_properties,
    "LogRule": log_rule_public_properties,
    "Task": task_serialized_properties,
}

table_properties: Dict[str, List[str]] = {
    "configuration": device_configuration_properties,
    "device": device_table_properties,
    "instance": instance_table_properties,
    "link": link_table_properties,
    "log": log_public_properties,
    "logrule": log_rule_table_properties,
    "pool": pool_table_properties,
    "service": service_table_properties,
    "task": task_table_properties,
    "user": user_table_properties,
    "workflow": workflow_table_properties,
}


def table_static_entries(type: str, obj: db.Model) -> List[str]:
    status = "" if type != "task" else "Pause" if obj.is_active else "Resume"
    return {
        "configuration": [
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showConfigurations('{obj.id}')">
            Configuration</button>""",
            f"""<label class="btn btn-default btn-xs btn-file"
            style="width:100%;"><a href="download_configuration/{obj.name}">
            Download</a></label>""",
        ],
        "device": [
            f"""<button type="button" class="btn btn-info btn-xs"
            onclick="deviceAutomationModal('{obj.id}')">
            Automation</button>""",
            f"""<button type="button" class="btn btn-success btn-xs"
            onclick="connectionParametersModal('{obj.id}')">
            Connect</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('device', '{obj.id}')">Edit</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('device', '{obj.id}', true)">
            Duplicate</button>""",
            f"""<button type="button" class="btn btn-danger btn-xs"
            onclick="confirmDeletion('device', '{obj.id}')">
            Delete</button>""",
        ],
        "instance": [
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('instance', '{obj.id}')">Edit</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('instance', '{obj.id}', true)">
            Duplicate</button>""",
            f"""<button type="button" class="btn btn-danger btn-xs"
            onclick="confirmDeletion('instance', '{obj.id}')">
            Delete</button>""",
        ],
        "link": [
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('link', '{obj.id}')">Edit</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('link', '{obj.id}', true)">Duplicate
            </button>""",
            f"""<button type="button" class="btn btn-danger btn-xs"
            onclick="confirmDeletion('link', '{obj.id}')">Delete</button>""",
        ],
        "log": [
            f"""<button type="button" class="btn btn-danger btn-xs"
            onclick="deleteInstance('Log', '{obj.id}')">Delete</button>"""
        ],
        "logrule": [
            f"""<button type="button" class="btn btn-info btn-xs"
            onclick="showTypeModal('logrule', '{obj.id}')">
            Edit</button>""",
            f"""<button type="button" class="btn btn-danger btn-xs"
            onclick="deleteInstance('logrule', '{obj.id}')">
            Delete</button>""",
        ],
        "pool": [
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('pool', '{obj.id}')">
            Edit properties</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="updatePool('{obj.id}')">Update</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('pool', '{obj.id}', true)">
            Duplicate</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showPoolObjects('{obj.id}')">Edit objects</button>""",
            f"""<button type="button" class="btn btn-danger btn-xs"
            onclick="confirmDeletion('pool', '{obj.id}')">Delete</button>""",
        ],
        "service": [
            f"""<button type="button" class="btn btn-info btn-xs"
            onclick="showLogs('{obj.id}')"></i>Logs</a></button>""",
            f"""<button type="button" class="btn btn-success btn-xs"
            onclick="runJob('{obj.id}')">Run</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="editService('{obj.id}')">Edit</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="editService('{obj.id}', true)">Duplicate</button>""",
            f"""<button type="button" class="btn btn-danger btn-xs"
            onclick="confirmDeletion('service', '{obj.id}')">
            Delete</button>""",
        ],
        "task": [
            f"""<button id="pause-resume-{obj.id}" type="button"
            class="btn btn-success btn-xs" onclick=
            "{status.lower()}Task('{obj.id}')">{status}</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('task', '{obj.id}')">Edit</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('task', '{obj.id}', true)">
            Duplicate</button>""",
            f"""<button type="button" class="btn btn-danger btn-xs"
            onclick="confirmDeletion('task', '{obj.id}')">
            Delete</button>""",
        ],
        "user": [
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('user', '{obj.id}')">Edit</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('user', '{obj.id}', true)">
            Duplicate</button>""",
            f"""<button type="button" class="btn btn-danger btn-xs"
            onclick="confirmDeletion('user', '{obj.id}')">Delete</button>""",
        ],
        "workflow": [
            f"""<button type="button" class="btn btn-info btn-xs"
            onclick="showLogs('{obj.id}')"></i>Logs</a></button>""",
            f"""<button type="button" class="btn btn-success btn-xs"
            onclick="runJob('{obj.id}')">Run</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showTypeModal('workflow', '{obj.id}')">
            Edit</button>""",
            f"""<button type="button" class="btn btn-primary btn-xs"
            onclick="showWorkflowModalDuplicate('{obj.id}')">
            Duplicate</button>""",
            f"""<button type="button" class="btn btn-danger btn-xs"
            onclick="confirmDeletion('workflow', '{obj.id}')">
            Delete</button>""",
        ],
    }[type]


default_diagrams_properties: Dict[str, str] = {
    "Device": "model",
    "Link": "model",
    "User": "name",
    "Service": "type",
    "Workflow": "vendor",
    "Task": "type",
}

object_diagram_properties: List[str] = ["model", "vendor", "subtype", "location"]

device_diagram_properties: List[str] = (
    object_diagram_properties
    + ["operating_system", "os_version"]
    + list(p for p, v in custom_properties.items() if v["add_to_dashboard"])
)

user_diagram_properties: List[str] = ["name"]

workflow_diagram_properties: List[str] = ["type", "vendor", "operating_system"]

service_diagram_properties: List[str] = ["type", "device_multiprocessing"]

task_diagram_properties: List[str] = ["type", "status", "frequency"]

type_to_diagram_properties: Dict[str, List[str]] = {
    "Device": device_diagram_properties,
    "Link": object_diagram_properties,
    "User": user_diagram_properties,
    "Service": service_diagram_properties,
    "Workflow": workflow_diagram_properties,
    "Task": task_diagram_properties,
}

pretty_names: Dict[str, str] = {
    "access_rights": "Access rights",
    "action": "Action",
    "call_type": "Type of call",
    "command": "Command",
    "current_configuration": "Current Configuration",
    "content": "Content",
    "content_match": "Content Match",
    "content_match_regex": "Match content against Regular expression",
    "content_type": "Content type",
    "cpu_load": "CPU load",
    "creator": "Creator",
    "delete_archive": "Delete archive",
    "delete_folder": "Delete folder",
    "delete_spaces_before_matching": "Delete spaces before matching",
    "description": "Description",
    "destination": "Destination",
    "destination_file": "Destination file",
    "destination_name": "Destination",
    "destination_path": "Destination path",
    "dest_file": "Destination file",
    "device_multiprocessing": "Device multiprocessing",
    "dict_match": "Dictionnary match",
    "direction": "Direction",
    "display_only_failed_nodes": "Display only failed nodes",
    "driver": "Driver",
    "email": "Email",
    "enable_mode": 'Enter "Enable" mode',
    "enable_password": "Enable password",
    "end_date": "End date",
    "fast_cli": "Fast CLI",
    "file": "File",
    "file_system": "File system",
    "frequency": "Frequency",
    "getters": "Getters",
    "global_delay_factor": "Global delay factor",
    "has_targets": "Has targets",
    "headers": "Headers",
    "inventory_from_selection": "Inventory from selection",
    "ip_address": "IP address",
    "is_active": "Is active",
    "job_name": "Service / Workflow",
    "longitude": "Longitude",
    "latitude": "Latitude",
    "load_known_host_keys": "Load known host keys",
    "location": "Location",
    "look_for_keys": "Look for keys",
    "missing_host_key_policy": "Missing Host Key Policy",
    "model": "Model",
    "name": "Name",
    "napalm_driver": "Napalm driver",
    "negative_logic": "Negative Logic",
    "netmiko_driver": "Netmiko driver",
    "never_update": "Never update",
    "next_run_time": "Next runtime",
    "number_of_configuration": "Number of configurations stored",
    "operating_system": "Operating System",
    "optional_args": "Optional arguments",
    "os_version": "OS version",
    "params": "Parameters",
    "pass_device_properties": "Pass device properties to the playbook",
    "password": "Password",
    "payload": "Payload",
    "permission": "Permission",
    "port": "Port",
    "positions": "Positions",
    "protocol": "Protocol",
    "recurrent": "Recurrent",
    "source": "Source",
    "source_name": "Source",
    "source_file": "Source file",
    "source_ip": "Source IP address",
    "start_date": "Start date",
    "status": "Status",
    "subtype": "Subtype",
    "text file": "File",
    "time_before_next_run": "Time before next run",
    "timeout": "Timeout (in seconds)",
    "type": "Type",
    "update_dictionnary": "Update dictionnary",
    "url": "URL",
    "use_device_driver": "Use driver from device",
    "username": "Username",
    "validation_method": "Validation Method",
    "vendor": "Vendor",
    "waiting_time": "Waiting time",
    "weight": "Weight",
}

# Import properties

pretty_names.update({k: v["pretty_name"] for k, v in custom_properties.items()})
reverse_pretty_names: Dict[str, str] = {v: k for k, v in pretty_names.items()}

property_types: Dict[str, str] = {
    "devices": "object-list",
    "links": "object-list",
    "pools": "object-list",
    "jobs": "object-list",
    "edges": "object-list",
    "permissions": "list",
    "job": "object",
    "source": "object",
    "destination": "object",
    "import_export_types": "list",
    "send_notification": "bool",
    "multiprocessing": "bool",
    "is_active": "bool",
    "display_only_failed_nodes": "bool",
    "use_workflow_targets": "bool",
    "never_update": "bool",
    "mattermost_verify_certificate": "bool",
    "push_to_git": "bool",
}

relationships: Dict[str, Dict[str, str]] = {
    "Device": {"job": "Job"},
    "Link": {"source": "Device", "destination": "Device"},
    "Pool": {"device": "Device", "link": "Link"},
    "Service": {
        "creator": "User",
        "device": "Device",
        "pool": "Pool",
        "workflow": "Workflow",
        "task": "Task",
    },
    "Task": {"job": "Job"},
    "Workflow": {
        "creator": "User",
        "edge": "WorkflowEdge",
        "job": "Job",
        "device": "Device",
        "pool": "Pool",
    },
    "WorkflowEdge": {"source": "Job", "destination": "Job", "workflow": "Workflow"},
    "Parameters": {"pool": "Pool"},
    "LogRule": {"job": "Job", "log": "Log"},
}

device_import_properties: List[str] = device_public_properties + ["id"]

link_import_properties: List[str] = link_properties + ["id"]

pool_import_properties: List[str] = pool_public_properties + ["devices"]

service_import_properties: List[str] = service_public_properties + [
    "id",
    "type",
    "devices",
    "pools",
]

task_import_properties: List[str] = base_properties + [
    "start_date",
    "end_date",
    "frequency",
    "status",
    "job",
]

workflow_import_properties: List[str] = workflow_public_properties + [
    "id",
    "jobs",
    "edges",
]

workflow_edge_import_properties: List[str] = [
    "id",
    "name",
    "subtype",
    "source_id",
    "destination_id",
    "workflow",
]

import_properties: Dict[str, List[str]] = {
    "User": user_public_properties,
    "Device": device_import_properties,
    "Link": link_import_properties,
    "Pool": pool_import_properties,
    "Service": service_import_properties,
    "Workflow": workflow_import_properties,
    "WorkflowEdge": workflow_edge_import_properties,
    "Task": task_import_properties,
}

# Export topology properties

export_properties: Dict[str, List[str]] = {
    "Device": device_public_properties,
    "Link": link_table_properties,
}

# Properties to not migrate

dont_migrate: Dict[str, List[str]] = {
    "Device": ["jobs"],
    "Service": ["logs", "state", "tasks", "workflows", "creator_name"],
    "Task": [
        "job_name",
        "next_run_time",
        "is_active",
        "time_before_next_run",
        "status",
    ],
    "Workflow": ["last_modified", "logs", "state", "status", "creator_name"],
}
