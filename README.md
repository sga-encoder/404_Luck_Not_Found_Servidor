# Mi Proyecto Python

Este es un proyecto de ejemplo en Python que permite instalar paquetes y contiene una estructura básica para el desarrollo y las pruebas.

## Estructura del Proyecto

```
Casino-de-Terminal
├── src
│   ├── __init__.py
│   ├── main.py
│   ├── model
│   │   ├── salaDeJuego
│   │   │    ├── enums
│   │   │    └── juego
│   │   │       └── juegosDeCartas
│   │   └── usuario
│   └── Utils
├── tests
│   ├── __init__.py
│   └── test_main.py
├── README.md
├── pyproject.toml
├── setup.py
├── .gitignore
└── install.md

```

### Prerrequisitos

Estos son los programas que necesitas para poder instalar el proyecto. Se recomienda ejecutar estos comandos en PowerShell como administrador.

### Scoop

Primero, instala Scoop, que es un gestor de paquetes para Windows:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

### python

Para instalar Python, utilizaremos `scoop`, ejecuta el siguiente comando en PowerShell:

```powershell
scoop install python
```

### pipx

instalamos `pipx` con `scoop` que es un gestor de paquetes para python

```powershell
scoop install pipx
pipx ensurepath
```

### potry

instalamos `poetry` con `pipx` que es un gestor de paquetes para python que lo que hace es crear un entorno virtual para cada proyecto

```powershell
pipx install poetry
```

## Instalar el Proyecto

Clona el repositorio y navega al directorio del proyecto:

```powershell
git clone git@github.com:sga-encoder/Casino-Virtual.git
cd Casino-Virtual
```
luego, instalamos las dependencias usando potry

```powershell
poetry install
```

### Instalar dependencias de desarrollo externas del poetry
    ```powershell
    $ pip install asciimatics
```

### Correr el Proyecto

Para ejecutar el proyecto, utiliza el siguiente comando:

```powershell
poetry run python main.py
```

### Correr el proyecto
Ejecutar el proyecto por los ambientes de pythom
python -m src.main