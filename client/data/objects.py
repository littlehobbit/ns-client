from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum, auto

Attributes = List[List[str]]
Address = List[str]


@dataclass
class Device:
    name: str
    type: str
    attributes: Attributes
    ipv4_addresses: List[Address]
    ipv6_addresses: List[Address]


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
    ipv4_routes: List[Route]
    ipv6_routes: List[Route]


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
