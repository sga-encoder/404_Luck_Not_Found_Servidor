import asyncio
from src.model.usuario.Usuario import Usuario
from src.utils.firestore import add_data_with_id, delete_data, get_data, update_data, get_collection_data

class UsuarioServicio:
    """
    Servicio para gestionar operaciones CRUD sobre usuarios en Firestore.
    """

    async def agregar_usuario(self, usuario_dict: dict) -> None:
        """
        Agrega un nuevo usuario a la colección 'usuarios' en Firestore.

        Args:
            usuario_dict (dict): Diccionario con los datos del usuario a agregar.

        Raises:
            ValueError: Si el ID del usuario es vacío.
        """
        usuario = self.datos_correctos(usuario_dict)
        usuario_id = usuario.get_id()
        
        if not usuario_id:
            raise ValueError("El ID del usuario no puede estar vacío")
        
        usuario_id = await add_data_with_id('usuarios', usuario.to_dict(), usuario_id)
        print(f'Usuario agregado con ID: {usuario_id}')

    async def eliminar_usuario(self, id: str) -> None:
        """
        Elimina un usuario de la colección 'usuarios' en Firestore.

        Args:
            id (str): ID del usuario a eliminar.
        """
        usuario_id = await delete_data('usuarios', id)
        print(f'Usuario eliminado con ID: {usuario_id}')

    async def actualizar_usuario(self, id: str, usuario_dict: dict) -> None:
        """
        Actualiza los datos de un usuario en la colección 'usuarios' en Firestore.

        Args:
            id (str): ID del usuario a actualizar.
            usuario_dict (dict): Diccionario con los datos a actualizar.

        Raises:
            ValueError: Si se intenta actualizar el ID, saldo, total_apostado o historial del usuario.
        """
        if not "id" in usuario_dict and not "saldo" in usuario_dict and not "total_apostado" in usuario_dict and not "historial" in usuario_dict:
            usuario_id = await update_data('usuarios', id, usuario_dict)
            print(f'Usuario actualizado con ID: {usuario_id}')
        else:
            raise ValueError("No se puede actualizar el ID, saldo, total_apostado o historial del usuario")

    async def obtener_usuario(self, id: str) -> Usuario:
        """
        Obtiene un usuario de la colección 'usuarios' en Firestore.

        Args:
            id (str): ID del usuario a obtener.

        Returns:
            Usuario: Instancia de Usuario con los datos obtenidos.
        """
        usuario_dict = await get_data('usuarios', id)
        usuario = Usuario.from_dict(usuario_dict)
        return usuario

    @staticmethod
    async def obtener_todos_usuarios() -> list[Usuario]:
        """
        Obtiene todos los usuarios de la colección 'usuarios' en Firestore.

        Returns:
            list[Usuario]: Lista de instancias de Usuario.
        """
        usuarios_dict = await get_collection_data('usuarios')
        usuarios = [Usuario.from_dict(usuario_dict) for usuario_dict in usuarios_dict]
        return usuarios
    
    def datos_correctos(self, usuario_dict: dict) -> Usuario:
        """
        Verifica y crea una instancia de Usuario a partir de un diccionario de datos.

        Args:
            usuario_dict (dict): Diccionario con los datos del usuario.

        Returns:
            Usuario: Instancia de Usuario creada.

        Raises:
            ValueError: Si los datos del usuario son incorrectos.
        """
        if "nombre" in usuario_dict and "apellido" in usuario_dict and "saldo" in usuario_dict:
            nombre, apellido, saldo = str(usuario_dict["nombre"]), str(usuario_dict["apellido"]), float(usuario_dict["saldo"])
            usuario = Usuario.crear_usuario(nombre, apellido, saldo)
            return usuario
        else:
            return ValueError("Los datos del usuario son incorrectos")


