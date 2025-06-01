from asciimatics.screen import Screen
import time
import pyfiglet


from src.view.screens.home import home
from src.view.screens.juegos.poker import poker
from src.view.screens.juegos.blackjack import blackjack
from src.view.screens.juegos.knucklebones.knucklebones import knucklebones
from src.view.utils.events import add_key_listener
from src.view.utils.helpers import create_card, font_tester, font_tester_recomded
from src.view.utils.printers import print_button, print_text

def inicio(screen):
    screen.mouse = True
    contador = [0]
    text = {
        'text': '404-LUCK-NOT FOUND',
        'x-center': 0,
        'y-center': -5,
        'font': 'big_money-ne',
        'justify': 'center',
        'max-width': 130,
    }
    boton_text = {
        'text': '[  INICIAR JUEGO  ]',
        'x-center': 0,
        'y-center': 5,
        'color': Screen.COLOUR_WHITE,
        'bg': Screen.COLOUR_BLUE
    }
    while True:
        screen.refresh()
        print_text(screen, text, True)
        event = screen.get_event()  # Solo aquí
        button_inicio = print_button(
            screen,
            boton_text,
            event,
            click=lambda: True
        )
        print_text(screen, {'text': f'Contador: {contador[0]}', 'x-center': 0, 'y-center': 8})
        if button_inicio['result']:
            return button_inicio['result']
        # Escuchar Enter como 10 y 13
        add_key_listener([10, 13], event, lambda: (contador.__setitem__(0, contador[0] + 1)))

def main(screen):
    resultado = inicio(screen)
    if resultado:
        card = home(screen)
        if card == 'poker':
            poker(screen)
        elif card == 'blackjack':
            blackjack(screen)
        elif card == 'knucklebones':
            knucklebones(screen)

def main_dev(screen):
    knucklebones(screen)



if __name__ == "__main__":
    # font_tester('v.s')
    # font_tester_recomded('404-LUCK-NOT FOUND')
    Screen.wrapper(main)
    # Screen.wrapper(main_dev)
    # print(create_card({
    #     'width': 55,
    #     'height': 27,
    #     'text': '',
    #     'ascii_x': '│',
    #     'ascii_y': '─',
    #     'grid_divider_x': 3,
    #     'grid_divider_y': 3,
    #     'corner': ['╭', '╮', '╰', '╯'],
    #     'grid': True,
    # }))