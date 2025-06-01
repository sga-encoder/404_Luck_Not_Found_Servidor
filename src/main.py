import os
import sys

# Imprime la ruta actual para depuración

# Añadir el directorio raíz del proyecto al path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imprimir sys.path para ver dónde está buscando Python
# print(f"Python está buscando en estas rutas: {sys.path}")

try:
    from src.model.salaDeJuego.juego.KnuckleBones import KnuckleBones
    from src.model.salaDeJuego.juego.juegosDeCartas.BlackJack import BlackJack
    from src.model.salaDeJuego.juego.juegosDeCartas.Mazo import Mazo
    from src.model.salaDeJuego.juego.juegosDeCartas.Poker import Poker
    from src.model.usuario.Usuario import Usuario
    from src.model.usuario.UsuarioServicio import UsuarioServicio
except ImportError as e:
    print(f"Error importando módulos: {e}")
    sys.exit(1)

from asyncio import run
import asyncio

def main():
    usuario1 = Usuario.crear_usuario("Sebastian", "Garzon", 1000)
    usuario2 = Usuario.crear_usuario("Juan", "Perez", 1000)
    
    mesa = [[3, 3, 3], [2, 1, 0], [3, 1, 3]]
    
    blackjack=BlackJack("Miguel",7,2,100,False,10)
    blackjack.inicializar_juego()

"""knuckle = KnuckleBones("11")
    knuckle.set_jugadores([usuario1, usuario2])
    # knuckle.knuckle_bot(6, knuckle.get_mesa_de_juego())
    # print(knuckle.sumar_puntos(mesa))
    knuckle.inicializar_juego('KnuckleBones')
    # print(knuckle.columna_paralela([6, 3, 0], 3))"""
    

    
if __name__ == "__main__":
    main()