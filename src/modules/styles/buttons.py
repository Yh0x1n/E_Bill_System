"""
Módulo que administra el aspecto y creación de los botones.
"""

from PySide6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

class ButtonFactory(QPushButton, QLabel):
    def __init__(self):
        self.button_styles = {

            "default": """QPushButton {
                            background-color: #009345;
                            color: white;
                            border-radius: 10px;
                            text-align: right bottom;
                            padding: 15px;
                        }
                        QPushButton:hover {
                            background-color: #006A32;
                        }""",
            
            "login/register": """
                                QPushButton {
                                    color: white;
                                    background-color: blue;
                                    border-radius: 15px;
                                    padding: 10px;
                                    font-family: "Archivo Medium";
                                }
                                QPushButton:hover {
                                    background-color: darkblue;
                                }
                         """,
            
            "sales": """QPushButton{
                            background-color: transparent;
                            color: white;
                            border-radius: 0px;
                            font-family: "Archivo Medium";
                            text-align: right;
                        }
                        QPushButton:hover {
                            text-decoration: underline;
                        }""",

            "logout": """QPushButton {
                            background-color: transparent;
                            color: white;
                            border-radius: 0px;
                            font-family: "Archivo Medium";
                        }
                        QPushButton:hover {
                            text-decoration: underline;
                        }""",

            "exit": """QPushButton {
                            background-color: #E50202;
                            color: white;
                            border-radius: 10px;
                            text-align: right bottom;
                            padding: 15px;
                        }
                        QPushButton:hover {
                            background-color: #8D0000;
                        }""",

            "default_black": """QPushButton{
                            color: black;
                            font-family: "Archivo Medium";
                            background-color: transparent;
                            border-radius: 35px;
                        }
                        QPushButton:hover{
                            background-color: #f0f0f0;
                        }""",

            "back": """QPushButton{
                            background-color: transparent;
                            color: black;
                            font-family: "Archivo Medium";
                            text-align: right;
                        }
                        QPushButton:hover{
                            text-decoration:underline;
                        }""",

            "accept": """QPushButton{
                            background-color: blue;
                            color: white;
                            font-family: "Archivo Medium";
                            text-align: center;
                            border-radius: 20px;    
                        }
                        QPushButton:hover{
                            background-color: darkblue;
                        }
                        """,
            "cancel": """QPushButton{
                            background-color: red;
                            color: white;
                            font-family: "Archivo Medium";
                            text-align: center;
                            border-radius: 20px;    
                        }
                        QPushButton:hover{
                            background-color: darkred;
                        }"""
        }

    def create_button(self, text, style="default", icon_path=None, font_size=16, min_size=(295, 150), icon_position = Qt.AlignCenter):
        button = QPushButton(text)
        button.setFont(QFont("Archivo Black", font_size))
        button.setStyleSheet(self.button_styles[style])
        button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        button.setMinimumSize(*min_size)

        if icon_path:
            icon_label = QLabel(button)
            icon_label.setPixmap(QIcon(icon_path).pixmap(75, 75))
            icon_label.setStyleSheet("background: transparent;")
            button.setLayout(QHBoxLayout())
            button.layout().addWidget(icon_label, 0, icon_position)

        return button