"""Módulo de ayuda y guía al usuario"""

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QMainWindow, QPushButton
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt
import os
from resource_util import resource_path
from styles.buttons import ButtonFactory

class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lanchmann - Ayuda y Guía al Usuario")
        self.setWindowIcon(QIcon(resource_path("assets/pictures/AqualabLogo.jpg")))
        self.setMinimumSize(900, 700)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color: white;")
        
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        
        layout = QVBoxLayout(content)
        layout.setAlignment(Qt.AlignTop)
        
        sections = [
            {
                'title': 'Menú Principal',
                'desc': 'Desde el menú principal puedes acceder a los módulos de Clientes, Productos y Servicios, y Facturación. Utiliza los botones de la barra lateral para navegar entre las diferentes funcionalidades del sistema.',
                'imgs': ['src/assets/screenshots/Menú.png'],
                'actions': [
                    ('Navegación', 'Haz clic en los botones de la barra lateral para acceder a cada módulo.')
                ]
            },
            {
                'title': 'Clientes',
                'desc': 'En el módulo de clientes puedes gestionar toda la información de tus clientes. Las acciones disponibles incluyen agregar, editar, ver detalles y eliminar clientes.',
                'imgs': [
                    'src/assets/screenshots/Clientes_main.png',
                    'src/assets/screenshots/Clientes_agregar.png',
                    'src/assets/screenshots/Clientes_editar.png',
                    'src/assets/screenshots/Clientes_detalles.png'
                ],
                'actions': [
                    ('Agregar cliente', 'Presiona el botón de “+” para abrir el formulario de registro de un nuevo cliente.'),
                    ('Editar cliente', 'Selecciona un cliente de la lista y haz clic en el ícono de lápiz para modificar sus datos.'),
                    ('Mostrar detalles', 'Haz doble clic sobre un cliente para ver toda su información en una ventana emergente.'),
                    ('Eliminar cliente', 'Selecciona un cliente y haz clic en el ícono de papelera para eliminarlo.')
                ]
            },
            {
                'title': 'Productos y Servicios',
                'desc': 'Gestiona tus productos y servicios. Puedes agregar nuevos productos, editar los existentes, ver detalles o eliminarlos.',
                'imgs': [
                    'src/assets/screenshots/Productos_main.png',
                    'src/assets/screenshots/Productos_agregar.png',
                    'src/assets/screenshots/Productos_editar.png',
                    'src/assets/screenshots/Productos_detalles.png'
                ],
                'actions': [
                    ('Agregar producto/servicio', 'Haz clic en el botón de “+” para registrar un nuevo producto o servicio.'),
                    ('Editar producto/servicio', 'Selecciona un producto y haz clic en el ícono de lápiz para modificar sus atributos.'),
                    ('Mostrar detalles', 'Haz doble clic sobre un producto para ver su información completa.'),
                    ('Eliminar producto/servicio', 'Selecciona un producto y haz clic en el ícono de papelera para eliminarlo.')
                ]
            },
            {
                'title': 'Facturación',
                'desc': 'En el módulo de facturación puedes generar nuevas facturas, gestionar las existentes, consultar detalles y exportar información.',
                'imgs': [
                    'src/assets/screenshots/Facturas_generar.png',
                    'src/assets/screenshots/Facturas_gestion.png',
                    'src/assets/screenshots/Facturas_gestion_detalles.png',
                    'src/assets/screenshots/Facturas_seleccionar.png'
                ],
                'actions': [
                    ('Generar factura', 'Completa los campos requeridos y presiona el botón correspondiente para crear una nueva factura.'),
                    ('Gestionar facturas', 'Accede a la lista de facturas generadas para ver, editar o eliminar registros.'),
                    ('Mostrar detalles', 'Haz doble clic sobre una factura para ver la información relevante asociada, o presiona el botón "abrir" para visualizar el archivo de la factura en formato PDF por medio de tu visor predeterminado.'),
                ]
            },
            {
                'title': 'Exportar Datos',
                'desc': 'Puedes exportar la información de clientes, productos y facturas a archivos Excel para su análisis o respaldo.',
                'imgs': [
                    'src/assets/icons/excel.png'
                ],
                'actions': [
                    ('Acción', 'Haz clic en el botón de exportación en cualquiera de los módulos de gestión para convertir la lista en una hoja de cálculo en formato Excel'),
                ]
            },
            {
                'title': 'Ajustes',
                'desc' : 'Establece la información de la empresa proveedora de las facturas, así como gestionar a los usuarios que utilizan el sistema.',
                'imgs' : [
                    'src/assets/screenshots/Ajustes.png'
                ],
                'actions': [
                    ('Información de la empresa', 'Puedes "Mostrar" o "Editar" la información del proveedor, completando los campos requeridos para que los datos de tu empresa aparezcan en las facturas.'),
                    ('Gestión de usuarios', 'Edita o elimina usuarios que tendrán acceso al sistema.'),
                ]
            }

        ]
        
        # Convertir rutas relativas a absolutas para las imágenes
        for section in sections:
            section['imgs'] = [resource_path("assets/" + img_path.split("assets/")[-1]) for img_path in section['imgs']]
        
        for section in sections:
            title = QLabel(section['title'])
            title.setFont(QFont("Archivo Black", 20))
            layout.addWidget(title)
            desc = QLabel(section['desc'])
            desc.setFont(QFont("Archivo Medium", 13))
            desc.setWordWrap(True)
            layout.addWidget(desc)
            if 'actions' in section:
                for action, detail in section['actions']:
                    action_label = QLabel(f"<b>{action}:</b> {detail}")
                    action_label.setFont(QFont("Archivo Medium", 12))
                    action_label.setWordWrap(True)
                    layout.addWidget(action_label)
            for img_path in section['imgs']:
                if os.path.exists(img_path):
                    pix = QPixmap(img_path).scaledToWidth(450, Qt.SmoothTransformation)
                    if os.path.basename(img_path) == 'excel.png':
                        pix = pix.scaledToHeight(50, Qt.SmoothTransformation)
                    img_label = QLabel()
                    img_label.setPixmap(pix)
                    img_label.setAlignment(Qt.AlignCenter)
                    layout.addWidget(img_label)
            layout.addSpacing(20)
        
        close_btn = ButtonFactory().create_button("Cerrar", style="accept", font_size=14, min_size=(120, 40))
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        
        # Estilo para la scrollbar
        scroll.setStyleSheet("""
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
        """)
        
        scroll.setWidget(content)
        self.setCentralWidget(scroll)

