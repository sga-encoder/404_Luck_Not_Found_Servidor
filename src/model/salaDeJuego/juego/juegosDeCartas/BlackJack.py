from src.model.salaDeJuego.juego.juegosDeCartas.JuegoDeCartas import JuegoDeCartas
from src.model.usuario.Usuario import Usuario
import random


class BlackJack(JuegoDeCartas):
    _plantarse: bool = False
    _cartas: dict[str,int] = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,
            "J":10,"Q":10,"K":10,"A":11}
    _apuesta: int = 1
    
    
    
    def __init__(self, id: str, capacidad: int, capacidadMinima: int, valor_entrada_mesa: int ,_plantarse: bool, _apuesta: int):
        super().__init__(id, capacidad, capacidadMinima, valor_entrada_mesa)
        self._apuesta = _apuesta
        self._plantarse = _plantarse
    
        
    def pedir(self, jugador: Usuario):
        print("falta implementar pedir()")
        pass
    
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

        #Calcula los puntos de la mano dada
        puntos=sum(BlackJack._cartas[carta] for carta in mano)
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
        #Reparte una carta al jugador o al crupier y devuelve el valor de la carta.
        return random.choice(list(BlackJack._cartas.keys()))
        

    def cartasIniciales(self):
        #Reparte dos cartas al jugador y devuelve el valor de las cartas.
        mano_inicial = [self.repartir_cartas(), self.repartir_cartas()]
        
        return mano_inicial

    def mostrar_CartasYPuntos(self, mano_jugador, mano_crupier):
        #Muestra las cartas de la mano.
        print(f"Mano del jugador: {mano_jugador}  || Puntos: {self.calcular_puntos(mano_jugador)}")
        print(f"Mano visible del crupier: {mano_crupier[0]}")
        #Muestra los puntos de el jugador y de crupier.

    def apostar(self, jugador: Usuario, monto: float):
        print("falta implementar apostar()")
        pass
    
    def inicializar_juego(self):
        """Inicializa el juego de BlackJack."""
        # Reparte las cartas iniciales al jugador y al crupier
        mano_jugador = self.cartasIniciales()
        mano_crupier = self.cartasIniciales()
        puntos =0

        while  puntos < 21 :
            puntos=self.calcular_puntos(mano_jugador)
            # Muestra las cartas y los puntos 
            self.mostrar_CartasYPuntos(mano_jugador, mano_crupier)
            # Pregunta al jugador si quiere pedir otra carta o plantarse
            plantarse = str(input("¿Quieres plantarte? (S/N): ").lower())
            # Si el jugador quiere pedir otra carta, se le reparte una nueva carta
            if plantarse == "n":
                mano_jugador.append(self.repartir_cartas())
            elif plantarse == "s":
                self._plantarse = True
                break
        # Si el jugador se planta, es hora de jugar al crupier
        puntos=self.calcular_puntos(mano_crupier)
        if puntos < 17:
            # El crupier pide cartas hasta que tenga al menos 17 puntos
            while puntos < 17:
                mano_crupier.append(self.repartir_cartas())
                puntos = self.calcular_puntos(mano_crupier)
            #Si el crupier tiene mas de 17 puntos muestra las cartas y los puntos del crupier
            if puntos >  17:
                print(f"Mano del crupier: {mano_crupier}  || Puntos: {puntos}")
        # Determina el ganador
        self.ganador(mano_jugador, mano_crupier)    


    
    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f"cartas: {self._cartas}\n"
        )
    
if __name__ == "__main__":
    inicializar_juego = BlackJack("222222", 10, 5, 10, True, 1)
    print(inicializar_juego)