import typing
from PyQt5.QtCore import QObject, pyqtSignal

import socketio


class SocketioClient(QObject):
    data_received = pyqtSignal(str)
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    connection_error = pyqtSignal(str)

    def __init__(self, parent: QObject = None) -> None:
        super().__init__(parent)

        self.sio = socketio.Client()
        self.sio.on('connect', self._on_connect)
        self.sio.on('disconnect', self._on_disconnect)
        self.sio.on('json', self._on_message)
        self.sio.on('connect_error', self._on_connect_error)

    def _on_message(self, message):
        self.data_received.emit(message)

    def _on_connect(self):
        print('connected')
        self.connected.emit()

    def _on_disconnect(self):
        print('disconnected')
        self.disconnected.emit()

    def _on_connect_error(self, data):
        print('error')
        self.connection_error.emit(data)

    def connect(self, url):
        try:
            self.sio.connect(url)
        except:
            pass
