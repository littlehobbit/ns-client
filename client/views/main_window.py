import json
from copy import deepcopy

import requests
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import (QAction, QFileDialog, QFrame, QMainWindow,
                             QMessageBox, QTextBrowser, QVBoxLayout)

import client.data.model as model
import client.data.settings as settings
from client.socketio_client import SocketioClient
from client.views.connection_list import ConnectionsList
from client.views.model_settings import ModelSettings
from client.views.node_list import NodeList
from client.views.remote_diag import RemoteDiag
from client.views.topology_view import TopologyView
from client.views.tracers_list import TracersList


class MainWindow(QMainWindow):
    log_window: QTextBrowser
    connect_button: QAction
    nodes_button: QAction
    export_button: QAction
    settings_button: QAction
    connections_button: QAction
    tracers_button: QAction
    stop_button: QAction
    run_button: QAction
    topology_window: QFrame

    def __init__(self, websocket: SocketioClient) -> None:
        super().__init__()
        import client.res.resources
        uic.loadUi('client/ui/MainWindow.ui', self)

        self.websocket = websocket
        self.websocket.data_received.connect(self._on_receive)
        self.websocket.connected.connect(self._on_connected)

        self.connect_button.triggered.connect(self.on_remotes_button)
        self.nodes_button.triggered.connect(self.on_nodes_button)

        self.export_button.triggered.connect(self.export_model)

        self.settings_button.triggered.connect(self.on_open_settings)

        self.connections_button.triggered.connect(self.on_open_connections)

        self.tracers_button.triggered.connect(self.on_open_tracers)

        self.stop_button.triggered.connect(self.send_stop)
        self.run_button.triggered.connect(self.send_model)

        self.topology_window.setLayout(QVBoxLayout())
        self.topology_window.layout().setContentsMargins(QtCore.QMargins(0, 0, 0, 0))

        self.topology_view = TopologyView()
        self.topology_window.layout().addWidget(self.topology_view)
        self.topology_view.update_topology()

    def on_remotes_button(self):
        diag = RemoteDiag(self)
        diag.accepted.connect(self.reconnect)
        diag.show()

    def on_nodes_button(self):
        NodeList(self).exec()
        self.topology_view.update_topology()

    def _on_receive(self, data):
        data = json.loads(data)
        if data['status'] == 'LOG':
            self.log_window.append(data['msg'])
        elif data['status'] == 'UPLOADED':
            self._show_message_box(
                QMessageBox.Information, f'Uploaded {data["msg"]}')
        elif data['status'] == 'ERROR':
            self.log_window.append('ERROR: ' + data['msg'])
            self._show_message_box(QMessageBox.Critical,
                                   'Error', 'Simulation error', data['msg'])

    def _show_message_box(self, icon,  text, title=None, informative_text=None):
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(text)

        if title is not None:
            msg.setWindowTitle(title)

        if informative_text is not None:
            msg.setInformativeText(informative_text)
        msg.exec_()

    def reconnect(self):
        self.websocket.connect(settings.remote_url)

    def _on_connected(self):
        self._show_message_box(QMessageBox.Information, f'Connected')

    def on_connection_error(self, err):
        self._show_message_box(QMessageBox.Critical, f'Connection Error', title='Error',
                               informative_text=f'Can\'t connect to "{settings.remote_url}"')

    def on_open_settings(self):
        new_settings = deepcopy(model.current_model.parameters)
        if ModelSettings(self, new_settings).exec() == 1:
            model.current_model.parameters = new_settings

    def on_open_connections(self):
        edited = deepcopy(model.current_model.connections)
        if ConnectionsList(self, edited).exec() == 1:
            model.current_model.connections = edited
            self.topology_view.update_topology()

    def export_model(self):
        file, _ = QFileDialog.getSaveFileName(self, 'Save File', filter='.xml')
        if len(file) > 0:
            with open(file + '.xml', 'w') as f:
                content = model.current_model.convert_to_xml()
                f.write(content)

    def on_open_tracers(self):
        edited = deepcopy(model.current_model.registers)
        if TracersList(self, edited).exec() == 1:
            model.current_model.registers = edited

    def send_model(self):
        url = settings.remote_url.strip()
        if self.check_url(url) == False:
            return

        headers = {'Content-Type': 'application/xml'}
        model_xml = model.current_model.convert_to_xml()
        with requests.post(url+'/start', headers=headers, data=model_xml) as res:
            if res.status_code != 200:
                json_msg = json.loads(res.text)
                self._show_message_box(QMessageBox.Critical,
                                       'Server error', 'Error', json_msg['error'])

    def send_stop(self):
        url = settings.remote_url.strip()
        if self.check_url(url) == False:
            return

        with requests.get(url+'/stop') as res:
            if res.status_code != 200:
                json_msg = json.loads(res.text)
                self._show_message_box(QMessageBox.Critical,
                                       'Server error', 'Error', json_msg['error'])

    def check_url(self, url) -> bool:
        if url == '':
            self._show_message_box(QMessageBox.Critical,
                                   'Can\'t stop', 'Error', 'Url is empty')
            return False
        return True
