from .JuegoDeCartas import JuegoDeCartas
from ....usuario.Usuario import Usuario
import random
import uuid
import threading
import asyncio
import concurrent.futures
import atexit
import gc
from ...SalaDeJuegoServicio import SalaDeJuegoServicio

class BlackJack(JuegoDeCartas):
    _plantarse: bool = False
    _cartas: dict[str,int] = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,
            "J":10,"Q":10,"K":10,"A":11}
    _apuesta: int = 1

    def __init__(self, jugador: str, capacidad: int, capacidadMinima: int, valor_entrada_mesa: int, _plantarse: bool = False, _apuesta: int = 1):
        # Generar ID primero y pasarlo al constructor padre
        sala_id = str(uuid.uuid4())
        
        # Pasar los 4 argumentos requeridos: id, capacidad, capacidadMinima, valor_entrada_mesa
        super().__init__(sala_id, capacidad, capacidadMinima, valor_entrada_mesa)
        
        self._plantarse = _plantarse
        self._apuesta = _apuesta
        self.servicio = SalaDeJuegoServicio()
        self.sala_activa_id = None
        self.manos_jugadores = {}
        self.mano_crupier = []
        self.estado_juego = "esperando"
        self.jugador_principal_id = jugador  # El jugador que inicia la sala
        
        # Lista para rastrear hilos activos
        self._hilos_activos = []
        
        # Bandera para indicar si el juego está siendo limpiado
        self._limpiando = False
        
        # Registrar limpieza al salir
        atexit.register(self._limpiar_al_salir)

    def _limpiar_al_salir(self):
        """
        Limpia recursos cuando el programa termina - VERSIÓN MEJORADA para gRPC
        """
        if self._limpiando:
            return  # Evitar limpieza múltiple
            
        self._limpiando = True
        print("🧹 Limpiando recursos de BlackJack...")
        
        try:
            # 1. Marcar el juego como finalizado
            self.estado_juego = "finalizado"
            
            # 2. Esperar a que terminen los hilos activos con timeout corto
            for hilo in self._hilos_activos:
                if hilo.is_alive():
                    print(f"⏳ Esperando hilo activo...")
                    hilo.join(timeout=1)  # Timeout muy corto
                    
            # 3. Limpiar referencias del servicio de Firestore
            if hasattr(self, 'servicio'):
                try:
                    # Intentar cerrar conexiones de Firestore si tiene el método
                    if hasattr(self.servicio, 'close') and callable(self.servicio.close):
                        self.servicio.close()
                    
                    # Limpiar la referencia
                    self.servicio = None
                    print("Servicio de Firestore limpiado")
                except Exception as e:
                    print(f" Error limpiando servicio Firestore: {e}")
            
            # 4. Forzar garbage collection para limpiar conexiones gRPC
            gc.collect()
            
            print("Limpieza completada")
            
        except Exception as e:
            print(f"Error durante limpieza: {e}")

    def _ejecutar_async_en_hilo(self, coro):
        """
        Ejecuta una corrutina usando ThreadPoolExecutor para evitar problemas de event loop
        """
        # Si estamos limpiando, no ejecutar más operaciones
        if self._limpiando or self.estado_juego == "finalizado":
            print("🚫 Operación cancelada - juego finalizado o limpiando")
            return None
            
        def ejecutar_corrutina():
            """Función que ejecuta la corrutina en un hilo separado"""
            loop = None
            try:
                # Verificar si ya hay un loop ejecutándose
                try:
                    loop = asyncio.get_running_loop()
                    print("⚠️ Loop ya ejecutándose, creando nuevo loop")
                    loop = None  # Necesitamos crear uno nuevo
                except RuntimeError:
                    # No hay loop ejecutándose, perfecto
                    pass
                
                # Crear y configurar nuevo event loop
                if loop is None:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                try:
                    # Ejecutar la corrutina con timeout más corto
                    resultado = loop.run_until_complete(asyncio.wait_for(coro, timeout=8))
                    print("✅ Operación async completada exitosamente")
                    return resultado
                except asyncio.TimeoutError:
                    print("⏱️ Timeout en operación de Firestore (8s)")
                    return None
                except Exception as e:
                    print(f"❌ Error ejecutando corrutina: {e}")
                    return None
                finally:
                    # Cerrar el loop de forma más agresiva para gRPC
                    if loop and not loop.is_closed():
                        try:
                            # Cancelar TODAS las tareas inmediatamente
                            pending = asyncio.all_tasks(loop)
                            for task in pending:
                                if not task.done():
                                    task.cancel()
                            
                            # NO esperar cancelación - cerrar inmediatamente
                            loop.close()
                            print("🔄 Event loop cerrado agresivamente")
                        except Exception as close_error:
                            print(f"⚠️ Error cerrando loop: {close_error}")
                        
            except Exception as e:
                print(f"❌ Error en hilo executor: {e}")
                return None
            finally:
                # Asegurarse de que el loop esté cerrado
                if loop and not loop.is_closed():
                    try:
                        loop.close()
                    except:
                        pass
        
        # Usar ThreadPoolExecutor para mejor manejo de hilos
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(ejecutar_corrutina)
                try:
                    # Timeout reducido para evitar bloqueos largos
                    resultado = future.result(timeout=10)
                    return resultado
                except concurrent.futures.TimeoutError:
                    print("⏱️ Timeout total en operación async (10s)")
                    return None
                except Exception as e:
                    print(f"❌ Error en ThreadPoolExecutor: {e}")
                    return None
        except Exception as e:
            print(f"❌ Error creando ThreadPoolExecutor: {e}")
            return None

    def crear_sala_activa_con_jugador(self, usuario) -> str:
        """
        Crea una sala activa en Firestore usando el servicio existente (THREAD-SAFE)
        """
        try:
            # Agregar jugador a la sala localmente primero
            if usuario not in self._jugadores:
                self._jugadores.append(usuario)
                print(f"{usuario} ha entrado a la sala de juego.")
            
            # Crear sala activa en Firestore usando hilo separado
            print(" Creando sala activa en Firestore...")
            
            coro_crear_sala = self.servicio.crear_sala_de_juego_activa(
                "BlackJack", 
                [usuario.get_id()]
            )
            
            self.sala_activa_id = self._ejecutar_async_en_hilo(coro_crear_sala)
            
            if self.sala_activa_id:
                # Inicializar manos localmente
                self.manos_jugadores[usuario.get_id()] = {
                    'cartas': [],
                    'puntos': 0,
                    'plantado': False
                }
                
                print(f" Sala activa creada en Firestore: {self.sala_activa_id}")
                return self.sala_activa_id
            else:
                print(" Error creando sala en Firestore")
                return None
            
        except Exception as e:
            print(f"Error creando sala activa: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _actualizar_sala_activa(self):
        """
        Actualiza la sala activa en Firestore usando el servicio existente (THREAD-SAFE)
        VERSIÓN MEJORADA - No actualizar si está finalizando
        """
        # NO actualizar si el juego está finalizado o limpiando
        if self.estado_juego == "finalizado" or self._limpiando:
            print("🚫 Actualización cancelada - juego finalizado")
            return
            
        if self.sala_activa_id:
            try:
                print("💾 Actualizando sala en Firestore...")
                
                # Crear la corrutina
                coro_actualizar = self.servicio.actualizar_manos_blackjack(
                    self.sala_activa_id,
                    self.manos_jugadores,
                    self.mano_crupier
                )
                
                # Ejecutar en hilo separado pero sin esperar el resultado
                # para evitar bloqueos al final del juego
                hilo = threading.Thread(
                    target=self._ejecutar_async_en_hilo_no_bloqueante, 
                    args=(coro_actualizar,),
                    daemon=True
                )
                hilo.start()
                self._hilos_activos.append(hilo)
                
                print("🚀 Actualización enviada a Firestore (no-bloqueante)")
                
            except Exception as e:
                print(f"Error actualizando sala activa: {e}")

    def obtener_estado_completo(self, jugador_id: str) -> dict:
        """
        Obtiene el estado completo del juego desde Firestore (THREAD-SAFE)
        CON CACHE para evitar llamadas repetidas - VERSIÓN MEJORADA
        """
        try:
            # Si el juego está finalizado, solo devolver datos locales
            if self.estado_juego == "finalizado" or self._limpiando:
                print("📋 Juego finalizado - usando solo datos locales")
                return {
                    'sala_id': self.sala_activa_id,
                    'estado': self.estado_juego,
                    'manos_jugadores': self.manos_jugadores,
                    'mano_crupier': self.mano_crupier,
                    'jugador_actual': jugador_id
                }
            
            # Evitar llamadas repetidas con un simple cache temporal
            if not hasattr(self, '_ultimo_estado_tiempo'):
                self._ultimo_estado_tiempo = 0
                self._ultimo_estado_cache = None
            
            import time
            tiempo_actual = time.time()
            
            # Si la última consulta fue hace menos de 3 segundos, usar cache
            if tiempo_actual - self._ultimo_estado_tiempo < 3 and self._ultimo_estado_cache:
                print("📋 Usando estado en cache")
                return self._ultimo_estado_cache
            
            # Solo consultar Firestore si el juego está activo
            if self.sala_activa_id and self.estado_juego == "en_curso":
                print("📥 Obteniendo estado desde Firestore...")
                
                coro_obtener = self.servicio.obtener_sala_activa(self.sala_activa_id)
                datos_sala = self._ejecutar_async_en_hilo(coro_obtener)
                
                if datos_sala:
                    print("✅ Estado obtenido desde Firestore")
                    # Actualizar cache
                    self._ultimo_estado_tiempo = tiempo_actual
                    self._ultimo_estado_cache = datos_sala
                    return datos_sala
                else:
                    print("⚠️ Error obteniendo estado de Firestore, usando datos locales")
            
            # Fallback: datos locales
            estado_local = {
                'sala_id': self.sala_activa_id,
                'estado': self.estado_juego,
                'manos_jugadores': self.manos_jugadores,
                'mano_crupier': self.mano_crupier,
                'jugador_actual': jugador_id
            }
            
            # Actualizar cache con datos locales
            self._ultimo_estado_tiempo = tiempo_actual
            self._ultimo_estado_cache = estado_local
            
            return estado_local
            
        except Exception as e:
            print(f"Error obteniendo estado: {e}")
            # Fallback: datos locales básicos
            return {
                'sala_id': self.sala_activa_id,
                'estado': self.estado_juego,
                'manos_jugadores': self.manos_jugadores,
                'mano_crupier': self.mano_crupier,
                'jugador_actual': jugador_id
            }

    def finalizar_juego(self):
        """
        Finaliza el juego y limpia recursos - VERSIÓN MEJORADA para gRPC
        """
        if self._limpiando:
            return  # Ya se está limpiando
            
        print("🏁 Finalizando juego...")
        
        # Marcar el juego como finalizado INMEDIATAMENTE
        self.estado_juego = "finalizado"
        
        # NO enviar más actualizaciones a Firestore al finalizar
        # para evitar operaciones gRPC pendientes
        print("🚫 Saltando actualización final de Firestore para evitar gRPC pendiente")
        
        # Limpiar recursos
        self._limpiar_al_salir()
        
        print("✅ Juego finalizado correctamente")

    def iniciar_partida_blackjack(self, jugador_id: str) -> dict:
        """
        Inicia una partida de BlackJack usando los métodos existentes
        """
        try:
            print("🎮 Inicializando juego...")
            
            # Repartir cartas iniciales usando cartasIniciales existente
            mano_jugador = self.cartasIniciales()  # Array de 2 cartas
            mano_crupier = self.cartasIniciales()   # Array de 2 cartas
            
            # Calcular puntos usando calcular_puntos existente
            puntos_jugador = self.calcular_puntos(mano_jugador)
            puntos_crupier = self.calcular_puntos(mano_crupier)
            
            print(f"🃏 Cartas jugador: {mano_jugador} -> {puntos_jugador} puntos")
            print(f"🃏 Cartas crupier: {mano_crupier} -> {puntos_crupier} puntos")
            
            # Actualizar estado local
            self.manos_jugadores[jugador_id] = {
                'cartas': mano_jugador,
                'puntos': puntos_jugador,
                'plantado': False
            }
            self.mano_crupier = mano_crupier
            self.estado_juego = "en_curso"
            
            # Actualizar en Firestore usando método thread-safe
            self._actualizar_sala_activa()
            
            return {
                'success': True,
                'mano_jugador': mano_jugador,
                'mano_crupier': [mano_crupier[0]],  # Solo mostrar primera carta
                'puntos_jugador': puntos_jugador,
                'mensaje': 'Partida iniciada con cartas repartidas'
            }
            
        except Exception as e:
            print(f"Error en iniciar_partida_blackjack: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}

    def pedir_carta_jugador(self, jugador_id: str) -> dict:
        """
        Un jugador pide una carta usando repartir_cartas existente
        """
        if self._limpiando or self.estado_juego == "finalizado":
            return {'success': False, 'error': 'Juego finalizado'}
            
        try:
            if jugador_id not in self.manos_jugadores:
                return {'success': False, 'error': 'Jugador no encontrado'}
            
            if self.manos_jugadores[jugador_id]['plantado']:
                return {'success': False, 'error': 'Jugador ya está plantado'}
            
            # Usar el método repartir_cartas existente
            nueva_carta = self.repartir_cartas()
            print(f"🃏 Nueva carta repartida: {nueva_carta}")
            
            # Actualizar mano del jugador
            self.manos_jugadores[jugador_id]['cartas'].append(nueva_carta)
            
            # Recalcular puntos usando calcular_puntos existente
            nuevos_puntos = self.calcular_puntos(self.manos_jugadores[jugador_id]['cartas'])
            self.manos_jugadores[jugador_id]['puntos'] = nuevos_puntos
            
            # Verificar si se pasó de 21
            if nuevos_puntos > 21:
                self.manos_jugadores[jugador_id]['plantado'] = True
                # Automáticamente jugar turno del crupier
                resultado_crupier = self._jugar_turno_crupier()
                resultado_partida = self.ganador(self.manos_jugadores[jugador_id]['cartas'], self.mano_crupier)
                mensaje = f'Nueva carta: {nueva_carta} - Te pasaste de 21. {resultado_partida}'
                # Finalizar juego
                self.finalizar_juego()
            else:
                mensaje = f'Nueva carta: {nueva_carta} (Puntos: {nuevos_puntos})'
                # Actualizar en Firestore usando método thread-safe
                self._actualizar_sala_activa()
            
            return {
                'success': True,
                'nueva_carta': nueva_carta,
                'puntos': nuevos_puntos,
                'plantado': self.manos_jugadores[jugador_id]['plantado'],
                'mensaje': mensaje
            }
            
        except Exception as e:
            print(f"Error en pedir_carta_jugador: {e}")
            return {'success': False, 'error': str(e)}

    def plantarse_jugador(self, jugador_id: str) -> dict:
        """
        Un jugador se planta y se ejecuta el turno del crupier
        """
        if self._limpiando or self.estado_juego == "finalizado":
            return {'success': False, 'error': 'Juego finalizado'}
            
        try:
            if jugador_id not in self.manos_jugadores:
                return {'success': False, 'error': 'Jugador no encontrado'}
            
            # Plantar al jugador
            self.manos_jugadores[jugador_id]['plantado'] = True
            print(f"🛑 Jugador {jugador_id} se plantó")
            
            # Jugar turno del crupier
            resultado_crupier = self._jugar_turno_crupier()
            
            # Determinar ganador usando el método existente
            mano_jugador = self.manos_jugadores[jugador_id]['cartas']
            resultado_partida = self.ganador(mano_jugador, self.mano_crupier)
            
            # Finalizar juego
            self.finalizar_juego()
            
            return {
                'success': True,
                'plantado': True,
                'mano_crupier_completa': self.mano_crupier,
                'puntos_crupier': self.calcular_puntos(self.mano_crupier),
                'resultado': resultado_partida,
                'mensaje': f'Te plantaste. {resultado_partida}'
            }
            
        except Exception as e:
            print(f"Error en plantarse_jugador: {e}")
            return {'success': False, 'error': str(e)}

    def _jugar_turno_crupier(self) -> dict:
        """
        Ejecuta el turno del crupier usando los métodos existentes
        """
        try:
            puntos_crupier = self.calcular_puntos(self.mano_crupier)
            print(f"🤵 Crupier empieza con {puntos_crupier} puntos")
            
            # Crupier juega hasta 17 usando repartir_cartas existente
            while puntos_crupier < 17:
                nueva_carta = self.repartir_cartas()
                self.mano_crupier.append(nueva_carta)
                puntos_crupier = self.calcular_puntos(self.mano_crupier)
                print(f"🤵 Crupier toma {nueva_carta}, ahora tiene {puntos_crupier} puntos")
            
            print(f"🤵 Crupier termina con {puntos_crupier} puntos")
            
            return {
                'success': True,
                'puntos_crupier': puntos_crupier,
                'resultado': 'Crupier terminó su turno'
            }
            
        except Exception as e:
            print(f"Error en _jugar_turno_crupier: {e}")
            return {'success': False, 'error': str(e)}

    def calcular_puntos(self, mano) -> int:
        # Calcula los puntos de la mano dada
        puntos = sum(BlackJack._cartas[carta] for carta in mano)
        # Si hay un As y los puntos son mayores a 21, resta 10 puntos
        if 'A' in mano and puntos > 21:
            puntos -= 10
        return puntos

    def repartir_cartas(self) -> str:
        # Reparte una carta al jugador o al crupier y devuelve el valor de la carta.
        return random.choice(list(BlackJack._cartas.keys()))

    def cartasIniciales(self):
        # Reparte dos cartas al jugador y devuelve el valor de las cartas.
        mano_inicial = [self.repartir_cartas(), self.repartir_cartas()]
        return mano_inicial

    def ganador(self, mano_jugador, mano_crupier):
        puntos_jugador = self.calcular_puntos(mano_jugador)
        puntos_crupier = self.calcular_puntos(mano_crupier)
        
        if puntos_jugador > 21:
            return "Perdiste - Te pasaste de 21"
        elif puntos_crupier > 21:
            return "¡Ganaste! - El crupier se pasó de 21"
        elif puntos_jugador > puntos_crupier:
            return "¡Ganaste! - Tienes más puntos que el crupier"
        elif puntos_jugador < puntos_crupier:
            return "Perdiste - El crupier tiene más puntos"
        else:
            return "Empate - Mismos puntos"

    def apostar(self, jugador: Usuario, monto: float):
        print("falta implementar apostar()")
        pass

    def inicializar_juego(self):
        """Inicializa el juego de BlackJack de forma simplificada."""
        print("🎮 BlackJack inicializado correctamente")
        # Solo limpiar estado previo
        self.manos_jugadores = {}
        self.mano_crupier = []
        self.estado_juego = "inicializado"
