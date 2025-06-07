from typing import Any, Dict, List, Union

class PrettyPrinter:
    """
    Clase para imprimir datos de forma dinámica y estructurada.
    """
    
    @staticmethod
    def print_dynamic_data(data, indent="", max_depth=3, current_depth=0):
        """
        Imprime datos de forma dinámica, adaptándose a cualquier estructura.
        
        Args:
            data: Los datos a imprimir (dict, list, o valor simple)
            indent: Indentación actual
            max_depth: Profundidad máxima para evitar recursión infinita
            current_depth: Profundidad actual
        """
        if current_depth > max_depth:
            print(f"{indent}[Datos muy profundos, truncados...]")
            return
        
        if isinstance(data, dict):
            # Determinar el tipo de documento dinámicamente
            doc_type = PrettyPrinter._detect_document_type(data)
            if doc_type and current_depth == 0:
                print(f"{indent}🏷️  Tipo detectado: {doc_type}")
            
            for key, value in data.items():
                icon = PrettyPrinter._get_field_icon(key, value)
                
                if isinstance(value, dict):
                    print(f"{indent}{icon} {key}:")
                    PrettyPrinter.print_dynamic_data(value, indent + "   ", max_depth, current_depth + 1)
                elif isinstance(value, list):
                    print(f"{indent}{icon} {key}: [{len(value)} elementos]")
                    if len(value) <= 5:  # Mostrar solo si hay pocos elementos
                        for i, item in enumerate(value):
                            if isinstance(item, (dict, list)):
                                print(f"{indent}   [{i}]:")
                                PrettyPrinter.print_dynamic_data(item, indent + "      ", max_depth, current_depth + 1)
                            else:
                                print(f"{indent}   [{i}] {item}")
                    else:
                        # Mostrar solo los primeros elementos
                        for i in range(len(value)):
                            if isinstance(value[i], (dict, list)):
                                print(f"{indent}   [{i}]:")
                                PrettyPrinter.print_dynamic_data(value[i], indent + "      ", max_depth, current_depth + 1)
                            else:
                                print(f"{indent}   [{i}] {value[i]}")
                else:
                    # Valor simple
                    formatted_value = PrettyPrinter._format_value(value)
                    print(f"{indent}{icon} {key}: {formatted_value}")
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                print(f"{indent}[{i}]:")
                PrettyPrinter.print_dynamic_data(item, indent + "   ", max_depth, current_depth + 1)
        else:
            print(f"{indent}{PrettyPrinter._format_value(data)}")
    
    @staticmethod
    def format_dynamic_data(data, indent="", max_depth=3, current_depth=0):
        """
        Formatea datos de forma dinámica, adaptándose a cualquier estructura.
        
        Args:
            data: Los datos a formatear (dict, list, o valor simple)
            indent: Indentación actual
            max_depth: Profundidad máxima para evitar recursión infinita
            current_depth: Profundidad actual
            
        Returns:
            str: Cadena de texto con los datos formateados
        """
        result = []
        
        if current_depth > max_depth:
            result.append(f"{indent}[Datos muy profundos, truncados...]")
            return "\n".join(result)
        
        if isinstance(data, dict):
            # Determinar el tipo de documento dinámicamente
            doc_type = PrettyPrinter._detect_document_type(data)
            if doc_type and current_depth == 0:
                result.append(f"{indent}🏷️  Tipo detectado: {doc_type}")
            
            for key, value in data.items():
                icon = PrettyPrinter._get_field_icon(key, value)
                
                if isinstance(value, dict):
                    result.append(f"{indent}{icon} {key}:")
                    result.append(PrettyPrinter.format_dynamic_data(value, indent + "   ", max_depth, current_depth + 1))
                elif isinstance(value, list):
                    result.append(f"{indent}{icon} {key}: [{len(value)} elementos]")
                    if len(value) <= 5:  # Mostrar solo si hay pocos elementos
                        for i, item in enumerate(value):
                            if isinstance(item, (dict, list)):
                                result.append(f"{indent}   [{i}]:")
                                result.append(PrettyPrinter.format_dynamic_data(item, indent + "      ", max_depth, current_depth + 1))
                            else:
                                result.append(f"{indent}   [{i}] {item}")
                    else:
                        # Mostrar solo los primeros elementos
                        for i in range(len(value)):
                            if isinstance(value[i], (dict, list)):
                                result.append(f"{indent}   [{i}]:")
                                result.append(PrettyPrinter.format_dynamic_data(value[i], indent + "      ", max_depth, current_depth + 1))
                            else:
                                result.append(f"{indent}   [{i}] {value[i]}")
                else:
                    # Valor simple
                    formatted_value = PrettyPrinter._format_value(value)
                    result.append(f"{indent}{icon} {key}: {formatted_value}")
        
        elif isinstance(data, list):
            for i, item in enumerate(data):
                result.append(f"{indent}[{i}]:")
                result.append(PrettyPrinter.format_dynamic_data(item, indent + "   ", max_depth, current_depth + 1))
        else:
            result.append(f"{indent}{PrettyPrinter._format_value(data)}")
        
        return "\n".join(result)
    
    @staticmethod
    def _detect_document_type(data):
        """Detecta el tipo de documento basado en sus campos"""
        if not isinstance(data, dict):
            return None
        
        # Detectar diferentes tipos de documentos
        if 'juego' in data and 'jugadores' in data:
            return f"Sala de Juego - {data.get('juego', 'Desconocido')}"
        elif 'nombre' in data and 'email' in data:
            return "Usuario"
        elif 'partida_id' in data and 'movimiento' in data:
            return "Movimiento de Juego"
        elif 'cartas' in data or 'tablero' in data:
            return "Estado de Partida"
        elif 'timestamp' in data and 'evento' in data:
            return "Evento/Log"
        else:
            return "Documento Genérico"
    
    @staticmethod
    def _get_field_icon(field_name, value):
        """Obtiene un icono apropiado para el campo basado en su nombre y valor"""
        field_lower = field_name.lower()
        
        # Iconos basados en el nombre del campo
        if 'id' in field_lower:
            return "🆔"
        elif field_lower in ['juego', 'game', 'tipo_juego']:
            return "🎮"
        elif field_lower in ['jugadores', 'players', 'usuarios']:
            return "👥"
        elif field_lower in ['estado', 'status', 'state']:
            return "🎯"
        elif field_lower in ['turno', 'turn', 'turno_actual']:
            return "⏰"
        elif field_lower in ['fecha', 'timestamp', 'date', 'time', 'fecha_hora']:
            return "📅"
        elif field_lower in ['cartas', 'cards', 'mano']:
            return "🃏"
        elif field_lower in ['tablero', 'board', 'mesa']:
            return "🎲"
        elif field_lower in ['puntos', 'score', 'puntaje']:
            return "🏆"
        elif field_lower in ['dinero', 'money', 'coins', 'creditos']:
            return "💰"
        elif field_lower in ['nivel', 'level', 'rango']:
            return "⭐"
        elif field_lower in ['capacidad', 'max', 'limite']:
            return "📏"
        elif field_lower in ['activo', 'active', 'online']:
            return "🟢" if value else "🔴"
        elif field_lower in ['historial', 'history', 'log']:
            return "📚"
        elif isinstance(value, bool):
            return "✅" if value else "❌"
        elif isinstance(value, (int, float)) and value == 0:
            return "0️⃣"
        elif isinstance(value, list):
            return "📋"
        elif isinstance(value, dict):
            return "📁"
        else:
            return "📄"
    
    @staticmethod
    def _format_value(value):
        """Formatea un valor para mostrar de forma más legible"""
        if value is None:
            return "❌ None"
        elif isinstance(value, bool):
            return "✅ True" if value else "❌ False"
        elif isinstance(value, str) and len(value) > 50:
            return f'"{value[:47]}..."'
        elif isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            return str(value)

# Función de conveniencia para uso directo
def print_data(data, indent="", max_depth=3):
    """
    Función de conveniencia para imprimir datos usando PrettyPrinter.
    
    Args:
        data: Los datos a imprimir
        indent: Indentación inicial
        max_depth: Profundidad máxima
    """
    PrettyPrinter.print_dynamic_data(data, indent, max_depth)

def format_data(data, indent="", max_depth=3):
    """
    Función de conveniencia para formatear datos usando PrettyPrinter.
    
    Args:
        data: Los datos a formatear
        indent: Indentación inicial
        max_depth: Profundidad máxima
        
    Returns:
        str: Cadena de texto con los datos formateados
    """
    return PrettyPrinter.format_dynamic_data(data, indent, max_depth)
