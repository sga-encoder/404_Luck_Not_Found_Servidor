from .Usuario import Usuario
from .KnuckleBones import KnuckleBones
import json
from typing import List, Dict
from datetime import datetime


class SaladeJuegos:
    capacidad: int = 1
    capacidadMinima: int = 1
    jugadores: List[Usuario] = []
    turnoActivo = Usuario()
    historial: List[Dict]
    fechaHoraInicio = datetime.now()
    # fechaHoraFin es un metodo
    listaEspera = list
    apuestas: int


