from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    FloatField,
    HiddenField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
)

from eNMS.automation.helpers import NAPALM_DRIVERS, NETMIKO_DRIVERS
from eNMS.base.models import MultipleObjectField, ObjectField
from eNMS.base.properties import (
    custom_properties,
    pool_link_properties,
    link_subtypes,
    pool_device_properties,
    device_subtypes,
)


def configure_device_form(cls: FlaskForm) -> FlaskForm:
    for property in custom_properties:
        setattr(cls, property, StringField())
    return cls


def configure_pool_form(cls: FlaskForm) -> FlaskForm:
    cls.device_properties = pool_device_properties
    cls.link_properties = pool_link_properties
    boolean_fields = ["never_update"]
    for cls_name, properties in (
        ("device", pool_device_properties),
        ("link", pool_link_properties),
    ):
        for property in properties:
            boolean_field = f"{cls_name}_{property}_regex"
            setattr(cls, f"{cls_name}_{property}", StringField(property))
            setattr(cls, boolean_field, BooleanField("Regex"))
            boolean_fields.append(boolean_field)
    setattr(cls, "boolean_fields", HiddenField(default=",".join(boolean_fields)))
    return cls


class GottyConnectionForm(FlaskForm):
    address_choices = [("ip_address", "IP address"), ("name", "Name")] + [
        (property, values["pretty_name"])
        for property, values in custom_properties.items()
        if values.get("is_address", False)
    ]
    address = SelectField(choices=address_choices)


class AddObjectForm(FlaskForm):
    id = HiddenField()
    name = StringField()
    description = StringField()
    location = StringField()
    vendor = StringField()
    model = StringField()


@configure_device_form
class AddDevice(AddObjectForm):
    device_types = [subtype for subtype in device_subtypes.items()]
    subtype = SelectField(choices=device_types)
    ip_address = StringField("IP address")
    port = IntegerField(default=22)
    operating_system = StringField()
    os_version = StringField()
    longitude = FloatField(default=0.0)
    latitude = FloatField(default=0.0)
    username = StringField()
    password = PasswordField()
    enable_password = PasswordField()
    napalm_driver = SelectField(choices=NAPALM_DRIVERS)
    netmiko_driver = SelectField(choices=NETMIKO_DRIVERS)


class AddLink(AddObjectForm):
    link_types = [subtype for subtype in link_subtypes.items()]
    subtype = SelectField(choices=link_types)
    source = ObjectField("Device")
    destination = ObjectField("Device")


@configure_pool_form
class AddPoolForm(FlaskForm):
    id = HiddenField()
    name = StringField()
    description = StringField()
    never_update = BooleanField("Never update (for manually selected pools)")


class PoolObjectsForm(FlaskForm):
    list_fields = HiddenField(default="devices,links")
    devices = MultipleObjectField("Device")
    links = MultipleObjectField("Link")


class ImportExportForm(FlaskForm):
    boolean_fields = HiddenField(default="update_pools,replace")
    export_filename = StringField()
    update_pools = BooleanField()
    replace = BooleanField()


class OpenNmsForm(FlaskForm):
    opennms_rest_api = StringField()
    opennms_devices = StringField()
    node_type = [subtype for subtype in device_subtypes.items()]
    subtype = SelectField(choices=node_type)
    opennms_login = StringField()
    password = PasswordField()


class NetboxForm(FlaskForm):
    netbox_address = StringField(default="http://0.0.0.0:8000")
    netbox_token = PasswordField()
    node_type = [subtype for subtype in device_subtypes.items()]
    netbox_type = SelectField(choices=node_type)


class LibreNmsForm(FlaskForm):
    librenms_address = StringField(default="http://librenms.example.com")
    node_type = [subtype for subtype in device_subtypes.items()]
    librenms_type = SelectField(choices=node_type)
    librenms_token = PasswordField()


class DeviceAutomationForm(FlaskForm):
    list_fields = HiddenField(default="jobs")
    jobs = MultipleObjectField("Job")


class CompareConfigurationsForm(FlaskForm):
    display = SelectField(choices=())
    compare_with = SelectField(choices=())
