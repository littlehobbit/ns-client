from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

from client.data.objects import *
from client.xml.serialize import (serialize_connections, serialize_node,
                                  serialize_registers)


@dataclass
class Model:
    name: str
    duration: str
    populate_tables: bool
    precision: Precision
    nodes: List[Node]
    connections: List[Connection]
    registers: List[Register]

    def convert_to_xml(self):
        return '<?xml version="1.0" encoding="UTF-8"?>' + self._serialize()

    def _serialize(self):
        return f'<model name="{self.name}">' \
            + f'<populate-routing-tables>{str(self.populate_tables).lower()}</populate-routing-tables>' \
            + f'<duration>{self.duration}</duration>' \
            + f'<precision>{self.precision.name}</precision>' \
            + ''.join(map(serialize_node, self.nodes)) \
            + serialize_connections(self.connections) \
            + serialize_registers(self.registers) \
            + '</model>'


current_model = Model(
    name='default',
    duration='5s',
    populate_tables=False,
    precision=Precision.NS,
    nodes=[
        Node(
            name='node-1',
            devices=[
                Device(name='device1',
                       type='Csma',
                       attributes=[['name', 'value']],
                       ipv4_addresses=[
                           ['1.1.1.1', '255.255.255.0']
                       ],
                       ipv6_addresses=[
                           ['dead:cffe:feed::1', '32']
                       ])
            ],
            applications=[
                Application('app', 'ns3::UdpEchoClientApplication', [])
            ],
            ipv4_routes=[
                Route(
                    network='10.101.0.0',
                    netmask='255.255.0.0',
                    dst='eth0',
                    metric=10
                ),
                Route(
                    network='10.101.0.0',
                    netmask='255.255.0.0',
                    dst='eth0',
                    metric=10
                )],
            ipv6_routes=[
                Route(
                    network='2001:dead:beef:1002::0',
                    prefix='64',
                    dst='eth1',
                    metric=30
                ),
                Route(
                    network='2001:dead:beef:1002::0',
                    prefix='64',
                    dst='eth1',
                    metric=30
                )
            ]
        ),
        Node(
            name='node-2',
            devices=[],
            applications=[],
            ipv4_routes=[],
            ipv6_routes=[]
        )
    ],
    connections=[],
    registers=[]
)
