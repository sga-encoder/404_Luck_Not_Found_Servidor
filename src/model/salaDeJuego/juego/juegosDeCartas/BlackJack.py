from src.model.salaDeJuego.juego.juegosDeCartas import JuegoDeCartas
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
    
    def plantarse(self, plantarse: str) -> bool: 
        if plantarse.charAt(0) == "S" or plantarse.charAt(0) == "s":
            self._plantarse = True
            return self._plantarse
        elif plantarse.charAt(0) == "N" or plantarse.charAt(0) == "n":            
            self._plantarse = False
            return self._plantarse
    
    def doblar(self, jugador: Usuario):
        print("falta implementar doblear()")
        pass
    
    def separar(self, jugador: Usuario):
        print("falta implementar separar()")
        pass
    
    def seguro(self, jugador: Usuario, monto: float):
        print("falta implementar seguro()")
        pass
    
    def retirarse(self, jugador: Usuario):
        print("falta implementar retirarse()")
        pass
    
    def repartir_cartas(self):
        """Reparte una carta al jugador o al crupier y devuelve el valor de la carta."""
        return random.choice(list(BlackJack._cartas.keys()))

    def cartasIniciales(self):
        """Reparte dos cartas al jugador y devuelve el valor de las cartas."""
        mano_jugador = [self.repartir_cartas(), self.repartir_cartas()]
        mano_crupier = [self.repartir_cartas(), self.repartir_cartas()]
        return mano_jugador, mano_crupier

    def apostar(self, jugador: Usuario, monto: float):
        print("falta implementar apostar()")
        pass
    
    def inicializar_juego(self):
        """Inicializa el juego de BlackJack."""
        mano_jugador, mano_crupier = self.cartasIniciales()

        print(f"Mano del jugador: {mano_jugador}")
        print(f"Mano del crupier: {mano_crupier}")
        plantarse = (input("¿Quieres seguro? (Si/No): "))
        plantarse = self.plantarse(plantarse)

        if plantarse:
            mano_jugador.append(self.repartir_carta())
        else:
            print("El jugador se planta.")
        
    
    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f"seguro: {self.__seguro}\n"
        )
    
if __name__ == "__main__":
    inicializar_juego = BlackJack("222222", 10, 5, 10, True, 1)