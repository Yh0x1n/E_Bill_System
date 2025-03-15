"""
Módulo que administra los labels de la interfaz gráfica.
"""

from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class LabelFactory(QLabel):
    def __init__(self):
        self.label_styles = {
            "default" : """QLabel{
                                background-color: transparent;
                                color: white;
                            }""",
            "medium_black" : """QLabel{
                                    background-color: transparent;
                                    color: black;
                                    font-family: "Archivo Medium"
                                }""",
            "medium_white" : """QLabel{
                                    background-color: transparent;
                                    color: white;
                                    font-family: "Archivo Medium"
                                }""",
            "money" : """QLabel{
                                background-color:transparent;
                                color: #0071BD;
                                font-family: "Archivo Medium";
                            }""",
            "bold_black" : """QLabel{
                                    background-color:transparent;
                                    color:black;
                                    font-family: "Archivo Black";
                                }""",
            "bold_white" : """QLabel{
                                background-color: transparent;
                                color: white;
                                font-family: "Archivo Black";
                            }""",
                                
        }

    def create_label(self, text, font = "Archivo", style = "default", font_size = 12):
        label = QLabel(text)
        label.setFont(QFont(font, font_size))
        label.setStyleSheet(self.label_styles[style])
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        return label