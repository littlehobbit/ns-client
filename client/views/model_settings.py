from client.data.objects import Application
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from client.data.objects import Precision


class ModelSettings(QDialog):
    name_edit: QLineEdit
    duration_edit: QLineEdit
    time_combo: QComboBox

    def __init__(self, parent, settings):
        super().__init__(parent)
        uic.loadUi('client/ui/ModelSettings.ui', self)

        self.settings = settings

        self.name_edit.setText(settings.name)
        self.name_edit.textChanged.connect(self.on_name_change)

        self.duration_edit.setText(settings.duration)
        self.duration_edit.textChanged.connect(self.on_duration_change)

        self.time_combo.addItems(
            [e.name for e in Precision]
        )
        self.time_combo.setCurrentText(settings.precision.name)
        self.time_combo.currentTextChanged.connect(self.on_change_precision)

    def on_name_change(self, new_name):
        self.settings.name = new_name

    def on_duration_change(self, new_duration):
        self.settings.duration = new_duration

    def on_change_precision(self, new_precision):
        self.settings.precision = Precision[new_precision]
