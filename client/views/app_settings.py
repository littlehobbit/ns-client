from copy import deepcopy
from typing import List

from client.data.objects import Application
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from client.views.attributes_model import AttributesModel
from client.data.objects import Address


class ApplicationsSettings(QDialog):
    name_edit: QLineEdit
    type_edit: QLineEdit


    def __init__(self, parent: QtCore.QObject, editable: Application):
        super().__init__(parent)
        uic.loadUi('client/ui/AppSettings.ui', self)

        self.editable = editable

        self.name_edit.setText(self.editable.name)
        self.type_edit.setText(self.editable.type)

        self.name_edit.textChanged.connect(self.on_update_name)
        self.type_edit.textChanged.connect(self.on_update_type)

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
    
    def on_update_name(self, name):
      self.editable.name = name.strip()
    
    def on_update_type(self, type):
      self.editable.type = type.strip()
