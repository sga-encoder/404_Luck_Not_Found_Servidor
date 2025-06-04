"""
Módulo de utilidades para el Casino Virtual
"""

__version__ = "0.1.0"
__author__ = "sga-encoder"

# Importar funciones de utilidad
from .Util import generador_random

# Importar funciones y clase de Firestore
from .firestore import (
    Firestore,
    increment,
    decrement,
    array_union
)

# Exportar todo lo que se debe poder importar desde el módulo utils
__all__ = [
    'generador_random',
    'Firestore',
    'increment',
    'decrement',
    'array_union'
]
