from src.model.salaDeJuego.juego.KnuckleBones import KnuckleBones
from src.model.salaDeJuego.juego.juegosDeCartas.BlackJack import BlackJack
from src.model.salaDeJuego.juego.juegosDeCartas.Mazo import Mazo
from src.model.salaDeJuego.juego.juegosDeCartas.Poker import Poker
from src.model.usuario.Usuario import Usuario
from src.model.usuario.UsuarioServicio import UsuarioServicio
from asyncio import run
import asyncio




def main():
    print(Usuario.crear_usuario("xxxx", "xxxx", 1000))
    print(BlackJack("222222", 10, 5, 10))
    print(Poker("222222", 10, 5, 10))
    print(KnuckleBones("222222", 10, 5))
    # print(Mazo(52))
    
async def test_usuario_servicio():
    servicioUsuario = UsuarioServicio()
    await servicioUsuario.agregar_usuario({"nombre": "xxxx", "apellido": "xxxx", "saldo": 1000})

if __name__ == "__main__":
    main()
    asyncio.run(test_usuario_servicio())