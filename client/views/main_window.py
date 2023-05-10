import json

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import client.data.settings as settings
from client.socketio_client import SocketioClient
from client.views.node_list import NodeList
from client.views.remote_diag import RemoteDiag
import client.data.model as model


class MainWindow(QMainWindow):
    log_window: QTextBrowser
    connect_button: QAction
    nodes_button: QAction
    export_button: QAction

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

    def on_remotes_button(self):
        diag = RemoteDiag(self)
        diag.accepted.connect(self.reconnect)
        diag.show()

    def on_nodes_button(self):
        diag = NodeList(self)
        diag.show()

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
        self._show_message_box(QMessageBox.Critical, f'Connected', title='Error',
                               informative_text=f'Can\'t connect to "{settings.remote_url}"')

    def export_model(self):
        file, _ = QFileDialog.getSaveFileName(self, 'Save File')
        with open(file, 'w') as f:
            content = model.current_model.convert_to_xml()
            f.write(content)
