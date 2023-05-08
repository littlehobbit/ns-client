from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

from client.data.objects import Connection, Node, Precision, Register

from client.xml.serialize import serialize_node, serialize_connections, serialize_registers


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
    nodes=[],
    connections=[],
    registers=[]
)
