from servidor.src.model.salaDeJuego.enums.Etapas import Etapas
from servidor.src.model.usuario.Usuario import Usuario
from servidor.src.model.salaDeJuego.juego.juegosDeCartas.JuegoDeCartas import JuegoDeCartas



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
        # El jugador abandona la mano
        jugador_info = next((j for j in self._mano_de_jugadores if j['jugador'] == usuario and j['en_juego']), None)
        if jugador_info:
            jugador_info['en_juego'] = False
            self._historial.append(f"{usuario._nombre} se retiró de la mano.")
            print(f"{usuario._nombre} se ha retirado de la mano.")
            # Si solo queda un jugador activo, gana el pozo automáticamente
            activos = [j for j in self._mano_de_jugadores if j['en_juego']]
            if len(activos) == 1:
                ganador = activos[0]['jugador']
                ganador._saldo += self.__pozo
                self._historial.append(f"{ganador._nombre} ganó el pozo de {self.__pozo} por abandono de los demás.")
                print(f"{ganador._nombre} gana el pozo de {self.__pozo} por abandono de los demás.")
                self.__pozo = 0
                # Lógica de cierre de mano: preguntar si quieren seguir, reiniciar, etc.
                self.preguntar_continuar_jugadores()
        else:
            print(f"{usuario._nombre} no está en juego o ya se retiró.")
    
    def pasar(self, usuario: Usuario):
        # El jugador solo puede pasar si igualó la apuesta máxima
        max_apuesta = max(j['apuesta'] for j in self._mano_de_jugadores if j['en_juego'])
        jugador_info = next((j for j in self._mano_de_jugadores if j['jugador'] == usuario and j['en_juego']), None)
        if not jugador_info:
            print(f"{usuario._nombre} no está en juego o ya se retiró.")
            return
        if jugador_info['apuesta'] != max_apuesta:
            print(f"{usuario._nombre} no puede pasar, debe igualar ({max_apuesta - jugador_info['apuesta']}) o retirarse.")
            return
        self._historial.append(f"{usuario._nombre} pasó")

    def igualar(self, usuario: Usuario):
        # El jugador iguala la apuesta máxima actual
        max_apuesta = max(j['apuesta'] for j in self._mano_de_jugadores if j['en_juego'])
        jugador_info = next((j for j in self._mano_de_jugadores if j['jugador'] == usuario and j['en_juego']), None)
        if not jugador_info:
            print(f"{usuario._nombre} no está en juego o ya se retiró.")
            return
        diferencia = max_apuesta - jugador_info['apuesta']
        if diferencia <= 0:
            print(f"{usuario._nombre} ya igualó la apuesta máxima.")
            return
        if usuario._saldo >= diferencia:
            usuario._saldo -= diferencia
            jugador_info['apuesta'] += diferencia
            self.__pozo += diferencia
            self._historial.append(f"{usuario._nombre} igualó con {diferencia}")
        elif usuario._saldo > 0:
            # ALL IN: iguala con todo lo que tiene
            all_in_monto = usuario._saldo
            jugador_info['apuesta'] += all_in_monto
            self.__pozo += all_in_monto
            usuario._saldo = 0
            self.set_all_in(True)
            self._historial.append(f"{usuario._nombre} fue ALL IN igualando con {all_in_monto}")
        else:
            print(f"{usuario._nombre} no tiene saldo suficiente para igualar.")

    def subir(self, usuario: Usuario, monto: float):
        # El jugador solo puede subir si ya hay una apuesta previa
        max_apuesta = max(j['apuesta'] for j in self._mano_de_jugadores if j['en_juego'])
        jugador_info = next((j for j in self._mano_de_jugadores if j['jugador'] == usuario and j['en_juego']), None)
        if not jugador_info:
            print(f"{usuario._nombre} no está en juego o ya se retiró.")
            return
        if max_apuesta == 0:
            print(f"No puedes subir, primero debes apostar.")
            return
        total = (max_apuesta - jugador_info['apuesta']) + monto
        if monto <= 0:
            print(f"El monto a subir debe ser mayor a 0.")
            return
        if usuario._saldo >= total:
            usuario._saldo -= total
            jugador_info['apuesta'] += total
            self.__pozo += total
            self._historial.append(f"{usuario._nombre} subió la apuesta en {monto}")
        elif usuario._saldo > 0:
            # ALL IN: sube con todo lo que tiene
            all_in_monto = usuario._saldo
            jugador_info['apuesta'] += all_in_monto
            self.__pozo += all_in_monto
            usuario._saldo = 0
            self.set_all_in(True)
            self._historial.append(f"{usuario._nombre} fue ALL IN subiendo con {all_in_monto}")
        else:
            print(f"{usuario._nombre} no tiene saldo suficiente para subir la apuesta.")

    def repartir_cartas(self):
        # Barajar el mazo si es necesario
        if hasattr(self._mazo, 'baragear'):
            self._mazo.baragear()
        # Repartir 2 cartas a cada jugador activo
        self._mano_de_jugadores = []
        for jugador in self.get_jugadores_activos():
            mano = [self._mazo.sacar_carta(), self._mazo.sacar_carta()]
            self._mano_de_jugadores.append({'jugador': jugador, 'mano': mano, 'en_juego': True, 'apuesta': 0})
        # Inicializar cartas comunitarias
        self.cartas_comunitarias = []

    def apostar(self, usuario: Usuario, monto: float):
        # Solo puede apostar si no hay apuesta previa (apuesta máxima = 0)
        max_apuesta = max(j['apuesta'] for j in self._mano_de_jugadores if j['en_juego'])
        jugador_info = next((j for j in self._mano_de_jugadores if j['jugador'] == usuario and j['en_juego']), None)
        if not jugador_info:
            print(f"{usuario._nombre} no está en juego o ya se retiró.")
            return
        if max_apuesta > 0:
            print(f"No puedes apostar, ya hay una apuesta previa. Debes igualar, subir o retirarte.")
            return
        if monto <= 0 or monto > usuario._saldo:
            print(f"Monto inválido para apostar.")
            return
        usuario._saldo -= monto
        jugador_info['apuesta'] += monto
        self.__pozo += monto
        self._historial.append(f"{usuario._nombre} apostó {monto}")

    def get_jugadores_activos(self) -> list:
        # Devuelve solo los jugadores activos (en_juego=True)
        return [j['jugador'] for j in getattr(self, '_mano_de_jugadores', []) if j.get('en_juego', True)] if hasattr(self, '_mano_de_jugadores') and self._mano_de_jugadores else self._jugadores

    def inicializar_juego(self):
        # Siempre usar self._jugadores para validar el inicio
        jugadores = self._jugadores
        if len(jugadores) < self._capacidadMinima:
            print(f"No hay suficientes jugadores para iniciar el Poker. Jugadores actuales: {len(jugadores)}")
            return
        self.set_dealer(jugadores[0])
        self.set_etapa(Etapas.PRE_FLOP)
        self.set_all_in(False)
        self.set_pozo(0)
        if hasattr(self._mazo, 'crear_mazo'):
            self._mazo.crear_mazo()
        if hasattr(self._mazo, 'baragear'):
            self._mazo.baragear()
        self.repartir_cartas()
        print("Juego de Poker inicializado. Dealer:", self.get_dealer()._nombre)
        print("Cartas repartidas a los jugadores.")
        self._historial.append(f"Poker inicializado por {self.get_dealer()._nombre} a las {getattr(self, '_fechaHoraInicio', 'ahora')}")
        # Mostrar manos iniciales (solo para debug, en real oculto)
        for jugador_info in self._mano_de_jugadores:
            print(f"{jugador_info['jugador']._nombre}: {jugador_info['mano']}")

    def avanzar_etapa(self):
        # Si solo queda un jugador, termina la partida y le da el pozo
        activos = [j for j in self._mano_de_jugadores if j['en_juego']]
        if len(activos) == 1:
            ganador = activos[0]['jugador']
            ganador._saldo += self.__pozo
            self._historial.append(f"{ganador._nombre} ganó el pozo de {self.__pozo} por abandono de los demás.")
            print(f"{ganador._nombre} gana el pozo de {self.__pozo} por abandono de los demás.")
            self.__pozo = 0
            self.set_etapa(Etapas.SHOWDOWN)
            return
        # Avanza la etapa del juego y reparte cartas comunitarias
        if self.__etapa == Etapas.PRE_FLOP:
            # Flop: 3 cartas comunitarias
            for _ in range(3):
                self.cartas_comunitarias.append(self._mazo.sacar_carta())
            self.set_etapa(Etapas.FLOP)
            self._historial.append("FLOP: " + str(self.cartas_comunitarias))
        elif self.__etapa == Etapas.FLOP:
            # Turn: 1 carta comunitaria
            self.cartas_comunitarias.append(self._mazo.sacar_carta())
            self.set_etapa(Etapas.TURN)
            self._historial.append("TURN: " + str(self.cartas_comunitarias))
        elif self.__etapa == Etapas.TURN:
            # River: 1 carta comunitaria
            self.cartas_comunitarias.append(self._mazo.sacar_carta())
            self.set_etapa(Etapas.RIVER)
            self._historial.append("RIVER: " + str(self.cartas_comunitarias))
        elif self.__etapa == Etapas.RIVER:
            # Al llegar a RIVER, automáticamente pasar a SHOWDOWN y determinar el ganador
            self.set_etapa(Etapas.SHOWDOWN)
            self._historial.append("SHOWDOWN")
            self.showdown()
        else:
            print("La partida ya está en SHOWDOWN o finalizada.")

    def showdown(self):
        # Si ya hay un ganador por abandono, no hacer nada
        if self.__etapa != Etapas.SHOWDOWN:
            print("No es la etapa de showdown aún.")
            return
        activos = [j for j in self._mano_de_jugadores if j['en_juego']]
        if len(activos) == 1:
            ganador = activos[0]['jugador']
            ganador._saldo += self.__pozo
            self._historial.append(f"{ganador._nombre} ganó el pozo de {self.__pozo} por abandono de los demás.")
            print(f"{ganador._nombre} gana el pozo de {self.__pozo} por abandono de los demás.")
            self.__pozo = 0
            # Preguntar si quieren continuar después de determinar el ganador por abandono
            self.preguntar_continuar_jugadores()
            return
        if not activos:
            print("No hay jugadores activos para el showdown.")
            return
        # Evaluar manos (simplificado: mayor carta de la mano + comunidad)
        def mejor_carta(mano, comunidad):
            valores = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13,'A':14}
            return max([valores.get(str(c)[:-1], 0) for c in mano + comunidad])
        
        mejor = -1
        ganador = None
        for jugador_info in activos:
            valor = mejor_carta(jugador_info['mano'], self.cartas_comunitarias)
            if valor > mejor:
                mejor = valor
                ganador = jugador_info['jugador']
                
        if ganador:
            ganador._saldo += self.__pozo
            self._historial.append(f"{ganador._nombre} ganó el pozo de {self.__pozo} en el showdown.")
            print(f"{ganador._nombre} es el ganador y recibe el pozo de {self.__pozo}!")
            self.__pozo = 0
        else:
            print("Empate o no se pudo determinar el ganador.")
            
        # Preguntar si quieren continuar después de determinar el ganador
        self.preguntar_continuar_jugadores()

    def preguntar_continuar_jugadores(self):
        jugadores_a_remover = []
        for jugador in self._jugadores[:]:
            # Validar nombre y apellido antes de preguntar
            if not hasattr(jugador, '_nombre') or not jugador._nombre or len(jugador._nombre) < 3 or len(jugador._nombre) > 30:
                print(f"[ERROR] El jugador con ID {getattr(jugador, 'id', 'desconocido')} tiene un nombre inválido. Se omite de la sala.")
                self.procesar_salida_jugador(jugador)
                continue
            if not hasattr(jugador, '_apellido') or not jugador._apellido or len(jugador._apellido) < 3 or len(jugador._apellido) > 30:
                print(f"[ERROR] El jugador {jugador._nombre} tiene un apellido inválido. Se omite de la sala.")
                self.procesar_salida_jugador(jugador)
                continue
            while True:
                respuesta = input(f"{jugador._nombre}, ¿quieres seguir en la mesa? (s/n): ").strip().lower()
                if respuesta in ("s", "n"):
                    break
                print("Respuesta inválida. Escribe 's' o 'n'.")
            if respuesta == "n":
                self.procesar_salida_jugador(jugador)
                jugadores_a_remover.append(jugador)
        # Si quedan al menos 2 jugadores, reiniciar la mano automáticamente
        if len(self._jugadores) >= 2:
            print("\nIniciando una nueva mano...")
            self.inicializar_juego()
        else:
            print("\nNo hay suficientes jugadores para continuar la mesa. Esperando nuevos jugadores...")

    def procesar_salida_jugador(self, jugador):
        # Guardar historial de ganancias/perdidas
        saldo_final = jugador._saldo
        saldo_inicial = getattr(jugador, '_saldo_inicial', 1000)  # fallback si no existe
        ganancia = saldo_final - saldo_inicial
        try:
            self.guardar_registro_jugador(jugador, ganancia)
        except Exception as e:
            print(f"Error guardando historial de {jugador._nombre}: {e}")
        # Retirar de la sala y dar paso a lista de espera
        self.salir_sala_de_juego(jugador)
        print(f"{jugador._nombre} ha salido de la mesa. Ganancia/perdida de la sesión: {ganancia}")

    def all_in(self, usuario: Usuario):
        # El jugador va all-in con todo su saldo
        jugador_info = next((j for j in self._mano_de_jugadores if j['jugador'] == usuario and j['en_juego']), None)
        if jugador_info and usuario._saldo > 0:
            monto = usuario._saldo
            jugador_info['apuesta'] += monto
            self.__pozo += monto
            usuario._saldo = 0
            self.set_all_in(True)
            self._historial.append(f"{usuario._nombre} fue ALL IN con {monto}")
        else:
            print(f"{usuario._nombre} no puede ir all-in.")

    # @override
    def __repr__(self) -> str:
        return (f"{super().__repr__()}"
                f"dealer: {self.__dealer}\n"
                f"etapa: {self.__etapa}\n"
                f"all_in: {self.__all_in}\n"
                f"pozo: {self.__pozo}\n")
    
    def jugar_partida(self):
        print("\n¡Bienvenido a Poker Texas Hold'em!")
        jugadores = self._jugadores
        turno = 0
        acciones_realizadas = set()
        from servidor.src.model.salaDeJuego.enums.Etapas import Etapas
        def limpiar():
            import os, sys
            os.system('cls' if sys.platform == 'win32' else 'clear')
        def mostrar_estado(jugador, poker):
            print(f"\nTu saldo: {jugador._saldo}")
            mano = []
            for j in poker._mano_de_jugadores:
                if j['jugador'] == jugador:
                    mano = j.get('mano', [])
                    if mano is None:
                        mano = []
                    break
            print(f"Tus cartas: {mano if mano else 'No repartidas'}")
            print(f"Cartas comunitarias: {getattr(poker, 'cartas_comunitarias', [])}")
            print(f"Pozo actual: {poker.get_pozo()}")
            print(f"Etapa: {poker.get_etapa()}")
            print()
        def pedir_monto(jugador):
            try:
                monto = float(input("Monto a apostar/subir: "))
                if monto <= 0 or monto > jugador._saldo:
                    raise ValueError
                return monto
            except Exception:
                print("Monto inválido.")
                return pedir_monto(jugador)
        while self.get_etapa() != Etapas.SHOWDOWN:
            jugador = jugadores[turno % len(jugadores)]
            if not any(j['jugador'] == jugador and j['en_juego'] for j in self._mano_de_jugadores):
                turno += 1
                continue
            limpiar()
            print(f"Turno de {jugador._nombre}")
            mostrar_estado(jugador, self)
            max_apuesta = max(j['apuesta'] for j in self._mano_de_jugadores if j['en_juego'])
            jugador_info = next(j for j in self._mano_de_jugadores if j['jugador'] == jugador)
            if jugador_info['apuesta'] < max_apuesta:
                acciones = ['igualar', 'subir', 'retirarse', 'all-in']
            else:
                acciones = ['apostar', 'subir', 'pasar', 'retirarse', 'all-in']
            print("Acciones disponibles:")
            for i, acc in enumerate(acciones):
                print(f"  {i+1}. {acc}")
            eleccion = input("Elige acción (número): ")
            try:
                idx = int(eleccion) - 1
                if idx < 0 or idx >= len(acciones):
                    raise ValueError
                accion = acciones[idx]
            except Exception:
                print("Opción inválida.")
                continue
            if accion == 'apostar':
                monto = pedir_monto(jugador)
                self.apostar(jugador, monto)
            elif accion == 'igualar':
                self.igualar(jugador)
            elif accion == 'subir':
                monto = pedir_monto(jugador)
                self.subir(jugador, monto)
            elif accion == 'all-in':
                self.all_in(jugador)
            elif accion == 'pasar':
                self.pasar(jugador)
            elif accion == 'retirarse':
                self.retirarse(jugador)
            acciones_realizadas.add(jugador)
            activos = [j for j in self._mano_de_jugadores if j['en_juego']]
            if len(activos) == 1:
                self.avanzar_etapa()
                acciones_realizadas.clear()
            elif len(acciones_realizadas) == len([j for j in jugadores if any(m['jugador'] == j and m['en_juego'] for m in self._mano_de_jugadores)]):
                if all(j['apuesta'] == max(j2['apuesta'] for j2 in activos) for j in activos):
                    self.avanzar_etapa()
                    for j in activos:
                        j['apuesta'] = 0
                    acciones_realizadas.clear()
            turno += 1
        limpiar()
        print("\n--- SHOWDOWN ---")
        for jugador in jugadores:
            mostrar_estado(jugador, self)
        self.showdown()
        print("\nHistorial:")
        for h in self._historial:
            print(h)