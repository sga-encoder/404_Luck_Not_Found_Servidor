from src.model.salaDeJuego.SalaDeJuego import SalaDeJuego


class KnuckleBones(SalaDeJuego):
    _mesa_de_juego: list
    
    def __init__(self, id: str, capacidad: int, capacidadMinima: int):
        super().__init__(id, capacidad, capacidadMinima)
        self.__mesa_de_juego = []
    
    def get_mesa_de_juego(self) -> list:
        return self.__mesa_de_juego
    
    def set_mesa_de_juego(self, mesa_de_juego: list):
        self.__mesa_de_juego = mesa_de_juego
        
    def poner_dado(self, posicion_x: int, posicion_y: int, valor: int):
        print("falta implementar poner_dado()")
        pass

    def eliminar_dado(self, posicion_x: int, posicion_y: int):
        print("falta implementar eliminar_dado()")
        pass
    
    def determinar_ganador(self):
        print("falta implementar determinar_ganador()")
        pass
    
    def inicializar_juego(self, juego):
        """
        Implementación del método abstracto de SalaDeJuego
        """
        print("falta implementar iniciar_juego()")
        pass
        
    def __repr__(self) -> str:
        return (f"{super().__repr__()}"
                f"mesa_de_juego: {self.__mesa_de_juego}\n")