from src.model.salaDeJuego.juego.juegosDeCartas.JuegoDeCartas import JuegoDeCartas
from src.model.usuario.Usuario import Usuario


class BlackJack(JuegoDeCartas):
    _seguro: bool
    
    def __init__(self, id: str, capacidad: int, capacidadMinima: int, valor_entrada_mesa: int):
        super().__init__(id, capacidad, capacidadMinima, valor_entrada_mesa)
        self.__seguro = False
    
    def get_seguro(self):
        return self.__seguro

    def set_seguro(self, seguro: bool):
        self.__seguro = seguro
        
    def pedir(self, jugador: Usuario):
        print("falta implementar pedir()")
        pass
    
    def plantarse(self, jugador: Usuario):
        print("falta implementar plantarse()")
        pass
    
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
        print("falta implementar repartir_cartas()")
        pass
    
    def apostar(self, jugador: Usuario, monto: float):
        print("falta implementar apostar()")
        pass
    
    def inicializar_juego(self):
        print("falta implementar inicializar_juego()")
        pass
    
    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f"seguro: {self.__seguro}\n"
        )