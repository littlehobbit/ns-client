from copy import deepcopy
from typing import List

import client.data.model as model
from client.data.objects import Register

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLineEdit, QComboBox, QDialog


class TracerSettings(QDialog):
    value_edit: QLineEdit
    type_combo: QComboBox
    source_edit: QLineEdit
    file_edit: QLineEdit
    start_edit: QLineEdit
    end_edit: QLineEdit
    sink_edit: QLineEdit

    def __init__(self, parent: QWidget, tracer: Register) -> None:
        super().__init__(parent)
        uic.loadUi('client/ui/TracerSettings.ui', self)

        self.tracer = tracer

        self.type_combo.addItems(
            [
                'ns3::ApplicationPacketProbe',
                'ns3::BooleanProbe',
                'ns3::DoubleProbe',
                'ns3::Ipv4PacketProbe',
                'ns3::Ipv6PacketProbe',
                'ns3::PacketProbe',
                'ns3::Uinteger16Probe',
                'ns3::Uinteger32Probe',
                'ns3::Uinteger8Probe'
            ]
        )
        if tracer.type != '':
            self.type_combo.setCurrentText(tracer.type)
        self.type_combo.currentTextChanged.connect(self.on_change_type)

        self.value_edit.setText(tracer.value_name)
        self.value_edit.textChanged.connect(self.on_change_value_name)

        self.source_edit.setText(tracer.source)
        self.source_edit.textChanged.connect(self.on_change_source)

        self.file_edit.setText(tracer.file)
        self.file_edit.textChanged.connect(self.on_change_file)

        self.start_edit.setText(tracer.start)
        self.start_edit.textChanged.connect(self.on_change_start)

        self.end_edit.setText(tracer.end)
        self.end_edit.textChanged.connect(self.on_change_end)

        self.sink_edit.setText(tracer.sink)
        self.sink_edit.textChanged.connect(self.on_change_sink)

    def on_change_type(self, new_type):
        self.tracer.type = new_type

    def on_change_value_name(self, new_name: str):
        self.tracer.value_name = new_name.strip()

    def on_change_source(self, new_source: str):
        self.tracer.source = new_source.strip()

    def on_change_file(self, new_file: str):
        self.tracer.file = new_file.strip()

    def on_change_start(self, new_start: str):
        self.tracer.start = new_start.strip()

    def on_change_end(self, new_end: str):
        new_end = new_end.strip()
        self.tracer.end = None if new_end == '' else new_end

    def on_change_sink(self, new_sink: str):
        new_sink = new_sink.strip()
        self.tracer.sink = None if new_sink == '' else new_sink
