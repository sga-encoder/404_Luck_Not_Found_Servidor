import asyncio
import uuid
from .SalaDeJuego import SalaDeJuego
from datetime import datetime
from ..usuario import Usuario
from ...utils.firestore import add_data, add_data_with_id, array_remove, array_union, delete_data, get_data, update_data, get_collection_data, add_realtime_listener, add_collection_listener

class SalaDeJuegoServicio:
    """
    Servicio para gestionar operaciones CRUD sobre salas de juego en Firestore.
    """

    async def crear_sala_de_juego(self, sala: SalaDeJuego) -> None:
        """
        Crea una nueva sala de juego en la colección 'salas_de_juego' en Firestore.
        Args:
            sala (SalaDeJuego): Instancia de SalaDeJuego con los datos de la sala a agregar.
        """
        sala_id = await add_data('salas_de_juego_activas', sala.__dict__)
        print(f'Sala de juego agregada con ID: {sala_id}')
        

    async def eliminar_sala_de_juego(self, id: str) -> None:
        """
        Elimina una sala de juego de la colección 'salas_de_juego' en Firestore.
        Args:
            id (str): ID de la sala a eliminar.
        """
        sala_id = await delete_data('salas_de_juego', id)
        print(f'Sala de juego eliminada con ID: {sala_id}')

    async def actualizar_sala_de_juego(self, id: str, sala_de_juego_dict: dict) -> None:
        """
        Actualiza los datos de una sala de juego en la colección 'salas_de_juego' en Firestore.
        Args:
            id (str): ID de la sala a actualizar.
            sala_de_juego_dict (dict): Diccionario con los datos a actualizar.
        """
        sala_id = await update_data('salas_de_juego', id, sala_de_juego_dict)
        print(f'Sala de juego actualizada con ID: {sala_id}')
    async def agregar_jugador_a_lista_de_espera(self, id: str, usuario: Usuario):
        """
        Agrega un usuario a la lista de espera de una sala de juego.
        Args:
            id (str): ID de la sala de juego.
            usuario (Usuario): Instancia del usuario que se agrega a la lista de espera.
        """
        sala_id = await update_data('salas_de_juego_activas', id, {'listaDeEspera': array_union([usuario.get_id()])})
        print(f'Usuario {usuario.get_id()} agregado a la lista de espera de la sala de juego con ID: {sala_id}')
        
    async def eliminar_jugador_de_lista_de_espera(self, id: str, usuario: Usuario):
        """
        Elimina un usuario de la lista de espera de una sala de juego.
        Args:
            id (str): ID de la sala de juego.
            usuario (Usuario): Instancia del usuario que se elimina de la lista de espera.
        """
        sala_id = await update_data('salas_de_juego_activas', id, {'listaDeEspera': array_remove([usuario.get_id()])})
        print(f'Usuario {usuario.get_id()} eliminado de la lista de espera de la sala de juego con ID: {sala_id}')
        
    async def entrar_sala_de_juego(self, id: str, usuario: Usuario):
        """
        Permite que un usuario entre a una sala de juego.
        Args:
            id (str): ID de la sala de juego.
            usuario (Usuario): Instancia del usuario que entra a la sala.
        """
        sala_id = await update_data('salas_de_juego_activas', id, {'jugadores': array_union([usuario.get_id()])})
        print(f'Usuario {usuario.get_id()} agregado a la sala de juego con ID: {sala_id}')
    
    async def salir_sala_de_juego(self, id: str, usuario: Usuario):
        """
        Permite que un usuario salga de una sala de juego.
        Args:
            id (str): ID de la sala de juego.
            usuario (Usuario): Instancia del usuario que sale de la sala.
        """
        sala_id = await update_data('salas_de_juego_activas', id, {'jugadores': array_remove([usuario.get_id()])})
        print(f'Usuario {usuario.get_id()} eliminado de la sala de juego con ID: {sala_id}')
    async def agregar_en_historial_sala_de_juego(self, id: str, historial: list) -> None:
        """
        Agrega un nuevo registro al historial de una sala de juego en la colección 'salas_de_juego' en Firestore.
        Args:
            id (str): ID de la sala a actualizar.
            historial (list): Lista con el nuevo historial a agregar.
        """
        sala_id = await update_data('salas_de_juego_activas', id, {'historial': array_union([historial])})
        print(f'Historial de sala de juego actualizado con ID: {sala_id}')
        
    async def guardar_registro_sala_de_juego(self, id: str, registro: dict) -> str:
        sala_id = await add_data_with_id('salas_de_juego', registro, id)
        print(f'Sala de juego guardada con ID: {sala_id}')
        return sala_id

    async def obtener_sala_de_juegos_activa(self, id: str) -> SalaDeJuego:
        """
        Obtiene una sala de juego de la colección 'salas_de_juego' en Firestore.
        Args:
            id (str): ID de la sala a obtener.
        Returns:
            SalaDeJuego: Instancia de SalaDeJuego con los datos obtenidos.
        """
        sala_dict = await get_data('salas_de_juego_activas', id)
        # Aquí deberías tener un método from_dict en SalaDeJuego para reconstruir la instancia
        # return SalaDeJuego.from_dict(sala_dict)
        return sala_dict
    
    async def obtener_collection_salas_de_juego(self) -> list:
        """
        Obtiene todas las salas de juego activas de la colección 'salas_de_juego_activas' en Firestore.
        Returns:
            list: Lista de diccionarios con los datos de las salas de juego activas.
        """
        return await get_collection_data('salas_de_juego_activas')

    async def crear_sala_de_juego_activa(self, sala_data: dict) -> str:
        """
        Crea una nueva sala de juego activa con ID aleatorio en Firestore.
        Args:
            tipo_juego (str): Tipo de juego (BlackJack, Poker, etc.)
            jugadores (list): Lista opcional de jugadores iniciales
        Returns:
            str: ID de la sala creada
        """
        
        sala_id = await add_data('salas_de_juego_activas', sala_data)
        print(f'Sala de juego activa creada con ID: {sala_id}')
        return sala_id

    async def actualizar_manos_blackjack(self, sala_id: str, manos_jugadores: dict, mano_crupier: list):
        """
        Actualiza las manos de los jugadores y del crupier en una sala de BlackJack.
        """
        await update_data('salas_de_juego_activas', sala_id, {
            'manos_jugadores': manos_jugadores,
            'mano_crupier': mano_crupier
        })

    async def agregar_jugador_a_sala_activa(self, sala_id: str, jugador_id: str):
        """
        Agrega un jugador a una sala activa.
        """
        await update_data('salas_de_juego_activas', sala_id, {
            'jugadores': array_union([jugador_id])
        })

    def iniciar_listener_sala_especifica(self, sala_id: str, callback, error_callback=None):
        """
        Inicia un listener en tiempo real para una sala específica.
        
        Args:
            sala_id (str): ID de la sala a escuchar
            callback (Callable): Función que se ejecuta cuando hay cambios
            error_callback (Callable, optional): Función que se ejecuta en caso de error
            
        Returns:
            function: Función para detener el listener
        """
        return add_realtime_listener('salas_de_juego_activas', sala_id, callback, error_callback)
    
    def iniciar_listener_salas_activas(self, callback, filtros=None, error_callback=None):
        """
        Inicia un listener en tiempo real para todas las salas activas.
        
        Args:
            callback (Callable): Función que se ejecuta cuando hay cambios
            filtros (dict, optional): Filtros para la consulta (ej: {'tipo_juego': 'BlackJack'})
            error_callback (Callable, optional): Función que se ejecuta en caso de error
            
        Returns:
            function: Función para detener el listener
        """
        return add_collection_listener('salas_de_juego_activas', callback, filtros, error_callback)

    async def obtener_sala_activa(self, sala_id: str):
        """
        Obtiene los datos de una sala activa.
        """
        return await get_data('salas_de_juego_activas', sala_id)