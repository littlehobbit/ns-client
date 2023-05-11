import typing
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

import client.data.settings as settings


class RemoteDiag(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        import client.res.resources
        uic.loadUi('client/ui/ConnectRemote.ui', self)

        self.url_edit.setText(settings.remote_url)

    def accept(self):
        settings.remote_url = self.url_edit.text().strip()
        super().accept()
