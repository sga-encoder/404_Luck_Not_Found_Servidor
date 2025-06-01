from asciimatics.screen import Screen
from pyfiglet import Figlet

from src.view.utils.helpers import create_card


def print_text(screen, data: dict, asccii_art: bool = False) -> dict:
    """
    Dibuja texto en la pantalla usando Asciimatics con soporte para arte ASCII y posicionamiento personalizado avanzado.
    
    Esta función es la base del sistema de renderizado de texto y proporciona múltiples opciones de 
    posicionamiento tanto absoluto como relativo, además de soporte completo para arte ASCII usando pyfiglet.

    Args:
        screen: Objeto Screen de asciimatics donde se imprimirá el texto.
        data (dict): Diccionario de configuración con las siguientes claves posibles:
            
            **Contenido (obligatorio):**
            - 'text' (str): El texto a mostrar. Puede contener saltos de línea (\n) para texto multilínea.
            
            **Configuración de Arte ASCII (opcional):**
            - 'font' (str): Fuente para arte ASCII (por defecto 'slant'). 
              Fuentes disponibles: 'slant', 'banner', 'big', 'block', etc.
            - 'justify' (str): Justificación del arte ASCII ('left', 'center', 'right'). Por defecto 'left'.
            - 'max-width' (int): Ancho máximo para el arte ASCII (por defecto 100).
            
            **Configuración Visual (opcional):**
            - 'color' (int): Color del texto usando constantes de Screen.COLOUR_* (por defecto Screen.COLOUR_WHITE).
            - 'bg' (int): Color de fondo usando constantes de Screen.COLOUR_* (opcional).
            
            **Posicionamiento Absoluto (opcional):**
            - 'x_position' (int): Posición X absoluta en caracteres.
            - 'y_position' (int): Posición Y absoluta en líneas.
            - 'x' (int): Alias para 'x_position'.
            - 'y' (int): Alias para 'y_position'.
            
            **Posicionamiento Relativo al Centro (opcional):**
            - 'x-center' (int): Desplazamiento horizontal desde el centro de la pantalla.
              Valores negativos mueven a la izquierda, positivos a la derecha.
            - 'y-center' (int): Desplazamiento vertical desde el centro de la pantalla.
              Valores negativos mueven hacia arriba, positivos hacia abajo.
            
            **Posicionamiento desde Bordes (opcional):**
            - 'x-right' (int): Distancia desde el borde derecho de la pantalla.
            - 'y-bottom' (int): Distancia desde el borde inferior de la pantalla.
        
        asccii_art (bool): Si es True, renderiza el texto como arte ASCII usando pyfiglet.
            Cuando está activado, utiliza las opciones 'font', 'justify' y 'max-width' del diccionario data.

    Returns:
        dict: Diccionario con información sobre el texto renderizado:
            - 'width' (int): Ancho máximo del texto en caracteres.
            - 'height' (int): Altura del texto en líneas.
            - 'x_position' (int): Posición X final donde se renderizó el texto.
            - 'y_position' (int): Posición Y final donde se renderizó el texto.

    Raises:
        ValueError: Si el diccionario 'data' no contiene la clave 'text'.

    Ejemplos:
        # Texto simple centrado
        print_text(screen, {
            'text': 'Hola Mundo',
            'x-center': 0,
            'y-center': 0,
            'color': Screen.COLOUR_RED
        })
        
        # Arte ASCII con fuente personalizada
        print_text(screen, {
            'text': 'CASINO',
            'font': 'banner',
            'justify': 'center',
            'x-center': 0,
            'y': 5,
            'color': Screen.COLOUR_CYAN
        }, asccii_art=True)
        
        # Texto multilínea posicionado absolutamente
        print_text(screen, {
            'text': 'Línea 1\nLínea 2\nLínea 3',
            'x_position': 10,
            'y_position': 20,
            'color': Screen.COLOUR_GREEN,
            'bg': Screen.COLOUR_BLACK
        })
        
        # Texto desde borde derecho
        print_text(screen, {
            'text': 'Esquina',
            'x-right': 5,
            'y-bottom': 2,
            'color': Screen.COLOUR_YELLOW
        })

    Notas:
        - El sistema de posicionamiento tiene prioridad: absoluto > relativo al centro > desde bordes.
        - Para texto multilínea, 'width' devuelve el ancho de la línea más larga.
        - El arte ASCII puede generar texto significativamente más grande que el texto original.
        - Los colores de fondo solo se aplican a los caracteres del texto, no al área completa.
        - El posicionamiento relativo se calcula dinámicamente basado en el tamaño de la pantalla.
    """
    if( 'text' not in data):
        raise ValueError("El diccionario debe contener la clave 'text'.")
    
    font = data['font'] if 'font' in data else 'slant'
    color = data['color'] if 'color' in data else Screen.COLOUR_WHITE
    bg = data['bg'] if 'bg' in data else None
    justify = data['justify' ] if 'justify' in data else 'left'
    max_width = data['max-width' ] if 'max-width' in data else 100
    x_position = 0
    y_position = 0
    text = []
    height = 0
    if asccii_art:
        f = Figlet(font=font, width=max_width, justify=justify)
        ascii_text = f.renderText(data['text'])
        text = ascii_text.split('\n')
        height = len(text)
    else:
        text = data['text'].split('\n')
        height = len(text)
    
    # Calcular el ancho máximo de todas las líneas
    width = max(len(line) for line in text) if text else 0
    if 'y_position' in data:
        y_position = data['y_position']
    else:
        if 'y' in data:
            y_position = data['y']
        elif 'y-center' in data:
            y_position = (screen.height // 2 - height // 2) + data['y-center']
        elif 'y-bottom' in data:
            y_position = screen.height - height - data['y-bottom']

    for idx, line in enumerate(text):
        # Usar el ancho máximo para la posición x
        if 'x_position' in data:
            x_position = data['x_position']
        else:
            if 'x' in data:
                x_position = data['x']
            elif 'x-center' in data:
                x_position = (screen.width - width) // 2 + data['x-center']
            elif 'x-right' in data:
                x_position = screen.width - width - data['x-right']

        if(bg is not None):
            screen.print_at(line, x_position, y_position + idx, colour=color, bg=bg)
        else:
            screen.print_at(line, x_position, y_position + idx, colour=color)

    # print(f"[DEBUG] print_text: x_position={x_position}, y_position={y_position}, width={width}, height={height}")
    return {
        "width": width,
        "height": height,
        "x_position": x_position,
        "y_position": y_position
    }
    
def print_button(screen, data: dict, event=None, click=None) -> dict:
    from src.view.utils.events import add_mouse_listener  # Importación local para evitar ciclo

    """
    Dibuja un botón en la pantalla y detecta si ha sido presionado mediante un clic del mouse.

    Args:
        screen: Objeto Screen de asciimatics donde se imprimirá el botón.
        data (dict): Diccionario con las siguientes claves posibles:
            - 'text' (str): El texto a mostrar (obligatorio).
            - 'font' (str): Fuente para arte ASCII (opcional, por defecto 'slant').
            - 'color' (int): Color del texto (opcional, por defecto blanco).
            - 'bg' (int): Color de fondo (opcional).
            - 'x', 'x-center', 'x-right' (int): Posición horizontal (opcional).
            - 'y', 'y-center', 'y-bottom' (int): Posición vertical (opcional).
        event: Evento de entrada (generalmente un MouseEvent) a evaluar para detectar el clic.
        click (callable, opcional): Función a ejecutar si el botón es presionado.

    Returns:
        dict: Diccionario con la siguiente información:
            - 'result': Resultado de la función click() si se presionó el botón, None en caso contrario.
            - 'width': Ancho del botón (int)
            - 'height': Alto del botón (int)
            - 'x_position': Posición x del botón (int)
            - 'y_position': Posición y del botón (int)

    Notas importantes:
        - Debes activar el modo mouse: antes de usar botones con clic, asegúrate de tener 'screen.mouse = True'.
        - El orden importa: siempre llama a 'screen.refresh()' antes de 'screen.get_event()'.
        - El área de clic del botón cubre todo el bloque de texto generado, no solo una línea.
        - El evento debe ser un objeto MouseEvent y debe tener 'event.buttons != 0' para que se considere un clic.
        - El botón puede tener varias líneas (por ejemplo, si el texto contiene saltos de línea o es arte ASCII).
        - El área de detección se calcula usando el ancho máximo y la altura total del texto renderizado.
        - Si el usuario hace clic dentro de esa área, se ejecuta la función click y su resultado se devuelve en 'result'.

    Ejemplo de uso:
        screen.mouse = True  # Habilitar eventos de mouse
        while True:
            print_button(screen, data, ...)
            screen.refresh()  # Refresca antes de obtener el evento
            event = screen.get_event()
            resultado = print_button(screen, data, event, click=lambda: True)
            if resultado['result']:
                print("¡Botón presionado!")    """
    button= print_text(screen, data)
    # screen.refresh()
    result = add_mouse_listener(screen, button, event, click, element_id=f"button_{button['x_position']}_{button['y_position']}") if click else None
    return {
        "result": result,
        "width": button['width'],
        "height": button['height'],
        "x_position": button['x_position'],
        "y_position": button['y_position']
    }
    
def print_card(screen, data: dict, event=None, click=None) -> dict:
    from src.view.utils.events import add_mouse_listener  # Importación local para evitar ciclo

    """
    Dibuja una carta visual personalizada en la pantalla usando Asciimatics y permite detectar si ha sido presionada mediante un clic del mouse.

    Parámetros:
        screen: Objeto Screen de asciimatics donde se imprimirá la carta.
        data (dict): Diccionario de configuración de la carta. Claves posibles:
            - 'text' (str): Texto a mostrar dentro de la carta (obligatorio).
            - 'width' (int): Ancho de la carta (opcional, por defecto 21).
            - 'height' (int): Alto de la carta (opcional, por defecto 13).
            - 'ascii_x' (str): Caracter para los bordes horizontales (opcional, por defecto '██').
            - 'ascii_y' (str): Caracter para los bordes verticales (opcional, por defecto '█').
            - 'corner' (list): Caracteres para las esquinas (opcional, por defecto ['█','█','█','█']).
            - 'color' (int): Color del texto y bordes (opcional, por defecto blanco).
            - 'bg' (int): Color de fondo (opcional, por defecto Screen.COLOUR_DEFAULT).
            - 'x', 'x-center', 'x-right' (int): Posición horizontal (opcional).
            - 'y', 'y-center', 'y-bottom' (int): Posición vertical (opcional).
        event: Evento de entrada (MouseEvent) a evaluar para detectar el clic (opcional).
        click (callable, opcional): Función a ejecutar si la carta es presionada.

    Retorna:
        dict: Diccionario con la siguiente información:
            - 'result': Resultado de la función click() si se presionó la carta, None en caso contrario.
            - 'width': Ancho de la carta (int).
            - 'height': Alto de la carta (int).
            - 'x_position': Posición x de la carta (int).
            - 'y_position': Posición y de la carta (int).

    Notas:
        - Es necesario activar el modo mouse: antes de usar cartas con clic, asegúrate de tener 'screen.mouse = True'.
        - El área de clic de la carta cubre todo el bloque generado por la función create_card.
        - El evento debe ser un objeto MouseEvent y debe tener 'event.buttons != 0' para que se considere un clic.
        - El área de detección se calcula usando el ancho y la altura de la carta renderizada.
        - Si el usuario hace clic dentro de esa área, se ejecuta la función click y su resultado se devuelve en 'result'.
    """
    width = data['width'] if 'width' in data else 21
    height = data['height'] if 'height' in data else 13
    text = data['text'] if 'text' in data else ''
    ascii_x = data['ascii_x'] if 'ascii_x' in data else '─'
    ascii_y = data['ascii_y'] if 'ascii_y' in data else '│'
    corner = data['corner'] if 'corner' in data else ['╭', '╮', '╰', '╯']
    color = data['color'] if 'color' in data else Screen.COLOUR_WHITE
    bg = data['bg'] if 'bg' in data else Screen.COLOUR_DEFAULT
    justify = data['justify'] if 'justify' in data else 'left'
    grid = data['grid'] if 'grid' in data else False
    max_width = data['max-width'] if 'max-width' in data else 100
    grid_ascii_x = data['grid_ascii_x'] if 'grid_ascii_x' in data else ascii_x
    grid_ascii_y = data['grid_ascii_y'] if 'grid_ascii_y' in data else ascii_y
    grid_intersections = data['grid_intersection'] if 'grid_intersection' in data else ['┼', '┬', '┴', '├', '┤']
    grid_divider_x = data['grid_divider_x'] if 'grid_divider_x' in data else 2
    grid_divider_y = data['grid_divider_y'] if 'grid_divider_y' in data else 2
    grid_cell_width = width-(2*len(ascii_x))-grid_divider_x+1 // grid_divider_x
    grid_cell_height = height-(2*len(ascii_y))-grid_divider_y+1 // grid_divider_y
    grid_click = data['grid_click'] if 'grid_click' in data else None
    data_card = {
        'width': width,
        'height': height,
        'text': text,
        'ascii_x': ascii_x,
        'ascii_y': ascii_y,
        'corner': corner,
        'grid': grid,
        'grid_ascii_x': grid_ascii_x,
        'grid_ascii_y': grid_ascii_y,
        'grid_intersections': grid_intersections,
        'grid_divider_x': grid_divider_x,
        'grid_divider_y': grid_divider_y,
        'grid_cell_width': grid_cell_width,
        'grid_cell_height': grid_cell_height	
    }
    
    card_create = create_card(data_card)
    card_data = {
        'color': color,
        'bg': bg,
        'justify': justify,
        'max-width': max_width
    }
    
    card_data['text'] = card_create['text'] if grid else card_create
        
    if 'x' in data:
        card_data['x'] = data['x']
    if 'x-center' in data:
        card_data['x-center'] = data['x-center']
    if 'x-right' in data:
        card_data['x-right'] = data['x-right']
    if 'y' in data:
        card_data['y'] = data['y']
    if 'y-center' in data:
        card_data['y-center'] = data['y-center']
    if 'y-bottom' in data:
        card_data['y-bottom'] = data['y-bottom']
    if 'x_position' in data:
        card_data['x_position'] = data['x_position']
    if 'y_position' in data:
        card_data['y_position'] = data['y_position']
    
    card = print_text(screen, card_data)
    grid_num_cells = None
    grid_cell = []
    if grid:
        data_position = card_create['data']
        grid_num_cells = grid_divider_x * grid_divider_y
        if 'content' in data:
            content = data['content']
            for i in range(grid_num_cells):
                if str(i) in content:
                    padding_top = 0
                    padding_left = 0
                    padding_bottom = 0
                    padding_right = 0
                    padding=[]
                    if 'padding' in content[str(i)]:
                        padding = content[str(i)]
                        padding_top=padding[0]
                        padding_left=padding[1]
                        padding_bottom=padding[2]
                        padding_right=padding[3]
                    else:
                        padding_top = content[str(i)]['padding-top'] if 'padding-top' in content[str(i)] else 0
                        padding_left = content[str(i)]['padding-left'] if 'padding-left' in content[str(i)] else 0
                        padding_bottom = content[str(i)]['padding-bottom'] if 'padding-bottom' in content[str(i)] else 0
                        padding_right = content[str(i)]['padding-right'] if 'padding-right' in content[str(i)] else 0

                    data_aux={
                        'text': content[str(i)]['text'], 
                        'color': content[str(i)]['color'] if 'color' in content[str(i)] else screen.COLOUR_WHITE, 
                        'bg': content[str(i)]['bg'] if 'bg' in content[str(i)] else screen.COLOUR_DEFAULT, 
                        'position': content[str(i)]['position'] if 'position' in content[str(i)] else 'top_left_corner',
                        'padding': padding,
                        'padding-top': padding_top,
                        'padding-left': padding_left,
                        'padding-bottom': padding_bottom,
                        'padding-right': padding_right,
                        }
                    if 'button' in content[str(i)] and content[str(i)]['button']:
                        data_aux['button'] = content[str(i)]['button']
                    if 'event' in content[str(i)]:
                        data_aux['event'] = content[str(i)]['event']
                    if 'click' in content[str(i)]:
                        data_aux = content[str(i)]['click']
                    grid_cell.append(data_aux)
                else:
                    grid_cell.append([])
            
        posicion = 0
        
        
        for i in range(len(data_position['position_cell_divider_x'])):
            for j in range(len(data_position['position_cell_divider_y'])):
                text_cell = ''
                if posicion < grid_num_cells and grid_cell[posicion] != []:
                    text_cell = grid_cell[posicion]['text']
                    p=[grid_cell[posicion]['padding-top'], grid_cell[posicion]['padding-left'], grid_cell[posicion]['padding-bottom'], grid_cell[posicion]['padding-right']]
                    posicion_cell_x = [
                        card['x_position'] + data_position['position_cell_divider_x'][i] - data_position['grid_cell_width']+1+p[1]-p[3],
                        card['x_position'] + data_position['position_cell_divider_x'][i] - len(text_cell.split('\n'))+1+p[3]-p[1],
                        card['x_position'] + data_position['position_cell_divider_x'][i] - len(text_cell.split('\n')[0])+1+p[3]-p[1],
                    ]
                    posicion_cell_y = [
                        card['y_position'] + data_position['position_cell_divider_y'][j] - data_position['grid_cell_height']+1+p[0]-p[2],
                        card['y_position'] + data_position['position_cell_divider_y'][j] - len(text_cell.split('\n'))+1+p[2]-p[0],
                        card['y_position'] + data_position['position_cell_divider_y'][j] - len(text_cell.split('\n')[0])+1+p[2]-p[0],
                    ]
                else:
                    text_cell = ' '
                    posicion_cell_x = [
                        card['x_position'] + data_position['position_cell_divider_x'][i] - data_position['grid_cell_width']+1,
                        card['x_position'] + data_position['position_cell_divider_x'][i] - len(text_cell.split('\n'))+1,
                        card['x_position'] + data_position['position_cell_divider_x'][i] - len(text_cell.split('\n')[0])+1,
                    ]
                    posicion_cell_y = [
                        card['y_position'] + data_position['position_cell_divider_y'][j] - data_position['grid_cell_height']+1,
                        card['y_position'] + data_position['position_cell_divider_y'][j] - len(text_cell.split('\n'))+1,
                        card['y_position'] + data_position['position_cell_divider_y'][j] - len(text_cell.split('\n')[0])+1
                    ]

                posicion_cell = {
                    'top_left_corner': (posicion_cell_x[0], posicion_cell_y[0]),
                    'top_right_corner': (posicion_cell_x[1], posicion_cell_y[0]),
                    'bottom_right_corner': (posicion_cell_x[2], posicion_cell_y[1]),
                    'bottom_left_corner': (posicion_cell_x[0], posicion_cell_y[2])
                }
                
                if posicion < grid_num_cells and grid_cell[posicion] != []:
                    if 'button' in grid_cell[posicion]:
                        print_button(screen, {
                            'text': text_cell,
                            'color': grid_cell[posicion]['color'],
                            'bg': grid_cell[posicion]['bg'],
                            'x_position': posicion_cell[grid_cell[posicion]['position']][0],
                            'y_position': posicion_cell[grid_cell[posicion]['position']][1],
                        }, grid_cell[posicion]['event'] if 'event' in grid_cell[posicion] else None, grid_cell[posicion]['click'] if 'click' in grid_cell[posicion] else None)
                    else:
                        print_text(screen, {
                            'text': text_cell,
                            'color': grid_cell[posicion]['color'],
                            'bg': grid_cell[posicion]['bg'],
                            'x_position': posicion_cell[grid_cell[posicion]['position']][0],
                            'y_position': posicion_cell[grid_cell[posicion]['position']][1],
                        })
                posicion += 1
    # screen.refresh()
    result = None
    if grid_click == 'column' and grid and 'click' in data:
        result = []
        for i in range(len(data_position['position_cell_divider_x'])):
            x = card['x_position'] + len(grid_ascii_y) + (data_position['grid_cell_width'] + 1) * i
            y = card['y_position'] + len(grid_ascii_x)
            width = data_position['grid_cell_width'] - len(grid_ascii_x)
            height = card['height'] - (len(grid_ascii_x) * 2)- len(grid_ascii_y)
            column = {
                'x_position': x,
                'y_position': y,
                'width': width,
                'height': height            }
            if str(i) in data['click']:
                click_column = data['click'][str(i)]
                result.append(add_mouse_listener(screen, column, click_column['event'], click_column['click'], click_column['test'] if 'test' in click_column else False, element_id=f"grid_column_{i}_{column['x_position']}_{column['y_position']}"))
    elif grid_click == 'row':
        result = []
        for i in range(len(data_position['position_cell_divider_y'])):
            x = card['x_position'] + len(grid_ascii_x)
            y = card['y_position'] + (data_position['grid_cell_height'] * i) + i + len(grid_ascii_y)
            width = card['width'] - (len(grid_ascii_y) * 2) - 1
            height = data_position['grid_cell_height'] - len(grid_ascii_x)
            column = {
                'x_position': x,                'y_position': y,
                'width': width,
                'height': height
            }
            if str(i) in data['click']:
                click_row = data['click'][str(i)]
                aux = add_mouse_listener(screen, column, click_row['event'], click_row['click'], click_row['test'] if 'test' in click_row else False, element_id=f"grid_row_{i}_{column['x_position']}_{column['y_position']}")
                result.append(aux)
    else:
        result = add_mouse_listener(screen, card, event, click, element_id=f"card_{card['x_position']}_{card['y_position']}") if click else None
    return {
        "result": result,
        "width": width,
        "height": height,
        "x_position": card['x_position'],
        "y_position": card['y_position']
    }
