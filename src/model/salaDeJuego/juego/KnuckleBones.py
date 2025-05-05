from operator import index
from turtle import position
from typing import Self
from src.model.salaDeJuego.SalaDeJuego import SalaDeJuego
from src.utils.Util import generador_random


class KnuckleBones(SalaDeJuego):
    _mesa_de_juego: list
    _cantidad_de_dados_puestos: list
    
    def __init__(self, id: str):
        super().__init__(id, 2, 2)
        self._mesa_de_juego = [[
                                [0, 0, 0], 
                                [0, 0, 0], 
                                [0, 0, 0]
                            ],[
                                [0, 0, 0], 
                                [0, 0, 0], 
                                [0, 0, 0]
                            ]]
        self._cantidad_de_dados_puestos = [0, 0]
        
    
    def get_mesa_de_juego(self) -> list:
        return self._mesa_de_juego
    
    def get_oponente_index(self):
        if self.get_jugador_activo_index() == 0:
            return 1
        else:
            return 0
    
    def __get_position(self, posicion: int, invetida: bool) -> int:
        posiciones = [[0, 1, 2],[2, 1, 0]]
        index = -1
        if invetida:
            index = self.get_oponente_index()
        else:
            index = self.get_jugador_activo_index()
            
        return posiciones[index][posicion]
    
    def poner_dado(self, posicion: int, valor: int) -> None:
        index_activo = self.get_jugador_activo_index()
        for i in range(3):
            if self._mesa_de_juego[index_activo][posicion][self.__get_position(i, False)] == 0:
                self._mesa_de_juego[index_activo][posicion][self.__get_position(i, False)] = valor
                self._cantidad_de_dados_puestos[index_activo] += 1
                break
        

    def __eliminar_dado(self, posicion: int, valor: int):
        index_activo = self.get_oponente_index()
        for i in range(3):
            if self._mesa_de_juego[index_activo][self.__get_position(posicion, True) if index_activo == 1 else self.__get_position(posicion, False)][self.__get_position(i, True)] == valor	:
                self._cantidad_de_dados_puestos[index_activo] -= 1
                self._mesa_de_juego[index_activo][self.__get_position(posicion, True) if index_activo == 1 else self.__get_position(posicion, False)][self.__get_position(i, True)] = 0
                    
    def determinar_ganador(self):
        print("falta implementar determinar_ganador()")
        pass
    
    def finalizo_juego(self) -> bool:
        if self._cantidad_de_dados_puestos[0] == 9 or self._cantidad_de_dados_puestos[1] == 9:
            return True
        else:
            return False
        
    def cambiar_jugador_activo(self) -> None:
        self.set_turnoActivo(self.get_jugadores()[self.get_oponente_index()])
        
    def lanzar_dado(self) -> int:
        return generador_random(1, 6)
    
    def juego(self)->None:
        if  self.finalizo_juego():
            self.determinar_ganador()
        else:
            dado = self.lanzar_dado()
            self.print_mesa()
            print(f'a el jugador {self.get_turnoActivo().get_id()} El dado salió en {dado}')
            posicion = int(input('Ingrese la posición donde desea poner el dado (1,2,3): '))-1
            self.poner_dado(posicion, dado)
            self.__eliminar_dado(posicion, dado)
            self.cambiar_jugador_activo()
            self.juego()
            
    def print_mesa(self):
        string = (
            f"        {self._jugadores[1].get_id()}\n"
            f" ╔═════╤═════╤═════╗\n"
            f" ║  {self._mesa_de_juego[1][2][0]}  │  {self._mesa_de_juego[1][1][0]}  │  {self._mesa_de_juego[1][0][0]}  ║\n"
            f" ╟─────┼─────┼─────╢         posiciones\n"
            f" ║  {self._mesa_de_juego[1][2][1]}  │  {self._mesa_de_juego[1][1][1]}  │  {self._mesa_de_juego[1][0][1]}  ║     ╔═════╤═════╤═════╗\n"
            f" ╟─────┼─────┼─────╢     ║     │     │     ║\n"
            f" ║  {self._mesa_de_juego[1][2][2]}  │  {self._mesa_de_juego[1][1][2]}  │  {self._mesa_de_juego[1][0][2]}  ║     ║     │     │     ║\n"
            f" ╠═════╪═════╪═════╣     ║  {self.__get_position(0,False)+1}  │  {self.__get_position(1,False)+1}  │  {self.__get_position(2,False)+1}  ║\n"
            f" ║  {self._mesa_de_juego[0][0][0]}  │  {self._mesa_de_juego[0][1][0]}  │  {self._mesa_de_juego[0][2][0]}  ║     ║     │     │     ║\n"
            f" ╟─────┼─────┼─────╢     ║     │     │     ║\n"
            f" ║  {self._mesa_de_juego[0][0][1]}  │  {self._mesa_de_juego[0][1][1]}  │  {self._mesa_de_juego[0][2][1]}  ║     ╚═════╧═════╧═════╝\n"
            f" ╟─────┼─────┼─────╢       Jugador Activo:\n"
            f" ║  {self._mesa_de_juego[0][0][2]}  │  {self._mesa_de_juego[0][1][2]}  │  {self._mesa_de_juego[0][2][2]}  ║           {self._turnoActivo.get_id()}\n"
            f" ╚═════╧═════╧═════╝\n"
            f"        {self._jugadores[0].get_id()}\n")
            
        print(string)
            
        
    
    def inicializar_juego(self, juego):
        """
        Implementación del método abstracto de SalaDeJuego
        """
        print("falta implementar iniciar_juego()")
        pass
        
    def __repr__(self) -> str:
        return (f"{super().__repr__()}"
                f"mesa_de_juego: {self._mesa_de_juego}\n")