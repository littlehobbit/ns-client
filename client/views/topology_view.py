import os
import sys

import client.data.model as model
from PyQt5.QtCore import QMargins
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from pyvis.network import Network
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtCore import QUrl


class TopologyView(QWidget):
    web_view: QWebEngineView

    def __init__(self, *args):
        super().__init__(*args)
        self.web_view = QWebEngineView(self)

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.layout().addWidget(self.web_view)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))

    def update_topology(self):
        network = Network()
        network.set_template(os.path.join(
            os.getcwd(), 'client', 'html', 'topology_template.html')
        )

        id_per_node = {}
        for index, node in enumerate(model.current_model.nodes):
            network.add_node(index, node.name)
            id_per_node[node.name] = index

        for connection in model.current_model.connections:
            # endpoint = Node/Interface
            endpoints = [endpoint.split('/')[0]
                         for endpoint in connection.interfaces]

            if len(endpoints) == 2:
                # Create edge betwen two nodes
                src, dst = endpoints
                if src in id_per_node and dst in id_per_node:
                    network.add_edge(id_per_node[src], id_per_node[dst])
            elif len(endpoints) > 2:
                # Create proxy object and connect to it
                proxy = hash(connection.name)
                network.add_node(proxy, label=connection.name, shape='text')
                for node in endpoints:
                    if node in id_per_node:
                        network.add_edge(id_per_node[node], proxy)
            else:
                pass

        tolopogy = os.path.join(os.getcwd(), 'client', 'html', 'topology.html')
        network.save_graph(tolopogy)

        topology_path = QUrl.fromLocalFile(tolopogy)
        self.web_view.load(topology_path)
