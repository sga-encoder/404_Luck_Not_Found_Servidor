"""
Módulo principal del servidor para el Casino Virtual
"""

__version__ = "0.1.0"
__description__ = "Raíz de la aplicación del servidor"

# Importar las clases principales del modelo para facilitar el acceso
from .model import (
    Usuario, UsuarioServicio,
    SalaDeJuego, SalaDeJuegoServicio,
    JuegoDeCartas, Mazo, BlackJack, Poker
)
__author__ = "sga-encoder"

# Configurar el path para las importaciones
import os
import sys

# Añadir la carpeta src al path
src_path = os.path.dirname(os.path.abspath(__file__))
if src_path not in sys.path:
    sys.path.append(src_path)

# Importar módulos principales
from .utils import *
from .model import *
# from .view import *  # Eliminado - migrado al cliente

# Exportar símbolos principales
__all__ = [
    'utils',
    'model'
    # 'view'  # Eliminado - migrado al cliente
]