from src.model.salaDeJuego.juego.KnuckleBones import KnuckleBones
from src.model.salaDeJuego.juego.juegosDeCartas.BlackJack import BlackJack
from src.model.salaDeJuego.juego.juegosDeCartas.Mazo import Mazo
from src.model.salaDeJuego.juego.juegosDeCartas.Poker import Poker
from src.model.usuario.Usuario import Usuario

# ... existing code ...



def main():
    print(Usuario("Juan", "Garzon", 500, 0))
    print(BlackJack("222222", 10, 5, 10))
    print(Poker("222222", 10, 5, 10))
    print(KnuckleBones("222222", 10, 5))
    # print(Mazo(52))

if __name__ == "__main__":
    main()