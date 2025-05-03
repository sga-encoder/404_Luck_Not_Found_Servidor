"""
Módulo que define la clase Usuario del Casino
"""

from ...utils.Utils import generador_random


class Usuario:
    """
    Clase que representa un usuario del casino

    Attributes:
        __id (str): Identificador único del usuario
        __nombre (str): Nombre del usuario
        __apellido (str): Apellido del usuario
        __saldo (float): Saldo actual del usuario
        __total_apostado (float): Total de dinero apostado por el usuario
        __historial (list): Historial de transacciones del usuario
    """

    __id: str
    __nombre: str
    __apellido: str
    __saldo: float
    __total_apostado: float
    __historial: list

    def __init__(
        self,
        nombre: str,
        apellido: str,
        saldo: float = 0.0,
        total_apostado: float = 0.0,
    ) -> None:
        """
        Inicializa un nuevo usuario

        Args:
            nombre (str): Nombre del usuario
            apellido (str): Apellido del usuario
            saldo (float, optional): Saldo inicial. Por defecto 0.0
            total_apostado (float, optional): Total apostado inicial. Por defecto 0.0
        """
        self.set_nombre(nombre)
        self.set_apellido(apellido)
        self.__generar_id()
        self.set_saldo(saldo)
        self.set_total_apostado(total_apostado)
        self.__set_historial([])

    def get_id(self) -> str:
        """Retorna el ID del usuario"""
        return self.__id

    def get_nombre(self) -> str:
        """Retorna el nombre del usuario"""
        return self.__nombre

    def get_apellido(self) -> str:
        """Retorna el apellido del usuario"""
        return self.__apellido

    def get_saldo(self) -> float:
        """Retorna el saldo actual del usuario"""
        return self.__saldo

    def get_total_apostado(self) -> float:
        """Retorna el total apostado por el usuario"""
        return self.__total_apostado

    def get_historial(self) -> list:
        """Retorna el historial de transacciones del usuario"""
        return self.__historial

    def __generar_id(self) -> None:
        """
        Genera un ID único para el usuario usando las iniciales y un número aleatorio
        """
        num_random = generador_random(100, 999)
        self.__id = (
            f"{self.__nombre[0].upper()}{self.__apellido[0].upper()}{num_random}"
        )
        
    def set_id(self, id: str) -> None:
        """
        Establece el ID del usuario

        Args:
            id (str): Nuevo ID

        Raises:
            ValueError: Si el ID es inválido
        """
        if id == "" or id is None or len(id) < 3 or len(id) > 30:
            raise ValueError(
                "El ID no puede ser vacío o None y debe tener entre 3 y 30 caracteres"
            )
        else:
            self.__id = id
            
    def set_id(self) -> None:
        """
        Establece el ID del usuario

        Args:
            id (str): Nuevo ID

        Raises:
            ValueError: Si el ID es inválido
        """
        if id == "" or id is None or len(id) < 3 or len(id) > 30:
            raise ValueError(
                "El ID no puede ser vacío o None y debe tener entre 3 y 30 caracteres"
            )
        else:
            self.__id = self.__generar_id()

    def set_nombre(self, nombre: str) -> None:
        """
        Establece el nombre del usuario

        Args:
            nombre (str): Nuevo nombre

        Raises:
            ValueError: Si el nombre es inválido
        """
        self.__nombre = nombre
        if nombre == "" or nombre is None or len(nombre) < 3 or len(nombre) > 30:
            raise ValueError(
                "El nombre no puede ser vacío o None y debe tener entre 3 y 30 caracteres"
            )

    def set_apellido(self, apellido: str) -> None:
        """
        Establece el apellido del usuario

        Args:
            apellido (str): Nuevo apellido

        Raises:
            ValueError: Si el apellido es inválido
        """
        self.__apellido = apellido
        if (
            apellido == ""
            or apellido is None
            or len(apellido) < 3
            or len(apellido) > 30
        ):
            raise ValueError(
                "El apellido no puede ser vacío o None y debe tener entre 3 y 30 caracteres"
            )

    def set_saldo(self, saldo: float) -> None:
        """
        Establece el saldo del usuario

        Args:
            saldo (float): Nuevo saldo

        Raises:
            ValueError: Si el saldo es negativo
        """
        if saldo < 0:
            raise ValueError("El saldo no puede ser negativo")
        self.__saldo = saldo

    def set_total_apostado(self, total_apostado: float) -> None:
        """
        Establece el total apostado por el usuario

        Args:
            total_apostado (float): Nuevo total apostado

        Raises:
            ValueError: Si el total apostado es negativo
        """
        if total_apostado < 0:
            raise ValueError("El total apostado no puede ser negativo")
        self.__total_apostado = total_apostado

    def __set_historial(self, historial: list) -> None:
        """
        Establece el historial de transacciones

        Args:
            historial (list): Nueva lista de historial
        """
        self.__historial = historial

    def agregar_historial(self, registro: list) -> None:
        """
        Agrega un nuevo registro al historial

        Args:
            registro (list): Registro a agregar
        """
        self.__historial.append(registro)

    def aumentar_saldo(self, monto: float) -> None:
        """
        Aumenta el saldo del usuario

        Args:
            monto (float): Cantidad a aumentar

        Raises:
            ValueError: Si el monto es negativo o cero
        """
        if monto <= 0:
            raise ValueError("El monto a aumentar debe ser positivo")

        self.__saldo += monto

    def disminuir_saldo(self, monto: float) -> None:
        """
        Disminuye el saldo del usuario

        Args:
            monto (float): Cantidad a disminuir

        Raises:
            ValueError: Si el monto es negativo, cero o mayor al saldo actual
        """
        if monto <= 0 or monto > self.__saldo:
            raise ValueError(
                "El monto a disminuir debe ser positivo y no puede ser mayor al saldo actual"
            )
        self.__saldo -= monto
