"""
Módulo model para el Casino Virtual
Contiene las clases de modelo para el sistema
"""

__version__ = "0.1.0"
__author__ = "sga-encoder"

# Importar todas las clases de modelo principales
from .usuario import Usuario, UsuarioServicio
from .salaDeJuego import SalaDeJuego, SalaDeJuegoServicio

__all__ = [
    # Clases de usuario
    'Usuario',
    'UsuarioServicio',
    # Clases de sala de juego
    'SalaDeJuego', 
    'SalaDeJuegoServicio'
]