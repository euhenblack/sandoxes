import logging


class AppController():
    def __init__(self, ui, model):
        self._ui = ui
        self._model = model
        pass

    def refresh_ports(self):
        if not self._ui.pb_connect_unit.isEnabled():
            return
        self._ui.cb_unit.clear()
        self._ui.cb_tcp4.clear()
        for port in self._model.list_ports():
            if port.description.find("com0com") > -1:
                self._ui.cb_tcp4.addItem(port.name)
            else:
                self._ui.cb_unit.addItem(port.name)

    def connect_unit(self):
        self._ui.cb_unit.setDisabled(True)
        self._ui.pb_connect_unit.setDisabled(True)
        if not self._model.unit_is_connected():
            self._model.connect_unit(self._ui.cb_unit.currentText())
        else:
            self._model.disconnect_unit()

    def handle_unit_port_event(self):
        logging.debug(f'AppController handle_unit_port_event {self._model.unit_is_connected()}')
        self._ui.pb_connect_unit.setEnabled(True)
        if self._model.unit_is_connected():
            self._ui.cb_unit.setDisabled(True)
            self._ui.pb_connect_unit.setText("Disconnect unit")
        else:
            self._ui.cb_unit.setEnabled(True)
            self._ui.pb_connect_unit.setText("Connect unit")

    def connect_app(self):
        self._ui.cb_tcp4.setDisabled(True)
        self._ui.pb_connect_app.setDisabled(True)
        if not self._model.app_is_connected():
            self._model.connect_app(self._ui.cb_tcp4.currentText())
        else:
            self._model.disconnect_app()

    def handle_app_port_event(self):
        logging.debug(f'AppController handle_app_port_event {self._model.app_is_connected()}')
        self._ui.pb_connect_app.setEnabled(True)
        if self._model.app_is_connected():
            self._ui.cb_tcp4.setDisabled(True)
            self._ui.pb_connect_app.setText("Disconnect TCP4")
        else:
            self._ui.cb_tcp4.setEnabled(True)
            self._ui.pb_connect_app.setText("Connect TCP4")

    def handle_unit_data_received(self, data):
        self._ui.document = self._ui.document + data.decode("utf-8")
        self._ui.plainTextEdit.setPlainText(self._ui.document)
        self._ui.set_unit_button()

    def handle_app_data_received(self, data):
        self._ui.document = self._ui.document + data.decode("utf-8")
        self._ui.plainTextEdit.setPlainText(self._ui.document)
        self._ui.set_app_button()
