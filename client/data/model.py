from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

from client.data.objects import *
from client.xml.serialize import (serialize_connections, serialize_node,
                                  serialize_registers)


@dataclass
class ModelParameters:
    name: str
    duration: str
    populate_tables: bool
    precision: Precision


@dataclass
class Model:
    parameters: ModelParameters
    nodes: List[Node]
    connections: List[Connection]
    registers: List[Register]

    def convert_to_xml(self):
        return '<?xml version="1.0" encoding="UTF-8"?>' + self._serialize()

    def _serialize(self):
        return f'<model name="{self.parameters.name}">' \
            + f'<populate-routing-tables>{str(self.parameters.populate_tables).lower()}</populate-routing-tables>' \
            + f'<duration>{self.parameters.duration}</duration>' \
            + f'<precision>{self.parameters.precision.name}</precision>' \
            + ''.join(map(serialize_node, self.nodes)) \
            + serialize_connections(self.connections) \
            + serialize_registers(self.registers) \
            + '</model>'


current_model = Model(
    parameters=ModelParameters(name='default',
                               duration='5s',
                               populate_tables=False,
                               precision=Precision.NS),
    nodes=[],
    connections=[],
    registers=[]
)
