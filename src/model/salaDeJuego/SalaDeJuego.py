from typing import override
from src.model.usuario.Usuario import Usuario
from src.model.salaDeJuego.enums import Juegos
from datetime import datetime
from abc import ABC, abstractmethod
import json
import os

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

  def set_jugadores(self, jugadores):
    self._jugadores = jugadores
    # Inicializar el turno activo al primer jugador
    if jugadores and len(jugadores) > 0:
        self.set_turnoActivo(jugadores[0])
    
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
    """
    Inicializa un juego en la sala de juegos.
    Verifica si hay suficientes jugadores para comenzar.
    """
    if len(self._jugadores) < self._capacidadMinima:
        print("No hay suficientes jugadores para iniciar el juego.")
        return

    print(f"Iniciando el juego: {juego.name}")
    self._historial.append(f"Juego iniciado: {juego.name} a las {datetime.now()}")
    self._turnoActivo = self._jugadores[0]  # El primer jugador toma el turno inicial

  def entrar_sala_de_juego(self, usuario: Usuario):
    """
    Permite que un usuario entre a la sala de juego.
    Si la sala está llena, el usuario será agregado a la lista de espera.
    """
    if len(self._jugadores) < 7:
        self._jugadores.append(usuario)
        print(f"{usuario} ha entrado a la sala de juego.")
    else:
        self.__listaDeEspera.append(usuario)
        print(f"{usuario} ha sido agregado a la lista de espera.")

  def salir_sala_de_juego(self, usuario: Usuario):
    """
    Permite que un usuario salga de la sala de juego.
    Si hay usuarios en la lista de espera, el primero en la lista ocupará su lugar.
    """
    if usuario in self._jugadores:
        self._jugadores.remove(usuario)
        print(f"{usuario} ha salido de la sala de juego.")

        # Verificar si hay alguien en la lista de espera
        if self.__listaDeEspera:
            siguiente_usuario = self.__listaDeEspera.pop(0)
            self._jugadores.append(siguiente_usuario)
            print(f"{siguiente_usuario} ha entrado a la sala de juego desde la lista de espera.")
    else:
        print(f"{usuario} no está en la sala de juego.")
  
  def pagar_apuesta(self, usuario: Usuario, monto: float):
    """
    Registra y procesa el pago de una apuesta por parte de un jugador.
    """
    if usuario not in self._jugadores:
        print(f"{usuario} no está en la sala de juego y no puede realizar apuestas.")
        return

    self._apuestas.append({"usuario": usuario, "monto": monto})
    print(f"{usuario} ha realizado una apuesta de {monto}.")
  
  def get_jugadores_activos(self) -> list:
    """
    Devuelve una lista de jugadores actualmente activos en la sala.
    """
    return [jugador for jugador in self._jugadores if jugador is not None]
  
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

  def guardar_registro_sala(self, estado: str):
    """
    Guarda un registro de la sala de juegos en un archivo JSON.
    El estado puede ser "creada" o "finalizada".
    """
    registro = {
        "id": self._id,
        "tipo_juego": self.__class__.__name__,
        "capacidad": self._capacidad,
        "capacidad_minima": self._capacidadMinima,
        "jugadores": [str(jugador) for jugador in self._jugadores],
        "historial": self._historial,
        "estado": estado,
        "fecha_hora": str(datetime.now())
    }

    ruta = os.path.join("registros", f"sala_{self._id}.json")
    os.makedirs("registros", exist_ok=True)

    with open(ruta, "w") as archivo:
        json.dump(registro, archivo, indent=4)

  def guardar_registro_jugador(self, usuario: Usuario, monto: float):
    """
    Guarda un registro individual para cada jugador en un archivo JSON.
    """
    ruta = os.path.join("registros", f"jugador_{usuario.get_id()}.json")
    os.makedirs("registros", exist_ok=True)

    if os.path.exists(ruta):
        with open(ruta, "r") as archivo:
            registros = json.load(archivo)
    else:
        registros = []

    registro = {
        "mesa": self._id,
        "tipo_juego": self.__class__.__name__,
        "monto": monto,
        "fecha_hora": str(datetime.now())
    }

    registros.append(registro)

    with open(ruta, "w") as archivo:
        json.dump(registros, archivo, indent=4)