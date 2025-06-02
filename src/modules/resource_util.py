import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con PyInstaller y desarrollo."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, relative_path)
