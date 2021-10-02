"""
Application works as simple serial bridge between some HW and App
Main purpose is to decipher protocol to be possible catch run-time data
"""

import logging
import os
import sys
from PyQt6.QtWidgets import QApplication

from model.model import AppModel
from ui.main_window import MainWidnow


if __name__ == '__main__':
    if not os.path.exists("logs\\\\"):
        os.mkdir('logs')
    logging.basicConfig(filename='logs\log.txt',
                        filemode='w',
                        # format='%(threadName)s: %(message)s',
                        format='%(asctime)s %(threadName)s %(message)s',
                        level=logging.DEBUG)
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    model = AppModel()
    ui = MainWidnow(model)
    ui.show()
    app.exec()
