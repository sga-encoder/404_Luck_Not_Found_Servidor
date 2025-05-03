import asyncio
from src.model.usuario.Usuario import Usuario
from src.utils.firestore import add_data

class UsuarioServicio:

    async def agregar_usuario(self, usuario_dict: dict) -> None:
        
        usuario = self.datos_correctos(usuario_dict)
        usuario_id = await add_data('usuarios', usuario.to_dict(), usuario.get_id())
        print(f'Usuario agregado con ID: {usuario_id}')

    async def eliminar_usuario(self, id: str) -> None:
        print("falta implementar eliminar_usuario")
        pass

    async def actualizar_usuario(self, id: str, usuario_dict: dict) -> None:
        print("falta implementar actualizar_usuario")
        pass

    async def obtener_usuario(self, id: str) -> None:
        print("falta implementar obtener_usuario")
        pass
    
    def datos_correctos(self, usuario_dict: dict) -> Usuario:
        if "nombre" in usuario_dict and "apellido" in usuario_dict and "saldo" in usuario_dict:
            usuario = Usuario(usuario_dict["nombre"], usuario_dict["apellido"], usuario_dict["saldo"])
            return usuario
        else:
            return ValueError("Los datos del usuario son incorrectos")

# Ejemplo de uso
async def main():
    servicio = UsuarioServicio()
    await servicio.agregar_usuario({'nombre': 'Juan', 'apellido': 'Pérez', 'saldo': 1000})

if __name__ == "__main__":
    asyncio.run(main())

