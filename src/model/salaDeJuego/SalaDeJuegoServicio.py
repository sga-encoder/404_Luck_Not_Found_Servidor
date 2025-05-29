import asyncio
from src.model.salaDeJuego.SalaDeJuego import SalaDeJuego
from src.utils.firestore import add_data_with_id, delete_data, get_data, update_data, get_collection_data

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
        sala_id = sala.get_id()
        if not sala_id:
            raise ValueError("El ID de la sala no puede estar vacío")
        await add_data_with_id('salas_de_juego', sala.__dict__, sala_id)
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