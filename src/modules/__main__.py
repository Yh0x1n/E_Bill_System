#Aplicación de gestión de inventario utilizando SQL y Pandas
#Importaciones
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtCore import Qt
from login import LoginWindow
import os, sys
import traceback

# Utilidad para obtener la ruta absoluta de recursos (compatible con PyInstaller y desarrollo)
def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con PyInstaller y desarrollo."""
    try:
        # PyInstaller crea una carpeta temporal y almacena el path en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, relative_path)

# Ajuste para registrar las fuentes y configurarlas globalmente
def load_fonts():
    font_dir = resource_path("assets/fonts")
    fonts = [
        "Archivo-Black.ttf",
        "Archivo-Bold.ttf",
        "Archivo-Medium.ttf",
        "Archivo-Regular.ttf"
    ]

    font_families = []

    for font in fonts:
        font_path = os.path.join(font_dir, font)
        print(f"Intentando cargar la fuente: {font_path}")
        if os.path.exists(font_path):
            
            try:
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id == -1:
                    print(f"Advertencia: No se pudo cargar la fuente: {font_path}")
                else:
                    family = QFontDatabase.applicationFontFamilies(font_id)
                    if family:
                        font_families.append(family[0])
                        print(f"Fuente registrada: {family[0]}")
            except Exception as e:
                print(f"Excepción al cargar la fuente {font_path}: {e}")
        else:
            print(f"Advertencia: La ruta de la fuente no existe: {font_path}")

    # Configurar la primera fuente registrada como predeterminada global
    if font_families:
        default_font = QFont(font_families[0], 10)
        QApplication.setFont(default_font)
        print(f"Fuente predeterminada global configurada: {font_families[0]}")
    else:
        print("No se registraron fuentes. Usando la fuente predeterminada del sistema.")

# Manejo global de excepciones para capturar errores silenciosos
def main():
    try:
        QApplication.setAttribute(Qt.AA_DontUseNativeDialogs, True)
        app = QApplication(sys.argv)
        load_fonts()
        window = LoginWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print("Se produjo un error inesperado:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()