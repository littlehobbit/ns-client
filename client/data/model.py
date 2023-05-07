from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum, auto

Attributes = Dict[str, str]
Address = Tuple[str, str]

@dataclass
class Device:
    ipv4_addresses: List[Address]
    ipv6_addresses: List[Address]
    name: str
    type: str
    attributes: Attributes


@dataclass
class Application:
    name: str
    type: str
    attributes: Attributes


@dataclass
class Route:
    network: str
    dst: str
    metric: int
    prefix: Optional[int] = None
    netmask: Optional[str] = None


@dataclass
class Node:
    name: str
    devices: List[Device]
    applications: List[Application]
    routing: List[Route]


@dataclass
class Connection:
    name: str
    type: str
    interfaces: List[str]
    attributes: Attributes


@dataclass
class Register:
    value_name: str
    type: str
    source: str
    start: str
    file: str
    end: Optional[str] = None
    sink: Optional[str] = None


class Precision(Enum):
    NS = auto()
    MS = auto()
    S = auto()
    H = auto()


@dataclass
class Model:
    name: str
    duration: str
    populate_tables: bool
    precision: Precision
    nodes: List[Node]
    connections: List[Connection]
    registers: List[Register]


current_model = Model(
    name='default',
    duration='5s',
    populate_tables=False,
    precision=Precision.NS,
    nodes=[],
    connections=[],
    registers=[]
)
