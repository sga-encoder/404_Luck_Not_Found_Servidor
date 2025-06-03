# Documentación: Clase SalaDeJuego y KnuckleBones

## ¿Qué hace la clase SalaDeJuego?

La clase `SalaDeJuego` es una **clase abstracta base** que proporciona la infraestructura común para todos los juegos del casino virtual. Actúa como un marco genérico que maneja:

### 🏠 Gestión de Salas
- **Identificación única**: Cada sala tiene un ID único
- **Capacidad controlada**: Define máximo y mínimo de jugadores
- **Estado del juego**: Mantiene información sobre el estado actual

### 👥 Gestión de Jugadores
- **Entrada y salida**: Los jugadores pueden unirse y abandonar la sala
- **Lista de espera**: Si la sala está llena, los jugadores esperan en cola
- **Control de turnos**: Gestiona qué jugador tiene el turno activo
- **Verificación de capacidad**: Asegura que haya suficientes jugadores para iniciar

### 💰 Sistema de Apuestas
- **Registro de apuestas**: Cada jugador puede apostar montos específicos
- **Validación**: Solo jugadores en la sala pueden apostar
- **Historial**: Mantiene registro de todas las apuestas realizadas

### 📊 Persistencia y Registro
- **Archivos JSON**: Guarda información de salas y jugadores
- **Historial de partidas**: Registra todas las acciones importantes
- **Estados de sala**: Marca salas como "creada" o "finalizada"
- **Registro individual**: Cada jugador tiene su propio archivo de historial

### 🎮 Arquitectura de Juegos
- **Método abstracto**: `inicializar_juego()` debe ser implementado por cada juego
- **Polimorfismo**: Permite diferentes tipos de juegos con la misma interfaz
- **Extensibilidad**: Fácil agregar nuevos juegos heredando de esta clase

## Funcionalidades Específicas de KnuckleBones

### 🎲 Mecánicas del Juego
- **Mesa 3x3**: Cada jugador tiene una grilla de 3x3 para colocar dados
- **Turnos alternados**: Los jugadores toman turnos lanzando dados
- **Sistema de puntuación**: Dados iguales en la misma fila se multiplican
- **Eliminación de dados**: Colocar un dado elimina dados iguales del oponente

### 🤖 Inteligencia Artificial
- **Bot inteligente**: Incluye IA para jugar contra la computadora
- **Estrategia avanzada**: El bot evalúa múltiples jugadas posibles
- **Proyección de jugadas**: Simula resultados futuros para tomar decisiones

### 🎯 Características Técnicas
- **Visualización ASCII**: Muestra la mesa del juego en texto
- **Validación de jugadas**: Verifica que las posiciones sean válidas
- **Control de fin de juego**: Detecta cuándo termina la partida
- **Cálculo automático**: Suma puntos según las reglas del juego

## Archivos y Estructura

### 📁 Archivos Principales
```
SalaDeJuego.py          # Clase base abstracta
KnuckleBones.py         # Implementación específica del juego
Usuario.py              # Clase de usuario del casino
main.py                 # Ejemplos de uso básico
test_sala_knucklebones.py  # Pruebas completas
```

### 🗂️ Archivos Generados
```
registros/
├── sala_[ID].json      # Información de cada sala
├── jugador_[ID].json   # Historial de cada jugador
└── ...
```

## Métodos Principales de SalaDeJuego

### 🔧 Configuración
- `__init__(id, capacidad, capacidadMinima)`: Inicializa la sala
- `set_jugadores(lista)`: Configura los jugadores de la sala

### 👥 Gestión de Jugadores
- `entrar_sala_de_juego(usuario)`: Agrega un jugador a la sala
- `salir_sala_de_juego(usuario)`: Remueve un jugador de la sala
- `get_jugadores_activos()`: Obtiene la lista de jugadores activos

### 🎮 Control de Juego
- `iniciar_juego(tipo_juego)`: Inicia un juego específico
- `pagar_apuesta(usuario, monto)`: Registra una apuesta
- `inicializar_juego()`: Método abstracto para implementar

### 💾 Persistencia
- `guardar_registro_sala(estado)`: Guarda información de la sala
- `guardar_registro_jugador(usuario, monto)`: Guarda historial del jugador

## Métodos Específicos de KnuckleBones

### 🎲 Mecánicas de Juego
- `lanzar_dado()`: Genera un número aleatorio 1-6
- `poner_dado(mesa, posicion, valor)`: Coloca un dado en la mesa
- `sumar_puntos(mesa_jugador)`: Calcula los puntos de un jugador
- `finalizo_juego()`: Verifica si el juego terminó
- `determinar_ganador(mesa)`: Determina el ganador de la partida

### 🤖 Inteligencia Artificial
- `knuckle_bot(dado, mesa)`: IA que decide dónde colocar el dado
- `proyector_de_jugada(mesa, jugada, posicion, dado)`: Simula resultados
- `columna_optima(columna)`: Evalúa el estado de una columna
- `columna_paralela(col_oponente, col_activa, puntuacion, dado)`: Compara columnas

### 🎯 Utilidades
- `print_mesa()`: Muestra la mesa actual en ASCII
- `cambiar_jugador_activo()`: Cambia el turno al siguiente jugador
- `get_oponente_index()`: Obtiene el índice del oponente

## Ejemplos de Uso

### 🚀 Uso Básico
```python
# Crear usuarios
usuario1 = Usuario.crear_usuario("Alice", "Johnson", 1000)
usuario2 = Usuario.crear_usuario("Bob", "Smith", 1000)

# Crear sala
sala = KnuckleBones("SALA_001")

# Configurar juego
sala.entrar_sala_de_juego(usuario1)
sala.entrar_sala_de_juego(usuario2)
sala.pagar_apuesta(usuario1, 100.0)
sala.pagar_apuesta(usuario2, 100.0)

# Iniciar partida
sala.inicializar_juego("KnuckleBones")
```

### 🧪 Pruebas Completas
```bash
# Ejecutar todas las pruebas
python test_sala_knucklebones.py

# Ejecutar ejemplo básico
python src/main.py
```

## Características Destacadas

### ✅ Ventajas del Diseño
- **Modular**: Fácil agregar nuevos juegos
- **Robusto**: Manejo de errores y validaciones
- **Persistente**: Guarda todo el historial
- **Flexible**: Configurable para diferentes tipos de juego
- **Completo**: Incluye IA, validaciones y visualización

### 🔮 Extensibilidad
- Agregar nuevos juegos heredando de `SalaDeJuego`
- Implementar diferentes tipos de IA
- Personalizar sistemas de puntuación
- Integrar con bases de datos
- Agregar interfaz gráfica

### 📈 Casos de Uso
- **Casino virtual completo**
- **Juegos multijugador**
- **Torneos automatizados**
- **Análisis de estrategias**
- **Entrenamiento de IA**

## Estructura de Archivos JSON

### 📄 Registro de Sala
```json
{
    "id": "SALA_001",
    "tipo_juego": "KnuckleBones",
    "capacidad": 2,
    "capacidad_minima": 2,
    "jugadores": ["Alice Johnson", "Bob Smith"],
    "historial": [...],
    "estado": "finalizada",
    "fecha_hora": "2025-06-01 15:30:45"
}
```

### 👤 Registro de Jugador
```json
[
    {
        "mesa": "SALA_001",
        "tipo_juego": "KnuckleBones",
        "monto": 100.0,
        "fecha_hora": "2025-06-01 15:30:45"
    }
]
```

Esta documentación proporciona una visión completa de cómo funciona el sistema y cómo utilizarlo efectivamente.
