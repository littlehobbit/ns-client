from copy import deepcopy
from typing import List

import client.data.model as model
from client.data.objects import Connection
from client.views.connection_settings import ConnectionSettings

from PyQt5 import uic
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QDialog, QListView, QPushButton, QWidget


class ConnectionsList(QDialog):
    """ Connections list dialog """
    add_connection: QPushButton
    edit_connection: QPushButton
    delete_connection: QPushButton
    connections_list: QListView
    connections: List[Connection]

    def __init__(self, parent: QWidget, connections: List[Connection]) -> None:
        super().__init__(parent)
        uic.loadUi('client/ui/ConnectionsList.ui', self)

        self.connections = connections

        self.add_connection.clicked.connect(self.on_add)
        self.edit_connection.clicked.connect(self.on_edit)
        self.delete_connection.clicked.connect(self.on_delete)

        self.update_list()

    def on_add(self):
        new_connection = Connection('new-connection', '', [], [])
        if ConnectionSettings(self, new_connection).exec() == 1:
            self.connections.append(new_connection)
            self.update_list()

    def on_edit(self):
        index = self.connections_list.currentIndex().row()
        if index == -1:
            return

        edited = deepcopy(self.connections[index])
        if ConnectionSettings(self, edited).exec() == 1:
            self.connections[index] = edited
            self.update_list()

    def on_delete(self):
        index = self.connections_list.currentIndex().row()
        if len(self.connections) > 0:
            del self.connections[index]
            self.update_list()

    def update_list(self):
        list_model = QStandardItemModel()
        self.connections_list.setModel(list_model)

        for conn in self.connections:
            item = QStandardItem(conn.name)
            item.setEditable(False)
            list_model.appendRow(item)
