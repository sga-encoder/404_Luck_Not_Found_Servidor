from enum import Enum, auto

class Etapas(Enum):
    """
    Enumeración que representa las diferentes etapas del poker.
    """
    PRE_FLOP = auto()
    FLOP = auto()
    TURN = auto()
    RIVER = auto()
    SHOWDOWN = auto()

    def __str__(self):
        return self.name