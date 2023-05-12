from copy import deepcopy
from typing import List

import client.data.model as model
from client.data.objects import Register
from client.views.tracer_settings import TracerSettings

from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QDialog, QListView, QPushButton


class TracersList(QDialog):
    tracers_list: QListView
    add_tracer: QPushButton
    delete_tracer: QPushButton
    edit_tracer: QPushButton

    def __init__(self, parent: QWidget, tracers: List[Register]) -> None:
        super().__init__(parent)
        uic.loadUi('client/ui/TracersList.ui', self)

        self.tracers = tracers

        self.add_tracer.clicked.connect(self.on_add_tracer)
        self.edit_tracer.clicked.connect(self.on_edit_tracer)
        self.delete_tracer.clicked.connect(self.on_delete_tracer)

        self.update_list()

    def on_add_tracer(self):
        new_tracer = Register('val', '', '', '0s', 'file_name', None, None)
        if TracerSettings(self, new_tracer).exec() == 1:
            self.tracers.append(new_tracer)
            self.update_list()

    def on_edit_tracer(self):
        index = self.tracers_list.currentIndex().row()
        if index == -1:
            return

        edited = deepcopy(self.tracers[index])
        if TracerSettings(self, edited).exec() == 1:
            self.tracers[index] = edited
            self.update_list()

    def on_delete_tracer(self):
        index = self.tracers_list.currentIndex().row()
        if len(self.tracers) > 0:
            del self.tracers[index]
            self.update_list()

    def update_list(self):
        list_model = QStandardItemModel()
        self.tracers_list.setModel(list_model)

        for tracer in self.tracers:
            item = QStandardItem(tracer.value_name)
            item.setEditable(False)
            list_model.appendRow(item)
