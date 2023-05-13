from copy import deepcopy
from typing import List

from PyQt5 import uic
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QDialog, QListView, QPushButton, QWidget

import client.data.model as model
from client.data.objects import Node
from client.views.node_settings import NodeSettings


class NodeList(QDialog):
    """ List of nodes dialog

    Allow add/edit/delete nodes
    """

    add_button: QPushButton
    edit_button: QPushButton
    delete_button: QPushButton
    list_view: QListView
    nodes_list: List[Node]

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        uic.loadUi('client/ui/NodeList.ui', self)

        self.add_button.clicked.connect(self.on_add)
        self.edit_button.clicked.connect(self.on_edit)
        self.delete_button.clicked.connect(self.on_delete)

        self.nodes_list = deepcopy(model.current_model.nodes)
        self.update_list()

    def update_list(self) -> None:
        list_model = QStandardItemModel()
        self.list_view.setModel(list_model)

        for node in self.nodes_list:
            item = QStandardItem(node.name)
            item.setEditable(False)
            list_model.appendRow(item)

    def on_add(self):
        new_node = Node('new', [], [], [], [])
        if NodeSettings(self, new_node).exec() == 1:
            self.nodes_list.append(new_node)
            self.update_list()

    def on_edit(self):
        id = self.list_view.currentIndex().row()
        if id == -1:
            return

        edited = deepcopy(self.nodes_list[id])
        if NodeSettings(self, edited).exec() == 1:
            self.nodes_list[id] = edited
            self.update_list()

    def on_delete(self):
        to_delete = self.list_view.currentIndex().row()
        if len(self.nodes_list) > 0:
            del self.nodes_list[to_delete]
            self.update_list()

    def accept(self):
        model.current_model.nodes = self.nodes_list
        super().accept()
