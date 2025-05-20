from typing import override
from src.model.salaDeJuego.juego.juegosDeCartas.Mazo import Mazo
from src.model.salaDeJuego.SalaDeJuego import SalaDeJuego
from abc import ABC, abstractmethod

from src.model.usuario.Usuario import Usuario

class JuegoDeCartas(SalaDeJuego, ABC):
    _mazo: Mazo
    _monto_descartes: list
    _valor_entrada_mesa: int
    _mano_de_jugadores: list
    _mano_de_casino: list
    def __init__(self, id: str, capacidad: int, capacidadMinima: int, valor_entrada_mesa: int):
        super().__init__(id, capacidad, capacidadMinima)
        self._mazo = Mazo(52)
        self._monto_descartes = []
        self._valor_entrada_mesa = valor_entrada_mesa
        self._mano_de_jugadores = []
        self._mano_de_casino = []
    

    def get_mano_casino(self) -> list:
        """
        Método para obtener la mano del casino.
        """
        return self._mano_de_casino
    
    def set_mano_casino(self, mano_de_casino: list):
        """
        Método para establecer la mano del casino.
        """
        self._mano_de_casino = mano_de_casino
    
    @abstractmethod
    def  repartir_cartas(self)-> str:
        """
        Método abstracto para repartir cartas.
        Cada juego de cartas debe implementar su propia lógica.
        """
        pass
    
    @abstractmethod
    def apostar(self, jugador: Usuario, monto: int):
        """
        Método abstracto para apostar.
        Cada juego de cartas debe implementar su propia lógica.
        """
        pass
    
    @override
    def __repr__(self) -> str:
        return (f"{super().__repr__()}"
                f"mazo: {self._mazo}\n"
                f"monto_descartes: {self._monto_descartes}\n"
                f"valor_entrada_mesa: {self._valor_entrada_mesa}\n"
                f"mano_de_jugadores: {self._mano_de_jugadores}\n")
