import unittest

from client.data.model import Model
from client.data.objects import *
from client.xml.serialize import *
from client.xml.serialize import (_serialize_app, _serialize_attributes,
                                  _serialize_connection, _serialize_device,
                                  _serialize_precision, _serialize_route)


class TestXmlSerialization(unittest.TestCase):
    def test_serialize_app(self):
        app = Application(
            name='test',
            type='ns3::UdpEchoClient',
            attributes={
                'MaxSize': '1000'
            })

        self.assertEqual(
            _serialize_app(app),
            '<application name="test" type="ns3::UdpEchoClient">'
            + '<attributes>'
            + '<attribute key="MaxSize" value="1000"/>'
            + '</attributes></application>'
        )

    def test_serialize_applications_list(self):
        self.assertEqual(
            serialize_applications([]),
            '<applications></applications>'
        )

        self.assertEqual(
            serialize_applications([
                Application('first', 'default', {}),
                Application('second', 'default', {})
            ]),
            '<applications>'
            + '<application name="first" type="default"><attributes></attributes></application>'
            + '<application name="second" type="default"><attributes></attributes></application>'
            + '</applications>'
        )

    def test_serialize_device(self):
        self.assertEqual(
            _serialize_device(
                Device(
                    [('10.10.10.10', '255.255.255.0')],
                    [('dead:beaf:cffe::1', '32')],
                    'device',
                    'Csma',
                    {'Speed': '10mbps'}
                )),
            '<device name="device" type="Csma">'
            + '<address value="10.10.10.10" netmask="255.255.255.0"/>'
            + '<address value="dead:beaf:cffe::1" prefix="32"/>'
            + '<attributes>'
            + '<attribute key="Speed" value="10mbps"/>'
            + '</attributes>'
            + '</device>'
        )

        self.assertEqual(
            _serialize_device(
                Device(
                    [],
                    [('dead:beaf:cffe::1', '32')],
                    'device',
                    'Csma',
                    {'Speed': '10mbps'}
                )),
            '<device name="device" type="Csma">'
            + '<address value="dead:beaf:cffe::1" prefix="32"/>'
            + '<attributes>'
            + '<attribute key="Speed" value="10mbps"/>'
            + '</attributes>'
            + '</device>'
        )

    def test_serialize_devices(self):
        self.assertEqual(
            serialize_devices([]),
            '<device-list></device-list>'
        )

        self.assertEqual(
            serialize_devices([
                Device(
                    [],
                    [('dead:beaf:cffe::1', '32')],
                    'device',
                    'Csma',
                    {'Speed': '10mbps'}
                )
            ]),
            '<device-list>'
            + '<device name="device" type="Csma">'
            + '<address value="dead:beaf:cffe::1" prefix="32"/>'
            + '<attributes>'
            + '<attribute key="Speed" value="10mbps"/>'
            + '</attributes>'
            + '</device>'
            + '</device-list>'
        )

    def test_serialize_route(self):
        # <route network="10.101.0.0" netmask="255.255.0.0" dst="eth0" metric="10"/>
        self.assertEqual(
            _serialize_route(
                Route(
                    network='10.101.0.0',
                    netmask='255.255.0.0',
                    dst='eth0',
                    metric=10
                )
            ),
            '<route network="10.101.0.0" netmask="255.255.0.0" dst="eth0" metric="10"/>'
        )

        # <route network="2001:dead:beef:1002::0" prefix="64" dst="eth1" metric="30"/>
        self.assertEqual(
            _serialize_route(
                Route(
                    network='2001:dead:beef:1002::0',
                    prefix='64',
                    dst='eth1',
                    metric=30
                )
            ),
            '<route network="2001:dead:beef:1002::0" prefix="64" dst="eth1" metric="30"/>'
        )

    def test_serialize_connections(self):
        self.assertEqual(
            serialize_connections(
                [Connection(
                    name='test',
                    type='Csma',
                    interfaces=['eth0', 'eth1'],
                    attributes={}
                )]
            ),
            '<connections>'
            + '<connection name="test" type="Csma">'
            + '<interfaces>'
            + '<interface>eth0</interface>'
            + '<interface>eth1</interface>'
            + '</interfaces>'
            + '<attributes></attributes>'
            + '</connection>'
            + '</connections>'
        )

    def test_serialize_register(self):
        self.assertEqual(
            serialize_register(
                Register(
                    value_name='CWND',
                    type="ns3::Uinteger32Probe",
                    source="/NodeList/0/$ns3::TcpL4Protocol/SocketList/0/CongestionWindow",
                    start='1s',
                    file='cwnd'
                )
            ),
            '<registrator value_name="CWND"'
            + ' type="ns3::Uinteger32Probe"'
            + ' source="/NodeList/0/$ns3::TcpL4Protocol/SocketList/0/CongestionWindow"'
            + ' start="1s"'
            + ' file="cwnd"/>'
        )

        self.assertEqual(
            serialize_register(
                Register(
                    value_name="Bytes",
                    type="ns3::Ipv4PacketProbe",
                    source="/NodeList/0/$ns3::Ipv4L3Protocol/Tx",
                    start="0s",
                    end="2s",
                    file="sender_interface_write",
                    sink="OutputBytes"
                )
            ),
            '<registrator value_name="Bytes"'
            + ' type="ns3::Ipv4PacketProbe"'
            + ' source="/NodeList/0/$ns3::Ipv4L3Protocol/Tx"'
            + ' start="0s"'
            + ' end="2s"'
            + ' file="sender_interface_write"'
            + ' sink="OutputBytes"/>'
        )

    def test_serialise_registers(self):
        self.assertEqual(
            serialize_registers([]),
            '<statistics></statistics>'
        )

        self.assertEqual(
            serialize_registers([
                Register(
                    value_name='CWND',
                    type="ns3::Uinteger32Probe",
                    source="/NodeList/0/$ns3::TcpL4Protocol/SocketList/0/CongestionWindow",
                    start='1s',
                    file='cwnd'
                )]),
            '<statistics>'
            + '<registrator value_name="CWND"'
            + ' type="ns3::Uinteger32Probe"'
            + ' source="/NodeList/0/$ns3::TcpL4Protocol/SocketList/0/CongestionWindow"'
            + ' start="1s"'
            + ' file="cwnd"/>'
            '</statistics>'
        )

    def test_serialize_node(self):
        self.assertEqual(
            serialize_node(
                Node(
                    name='node',
                    devices=[],
                    applications=[],
                    routing=[]
                )
            ),
            '<node name="node">'
            + '<device-list></device-list>'
            + '<routing></routing>'
            + '<applications></applications>'
            + '</node>'
        )

    def test_serialize_model(self):
        self.assertEqual(
            Model(name='test',
                  duration='1s',
                  populate_tables=False,
                  precision=Precision.NS,
                  nodes=[],
                  connections=[],
                  registers=[]
                  ).convert_to_xml(),
            '<?xml version="1.0" encoding="UTF-8"?>'
            + '<model name="test">'
            + '<populate-routing-tables>false</populate-routing-tables>'
            + '<duration>1s</duration>'
            + '<precision>NS</precision>'
            + '<connections></connections>'
            + '<statistics></statistics>'
            + '</model>'
        )

        self.assertEqual(
            Model(name='test',
                  duration='1s',
                  populate_tables=True,
                  precision=Precision.MS,
                  nodes=[
                      Node(
                          name='test-node',
                          devices=[],
                          applications=[],
                          routing=[]
                      )
                  ],
                  connections=[],
                  registers=[]
                  ).convert_to_xml(),
            '<?xml version="1.0" encoding="UTF-8"?>'
            + '<model name="test">'
            + '<populate-routing-tables>true</populate-routing-tables>'
            + '<duration>1s</duration>'
            + '<precision>MS</precision>'
            + '<node name="test-node">'
            + '<device-list></device-list>'
            + '<routing></routing>'
            + '<applications></applications>'
            + '</node>'
            + '<connections></connections>'
            + '<statistics></statistics>'
            + '</model>'
        )
