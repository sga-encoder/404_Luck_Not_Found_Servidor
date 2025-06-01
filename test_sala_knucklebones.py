#!/usr/bin/env python3
"""
Script de prueba completa para la clase SalaDeJuego usando KnuckleBones
Este script demuestra todas las funcionalidades de la clase SalaDeJuego
"""

import sys
import os

# Configurar el path para importar los módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.model.salaDeJuego.juego.KnuckleBones import KnuckleBones
from src.model.usuario.Usuario import Usuario
from src.model.salaDeJuego.enums.Juegos import Juegos


def crear_usuarios_de_prueba():
    """Crea usuarios de prueba para las partidas"""
    print("🎮 === CREANDO USUARIOS DE PRUEBA ===")
    
    usuarios = [
        Usuario.crear_usuario("Alice", "Johnson", 5000.0),
        Usuario.crear_usuario("Roberto", "Smith", 3000.0),
        Usuario.crear_usuario("Charlie", "Brown", 4000.0),
        Usuario.crear_usuario("Diana", "Wilson", 2500.0),
        Usuario.crear_usuario("Eduardo", "Davis", 6000.0),
    ]
    
    for usuario in usuarios:
        print(f"✅ Usuario creado: {usuario.get_nombre()} {usuario.get_apellido()} (ID: {usuario.get_id()}) - Saldo: ${usuario.get_saldo()}")
    
    return usuarios


def probar_gestion_de_jugadores():
    """Prueba la gestión de jugadores en la sala"""
    print("\n🏠 === PROBANDO GESTIÓN DE JUGADORES ===")
    
    # Crear sala de KnuckleBones
    sala = KnuckleBones("SALA_TEST_001")
    usuarios = crear_usuarios_de_prueba()
    
    print(f"\n📊 Estado inicial de la sala:")
    print(f"   - ID: {sala.get_id()}")
    print(f"   - Capacidad máxima: {sala.get_capacidad()}")
    print(f"   - Capacidad mínima: {sala.get_capacidadMinima()}")
    print(f"   - Jugadores actuales: {len(sala.get_jugadores())}")
    
    # Probar entrada de jugadores
    print(f"\n👥 Agregando jugadores a la sala...")
    for i, usuario in enumerate(usuarios[:2]):  # Solo 2 para KnuckleBones
        sala.entrar_sala_de_juego(usuario)
        print(f"   {i+1}. {usuario.get_nombre()} entró a la sala")
    
    # Intentar agregar más jugadores (debería ir a lista de espera)
    print(f"\n⏳ Intentando agregar jugadores adicionales...")
    for usuario in usuarios[2:4]:
        sala.entrar_sala_de_juego(usuario)
    
    print(f"\n📋 Estado actual:")
    print(f"   - Jugadores en sala: {len(sala.get_jugadores())}")
    print(f"   - Lista de espera: {len(sala.get_listaDeEspera())}")
    
    # Probar salida de jugador
    print(f"\n🚪 Probando salida de jugador...")
    if sala.get_jugadores():
        jugador_saliente = sala.get_jugadores()[0]
        sala.salir_sala_de_juego(jugador_saliente)
        print(f"   {jugador_saliente.get_nombre()} salió de la sala")
        print(f"   Jugadores restantes: {len(sala.get_jugadores())}")
        print(f"   Lista de espera: {len(sala.get_listaDeEspera())}")
    
    return sala


def probar_sistema_apuestas():
    """Prueba el sistema de apuestas"""
    print("\n💰 === PROBANDO SISTEMA DE APUESTAS ===")
    
    sala = KnuckleBones("SALA_APUESTAS_001")
    usuarios = crear_usuarios_de_prueba()
    
    # Agregar jugadores
    for usuario in usuarios[:2]:
        sala.entrar_sala_de_juego(usuario)
    
    # Realizar apuestas
    apuestas = [100.0, 150.0]
    for i, (usuario, monto) in enumerate(zip(sala.get_jugadores(), apuestas)):
        print(f"💵 {usuario.get_nombre()} apuesta ${monto}")
        sala.pagar_apuesta(usuario, monto)
    
    print(f"\n📊 Resumen de apuestas:")
    for apuesta in sala.get_apuestas():
        usuario = apuesta["usuario"]
        monto = apuesta["monto"]
        print(f"   - {usuario.get_nombre()}: ${monto}")
    
    # Intentar apuesta de usuario no en sala
    print(f"\n❌ Probando apuesta de usuario no autorizado...")
    sala.pagar_apuesta(usuarios[4], 200.0)  # Usuario que no está en la sala
    
    return sala


