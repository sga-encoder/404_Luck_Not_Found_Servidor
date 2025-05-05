from typing import override


class Mazo:
    _tamanoDeMazo: int
    _mazo: list
    
    def __init__(self, tamanoDeMazo: int):
        self.__tamanoDeMazo = tamanoDeMazo
        self.__mazo = []

    def get_tamanoDeMazo(self) -> int:
        return self.__tamanoDeMazo

    def set_tamanoDeMazo(self, tamanoDeMazo: int):
        self.__tamanoDeMazo = tamanoDeMazo

    def get_mazo(self) -> list:
        return self.__mazo

    def set_mazo(self, mazo: list):
        self.__mazo = mazo
    
    def baragear(self):
        print("falta implementar barajar()")
        pass
    
    def sacar_carta(self):
        print("falta implementar sacar_carta()")
        pass
    
    def ingresar_carta(self):
        print("falta implementar ingresar_carta()")
        pass
    
    def crear_mazo(self):
        print("falta implementar crear_mazo()")
        pass
    
    @override
    def __repr__(self) -> str:
        return (
            f"tamanoDeMazo: {self.__tamanoDeMazo}\n"
            f"mazo: {self.__mazo}"
        )