from src.model.salaDeJuego.juego.juegosDeCartas.JuegoDeCartas import JuegoDeCartas
from src.model.usuario.Usuario import Usuario
import random


class BlackJack(JuegoDeCartas):
    _plantarse: bool = False
    _cartas: int = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,
            "J":10,"Q":10,"K":10,"A":11}
    _apuesta: int = 1
    
    
    
    def __init__(self, id: str, capacidad: int, capacidadMinima: int, valor_entrada_mesa: int ,_plantarse: bool, _apuesta: int):
        super().__init__(id, capacidad, capacidadMinima, valor_entrada_mesa)
        self._apuesta = _apuesta
        self._plantarse = _plantarse
    
        
    def pedir(self, jugador: Usuario):
        print("falta implementar pedir()")
        pass
    
    def plantarse(self, mano_jugador):

        plantarse = (input("¿Quieres pedir otra carta? (Si/No): "))
        plantarse = self.plantarse(plantarse)
    
        if plantarse.charAt(0) == "S" or plantarse.charAt(0) == "s":
            return print("El jugador se plantó.")
        elif plantarse.charAt(0) == "N" or plantarse.charAt(0) == "n":            
            mano_jugador.append(self.repartir_cartas())
    
    def calcular_puntos(self, mano_jugador, mano_crupier) -> int:

        #Calcula los puntos de la mano del jugador y del crupier.
        puntos_jugador = sum([BlackJack._cartas[carta] for carta in mano_jugador])
        puntos_crupier = sum([BlackJack._cartas[carta] for carta in mano_crupier])
        return puntos_jugador, puntos_crupier
    
    def doblar(self, jugador: Usuario):
        print("falta implementar doblear()")
        pass
    
    def separar(self, jugador: Usuario):
        print("falta implementar separar()")
        pass
    
    def retirarse(self, jugador: Usuario):
        print("falta implementar retirarse()")
        pass
    
    def repartir_cartas(self):
        #Reparte una carta al jugador o al crupier y devuelve el valor de la carta.
        return random.choice(list(BlackJack._cartas.keys()))

    def cartasIniciales(self):
        #Reparte dos cartas al jugador y devuelve el valor de las cartas.
        mano_jugador = [self.repartir_cartas(), self.repartir_cartas()]
        mano_crupier = [self.repartir_cartas(), self.repartir_cartas()]
        return mano_jugador, mano_crupier

    def mostrar_CartasYPuntos(self, mano_jugador, mano_crupier):
        #Muestra las cartas de la mano.
        print(f"Mano del jugador: {mano_jugador}")
        print(f"Mano del crupier: {mano_crupier}")
        #Muestra los puntos de el jugador y de crupier.
        puntos_jugador, puntos_crupier = self.calcular_puntos(mano_jugador, mano_crupier)
        print(f"Puntos del jugador: {puntos_jugador}")
        print(f"Puntos del crupier: {puntos_crupier}")

    def apostar(self, jugador: Usuario, monto: float):
        print("falta implementar apostar()")
        pass
    
    def inicializar_juego(self):
        """Inicializa el juego de BlackJack."""
        # Reparte las cartas iniciales al jugador y al crupier
        mano_jugador, mano_crupier = self.cartasIniciales()

        while self.calcular_puntos(mano_jugador) < 21:
            # Muestra las cartas y los puntos 
            self.mostrar_CartasYPuntos(mano_jugador, mano_crupier)
            # Pregunta al jugador si quiere pedir otra carta o plantarse
            self.plantarse(mano_jugador)
            # Muestra las cartas y los puntos 


    
    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f"cartas: {self._cartas}\n"
        )
    
if __name__ == "__main__":
    inicializar_juego = BlackJack("222222", 10, 5, 10, True, 1)
    print(inicializar_juego)