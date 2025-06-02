from src.view.utils.events import add_key_listener
from src.view.utils.printers import print_text,print_button,print_card
from asciimatics.screen import Screen
import pyfiglet
from src.view.screens.juegos.blackjack.cartas import sacar_carta



def blackjack_juego(screen):
    screen.clear()
    screen.mouse=True
    mesa = {
        'text': 'Mesa BlackJack',
        'x-center': 0,
        'y-center': -20,
        'font': 'elite',
        'justify': 'center',
        'color': Screen.COLOUR_CYAN,
    }


    boton_pedirCarta ={
        'text': '[ PEDIR CARTA ]',
        'x-center': -70,
        'y-center': 8,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_GREEN,
    }

    cartas_jugadores = [[sacar_carta(), sacar_carta()] for _ in range(7)]

    carta_oculta={
        'text': '┌─────────────┐'
        '        │ ?           │'
        '        │             │'
        '        │             │'
        '        │      #      │'
        '        │             │'
        '        │             │'
        '        │           ? │'
        '        └─────────────┘' ,
        'x-center': 0,
        'y-center': 0,
        'color': Screen.COLOUR_BLACK,
        'bg': Screen.COLOUR_WHITE,
        'height': 1,
        'width': 17
    }
    while True:
        screen.refresh()
        print_text(screen,mesa, True)
                # Mostrar todas las cartas del jugador alineadas horizontalmente
        for jugador_index, cartas in enumerate(cartas_jugadores):
            for carta_index, carta_texto in enumerate(cartas):
                carta = {
                    'text': carta_texto,
                    'x-center': -45 + (carta_index * 18),
                    'y-center': -6 + jugador_index * 5,  # separar por jugador
                    'color': Screen.COLOUR_BLACK,
                    'bg': Screen.COLOUR_WHITE,
                    'height': 4,
                    'width': 15
                }
                print_card(screen, carta)

        # Mostrar carta oculta del dealer (solo una fija de ejemplo)
        print_card(screen, carta_oculta)

        event = screen.get_event()

        # Solo el jugador 1 (índice 0) puede pedir más cartas
        print_button(
            screen,
            boton_pedirCarta,
            event,
            click=lambda: cartas_jugadores[0].append(sacar_carta())
        )

        salir = add_key_listener(ord('f'), event, lambda: 'salir')
        if salir == 'salir':
            return 'salir'