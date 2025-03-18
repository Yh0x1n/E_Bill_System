"""
Script que contiene los estilos de los mensajes de notificación al realizar una acción
"""

from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel
from PySide6.QtGui import QFont

class MsgBoxFactory(QMessageBox, QPushButton, QLabel):
    def __init__(self):
        self.msg_box_styles = {
                        "information" : """
                            QMessageBox {
                                background-color:white;
                            }
                            QMessageBox QLabel {
                                color: black;
                                font-size: 14px;
                            }
                            QMessageBox QPushButton {
                                background-color: blue;
                                color: white;
                                border-radius: 5px;
                                padding: 5px;
                            }
                            QMessageBox QPushButton:hover{
                                background-color:darkblue;
                            }
                        """,
                        "warning" : """
                            QMessageBox {
                                background-color:white;
                            }
                            QMessageBox QLabel {
                                color: black;
                                font-size: 14px;
                            }
                            QMessageBox QPushButton {
                                background-color: blue;
                                color: white;
                                border-radius: 5px;
                                padding: 5px;
                            }
                            QMessageBox QPushButton:hover {
                                background-color: darkblue;
                        }
                        """
                    }
    
    def create_msg_box(self, style, title, text, icon, font, font_size, button, button_role = None):
        msg_box = QMessageBox(icon, title, text)
        msg_box.addButton(button, button_role)
        msg_box.setFont(QFont(font, font_size))
        msg_box.setStyleSheet(self.msg_box_styles[style])

        return msg_box