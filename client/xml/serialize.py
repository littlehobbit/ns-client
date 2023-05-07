from typing import List

from client.data.model import *


def serialize_applications(apps: List[Application]):
    return '<applications>' \
        + ''.join(map(_serialize_app, apps)) \
        + '</applications>'


def _serialize_app(app: Application):
    return f'<application name="{app.name}" type="{app.type}">' \
        + _serialize_attributes(app.attributes) \
        + '</application>'


def _serialize_attributes(attributes: Attributes):
    return '<attributes>' \
        + ''.join(
            map(
                lambda attr: f'<attribute key="{attr[0]}" value="{attr[1]}"/>', attributes.items())
        ) \
        + '</attributes>'


def _serialize_device(device: Device):
    return f'<device name="{device.name}" type="{device.type}">' \
        + ''.join([f'<address value="{address}" netmask="{mask}"/>'
                   for address, mask in device.ipv4_addresses]) \
        + ''.join([f'<address value="{address}" prefix="{prefix}"/>'
                   for address, prefix in device.ipv6_addresses]) \
        + _serialize_attributes(device.attributes) \
        + '</device>'


def serialize_devices(devices: List[Device]):
    return '<device-list>'                                      \
        + ''.join(map(_serialize_device, devices))   \
        + '</device-list>'


def _serialize_route(route: Route):
    mask_type, content = ('prefix', route.prefix) if route.prefix is not None else (
        'netmask', route.netmask)
    return f'<route network="{route.network}" {mask_type}="{content}" dst="{route.dst}" metric="{route.metric}"/>'


def serialize_routing(routes: List[Route]):
    return '<routing>' + ''.join(map(_serialize_route, routes)) + '</routing>'


def _serialize_connection(connection: Connection):
    return f'<connection name="{connection.name}" type="{connection.type}">' \
        + '<interfaces>' \
        + ''.join(
            map(lambda iface: f'<interface>{iface}</interface>',
                connection.interfaces)
        ) \
        + '</interfaces>' \
        + _serialize_attributes(connection.attributes) \
        + '</connection>'


def serialize_connections(connections: List[Connection]):
    return '<connections>' + \
        ''.join(map(_serialize_connection, connections)) \
        + '</connections>'


def serialize_register(register: Register):
    return f'<registrator value_name="{register.value_name}"' \
        + f' type="{register.type}"'\
        + f' source="{register.source}"' \
        + f' start="{register.start}"' \
        + (f' end="{register.end}"' if register.end is not None else '') \
        + f' file="{register.file}"' \
        + (f' sink="{register.sink}"' if register.sink is not None else '') \
        + '/>'


def serialize_registers(registers: List[Register]):
    return '<statistics>' \
        + ''.join(map(serialize_register, registers)) \
        + '</statistics>'


def serialize_node(node: Node):
    return f'<node name="{node.name}">' \
        + serialize_devices(node.devices) \
        + serialize_routing(node.routing) \
        + serialize_applications(node.applications) \
        + '</node>'


def _serialize_precision(precision: Precision):
    return f'<precision>{precision.name}</precision>'


def _serialize_model(model: Model):
    return f'<model name="{model.name}">' \
        + f'<populate-routing-tables>{str(model.populate_tables).lower()}</populate-routing-tables>' \
        + f'<duration>{model.duration}</duration>' \
        + f'<precision>{model.precision.name}</precision>' \
        + ''.join(map(serialize_node, model.nodes)) \
        + serialize_connections(model.connections) \
        + serialize_registers(model.registers) \
        + '</model>'


def convert_to_xml(model: Model):
    return '<?xml version="1.0" encoding="UTF-8"?>' + _serialize_model(model)