"""
Módulo de administración de los estilos de las listas o tablas
"""

from PySide6.QtWidgets import QTableWidget

def apply_table_style(table: QTableWidget):
    """
    Aplica un estilo estándar a una tabla QTableWidget.
    :param table: Instancia de QTableWidget a la que se aplicará el estilo.
    """
    table.setStyleSheet(
        """
        QTableWidget {
            background-color: #f9f9f9;
            border: 1px solid #dcdcdc;
            border-radius: 5px;
            font-family: "Archivo Medium";
            font-size: 14px;
            color: #333333;
        }
        QTableWidget::item {
            padding: 5px;
            border: none;
        }
        QTableWidget::item:selected {
            background-color: #0078d7;
            color: white;
        }
        QHeaderView::section {
            background-color: #e1e1e1;
            border: 1px solid #dcdcdc;
            font-family: "Archivo Medium";
            font-size: 14px;
            font-weight: bold;
            color: #333333;
            padding: 4px;
        }
        QScrollBar:vertical {
            border: none;
            background: #f1f1f1;
            width: 12px;
            margin: 0px 0px 0px 0px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background: #b0b0b0;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background: #a0a0a0;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
            subcontrol-origin: margin;
        }
        QScrollBar:horizontal {
            border: none;
            background: #f1f1f1;
            height: 12px;
            margin: 0px 0px 0px 0px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal {
            background: #b0b0b0;
            min-width: 20px;
            border-radius: 6px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #a0a0a0;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
            subcontrol-origin: margin;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical,
        QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        """
    )

