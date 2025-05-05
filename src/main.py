from src.model.salaDeJuego.juego.KnuckleBones import KnuckleBones
from src.model.salaDeJuego.juego.juegosDeCartas.BlackJack import BlackJack
from src.model.salaDeJuego.juego.juegosDeCartas.Mazo import Mazo
from src.model.salaDeJuego.juego.juegosDeCartas.Poker import Poker
from src.model.usuario.Usuario import Usuario
from src.model.usuario.UsuarioServicio import UsuarioServicio
from asyncio import run
import asyncio




async def main():
    usuario = Usuario.crear_usuario("xxxx", "xxxx", 1000)
    servicioUsuario = UsuarioServicio()
    print(usuario)
    await servicioUsuario.agregar_usuario(usuario)
    await usuario.aumentar_saldo(1000)
    # print(BlackJack("222222", 10, 5, 10))
    # print(Poker("222222", 10, 5, 10))
    # print(KnuckleBones("222222", 10, 5))
    # print(Mazo(52))
    
# async def test_usuario_servicio():

if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(test_usuario_servicio())