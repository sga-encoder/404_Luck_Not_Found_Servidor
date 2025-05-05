from typing import override
from src.model.usuario.Usuario import Usuario
from src.model.salaDeJuego.enums import Juegos
from datetime import datetime
from abc import ABC, abstractmethod

class SalaDeJuego(ABC):
  _id: str
  _capacidad: int
  _capacidadMinima: int
  _jugadores: list
  _turnoActivo: Usuario
  _historial: list
  _fechaHoraInicio: datetime
  __listaDeEspera: list
  _apuestas: list
  
  def __init__(self, id: str, capacidad: int, capacidadMinima: int):
    self._id = id
    self._capacidad = capacidad
    self._capacidadMinima = capacidadMinima
    self._jugadores = []
    self._turnoActivo = None
    self._historial = []
    self._fechaHoraInicio = datetime.now()
    self.__listaDeEspera = []
    self._apuestas = []

  def get_id(self) -> str:
    return self._id

  def set_id(self, id: str):
    self._id = id
  
  def get_capacidad(self) -> int:
    return self._capacidad

  def set_capacidad(self, capacidad: int):
    self._capacidad = capacidad

  def get_capacidadMinima(self) -> int:
    return self._capacidadMinima

  def set_capacidadMinima(self, capacidadMinima: int):
    self._capacidadMinima = capacidadMinima

  def get_jugadores(self) -> list:
    return self._jugadores

  def set_jugadores(self, jugadores: list):
    self._jugadores = jugadores
    
  def get_jugador_activo_index(self) -> int:
    return self.get_jugadores().index(self.get_turnoActivo())

  def get_turnoActivo(self) -> Usuario:
    return self._turnoActivo

  def set_turnoActivo(self, turnoActivo: Usuario):
    self._turnoActivo = turnoActivo

  def get_historial(self) -> list:
    return self._historial
  
  def set_historial(self, historial: list):
    self._historial = historial
    
  def get_fechaHoraInicio(self) -> datetime:
    return self._fechaHoraInicio

  def set_fechaHoraInicio(self, fechaHoraInicio: datetime):
    self._fechaHoraInicio = fechaHoraInicio

  def get_listaDeEspera(self) -> list:
    return self.__listaDeEspera

  def set_listaDeEspera(self, listaDeEspera: list):
    self.__listaDeEspera = listaDeEspera

  def get_apuestas(self) -> list:
    return self._apuestas

  def set_apuestas(self, apuestas: list):
    self._apuestas = apuestas
    
  def iniciar_juego(self, juego: Juegos):
    print("falta implementar iniciar_juego()")
    pass
  
  def entrar_sala_de_juego(self, usuario: Usuario):
    print("falta implementar entrar_sala_de_juego()")
    pass
  
  def __entrar_sala_de_juego(self, usuario: Usuario, index: int):
    print("falta implementar __entrar_sala_de_juego()")
    pass

  def salir_sala_de_juego(self, usuario: Usuario):
    print("falta implementar salir_sala_de_juego()")
    pass
  
  def pagar_apuesta(self, usuario: Usuario, monto: float):
    print("falta implementar pagar_apuesta()")
    pass
  
  def get_jugadores_activos(self) -> list:
    print("falta implementar get_jugadores_activos()")
    pass
  
  @abstractmethod
  def inicializar_juego(self):
    """
    Método abstracto para inicializar el juego.
    Cada juego de cartas debe implementar su propia lógica.
    """
    pass
  
  @override
  def __repr__(self) -> str:
    
    return (
      f"id: {self._id}\n"
      f"capacidad: {self._capacidad}\n"
      f"capacidadMinima: {self._capacidadMinima}\n"
      f"jugadores: {self._jugadores}\n"
      f"turnoActivo: {self._turnoActivo}\n"
      f"historial: {self._historial}\n"
      f"fechaHoraInicio: {self._fechaHoraInicio}\n"
      f"listaDeEspera: {self.__listaDeEspera}\n"
      f"apuestas: {self._apuestas}\n"
    )