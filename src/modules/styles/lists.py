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
        """
    )