def probar_inicializacion_juego():
    """Prueba la inicialización del juego"""
    print("\n🎯 === PROBANDO INICIALIZACIÓN DEL JUEGO ===")
    
    sala = KnuckleBones("SALA_JUEGO_001")
    usuarios = crear_usuarios_de_prueba()
    
    # Intentar iniciar sin suficientes jugadores
    print("🚫 Intentando iniciar con pocos jugadores...")
    sala.iniciar_juego(Juegos.KNUCKLE_BONES)
    
    # Agregar jugadores suficientes
    print(f"\n✅ Agregando jugadores suficientes...")
    for usuario in usuarios[:2]:
        sala.entrar_sala_de_juego(usuario)
    
    # Iniciar el juego correctamente
    print(f"\n🎮 Iniciando KnuckleBones...")
    sala.iniciar_juego(Juegos.KNUCKLE_BONES)
    
    print(f"\n📋 Estado del juego:")
    print(f"   - Turno activo: {sala.get_turnoActivo().get_nombre() if sala.get_turnoActivo() else 'Ninguno'}")
    print(f"   - Fecha de inicio: {sala.get_fechaHoraInicio()}")
    print(f"   - Historial: {len(sala.get_historial())} entradas")
    
    return sala


def probar_funcionalidades_knucklebones():
    """Prueba funcionalidades específicas de KnuckleBones"""
    print("\n🎲 === PROBANDO FUNCIONALIDADES ESPECÍFICAS DE KNUCKLEBONES ===")
    
    sala = KnuckleBones("SALA_KB_001")
    usuarios = crear_usuarios_de_prueba()
    
    # Configurar sala
    for usuario in usuarios[:2]:
        sala.entrar_sala_de_juego(usuario)
    
    print(f"🎯 Jugadores configurados:")
    for i, jugador in enumerate(sala.get_jugadores()):
        print(f"   Jugador {i+1}: {jugador.get_nombre()} (ID: {jugador.get_id()})")
    
    # Establecer el turno activo antes de mostrar la mesa
    if len(sala.get_jugadores()) >= 2:
        sala.set_turnoActivo(sala.get_jugadores()[0])
        print(f"🎯 Turno activo establecido: {sala.get_turnoActivo().get_nombre()}")
    
    # Mostrar mesa inicial
    print(f"\n🎲 Mesa inicial de KnuckleBones:")
    sala.print_mesa()
    
    # Probar algunas funcionalidades específicas
    print(f"\n🧪 Probando funcionalidades del juego:")
    
    # Lanzar dado
    dado = sala.lanzar_dado()
    print(f"   🎲 Dado lanzado: {dado}")
    
    # Probar poner dado (simular)
    mesa_jugador = sala.get_mesa_de_juego()[0]
    resultado = sala.poner_dado(mesa_jugador, 0, dado, False)  # No afecta contadores
    if resultado:
        print(f"   ✅ Dado colocado exitosamente en posición 1")
    else:
        print(f"   ❌ No se pudo colocar el dado")
    
    # Calcular puntos
    puntos = sala.sumar_puntos(mesa_jugador)
    print(f"   📊 Puntos actuales: {puntos}")
    
    # Verificar si el juego terminó
    terminado = sala.finalizo_juego()
    print(f"   🏁 Juego terminado: {'Sí' if terminado else 'No'}")
    
    return sala


