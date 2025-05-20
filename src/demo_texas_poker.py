from src.model.salaDeJuego.juego.juegosDeCartas.Poker import Poker
from src.model.salaDeJuego.juego.juegosDeCartas.Mazo import Mazo
from src.model.usuario.Usuario import Usuario
from src.model.salaDeJuego.enums.Etapas import Etapas
import random

# --- Configuración inicial ---
MAX_JUGADORES = 7

# Crear jugadores
jugadores = [Usuario.crear_usuario(f"Jugador{i+1}", f"Apellido{i+1}", 1000) for i in range(MAX_JUGADORES)]

# Crear instancia de Poker
poker = Poker("mesa1", MAX_JUGADORES, 2, 100)

# Crear y barajar el mazo
mazo = Mazo(52)
mazo.set_mazo([f"{valor}{palo}" for palo in 'CDHT' for valor in list(map(str, range(2,11))) + list('JQKA')])
random.shuffle(mazo.get_mazo())
poker._mazo = mazo

# Asignar dealer
poker.set_dealer(jugadores[0])

# Repartir 2 cartas a cada jugador
manos = {jugador.get_id(): [mazo.get_mazo().pop(), mazo.get_mazo().pop()] for jugador in jugadores}

# Simular etapas del juego
etapas = [Etapas.PRE_FLOP, Etapas.FLOP, Etapas.TURN, Etapas.RIVER, Etapas.SHOWDOWN]
cartas_comunitarias = []

for etapa in etapas:
    poker.set_etapa(etapa)
    print(f"\nEtapa: {etapa}")
    if etapa == Etapas.FLOP:
        cartas_comunitarias += [mazo.get_mazo().pop() for _ in range(3)]
    elif etapa in [Etapas.TURN, Etapas.RIVER]:
        cartas_comunitarias.append(mazo.get_mazo().pop())
    print(f"Cartas comunitarias: {cartas_comunitarias}")
    # Simular apuestas simples
    for jugador in jugadores:
        accion = random.choice(['apostar', 'pasar', 'retirarse'])
        if accion == 'apostar':
            monto = random.randint(10, 100)
            print(f"{jugador.get_nombre()} apuesta {monto}")
            poker.set_pozo(poker.get_pozo() + monto)
        elif accion == 'pasar':
            print(f"{jugador.get_nombre()} pasa")
        else:
            print(f"{jugador.get_nombre()} se retira")
    print(f"Pozo actual: {poker.get_pozo()}")

# Mostrar manos finales
print("\n--- Manos de los jugadores ---")
for jugador in jugadores:
    print(f"{jugador.get_nombre()}: {manos[jugador.get_id()]}")
print(f"Cartas comunitarias finales: {cartas_comunitarias}")
print(f"Pozo final: {poker.get_pozo()}")
