from src.model.salaDeJuego.juego.KnuckleBones import KnuckleBones
from src.model.salaDeJuego.juego.juegosDeCartas.BlackJack import BlackJack
from src.model.salaDeJuego.juego.juegosDeCartas.Mazo import Mazo
from src.model.salaDeJuego.juego.juegosDeCartas.Poker import Poker
from src.model.usuario.Usuario import Usuario
from src.model.usuario.UsuarioServicio import UsuarioServicio
from asyncio import run
import asyncio




# async def main():
    # usuario = Usuario.crear_usuario("xxxx", "xxxx", 1000)
    # servicioUsuario = UsuarioServicio()
    # print(usuario)
    # await servicioUsuario.agregar_usuario(usuario)
    # await usuario.aumentar_saldo(1000)
    # print(BlackJack("222222", 10, 5, 10))
    # print(Poker("222222", 10, 5, 10))
    # print(KnuckleBones("222222", 10, 5))
    # print(Mazo(52))
    
# async def test_usuario_servicio():
def main():
    knuckle = KnuckleBones("111111")
    
    usuario1 = Usuario.crear_usuario("Sebastian", "Garzon Arias", 1000)
    usuario2 = Usuario.crear_usuario("Juan", "Perez", 1000)
    
    knuckle.set_jugadores([usuario1, usuario2])
    knuckle.set_turnoActivo(usuario1)
    knuckle.set_apuestas([100, 100])
    knuckle.juego()
    
    
if __name__ == "__main__":
    main()
    # asyncio.run(main())
    # asyncio.run(test_usuario_servicio())