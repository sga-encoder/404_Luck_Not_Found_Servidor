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

## prerequisitos
estos son los programas que necesitas para poder instalar el proyecto todo esto se recomendan hacerlo con powershell como administrador

### scoop

primero instalamos scoop que es un gestor de paquetes para windows

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```

### python

instalamos python con scoop

```powershell
scoop install python
```

### pipx

instalamos pipx con scoop que es un gestor de paquetes para python

```powershell
scoop install pipx
pipx ensurepath
```

### potry

instalamos potry con pipx que es un gestor de paquetes para python que lo que hace es crear un entorno virtual para cada proyecto

```powershell
pipx install poetry
```

## instalar el proyecto

```powershell
git clone git@github.com:sga-encoder/Casino-Virtual.git
cd Casino-Virtual
poetry install
```

### correr el proyecto

```powershell
poetry run python main.py
```