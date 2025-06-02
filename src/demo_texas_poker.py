import sys
# --- Monkeypatch para evitar inicialización de Firestore/Firebase ---
class FakeFirebaseAdmin:
    def __init__(self):
        self.credentials = type('fake', (), {'Certificate': lambda *a, **k: None})()
        self.firestore_async = lambda *a, **k: None
        self.firestore = lambda *a, **k: None
    def initialize_app(self, *a, **k):
        return None
sys.modules['firebase_admin'] = FakeFirebaseAdmin()
sys.modules['google'] = type('fake', (), {})()
sys.modules['google.oauth2'] = type('fake', (), {})()
sys.modules['google.oauth2.service_account'] = type('fake', (), {'Credentials': type('fake', (), {'from_service_account_info': lambda *a, **k: None})})()
sys.modules['google.auth'] = type('fake', (), {'exceptions': type('fake', (), {'InvalidValue': Exception})})()
sys.modules['google.auth.crypt'] = type('fake', (), {})()
sys.modules['google.auth.crypt.base'] = type('fake', (), {'RSASigner': type('fake', (), {'from_service_account_info': lambda *a, **k: None, 'from_string': lambda *a, **k: None})})()
sys.modules['google.auth.crypt._cryptography_rsa'] = type('fake', (), {})()
sys.modules['google.auth._helpers'] = type('fake', (), {'to_bytes': lambda x: x})()
# --- Fin monkeypatch ---

from src.model.usuario.Usuario import Usuario
from src.model.salaDeJuego.juego.juegosDeCartas.Poker import Poker
from src.model.salaDeJuego.enums.Etapas import Etapas

# --- Utilidades CLI ---
def limpiar():
    import os
    os.system('cls' if sys.platform == 'win32' else 'clear')

def mostrar_estado(jugador, poker):
    print(f"\nTu saldo: {jugador._saldo}")
    # Buscar la mano real del jugador (no None)
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

def pedir_accion(jugador, poker):
    acciones = ['apostar', 'igualar', 'subir', 'pasar', 'retirarse']
    print("Acciones disponibles:")
    for i, acc in enumerate(acciones):
        print(f"  {i+1}. {acc}")
    eleccion = input("Elige acción (número): ")
    try:
        idx = int(eleccion) - 1
        if idx < 0 or idx >= len(acciones):
            raise ValueError
        return acciones[idx]
    except Exception:
        print("Opción inválida.")
        return pedir_accion(jugador, poker)

def pedir_monto(jugador):
    try:
        monto = float(input("Monto a apostar/subir: "))
        if monto <= 0 or monto > jugador._saldo:
            raise ValueError
        return monto
    except Exception:
        print("Monto inválido.")
        return pedir_monto(jugador)

def main():
    print("Bienvenido a la demo CLI de Poker Texas Hold'em!")
    nombre1 = input("Nombre jugador 1: ")
    apellido1 = input("Apellido jugador 1 (3-30 caracteres): ")
    nombre2 = input("Nombre jugador 2: ")
    apellido2 = input("Apellido jugador 2 (3-30 caracteres): ")
    jugador1 = Usuario("U1", nombre1, apellido1, 1000)
    jugador2 = Usuario("U2", nombre2, apellido2, 1000)
    poker = Poker("mesa1", 7, 2, 0)  # Capacidad máxima 7, mínima 2
    poker._jugadores = [jugador1, jugador2]
    poker.inicializar_juego()
    jugadores = [jugador1, jugador2]
    turno = 0
    # --- Control de acciones por ronda ---
    acciones_realizadas = set()
    while poker.get_etapa() != Etapas.SHOWDOWN:
        jugador = jugadores[turno % len(jugadores)]
        if not any(j['jugador'] == jugador and j['en_juego'] for j in poker._mano_de_jugadores):
            turno += 1
            continue
        limpiar()
        print(f"Turno de {jugador._nombre}")
        mostrar_estado(jugador, poker)
        max_apuesta = max(j['apuesta'] for j in poker._mano_de_jugadores if j['en_juego'])
        jugador_info = next(j for j in poker._mano_de_jugadores if j['jugador'] == jugador)
        puede_pasar = jugador_info['apuesta'] == max_apuesta
        # Acciones válidas según el estado de la apuesta
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
            poker.apostar(jugador, monto)
        elif accion == 'igualar':
            poker.igualar(jugador)
        elif accion == 'subir':
            monto = pedir_monto(jugador)
            poker.subir(jugador, monto)
        elif accion == 'all-in':
            poker.all_in(jugador)
        elif accion == 'pasar':
            poker.pasar(jugador)
        elif accion == 'retirarse':
            poker.retirarse(jugador)
        acciones_realizadas.add(jugador)
        activos = [j for j in poker._mano_de_jugadores if j['en_juego']]
        if len(activos) == 1:
            poker.avanzar_etapa()
            acciones_realizadas.clear()
        elif len(acciones_realizadas) == len([j for j in jugadores if any(m['jugador'] == j and m['en_juego'] for m in poker._mano_de_jugadores)]):
            if all(j['apuesta'] == max(j2['apuesta'] for j2 in activos) for j in activos):
                poker.avanzar_etapa()
                for j in activos:
                    j['apuesta'] = 0
                acciones_realizadas.clear()
        turno += 1
    limpiar()
    print("\n--- SHOWDOWN ---")
    for jugador in jugadores:
        mostrar_estado(jugador, poker)
    poker.showdown()
    print("\nHistorial:")
    for h in poker._historial:
        print(h)

if __name__ == "__main__":
    main()
