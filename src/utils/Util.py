""""
Módulo de utilidades para el Casino
Proporciona funciones auxiliares utilizadas en todo el proyecto
"""

import secrets

def generador_random(minimo: int, maximo: int) -> int:
    """
    Genera un número aleatorio criptográficamente seguro entre un rango dado
    
    Args:
        minimo (int): El valor mínimo del rango (inclusive)
        maximo (int): El valor máximo del rango (inclusive)
        
    Returns:
        int: Un número aleatorio entre minimo y maximo
        
    Ejemplo:
        >>> generador_random(1, 10)
        7
    """
    return secrets.randbelow(maximo - minimo + 1) + minimo
