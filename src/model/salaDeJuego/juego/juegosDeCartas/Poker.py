from model.salaDeJuego.enums.Etapas import Etapas
from model.usuario.Usuario import Usuario
from model.salaDeJuego.juego.juegosDeCartas.JuegoDeCartas import JuegoDeCartas



class Poker(JuegoDeCartas):
    _dealer: Usuario
    _etapa: Etapas
    _all_in: bool
    _pozo: int
    
    def __init__(self, id: str, capacidad: int, capacidadMinima: int, valor_entrada_mesa: int):
        super().__init__(id, capacidad, capacidadMinima, valor_entrada_mesa)
        self.__dealer = None
        self.__etapa = Etapas.PRE_FLOP
        self.__all_in = False
        self.__pozo = 0

    def get_dealer(self):
        return self.__dealer

    def set_dealer(self, dealer: Usuario):  
        self.__dealer = dealer

    def get_etapa(self):
        return self.__etapa

    def set_etapa(self, etapa: Etapas):
        self.__etapa = etapa

    def get_all_in(self):
        return self.__all_in

    def set_all_in(self, all_in: bool):
        self.__all_in = all_in

    def get_pozo(self):
        return self.__pozo

    def set_pozo(self, pozo: int):
        self.__pozo = pozo
    
    def retirarse(self, usuario: Usuario):
        print("falta implementar retirarse()")
        pass
    
    def pasar(self, usuario: Usuario):
        print("falta implementar pasar()")
        pass
    
    def igualar(self, usuario: Usuario):
        print("falta implementar igualar()")
        pass
    
    def subir(self, usuario: Usuario, monto: float):
        print("falta implementar subir()")
        pass

    def repartir_cartas(self):
        print("falta implementar repartir_cartas()")
        pass
    
    def apostar(self, usuario: Usuario, monto: float):
        print("falta implementar apostar()")
        pass
    
    def inicializar_juego(self):
        print("falta implementar inicializar_juego()")
        pass
    
    # @override
    def __repr__(self) -> str:
        return (f"{super().__repr__()}"
                f"dealer: {self.__dealer}\n"
                f"etapa: {self.__etapa}\n"
                f"all_in: {self.__all_in}\n"
                f"pozo: {self.__pozo}\n")