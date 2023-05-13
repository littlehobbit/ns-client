from PyQt5.QtWidgets import QApplication

from client.socketio_client import SocketioClient
from client.views.main_window import MainWindow

# app = QApplication([])
app = QApplication(['', '--no-sandbox'])


websocket = SocketioClient()

window = MainWindow(websocket)
window.show()

websocket.connection_error.connect(window.on_connection_error)

app.exec()
