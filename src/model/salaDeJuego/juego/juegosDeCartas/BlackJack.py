from .JuegoDeCartas import JuegoDeCartas
from ....usuario.Usuario import Usuario
import random


class BlackJack(JuegoDeCartas):
    _plantarse: bool = False
    _cartas: dict[str,int] = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,
            "J":10,"Q":10,"K":10,"A":11}
    _apuesta: int = 1

    def __init__(self, jugador: str, capacidad: int, capacidadMinima: int, valor_entrada_mesa: int ,_plantarse: bool, _apuesta: int):
        super().__init__(jugador, capacidad, capacidadMinima, valor_entrada_mesa)
        self._apuesta = _apuesta
        self._plantarse = _plantarse

    def ganador(self, mano_jugador, mano_crupier):
        puntos_jugador = self.calcular_puntos(mano_jugador)
        puntos_crupier = self.calcular_puntos(mano_crupier)
        if puntos_jugador > 21:
            print("El jugador ha perdido, se ha pasado de 21 puntos.")
            print(f"Mano del crupier: {mano_crupier}  || Puntos: {puntos_crupier}")
        elif puntos_crupier > 21:
            print("El crupier ha perdido, se ha pasado de 21 puntos.")
        elif puntos_jugador > puntos_crupier:
            print("El jugador ha ganado.")
            print(f"Mano del crupier: {mano_crupier}  || Puntos: {puntos_crupier}")
        elif puntos_jugador < puntos_crupier or puntos_crupier == 21:
            print("El crupier ha ganado.")
            print(f"Mano del crupier: {mano_crupier}  || Puntos: {puntos_crupier}")

    def calcular_puntos(self, mano) -> int:
        # Calcula los puntos de la mano dada
        puntos = sum(BlackJack._cartas[carta] for carta in mano)
        # Si hay un As y los puntos son mayores a 21, resta 10 puntos
        if 'A' in mano and puntos > 21:
            puntos -= 10
        return puntos

    def doblar(self, jugador: Usuario):
        print("falta implementar doblear()")
        pass

    def separar(self, jugador: Usuario):
        print("falta implementar separar()")
        pass

    def retirarse(self, jugador: Usuario):
        print("falta implementar retirarse()")
        pass

    def repartir_cartas(self) -> str:
        # Reparte una carta al jugador o al crupier y devuelve el valor de la carta.
        return random.choice(list(BlackJack._cartas.keys()))

    def cartasIniciales(self):
        # Reparte dos cartas al jugador y devuelve el valor de las cartas.
        mano_inicial = [self.repartir_cartas(), self.repartir_cartas()]
        return mano_inicial

    def mostrar_CartasYPuntos(self, mano_jugador, mano_crupier):
        # Muestra las cartas de la mano.
        print(f"Mano del jugador: {mano_jugador}  || Puntos: {self.calcular_puntos(mano_jugador)}")
        print(f"Mano visible del crupier: {mano_crupier[0]}")
        # Muestra los puntos de el jugador y de crupier.

    def apostar(self, jugador: Usuario, monto: float):
        print("falta implementar apostar()")
        pass

    def inicializar_juego(self):
        """Inicializa el juego de BlackJack para 4 jugadores más el crupier."""
        # Crear 7 jugadores
        jugadores = [Usuario.crear_usuario_local(f"Jugador {i+1}", f"Apellido {i+1}") for i in range(4)]
        manos_jugadores = [self.cartasIniciales() for _ in range(4)]
        mano_crupier = self.cartasIniciales()
        plantados = [False] * 4

        for i, mano in enumerate(manos_jugadores):
            while not plantados[i]:
                print(f"\nTurno de {jugadores[i]._nombre}:")
                self.mostrar_CartasYPuntos(mano, mano_crupier)
                puntos = self.calcular_puntos(mano)
                if puntos >= 21:
                    plantados[i] = True
                    break
                plantarse = str(input(f"{jugadores[i]._nombre}, ¿Quieres plantarte? (S/N): ").lower())
                if plantarse == "n":
                    mano.append(self.repartir_cartas())
                elif plantarse == "s":
                    plantados[i] = True

        # Turno del crupier
        puntos_crupier = self.calcular_puntos(mano_crupier)
        while puntos_crupier < 17:
            mano_crupier.append(self.repartir_cartas())
            puntos_crupier = self.calcular_puntos(mano_crupier)
        print(f"\nMano final del crupier: {mano_crupier}  || Puntos: {puntos_crupier}")

        # Determinar ganadores
        for i, mano in enumerate(manos_jugadores):
            print(f"\nResultado para {jugadores[i]._nombre}:")
            self.ganador(mano, mano_crupier)

    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f"cartas: {self._cartas}\n"
        )

if __name__ == "__main__":
    inicializar_juego = BlackJack("222222", 10, 5, 10, True, 1)
    inicializar_juego.inicializar_juego()
