from copy import deepcopy
from typing import List

from PyQt5 import uic
from PyQt5.QtCore import QAbstractTableModel, QObject, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QDialog, QHeaderView, QLineEdit, QListView,
                             QTableView, QWidget)

from client.data.objects import Application, Device, Node, Route
from client.views.app_settings import ApplicationsSettings
from client.views.device_settings import DeviceSettings


class RoutesTableModel(QAbstractTableModel):
    """ Table model for node's routes """

    ipv4_header = ('net', 'mask', 'dst', 'metric')
    ipv6_header = ('net', 'prefix', 'dst', 'metric')

    def __init__(self, routes: List[Route], is_ipv6: bool, parent: QObject) -> None:
        super().__init__(parent)
        self.routes = routes
        self.is_ipv6 = is_ipv6

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            route = self.routes[index.row()]
            if index.column() == 0:
                return route.network
            elif index.column() == 1:
                return route.prefix if self.is_ipv6 else route.netmask
            elif index.column() == 2:
                return route.dst
            elif index.column() == 3:
                return route.metric

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            route = self.routes[index.row()]
            if index.column() == 0:
                route.network = value.strip()
            elif index.column() == 1:
                if self.is_ipv6:
                    route.prefix = value.strip()
                else:
                    route.netmask = value.strip()
            elif index.column() == 2:
                route.dst = value.strip()
            elif index.column() == 3:
                route.metric = int(value)
            return True
        return False

    def rowCount(self, index):
        return len(self.routes)

    def columnCount(self, index):
        return 4

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return (self.ipv6_header if self.is_ipv6 else self.ipv4_header)[section]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable


class NodeSettings(QDialog):
    """ Node settings dialog 

    This dialog allow set node parameters, accept them or discard
    """
    name_edit: QLineEdit
    device_list: QListView
    ipv4_routes: QTableView
    ipv6_routes: QTableView
    applications_list: QListView

    def __init__(self, parent: QWidget, editable_node: Node) -> None:
        super().__init__(parent)

        import client.res.resources
        uic.loadUi('client/ui/NodeSettings.ui', self)

        self.editable_node = editable_node
        self.name_edit.setText(editable_node.name)
        self.name_edit.textChanged.connect(self.update_node_name)

        self.delete_device.clicked.connect(self.on_delete_device)

        self.add_ipv4.clicked.connect(self.add_new_ipv4_route)
        self.add_ipv6.clicked.connect(self.add_new_ipv6_route)

        self.delete_ipv4.clicked.connect(self.on_delete_ipv4_route)
        self.delete_ipv6.clicked.connect(self.on_delete_ipv6_route)

        self.ipv4_routes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ipv6_routes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.edit_device.clicked.connect(self.on_edit_device)
        self.add_device.clicked.connect(self.on_add_device)

        self.add_app.clicked.connect(self.on_add_app)
        self.delete_app.clicked.connect(self.on_delete_app)
        self.edit_app.clicked.connect(self.on_edit_app)

        self.update_device_list()
        self.update_apps_list()
        self.update_ipv4_routes()
        self.update_ipv6_routes()

    def update_node_name(self, name):
        self.editable_node.name = name.strip()

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
        for app in self.editable_node.applications:
            item = QStandardItem(app.name)
            item.setEditable(False)
            list_model.appendRow(item)

    def update_ipv4_routes(self):
        self.ipv4_routes.setModel(RoutesTableModel(
            self.editable_node.ipv4_routes, False, self))

    def update_ipv6_routes(self):
        self.ipv6_routes.setModel(RoutesTableModel(
            self.editable_node.ipv6_routes, True, self))

    def on_delete_device(self):
        index = self.device_list.currentIndex().row()
        if len(self.editable_node.devices) > 0:
            del self.editable_node.devices[index]
            self.update_device_list()

    def on_add_device(self):
        new_device = Device('eth', 'Csma', [], [], [])
        if DeviceSettings(self, new_device).exec() == 1:
            self.editable_node.devices.append(new_device)
            self.update_device_list()

    def on_edit_device(self):
        index = self.device_list.currentIndex().row()
        if index == -1:
            return

        edited = deepcopy(self.editable_node.devices[index])
        if DeviceSettings(self, edited).exec() == 1:
            self.editable_node.devices[index] = edited
            self.update_device_list()

    def add_new_ipv4_route(self):
        self.editable_node.ipv4_routes.append(
            Route('', '', 0, netmask='')
        )
        self.update_ipv4_routes()

    def add_new_ipv6_route(self):
        self.editable_node.ipv6_routes.append(
            Route('', '', 0, prefix='16')
        )
        self.update_ipv6_routes()

    def on_delete_ipv4_route(self):
        index = self.ipv4_routes.currentIndex().row()
        if len(self.editable_node.ipv4_routes) > 0:
            del self.editable_node.ipv4_routes[index]
            self.update_ipv4_routes()

    def on_delete_ipv6_route(self):
        index = self.ipv6_routes.currentIndex().row()
        if len(self.editable_node.ipv6_routes) > 0:
            del self.editable_node.ipv6_routes[index]
            self.update_ipv6_routes()

    def on_add_app(self):
        new_app = Application('app', '', [])
        if ApplicationsSettings(self, new_app).exec() == 1:
            self.editable_node.applications.append(new_app)
            self.update_apps_list()

    def on_edit_app(self):
        index = self.applications_list.currentIndex().row()
        if index == -1:
            return

        edited_app = deepcopy(self.editable_node.applications[index])
        if ApplicationsSettings(self, edited_app).exec() == 1:
            self.editable_node.applications[index] = edited_app
            self.update_apps_list()

    def on_delete_app(self):
        index = self.applications_list.currentIndex().row()
        if len(self.editable_node.applications) > 0:
            del self.editable_node.applications[index]
            self.update_apps_list()
