from src.view.utils.events import add_key_listener
from src.view.utils.printers import print_text


def blackjack(screen):
    screen.clear()
    while True:
        print_text(screen, {'text': 'Blackjack Game', 'x-center': 0, 'y-center': 0})
        screen.refresh()
        event = screen.get_event()
        salir = add_key_listener(ord('f'), event, lambda: 'salir')
        if salir == 'salir':
            return 'salir'