from copy import deepcopy
from typing import List

from client.data.objects import Device
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from client.views.attributes_model import AttributesModel
from client.data.objects import Address


class AddressModel(QAbstractTableModel):
    def __init__(self, parent, addresses: List[Address], is_ipv6: bool = False):
        super().__init__(parent)

        self.addresses = addresses
        self.is_ipv6 = is_ipv6
        self.header = ('address', 'prefix') if is_ipv6 else (
            'address', 'netmap')

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header[section]

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.addresses[index.row()][index.column()]

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.addresses[index.row()][index.column()] = value.strip()
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable

    def rowCount(self, index):
        return len(self.addresses)

    def columnCount(self, index):
        return len(self.header)


class DeviceSettings(QDialog):
    editable: Device
    name_edit: QLineEdit
    type_combo: QComboBox
    attributes_table: QTableView

    def __init__(self, parent: QWidget, editable: Device) -> None:
        super().__init__(parent)
        uic.loadUi('client/ui/DeviceSettings.ui', self)

        self.editable = editable

        self.name_edit.setText(self.editable.name)
        self.name_edit.textChanged.connect(self.update_device_name)

        self.type_combo.addItems(['Csma', 'PPP'])
        if self.editable.type != '':
            self.type_combo.setCurrentText(self.editable.type)
        self.type_combo.currentIndexChanged.connect(self.update_device_type)

        self.ipv4_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ipv6_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.add_ipv4.clicked.connect(self.on_add_ipv4)
        self.delete_ipv4.clicked.connect(self.on_delete_ipv4)

        self.add_ipv6.clicked.connect(self.on_add_ipv6)
        self.delete_ipv6.clicked.connect(self.on_delete_ipv6)

        self.update_ipv4_addresses()
        self.update_ipv6_addresses()

        self.attributes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.add_attribute.clicked.connect(self.on_add_attribute)
        self.delete_attribute.clicked.connect(self.on_delete_attribute)
        self.update_attributes()

    def on_add_attribute(self):
        self.editable.attributes.append(['name', 'value'])
        self.update_attributes()

    def on_delete_attribute(self):
        index = self.attributes_table.currentIndex().row()
        if len(self.editable.attributes) > 0:
            del self.editable.attributes[index]
            self.update_attributes()

    def update_attributes(self):
        self.attributes_table.setModel(
            AttributesModel(
                self.editable.attributes, self
            )
        )

    def update_device_name(self, name):
        self.editable.name = name.strip()

    def update_device_type(self):
        self.editable.type = self.type_combo.currentText()

    def on_add_ipv4(self):
        self.editable.ipv4_addresses.append(['', ''])
        self.update_ipv4_addresses()

    def on_delete_ipv4(self):
        index = self.ipv4_list.currentIndex().row()
        if len(self.editable.ipv4_addresses) > 0:
            del self.editable.ipv4_addresses[index]
            self.update_ipv4_addresses()

    def on_add_ipv6(self):
        self.editable.ipv6_addresses.append(['', ''])
        self.update_ipv6_addresses()

    def on_delete_ipv6(self):
        index = self.ipv6_list.currentIndex().row()
        if len(self.editable.ipv6_addresses) > 0:
            del self.editable.ipv6_addresses[index]
            self.update_ipv6_addresses()

    def update_ipv4_addresses(self):
        self.ipv4_list.setModel(
            AddressModel(self, self.editable.ipv4_addresses)
        )

    def update_ipv6_addresses(self):
        self.ipv6_list.setModel(
            AddressModel(self, self.editable.ipv6_addresses, True)
        )
