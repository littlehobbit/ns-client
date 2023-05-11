from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import QAbstractTableModel, QObject, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from client.data.objects import Attributes


class AttributesModel(QAbstractTableModel):

    def __init__(self, attributes: Attributes, parent: QObject) -> None:
        super().__init__(parent)
        self.attributes = attributes
        self.header = ('name', 'value')

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.attributes[index.row()][index.column()]

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.attributes[index.row()][index.column()] = value.strip()
            return True
        return False

    def rowCount(self, index):
        return len(self.attributes)

    def columnCount(self, index):
        return len(self.header)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header[section]

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsEditable
