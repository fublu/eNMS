from collections import OrderedDict
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from netmiko.ssh_dispatcher import CLASS_MAPPER
from wtforms import (
    BooleanField,
    FileField,
    FloatField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    TextAreaField,
    TextField
)

getters_mapping = OrderedDict([
    ('ARP table', 'get_arp_table'),
    ('Interfaces counters', 'get_interfaces_counters'),
    ('Facts', 'get_facts'),
    ('Environment', 'get_environment'),
    ('Configuration', 'get_config'),
    ('Interfaces', 'get_interfaces'),
    ('Interface IP', 'get_interfaces_ip'),
    ('LLDP neighbors', 'get_lldp_neighbors'),
    ('LLDP neighbors detail', 'get_lldp_neighbors_detail'),
    ('MAC address', 'get_mac_address_table'),
    ('NTP servers', 'get_ntp_servers'),
    ('NTP statistics', 'get_ntp_stats'),
    ('Transceivers', 'get_optics'),
    ('SNMP', 'get_snmp_information'),
    ('Users', 'get_users'),
    ('Network instances (VRF)', 'get_network_instances'),
    ('NTP peers', 'get_ntp_peers'),
    ('BGP configuration', 'get_bgp_config'),
    ('BGP neighbors', 'get_bgp_neighbors'),
    ('IPv6', 'get_ipv6_neighbors_table'),
])

napalm_actions = OrderedDict([
    ('Load merge', 'load_merge_candidate'),
    ('Load replace', 'load_replace_candidate'),
])

netmiko_drivers = sorted(
    driver for driver in CLASS_MAPPER
    if 'telnet' not in driver and 'ssh' not in driver
)


class ScriptForm(FlaskForm):
    name = TextField('Name')
    description = TextField('Description')


class ConfigScriptForm(ScriptForm):
    vendor = TextField('Vendor')
    operating_system = TextField('Operating system')
    content = TextAreaField('')
    file = FileField('', validators=[FileAllowed(['yaml'], 'YAML only')])
    content_type_choices = (
        ('simple', 'Simple'),
        ('j2_template', 'Jinja2 template')
    )
    content_type = SelectField('', choices=content_type_choices)


class NetmikoConfigScriptForm(ConfigScriptForm):
    file = FileField('File', validators=[FileAllowed(['yaml'], 'YAML only')])
    netmiko_type_choices = (
        ('show_commands', 'Show commands'),
        ('configuration', 'Configuration')
    )
    netmiko_type = SelectField('', choices=netmiko_type_choices)
    drivers = [(driver, driver) for driver in netmiko_drivers]
    driver = SelectField('', choices=drivers)
    global_delay_factor = FloatField('global_delay_factor', default=1.)


class NapalmConfigScriptForm(ConfigScriptForm):
    action_choices = [(v, k) for k, v in napalm_actions.items()]
    action = SelectField('Actions', choices=action_choices)


class NapalmGettersForm(ScriptForm):
    getters_choices = [(v, k) for k, v in getters_mapping.items()]
    getters = SelectMultipleField('Nodes', choices=getters_choices)


class FileTransferScriptForm(ScriptForm):
    vendor = TextField('Vendor')
    operating_system = TextField('Operating system')
    driver_choices = (
        ('cisco_ios', 'Cisco IOS'),
        ('cisco_xe', 'Cisco IOS-XE'),
        ('cisco_xr', 'Cisco IOS-XR'),
        ('cisco_nxos', 'Cisco NX-OS'),
        ('juniper_junos', 'Juniper'),
        ('arista_eos', 'Arista')
    )
    driver = SelectField('', choices=driver_choices)
    source_file = TextField('Source file')
    dest_file = TextField('Destination file')
    file_system = TextField('File system')
    direction_choices = (('put', 'Upload'), ('get', 'Download'))
    direction = SelectField('', choices=direction_choices)
    overwrite_file = BooleanField()
    disable_md5 = BooleanField()
    inline_transfer = BooleanField()


class NetmikoValidationForm(ScriptForm):
    vendor = TextField('Vendor')
    operating_system = TextField('Operating system')
    drivers = [(driver, driver) for driver in netmiko_drivers]
    driver = SelectField('Driver', choices=drivers)
    command1 = TextField('Command 1')
    command2 = TextField('Command 2')
    command3 = TextField('Command 3')
    pattern1 = TextField('Pattern 1')
    pattern2 = TextField('Pattern 2')
    pattern3 = TextField('Pattern 3')


class AnsibleScriptForm(ScriptForm):
    vendor = TextField('Vendor')
    operating_system = TextField('Operating system')
    playbook_path = TextField('Path to playbook')
    arguments = TextField('Optional arguments')
    inventory_from_selection = BooleanField()


class RestCallScriptForm(ScriptForm):
    choices = ('GET', 'POST', 'PUT', 'DELETE')
    call_type = SelectField('Type', choices=tuple(zip(choices, choices)))
    url = TextField('URL')
    payload = TextAreaField('Payload')
    username = TextField('Username')
    password = PasswordField('Password')
    content = TextField('Content')
    content_regex = BooleanField()
