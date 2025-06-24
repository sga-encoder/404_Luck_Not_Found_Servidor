import copy
from servidor.src.model.salaDeJuego.SalaDeJuego import SalaDeJuego
from servidor.src.model.usuario import Usuario
from servidor.src.utils.Util import generador_random
from servidor.src.model.salaDeJuego.SalaDeJuegoServicio import SalaDeJuegoServicio


class KnuckleBones(SalaDeJuego):
    _mesa_de_juego: list
    _cantidad_de_dados_puestos: list
    _turno: int
    _historial: list

    def __init__(self):
        # from cliente.utils.user_session import UserSessionManager
        # usuario_data = UserSessionManager().load_user_session()
        super().__init__(2, 2)  # KnuckleBones requiere exactamente 2 jugadores
        # Inicializar el _id como None hasta que se establezca
        self.set_juego('KnuckleBones')
        self._mesa_de_juego = [
            [
                [0, 0, 0], 
                [0, 0, 0], 
                [0, 0, 0]
            ],
            [
                [0, 0, 0], 
                [0, 0, 0],
                [0, 0, 0]
            ]
        ]
        self._cantidad_de_dados_puestos = [0, 0]
        self._turno = 0
        self._inicia_el_bot = None
        self._historial = []

    def get_mesa_de_juego(self) -> list:
        return self._mesa_de_juego

    def get_oponente_index(self) -> int:
        if self.get_jugador_activo_index() == 0:
            return 1
        else:
            return 0

    def __get_position(self, posicion: int, invetida: bool) -> int:
        posiciones = [[0, 1, 2],[2, 1, 0]]
        index = -1
        if invetida:
            index = self.get_oponente_index()
        else:
            index = self.get_jugador_activo_index()
            
        return posiciones[index][posicion]

    def poner_dado(self, mesa_de_jugador: list, posicion: int, valor: int, esta_jugando = True) -> list:
        index_activo = self.get_jugador_activo_index()
        
        contador = 0
        for i in range(3):
            if mesa_de_jugador[posicion][self.__get_position(i, False)] == 0:
                mesa_de_jugador[posicion][self.__get_position(i, False)] = valor
                if esta_jugando:
                    self._cantidad_de_dados_puestos[index_activo] += 1
                break
            else:
                contador += 1
        if contador == 3:
                return []
        return mesa_de_jugador

    def __eliminar_dado(self, mesa_de_jugador: list, posicion: int, valor: int, esta_jugando = True) -> list:
        index_activo = self.get_oponente_index()
        columna = self.__get_position(posicion, True) if index_activo == 1 else self.__get_position(posicion, False)
        for i in range(3):
            if mesa_de_jugador[columna][self.__get_position(i, True)] == valor	:
                mesa_de_jugador[columna][self.__get_position(i, True)] = 0
                if esta_jugando:
                    self._cantidad_de_dados_puestos[index_activo] -= 1
        return mesa_de_jugador

    def determinar_ganador(self, mesa_de_juego: list) -> str:
        puntos_jugador = self.sumar_puntos(mesa_de_juego[self.get_jugador_activo_index()])
        puntos_oponente = self.sumar_puntos(mesa_de_juego[self.get_oponente_index()])
        self.print_mesa()
        mesaje = ''
        if puntos_jugador > puntos_oponente:
            mesaje = f'El jugador {self.get_jugadores()[self.get_jugador_activo_index()].get_id()} ha ganado'
        elif puntos_jugador < puntos_oponente:
            mesaje = f'El jugador {self.get_jugadores()[self.get_oponente_index()].get_id()} ha ganado'
        else:
            mesaje = 'Es un empate'
        return mesaje

    def knuckle_bot(self, dado: int, mesaJuego: list) -> dict:
        historial = {
            'puntaje_nodos': [0,0,0],
            'puntos_bot': self.sumar_puntos(mesaJuego[self.get_jugador_activo_index()]),
            'puntos_jugador': self.sumar_puntos(mesaJuego[self.get_oponente_index()]),
        }
        proyeccion_jugador = self.proyector_de_jugadas_del_jugador(mesaJuego, self.get_oponente_index())
        posicion = self.knuckle_bot_think(0, proyeccion_jugador, self._mesa_de_juego, historial, dado)
        print(f'El bot eligió la posición {posicion+1}')
        self.poner_dado(self._mesa_de_juego[self.get_jugador_activo_index()], posicion, dado)
        # if callback == []:
        #     historial['puntaje_nodos'].remove(posicion)
        #     callback = self.poner_dado(self._mesa_de_juego[self.get_jugador_activo_index()], historial['puntaje_nodos'], dado)
        historial['posicion'] = posicion

        return historial

    def knuckle_bot_think(self, posicion: int, proyeccion_jugador: list, mesa_de_juego: list, historial: dict, dado: int) -> int:
        valores = (historial['puntaje_nodos'], historial['puntos_bot'], historial['puntos_jugador'])
        puntaje, puntos_bot, puntos_jugador = valores
        
        if posicion == 3:
            maximo = max(puntaje)
            return puntaje.index(maximo)
        else:
            # Inicializar el puntaje de esta posición en 0 para evitar acumulaciones incorrectas
            puntaje[posicion] = 0
            
            # Evaluar cada posible jugada del jugador y su impacto
            for jugada_proyectada in proyeccion_jugador:
                proyeccion = self.proyector_de_jugada(mesa_de_juego, jugada_proyectada, posicion, dado)
                if proyeccion == {}:
                    continue
                puntos_proyectados_bot, puntos_proyectados_jugador = proyeccion['puntos_proyectados']
                diferencia_de_puntos_proyectados_jugador, diferencia_de_puntos_proyectados_bot = proyeccion['diferencia_de_puntos_proyectados']

                if puntos_bot < puntos_jugador:
                    # el bot va perdiendo
                    if puntos_proyectados_bot > puntos_bot:
                        puntaje[posicion] += puntos_proyectados_bot * 9 /1 if puntos_proyectados_jugador == 0 else puntos_proyectados_jugador
                    elif puntos_proyectados_bot == puntos_proyectados_jugador:
                        puntaje[posicion] += 5
                    else:
                        puntaje[posicion] -= puntos_proyectados_bot * 9 / 1 if puntos_proyectados_jugador == 0 else puntos_proyectados_jugador

                elif puntos_bot > puntos_jugador:
                    # el bot va ganando
                    puntaje[posicion] += 10

                else:
                    # el bot va empatando
                    puntaje[posicion] += 0

            # Añadir bonificación por el estado de la columna
            puntuacion_columna = self.columna_optima(mesa_de_juego[self.get_jugador_activo_index()][posicion])
            puntaje[posicion] += puntuacion_columna

            # Añadir bonificación por comparación con columna paralela
            columna_del_jugador_opuesto = mesa_de_juego[self.get_oponente_index()][posicion]
            columna_del_jugador_activo = mesa_de_juego[self.get_jugador_activo_index()][posicion]
            puntaje[posicion] += self.columna_paralela(columna_del_jugador_opuesto, columna_del_jugador_activo, puntuacion_columna, dado)

            # Pasar a la siguiente posición
            return self.knuckle_bot_think(posicion + 1, proyeccion_jugador, mesa_de_juego, historial, dado)

    def proyector_de_jugada(self, mesa_de_juego: list, jugada_proyectada: list, posicion: int, dado: int) -> dict:
        mesa = copy.deepcopy(mesa_de_juego)
        # Simular colocación del dado del bot
        bot = self.poner_dado(mesa[self.get_jugador_activo_index()], posicion, dado, False)
        
        if bot == []:
            return {}

        # Simular eliminación de dados del jugador
        jugador = self.__eliminar_dado(mesa[self.get_oponente_index()], posicion, dado, False)
        
        jugador = self.poner_dado(jugador, jugada_proyectada[0], jugada_proyectada[1], False)

        # Simular la jugada de respuesta del jugador y su impacto en el bot
        bot = self.__eliminar_dado(bot, jugada_proyectada[0], jugada_proyectada[1], False)
        
        # Calcular puntuaciones resultantes después de estas jugadas
        puntos_proyectados_jugador = self.sumar_puntos(jugador)
        puntos_proyectados_bot = self.sumar_puntos(bot)
        return { 
            'puntos_proyectados': [ puntos_proyectados_jugador, puntos_proyectados_bot],
            'mesa_de_juego_proyectada': [jugador , bot],
            'diferencia_de_puntos_proyectados': [
                puntos_proyectados_jugador - puntos_proyectados_bot,
                puntos_proyectados_bot - puntos_proyectados_jugador 
            ]
        }

    def columna_optima(self, columna_del_jugador_activo: list) -> int:
        contador = 0
        for i in range(3):
            if columna_del_jugador_activo[i] == 0:
                contador +=1
        if contador == 3:
            return 2
        elif contador == 2:
            return 1
        elif contador == 1:
            return 0
        else:
            return -2

    def columna_paralela(self, columna_del_jugador_opuesto: list, columna_del_jugador_activo: list, puntuacion_columna: int, dado: int) -> int:
        contador = 0
        for i in range(3):
            if columna_del_jugador_opuesto[i] > dado and columna_del_jugador_opuesto[i] != 0:
                contador -= 1

            if puntuacion_columna == 1 or puntuacion_columna == 0:
                if columna_del_jugador_activo[i] < dado and columna_del_jugador_activo[i] != 0:
                    contador -= 1

        return contador

    def proyector_de_jugadas_del_jugador(self, mesaDeJuego: list, indice_jugador: int) -> list:
        jugadas = []
        for i in range(6):
            for j in range(3):
                for k in range(3):
                    if mesaDeJuego[indice_jugador][j][k] == 0:
                        jugadas.append([ j, i + 1])
                        break
        return jugadas

    def sumar_puntos(self, mesa_del_jugador: list) -> int:
        puntos = 0
        for i in range(3):
            sum_aux = 0
            contador = 0
            for j in range(3):
                if(mesa_del_jugador[i][j] == mesa_del_jugador[i][0] and j != 0) or (mesa_del_jugador[i][j] == mesa_del_jugador[i][1] and j != 1) or (mesa_del_jugador[i][j] == mesa_del_jugador[i][2] and j != 2):
                    sum_aux += mesa_del_jugador[i][j]
                    contador += 1
                    if(j == 2):
                        puntos += sum_aux * contador
                else:                    
                    if contador > 1:
                        puntos += sum_aux * contador
                        sum_aux = 0
                        contador = 0
                    puntos += mesa_del_jugador[i][j]
                    
        return puntos

    def finalizo_juego(self) -> bool:
        if self._cantidad_de_dados_puestos[0] == 9 or self._cantidad_de_dados_puestos[1] == 9:
            return True
        else:
            return False

    def cambiar_jugador_activo(self) -> None:
        self.set_turnoActivo(self.get_jugadores()[self.get_oponente_index()])
        
    def lanzar_dado(self) -> int:
        return generador_random(1, 6)

    async def sincronizar_estado_con_firestore(self):
        """
        Sincroniza el estado actual del juego con Firestore.
        Actualiza la mesa_de_juego y otros datos del juego en tiempo real.
        """
        if self._id is not None:
            try:
                servicio = SalaDeJuegoServicio()
                # Usar actualizar_sala_de_juego que actualiza en 'salas_de_juego_activas'
                await servicio.actualizar_sala_de_juego(self._id, self.to_dict())
                print(f"Estado del juego sincronizado con Firestore para sala {self._id}")
            except Exception as e:
                print(f"Error al sincronizar estado con Firestore: {e}")
            except Exception as e:
                print(f"Error al sincronizar estado con Firestore: {e}")

    async def actualizar_jugador_activo(self, id: str, usuario: Usuario):
        """
        Actualiza el jugador activo en Firestore usando el servicio
        Args:
            id (str): ID de la sala de juego
            usuario (Usuario): Usuario que será el turno activo
        """
        try:
            servicio = SalaDeJuegoServicio()
            await servicio.actualizar_jugador_activo(id, usuario)
        except Exception as e:
            print(f"Error al actualizar jugador activo: {e}")

    def juego(self)-> str:
        index_activo = self.get_jugador_activo_index()
        index_oponente = self.get_oponente_index()
        if  self.finalizo_juego():
            return self.determinar_ganador(self._mesa_de_juego)
        else:
            dado = self.lanzar_dado()
            self.print_mesa()
            print(f'a el jugador {self.get_turnoActivo().get_id()} El dado salió en {dado}')
            if(self._turno > 0 and self._turno % 2 != 0):
                historial = self.knuckle_bot(dado, self._mesa_de_juego)
                self._historial.append(historial)
                posicion = historial['posicion']                # print(f'El bot eligió la posición {posicion+1}')
                
            else:
                posicion = int(input('Ingrese la posición donde desea poner el dado (1,2,3): '))-1
                
            self.poner_dado(self._mesa_de_juego[index_activo], posicion, dado)
            self.__eliminar_dado(self._mesa_de_juego[index_oponente], posicion, dado)
            self.cambiar_jugador_activo() 
            self._turno += 1
            return self.juego()
    
    def inicializar_juego(self):
        """
        Implementación del método abstracto de SalaDeJuego
        """
        # Primero verificar que hay suficientes jugadores y establecer turno activo
        if len(self._jugadores) < self._capacidadMinima:
            print("No hay suficientes jugadores para iniciar el juego.")
            return False
            
        # Establecer el turno activo al primer jugador
        self._turnoActivo = self._jugadores[0]
        
        # KnuckleBones siempre es KnuckleBones
        print(self._historial)
        return True
    
    def jugar_turno(self, usuario, dado, posicion, bot = False):
        index_activo = self.get_jugador_activo_index()
        index_oponente = self.get_oponente_index()
        inicia_el_bot = 0
        if bot:
            inicia_el_bot = generador_random(0, 1)
            
        if self.finalizo_juego():
            return self.determinar_ganador(self._mesa_de_juego)
        else:
            if inicia_el_bot == 0:
                
                if bot:
                    historial = self.knuckle_bot(dado, self._mesa_de_juego)
                    self._historial.append(historial)
                    posicion = historial['posicion']
                    self.poner_dado(self._mesa_de_juego[index_activo], posicion, dado)
                    self.__eliminar_dado(self._mesa_de_juego[index_oponente], posicion, dado)
                    self.cambiar_jugador_activo() 
                    self._turno += 1
            else:
                if bot:
                    historial = self.knuckle_bot(dado, self._mesa_de_juego)
                    self._historial.append(historial)
                    posicion = historial['posicion']
                    self.poner_dado(self._mesa_de_juego[index_activo], posicion, dado)
                    self.__eliminar_dado(self._mesa_de_juego[index_oponente], posicion, dado)
                    self.cambiar_jugador_activo() 
                    self._turno += 1
                self.poner_dado(self._mesa_de_juego[index_activo], posicion, dado)
                self.__eliminar_dado(self._mesa_de_juego[index_oponente], posicion, dado)
                self.cambiar_jugador_activo() 
                self._turno += 1
            
    def actualizar_instancia(self, data: dict):
        """
        Actualiza la instancia de KnuckleBones con los datos del diccionario
        Args:
            data (dict): Diccionario con los datos a actualizar
        """
        self._capacidad = data.get('capacidad', 2)
        self._capacidadMinima = data.get('capacidad_minima', 2)
        self._jugadores = data.get('jugadores', [])
        self._turnoActivo = data.get('turnoActivo', None)
        self._mesa_de_juego = self._listas_planas_a_mesa(data.get('mesa_jugador_0', [0] * 9), data.get('mesa_jugador_1', [0] * 9))
        self._cantidad_de_dados_puestos = data.get('cantidad_de_dados_puestos', [0, 0])
        self._turno = data.get('turno', 0)
        self._historial = data.get('historial_knucklebones', [])
        
    def _mesa_a_listas_planas(self, mesa_de_juego: list = None) -> dict:
        """
        Convierte la mesa de juego 3D a dos listas planas de 9 posiciones cada una
        Returns: dict con 'jugador_0' y 'jugador_1' como listas de 9 elementos
        """
        if mesa_de_juego is None:
            mesa_de_juego = self._mesa_de_juego
            
        jugador_0 = []
        jugador_1 = []
        
        # Convertir mesa del jugador 0 (fila por fila)
        for columna in range(3):
            for fila in range(3):
                jugador_0.append(mesa_de_juego[0][columna][fila])
                
        # Convertir mesa del jugador 1 (fila por fila)
        for columna in range(3):
            for fila in range(3):
                jugador_1.append(mesa_de_juego[1][columna][fila])
                
        return {
            'jugador_0': jugador_0,
            'jugador_1': jugador_1
        }

    def _listas_planas_a_mesa(self, jugador_0: list, jugador_1: list) -> list:
        """
        Convierte dos listas planas de 9 posiciones a la estructura 3D de la mesa
        Args:
            jugador_0: Lista de 9 elementos del jugador 0
            jugador_1: Lista de 9 elementos del jugador 1
        Returns: Mesa de juego en formato 3D [2][3][3]
        """
        if len(jugador_0) != 9 or len(jugador_1) != 9:
            raise ValueError("Cada lista debe tener exactamente 9 elementos")
            
        mesa = [
            [
                [0, 0, 0],
                [0, 0, 0], 
                [0, 0, 0]
            ],
            [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]
        ]
        
        # Reconstruir mesa del jugador 0
        index = 0
        for columna in range(3):
            for fila in range(3):
                mesa[0][columna][fila] = jugador_0[index]
                index += 1
                
        # Reconstruir mesa del jugador 1
        index = 0
        for columna in range(3):
            for fila in range(3):
                mesa[1][columna][fila] = jugador_1[index]
                index += 1
                
        return mesa

    def to_dict(self):
        # Obtener los atributos de la clase padre
        parent_dict = super().to_dict()
        
        # Convertir mesa de juego a formato plano
        mesa_plana = self._mesa_a_listas_planas()
        
        # Serializar el historial de KnuckleBones para evitar arrays anidados
        historial_serializado = []
        for entrada in self._historial:
            if isinstance(entrada, dict):
                # Convertir arrays anidados a strings o valores simples
                entrada_serializada = {}
                for key, value in entrada.items():
                    if isinstance(value, list):
                        # Convertir listas a strings para evitar arrays anidados
                        entrada_serializada[key] = str(value) if value else "[]"
                    else:
                        entrada_serializada[key] = value
                historial_serializado.append(entrada_serializada)
            else:
                historial_serializado.append(str(entrada))
        
        # Agregar los atributos específicos de KnuckleBones
        parent_dict.update({
            'mesa_jugador_0': mesa_plana['jugador_0'],
            'mesa_jugador_1': mesa_plana['jugador_1'],
            'cantidad_de_dados_puestos': self._cantidad_de_dados_puestos,
            'turno': self._turno,
            'historial_knucklebones': historial_serializado
        })
        
        return parent_dict

    @classmethod
    def from_dict(cls, data: dict):
        """
        Constructor simple de KnuckleBones desde diccionario
        """
        instance = cls()
        
        # Atributos de SalaDeJuego
        instance._id = data.get('id')
        instance._capacidad = data.get('capacidad', 2)
        instance._capacidadMinima = data.get('capacidad_minima', 2)
        instance._juego = data.get('juego', 'KnuckleBones')
        instance._jugadores = data.get('jugadores', [])
        instance._turnoActivo = data.get('turnoActivo')
        instance._SalaDeJuego__listaDeEspera = data.get('listaDeEspera', [])
        instance._apuestas = data.get('apuestas', [])
        instance._historial = data.get('historial', [])
        
        # Fecha de inicio
        from datetime import datetime
        fecha_str = data.get('fechaHoraInicio', datetime.now().isoformat())
        if isinstance(fecha_str, str):
            instance._fechaHoraInicio = datetime.fromisoformat(fecha_str)
        else:
            instance._fechaHoraInicio = fecha_str or datetime.now()
        
        # Usar conversor para reconstruir mesa
        mesa_0 = data.get('mesa_jugador_0', [0] * 9)
        mesa_1 = data.get('mesa_jugador_1', [0] * 9)
        instance._mesa_de_juego = instance._listas_planas_a_mesa(mesa_0, mesa_1)
        
        # Atributos específicos de KnuckleBones
        instance._cantidad_de_dados_puestos = data.get('cantidad_de_dados_puestos', [0, 0])
        instance._turno = data.get('turno', 0)
        
        return instance

    def __repr__(self) -> str:
        return (f"{super().__repr__()}"
                f"mesa_de_juego: {self._mesa_de_juego}\n")