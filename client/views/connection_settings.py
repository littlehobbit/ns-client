from typing import List

import client.data.model as model
from client.data.objects import Connection
from client.views.attributes_model import AttributesModel

from PyQt5 import uic
from PyQt5.QtCore import QAbstractListModel, QModelIndex, QObject, Qt
from PyQt5.QtWidgets import (QComboBox, QDialog, QHeaderView, QLineEdit,
                             QListView, QPushButton, QStyledItemDelegate,
                             QWidget)


class InterfaceModel(QAbstractListModel):
    """ List model for view/edit interfacew """

    def __init__(self, parent: QObject, interfaces: List[str]) -> None:
        super().__init__(parent)
        self.interfaces = interfaces

    def data(self, index: QModelIndex, role: int):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.interfaces[index.row()]

    def setData(self, index: QModelIndex, value, role: int) -> bool:
        if role == Qt.EditRole:
            self.interfaces[index.row()] = value.strip()
            return True
        return False

    def rowCount(self, index):
        return len(self.interfaces)

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable


class QComboBoxDelegate(QStyledItemDelegate):
    """ Combo box delecate to picking existing interfaces """

    def createEditor(self, parent, option, index):
        value = index.data(Qt.EditRole)

        editor = QComboBox(parent)
        editor.addItems(['None'])

        for node in model.current_model.nodes:
            editor.addItems(
                [f'{node.name}/{dev.name}' for dev in node.devices])

        editor.setCurrentText(value)

        editor.currentIndexChanged.connect(
            lambda: self.commitData.emit(editor))

        return editor


class ConnectionSettings(QDialog):
    """ Connection settings dialog """

    editable: Connection
    name_edit: QLineEdit
    type_combo: QComboBox
    add_interface: QPushButton
    delete_interface: QPushButton
    interfaces_list: QListView

    def __init__(self, parent: QWidget, editable: Connection) -> None:
        super().__init__(parent)
        uic.loadUi('client/ui/ConnectionSettings.ui', self)

        self.editable = editable

        self.type_combo.addItems(['Csma', 'Ppp'])
        self.type_combo.setCurrentText(editable.type)
        self.type_combo.currentTextChanged.connect(self.on_change_type)

        self.name_edit.setText(editable.name)
        self.name_edit.textChanged.connect(self.on_change_name)

        self.add_interface.clicked.connect(self.on_add_interface)
        self.delete_interface.clicked.connect(self.on_delete_interface)
        self.update_interfaces()

        self.attributes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.add_attribute.clicked.connect(self.on_add_attribute)
        self.delete_attribute.clicked.connect(self.on_delete_attribute)
        self.update_attributes()

    def on_change_type(self, type):
        self.editable.type = type

    def on_change_name(self, new_name):
        self.editable.name = new_name.strip()

    def on_add_interface(self):
        self.editable.interfaces.append('None')
        self.update_interfaces()

    def on_delete_interface(self):
        index = self.interfaces_list.currentIndex().row()
        if len(self.editable.interfaces) > 0:
            del self.editable.interfaces[index]
            self.update_interfaces()

    def on_add_attribute(self):
        self.editable.attributes.append(['name', 'value'])
        self.update_attributes()

    def on_delete_attribute(self):
        index = self.attributes_table.currentIndex().row()
        if len(self.editable.attributes) > 0:
            del self.editable.attributes[index]
            self.update_attributes()

    def update_interfaces(self):
        model = InterfaceModel(self, self.editable.interfaces)
        self.interfaces_list.setItemDelegate(QComboBoxDelegate())
        self.interfaces_list.setModel(
            model
        )

    def update_attributes(self):
        self.attributes_table.setModel(
            AttributesModel(
                self.editable.attributes, self
            )
        )
