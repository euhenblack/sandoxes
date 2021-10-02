from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow
from controller.controller import AppController
from ui.Ui_main_window import Ui_MainWindow

FLAT_DELAY = 150

class MainWidnow(QMainWindow, Ui_MainWindow):
    def __init__(self, model):
        super(MainWidnow, self).__init__()
        self.setupUi(self)
        self._model = model
        self._controller = AppController(self, model)
        self.actionRefresh_ports.triggered.connect(self._controller.refresh_ports)
        self.pb_connect_app.clicked.connect(self._controller.connect_app)
        self.pb_connect_unit.clicked.connect(self._controller.connect_unit)
        self._model.unit_port_event.connect(self._controller.handle_unit_port_event)
        self._model.app_port_event.connect(self._controller.handle_app_port_event)
        self._model.app_data_received.connect(self._controller.handle_app_data_received)
        self._controller.refresh_ports()
        self.document = ''
        self.unit_timer = QTimer()
        self.unit_timer.timeout.connect(self.reset_unit_button)
        self.app_timer = QTimer()
        self.app_timer.timeout.connect(self.reset_app_button)

    def set_unit_button(self):
        self.pb_un.setFlat(False)
        self.unit_timer.start(FLAT_DELAY)

    def reset_unit_button(self):
        self.pb_un.setFlat(True)

    def set_app_button(self):
        self.pb_tcp4.setFlat(False)
        self.app_timer.start(FLAT_DELAY)

    def reset_app_button(self):
        self.pb_tcp4.setFlat(True)
