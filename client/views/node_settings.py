from typing import List

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import QAbstractTableModel, QObject, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

import client.data.model as model
from client.data.objects import Node, Route


class RoutesTableModel(QAbstractTableModel):
    ipv4_header = ('net', 'mask', 'dst', 'metric')
    ipv6_header = ('net', 'prefix', 'dst', 'metric')

    def __init__(self, routes: List[Route], is_ipv6: bool, parent: QObject) -> None:
        super().__init__(parent)
        self.routes = routes
        self.is_ipv6 = is_ipv6

    def data(self, index, role):
        if role == Qt.DisplayRole:
            route = self.routes[index.row()]
            if index.column() == 0:
                return route.network
            elif index.column() == 1:
                return route.prefix if self.is_ipv6 else route.netmask
            elif index.column() == 2:
                return route.dst
            elif index.column() == 3:
                return route.metric

    def rowCount(self, index):
        return len(self.routes)

    def columnCount(self, index):
        return 4

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return (self.ipv6_header if self.is_ipv6 else self.ipv4_header)[section]


class NodeSettings(QDialog):
    name_edit: QLineEdit
    device_list: QListView

    def __init__(self, parent: QWidget, editable_node: Node) -> None:
        super().__init__(parent)

        import client.res.resources
        uic.loadUi('client/ui/NodeSettings.ui', self)

        self.editable_node = editable_node
        self.name_edit.setText(editable_node.name)
        self.name_edit.textChanged.connect(self.update_node_name)

        self.delete_device.clicked.connect(self.on_delete_device)

        self.update_device_list()
        self.update_apps_list()
        self.update_ipv4_routes()
        self.update_ipv6_routes()

    def update_node_name(self, name):
        self.editable_node.name = name

    def update_device_list(self):
        list_model = QStandardItemModel()
        self.device_list.setModel(list_model)

        for device in self.editable_node.devices:
            item = QStandardItem(device.name)
            item.setEditable(False)
            list_model.appendRow(item)

    def update_apps_list(self):
        list_model = QStandardItemModel()
        self.applications_list.setModel(list_model)

        for device in self.editable_node.applications:
            item = QStandardItem(device.name)
            item.setEditable(False)
            list_model.appendRow(item)

    def update_ipv4_routes(self):
        ipv4_routes = [
            route for route in self.editable_node.routing if route.netmask is not None]
        self.ipv4_routes.setModel(RoutesTableModel(ipv4_routes, False, self))

    def update_ipv6_routes(self):
        ipv6_routes = [
            route for route in self.editable_node.routing if route.prefix is not None]
        self.ipv6_routes.setModel(RoutesTableModel(ipv6_routes, True, self))

    def on_delete_device(self):
        index = self.device_list.currentIndex().row()
        if len(self.editable_node.devices) > 0:
            del self.editable_node.devices[index]
            self.update_device_list()