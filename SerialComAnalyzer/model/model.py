import logging
from threading import Thread
import serial
import serial.tools.list_ports
from PyQt6.QtCore import pyqtSignal, QObject


class AppModel(QObject):
    unit_data_received = pyqtSignal(bytes, name='unit_data_received', )
    app_data_received = pyqtSignal(bytes, name='app_data_received')
    unit_port_event = pyqtSignal(name='unit_port_event')
    app_port_event = pyqtSignal(name='app_port_event')

    def __init__(self, parent=None):
        super(AppModel, self).__init__()
        logging.debug('AppModel __init__')
        self._unit_port= None
        self._app_port = None
        self._data = []

    def port_listener_demon(self, is_it_unit, in_port_name, port_event):
        logging.debug(f'AppModel port_listener_demon starts')
        try:
            port = serial.Serial(in_port_name,
                                    baudrate=115200,
                                    parity=serial.PARITY_NONE,
                                    stopbits=1)
            if is_it_unit:
                self._unit_port = port
            else:
                self._app_port = port
            port_event.emit()
            while port.isOpen():
                z = port.read()
                if z and len(z) > 0 and z[0] != 0:
                    self._data.append(z)
                if is_it_unit:
                    self.handle_unit_data_received(z)
                    self.unit_data_received.emit(z)
                else:
                    self.handle_app_data_received(z)
                    self.app_data_received.emit(z)
            port = None
        except Exception as e:
            logging.error(f'Error in unit_listener_demon {in_port_name} \n{e}')
            port = None
        logging.debug(f'AppModel port_listener_demon ends')
        port_event.emit()

    def close_port(self, port):
        if port and port.isOpen():
            port.close()
            port = None

    def list_ports(self):
        return serial.tools.list_ports.comports()

    def connect_unit(self, port_name):
        logging.debug(f'AppModel connect_unit {port_name}')
        thread = Thread(target=self.port_listener_demon,
                        name= f'unit_demon_{port_name}',
                        args=(True,
                              port_name,
                              self.unit_port_event,
                              ))
        thread.start()

    def disconnect_unit(self):
        logging.debug(f'AppModel disconnect_unit')
        if self._unit_port and self._unit_port.isOpen():
            self._unit_listener_is_alive = False
            self._unit_port.cancel_read()
            self._unit_port.close()

    def unit_is_connected(self):
        if self._unit_port and self._unit_port.isOpen():
            return True
        else:
            return False

    def connect_app(self, port_name):
        logging.debug(f'AppModel connect_app {port_name}')
        thread = Thread(target=self.port_listener_demon,
                        name= f'app_demon_{port_name}',
                        args=(False,
                              port_name,
                              self.app_port_event,
                              ))
        thread.start()

    def disconnect_app(self):
        logging.debug(f'AppModel disconnect_app')
        if self._app_port and self._app_port.isOpen():
            self._app_listener_is_alive = False
            self._app_port.cancel_read()
            self._app_port.close()

    def app_is_connected(self):
        if self._app_port and self._app_port.isOpen():
            return True
        else:
            return False

    def handle_unit_data_received(self, data):
        # First send it further
        if self.app_is_connected():
            self._app_port.writelne(data)


    def handle_app_data_received(self, data):
        if self.unit_is_connected():
            self._unit_port.writelne(data)
