import asyncio
from .SalaDeJuego import SalaDeJuego
from ..usuario import Usuario
from ...utils.firestore import add_data, add_data_with_id, array_remove, array_union, delete_data, get_data, update_data, get_collection_data

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

    async def obtener_sala_de_juego(self, id: str) -> SalaDeJuego:
        """
        Obtiene una sala de juego de la colección 'salas_de_juego' en Firestore.
        Args:
            id (str): ID de la sala a obtener.
        Returns:
            SalaDeJuego: Instancia de SalaDeJuego con los datos obtenidos.
        """
        sala_dict = await get_data('salas_de_juego', id)
        # Aquí deberías tener un método from_dict en SalaDeJuego para reconstruir la instancia
        # return SalaDeJuego.from_dict(sala_dict)
        return sala_dict