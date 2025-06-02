import random
from typing import override


class Mazo:
    _tamanoDeMazo: int
    _mazo: list
    _cartas_originales: list
    
    def __init__(self, tamanoDeMazo: int):
        self.__tamanoDeMazo = tamanoDeMazo
        self.__mazo = []
        self._cartas_originales = self._generar_cartas_estandar()
        self.crear_mazo()

    def _generar_cartas_estandar(self):
        palos = ['♠', '♥', '♦', '♣']
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [f"{valor}{palo}" for palo in palos for valor in valores]

    def get_tamanoDeMazo(self) -> int:
        return self.__tamanoDeMazo

    def set_tamanoDeMazo(self, tamanoDeMazo: int):
        self.__tamanoDeMazo = tamanoDeMazo

    def get_mazo(self) -> list:
        return self.__mazo

    def set_mazo(self, mazo: list):
        self.__mazo = mazo
    
    def baragear(self):
        random.shuffle(self.__mazo)

    def sacar_carta(self):
        if not self.__mazo:
            print("El mazo está vacío, recreando y barajando...")
            self.crear_mazo()
            self.baragear()
        return self.__mazo.pop() if self.__mazo else None

    def ingresar_carta(self, carta):
        self.__mazo.append(carta)

    def crear_mazo(self):
        self.__mazo = self._cartas_originales.copy()
        self.baragear()

    @override
    def __repr__(self) -> str:
        return (
            f"tamanoDeMazo: {self.__tamanoDeMazo}\n"
            f"mazo: {self.__mazo}"
        )