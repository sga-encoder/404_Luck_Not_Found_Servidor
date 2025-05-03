from enum import Enum, auto

class Juegos(Enum):
    """
    Enumeración que representa los diferentes juegos disponibles en la sala de juego.
    """
    POKER = auto()
    BLACKJACK = auto()
    KNUCKLE_BONES = auto()
    
    def __str__(self):
        return self.name