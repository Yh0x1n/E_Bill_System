"""
Módulo que administra los estilos y creación de los mensajes de notificación.
"""

from PySide6.QtWidgets import QMessageBox, QPushButton, QLabel
from PySide6.QtGui import QFont, QIcon
import os

class MsgBoxFactory(QMessageBox, QPushButton, QLabel):
    def __init__(self):
        super().__init__()
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
                        """,
                        "question" : """QMessageBox{
                                background-color:white;
                            }
                            QMessageBox QLabel {
                                color: black;
                                border-radius: 5px;
                                padding: 5px;
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
                            """,
                    "error" : """
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
                            }"""
                    }
    
    def create_msg_box(self, style, title, text, icon, font, font_size, button, button_role = None):
        msg_box = QMessageBox(icon, title, text)
        msg_box.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "../../assets/pictures/AqualabLogo.jpg")))
        msg_box.addButton(button, button_role)
        msg_box.setFont(QFont(font, font_size))
        msg_box.setStyleSheet(self.msg_box_styles[style])

        return msg_box

    def create_question_box(self, style, title, text, icon, font, font_size, buttons = list, button_roles=list):
        question_box = QMessageBox(icon, title, text)
        question_box.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "../../assets/pictures/AqualabLogo.jpg")))
        
        if button_roles is None:
            button_roles = [None] * len(buttons)
        
        for button, role in zip(buttons, button_roles):
            question_box.addButton(button, role)
        
        question_box.setFont(QFont(font, font_size))
        question_box.setStyleSheet(self.msg_box_styles[style])
        
        return question_box