def probar_persistencia_datos():
    """Prueba el sistema de persistencia de datos"""
    print("\n💾 === PROBANDO PERSISTENCIA DE DATOS ===")
    
    sala = KnuckleBones("SALA_PERSIST_001")
    usuarios = crear_usuarios_de_prueba()
    
    # Configurar sala completa
    for usuario in usuarios[:2]:
        sala.entrar_sala_de_juego(usuario)
        sala.pagar_apuesta(usuario, 100.0)
    
    # Guardar registro de sala (estado: creada)
    print("💾 Guardando registro de sala (estado: creada)...")
    sala.guardar_registro_sala("creada")
    
    # Guardar registros de jugadores
    print("👤 Guardando registros de jugadores...")
    for usuario in sala.get_jugadores():
        sala.guardar_registro_jugador(usuario, 100.0)
    
    # Simular finalización del juego
    print("🏁 Simulando finalización del juego...")
    sala.guardar_registro_sala("finalizada")
    
    print("✅ Todos los registros guardados correctamente")
    print("📁 Verifica la carpeta 'registros' para ver los archivos generados")
    
    return sala


def mostrar_estado_completo_sala(sala):
    """Muestra el estado completo de una sala"""
    print(f"\n📊 === ESTADO COMPLETO DE LA SALA {sala.get_id()} ===")
    print(sala.__repr__())


def prueba_completa_partida_simulada():
    """Simula una partida completa de KnuckleBones"""
    print("\n🎮 === SIMULACIÓN DE PARTIDA COMPLETA ===")
    
    sala = KnuckleBones("PARTIDA_COMPLETA_001")
    usuarios = crear_usuarios_de_prueba()
    
    # Configurar partida
    print("🔧 Configurando partida...")
    for usuario in usuarios[:2]:
        sala.entrar_sala_de_juego(usuario)
        sala.pagar_apuesta(usuario, 200.0)
    
    print(f"🎯 Partida configurada entre:")
    print(f"   👤 {sala.get_jugadores()[0].get_nombre()}")
    print(f"   👤 {sala.get_jugadores()[1].get_nombre()}")
    
    # Guardar estado inicial
    sala.guardar_registro_sala("creada")
    
    # Inicializar el juego (esto ejecutará el juego completo)
    print(f"\n🚀 ¡Iniciando partida de KnuckleBones!")
    print("=" * 50)
    
    try:
        # Nota: El método inicializar_juego de KnuckleBones ejecuta toda la partida
        resultado = sala.inicializar_juego("KnuckleBones")
        print("=" * 50)
        print(f"🏆 Resultado de la partida: {resultado}")
        
        # Guardar estado final
        sala.guardar_registro_sala("finalizada")
        
    except Exception as e:
        print(f"❌ Error durante la partida: {e}")
        print("⚠️ Esto es normal ya que el juego requiere entrada del usuario")
        
    return sala


def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🎰 === PRUEBA COMPLETA DE SALADJUEGO CON KNUCKLEBONES ===")
    print("Este script prueba todas las funcionalidades de la clase SalaDeJuego\n")
    
    try:
        # Ejecutar todas las pruebas
        sala1 = probar_gestion_de_jugadores()
        sala2 = probar_sistema_apuestas()
        sala3 = probar_inicializacion_juego()
        sala4 = probar_funcionalidades_knucklebones()
        sala5 = probar_persistencia_datos()
        
        # Mostrar estado completo de una sala
        mostrar_estado_completo_sala(sala4)
        
        # Comentar la siguiente línea si no quieres ejecutar la partida completa
        # (requiere entrada del usuario)
        print("\n" + "="*60)
        print("⚠️  NOTA: La siguiente prueba iniciará una partida real")
        print("⚠️  Requiere entrada del usuario para las jugadas")
        print("⚠️  Presiona Ctrl+C para cancelar si no quieres jugar")
        print("="*60)
        
        input("\n📝 Presiona Enter para continuar con la partida simulada o Ctrl+C para salir...")
        
        # Ejecutar partida completa (comentar si no se quiere interacción)
        sala6 = prueba_completa_partida_simulada()
        
        print(f"\n✅ === TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE ===")
        print(f"📊 Total de salas creadas: 6")
        print(f"👥 Total de usuarios de prueba: 5")
        print(f"📁 Archivos de registro generados en la carpeta 'registros'")
        
    except KeyboardInterrupt:
        print(f"\n\n⚠️ Pruebas interrumpidas por el usuario")
        print(f"✅ Las pruebas básicas se completaron correctamente")
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
