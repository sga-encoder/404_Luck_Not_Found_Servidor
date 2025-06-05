from typing import override
from ..usuario import Usuario
from .enums import Juegos
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
  _juego: str
  
  def __init__(self, capacidad: int, capacidadMinima: int):
    # self._id = id
    self._capacidad = capacidad
    self._capacidadMinima = capacidadMinima
    self._jugadores = []
    self._turnoActivo = None
    self._historial = []
    self._fechaHoraInicio = datetime.now()
    self.__listaDeEspera = []
    self._apuestas = []
    self._juego = ''
  
  @classmethod
  def from_dict(cls, data: dict):
    # Crear una nueva instancia con los valores del diccionario
    # Valores predeterminados apropiados para KnuckleBones
    capacidad = data.get('capacidad', 2)
    capacidad_minima = data.get('capacidad_minima', 2)
    
    # Crear instancia usando el constructor
    instance = cls(capacidad, capacidad_minima)
    
    # Asignar los demás atributos
    instance._id = data.get('id')
    instance._jugadores = data.get('jugadores', [])
    instance._turnoActivo = data.get('turnoActivo', None)
    instance._historial = data.get('historial', [])
    instance._fechaHoraInicio = datetime.fromisoformat(data.get('fechaHoraInicio', datetime.now().isoformat()))
    instance._SalaDeJuego__listaDeEspera = data.get('listaDeEspera', [])
    instance._apuestas = data.get('apuestas', [])
    
    return instance
    

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

  def get_juego(self) -> str:
    return self._juego 
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
  def set_juego(self, juego: int):
    self._juego = juego
    
  def set_apuestas(self, apuestas: list):
    self._apuestas = apuestas
  async def crear_sala_de_juego(self, diccionario: dict):
    import src.model.salaDeJuego.SalaDeJuegoServicio as  SalaDeJuegoServicio
    servicio = SalaDeJuegoServicio()
    # Ahora esta función es async para usar await correctamente
    self._id = await servicio.crear_sala_de_juego_activa(diccionario)
  async def entrar_sala_de_juego(self, usuario: Usuario, diccionario: dict = None):
    """
    Permite que un usuario entre a la sala de juego.
    Si la sala está llena, el usuario será agregado a la lista de espera.
    """
    import src.model.salaDeJuego.SalaDeJuegoServicio as  SalaDeJuegoServicio
    servicio = SalaDeJuegoServicio()
    salas_activas = await servicio.obtener_collection_salas_de_juego()
    for sala in salas_activas:
      if sala.get('tipo_juego') == diccionario.get('tipo_juego') and len(sala.get('jugadores', [])) < sala.get('capacidad'):
        await servicio.entrar_sala_de_juego(sala.get('id'), usuario)
        self._id = sala.get('id')
        print(f"{usuario} ha entrado a la sala de juego.")
        return True
        
    if self._id is None:
      await self.crear_sala_de_juego(diccionario)
      
    if len(self._jugadores) < self._capacidad:
      self._jugadores.append(usuario)
      await servicio.entrar_sala_de_juego(self._id, usuario)
      print(f"{usuario} ha entrado a la sala de juego.")
      return True
    else:
      # Asegurar que _capacidadMinima tenga un valor válido
      capacidad_minima_segura = self._capacidadMinima if self._capacidadMinima is not None else 2
      if len(self.__listaDeEspera) > capacidad_minima_segura:  # Limitar la lista de espera
          await self.crear_sala_de_juego(diccionario)
          
      else:
        self.__listaDeEspera.append(usuario)
        await servicio.agregar_jugador_a_lista_de_espera(self._id, usuario)
        print(f"{usuario} ha sido agregado a la lista de espera.")
        return False

  def salir_sala_de_juego(self, usuario: Usuario):
    """
    Permite que un usuario salga de la sala de juego.
    Si hay usuarios en la lista de espera, el primero en la lista ocupará su lugar.
    """
    import src.model.salaDeJuego.SalaDeJuegoServicio as  SalaDeJuegoServicio
    servicio = SalaDeJuegoServicio()
    if usuario in self._jugadores:
        self._jugadores.remove(usuario)
        servicio.salir_sala_de_juego(self._id, usuario)
        self.guardar_registro_jugador(usuario, 0)  # Guardar registro de salida con monto 0
        
        print(f"{usuario} ha salido de la sala de juego.")

        # Verificar si hay alguien en la lista de espera
        if self.__listaDeEspera:
            siguiente_usuario = self.__listaDeEspera.pop(0)
            servicio.eliminar_jugador_de_lista_de_espera(self._id, siguiente_usuario)
            self.entrar_sala_de_juego(siguiente_usuario)
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
    import src.model.salaDeJuego.SalaDeJuegoServicio as  SalaDeJuegoServicio
    servicio = SalaDeJuegoServicio()
    # import json
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
    
    servicio.guardar_registro_sala_de_juego(self._id, registro)
    

    # ruta = os.path.join("registros", f"sala_{self._id}.json")
    # os.makedirs("registros", exist_ok=True)

    # with open(ruta, "w") as archivo:
    #     json.dump(registro, archivo, indent=4)

  def guardar_registro_jugador(self, usuario: Usuario, monto: float):
    """
    Guarda un registro individual para cada jugador en un archivo JSON.
    """
    # ruta = os.path.join("registros", f"jugador_{usuario.get_id()}.json")
    # os.makedirs("registros", exist_ok=True)

    # if os.path.exists(ruta):
    #     with open(ruta, "r") as archivo:
    #         registros = json.load(archivo)
    # else:
    #     registros = []
  
    
    registro = {
        "mesa": self._id,
        "tipo_juego": self.__class__.__name__,
        # "monto": monto,
        "fecha_hora": str(datetime.now())
    }
    usuario.agregar_historial(registro)

    # registros.append(registro)    # with open(ruta, "w") as archivo:
    #     json.dump(registros, archivo, indent=4)

  def to_dict(self) -> dict:
        """
        Convierte el objeto SalaDeJuego en un diccionario

        Returns:
            dict: Diccionario con los atributos del objeto SalaDeJuego
        """
        return {
            "id": self._id,
            "tipo_juego": self.__class__.__name__,
            "capacidad": self._capacidad,
            "capacidad_minima": self._capacidadMinima,
            "jugadores": [jugador.to_dict() for jugador in self._jugadores],
            "historial": self._historial,
            "estado": True if self._jugadores else False,
            "fecha_hora": str(datetime.now())
        }