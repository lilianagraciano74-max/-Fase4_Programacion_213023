import logging
from excepciones import ErrorReservaInvalida, ServicioNoDisponible

# ==========================================
# 1. CONFIGURACIÓN DEL LOGGING
# ==========================================
# Configura para guardar en archivo 'sistema_reservas.log' y mostrar en consola
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sistema_reservas.log', mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# ==========================================
# 2. LÓGICA DEL NEGOCIO
# ==========================================
def procesar_reserva(cliente: str, cantidad_personas: int, estado_servicio: str) -> None:
    """
    Procesa una reserva aplicando manejo robusto de excepciones.
    """
    logging.info(f"--- Iniciando intento de reserva para: {cliente} ---")
    
    try:
        # Validación de datos (Lanza excepción si es inválido)
        if cantidad_personas <= 0:
            raise ValueError(f"La cantidad de personas debe ser mayor a cero. Recibido: {cantidad_personas}")
            
        # Simulación de conexión a servicio externo
        if estado_servicio == "caido":
            try:
                # Simulamos un error de red/conexión de bajo nivel
                raise ConnectionError("Timeout al conectar con el servidor de reservas (Error 504).")
            except ConnectionError as e:
                # ENCADENAMIENTO DE EXCEPCIONES: Lanzamos nuestra excepción desde el error original
                raise ServicioNoDisponible("El servicio de reservas está temporalmente fuera de línea.") from e

    except ValueError as e:
        # Captura errores de validación de datos
        logging.error(f"Error de validación para {cliente}: {e}")
        print(f"❌ Error: {e}")
        
    except ServicioNoDisponible as e:
        # Captura errores de servicio (y muestra la causa original gracias al encadenamiento)
        logging.error(f"Error de servicio para {cliente}: {e} | Causa original: {e.__cause__}")
        print(f"⚠️ Lo sentimos: {e}")
        
    except Exception as e:
        # Captura cualquier otro error imprevisto (garantiza que el sistema no se caiga)
        logging.critical(f"Error inesperado en reserva de {cliente}: {e}")
        print("Ocurrió un error inesperado en el sistema.")
        
    else:
        # Se ejecuta SOLO si el bloque try no lanzó ninguna excepción
        logging.info(f"✅ Reserva exitosa para {cliente} ({cantidad_personas} personas).")
        print(f"✅ Reserva confirmada para {cliente}.")
        
    finally:
        # Se ejecuta SIEMPRE, haya error o no
        logging.info(f"Finalizando proceso de reserva para {cliente} (recursos liberados).\n")


# ==========================================
# 3. SIMULACIONES (10 CASOS)
# ==========================================
if __name__ == "__main__":
    print("==================================================")
    print("   INICIANDO 10 SIMULACIONES DEL SISTEMA DE RESERVAS")
    print("==================================================\n")
    
    # 1. Válida
    procesar_reserva("Ana", 2, "activo")
    # 2. Válida
    procesar_reserva("Carlos", 5, "activo")
    # 3. Inválida (Cantidad 0)
    procesar_reserva("Luis", 0, "activo")
    # 4. Inválida (Cantidad negativa)
    procesar_reserva("Marta", -3, "activo")
    # 5. Servicio no disponible (Falla de red)
    procesar_reserva("Pedro", 2, "caido")
    # 6. Válida
    procesar_reserva("Sofía", 1, "activo")
    # 7. Servicio no disponible (Falla de red)
    procesar_reserva("Jorge", 2, "caido")
    # 8. Válida
    procesar_reserva("Elena", 10, "activo")
    # 9. Inválida (Combina error de dato y servicio)
    procesar_reserva("Raúl", 0, "caido") 
    # 10. Válida
    procesar_reserva("Lucía", 4, "activo")

    print("==================================================")
    print("   SIMULACIONES COMPLETADAS. EL SISTEMA NO SE DETUVO.")
    print("   Revisa el archivo 'sistema_reservas.log' para ver los registros.")
    print("==================================================")