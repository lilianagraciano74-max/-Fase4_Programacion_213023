import logging
from abc import ABC, abstractmethod

# ==========================================
# 1. CONFIGURACIÓN DEL LOGGING
# ==========================================
# Se configura el registro de eventos en un archivo y en la consola
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sistema_fj.log', mode='w', encoding='utf-8'), 
        logging.StreamHandler()
    ]
)

# ==========================================
# 2. EXCEPCIONES PERSONALIZADAS
# ==========================================
# Clase para errores de validación de datos
class ErrorValidacion(Exception): 
    pass

# Clase para errores cuando un servicio externo falla
class ServicioNoDisponible(Exception): 
    pass

# ==========================================
# 3. CLASE ABSTRACTA BASE
# ==========================================
class Entidad(ABC):
    """Clase abstracta que representa una entidad general del sistema."""
    def __init__(self, id_entidad):
        self.id_entidad = id_entidad

    @abstractmethod
    def obtener_detalles(self):
        """Método abstracto que debe ser implementado por las clases hijas."""
        pass

# ==========================================
# 4. CLASE CLIENTE (Encapsulación y Validaciones)
# ==========================================
class Cliente(Entidad):
    """Clase que representa a un cliente con atributos privados y validaciones."""
    def __init__(self, id_cliente, nombre, correo, telefono):
        super().__init__(id_cliente)
        self._nombre = None
        self._correo = None
        self._telefono = None
        
        # Validaciones en el constructor
        self.set_nombre(nombre)
        self.set_correo(correo)
        self.set_telefono(telefono)

    def set_nombre(self, nombre):
        # Valida que el nombre tenga al menos 3 caracteres
        if len(nombre) < 3:
            raise ErrorValidacion(f"El nombre '{nombre}' es demasiado corto.")
        self._nombre = nombre

    def set_correo(self, correo):
        # Valida que tenga una sola arroba, sin espacios y un punto en el dominio
        if correo.count("@") != 1 or " " in correo or "." not in correo.split("@")[1]:
            raise ErrorValidacion(f"El correo '{correo}' no es válido.")
        self._correo = correo

    def set_telefono(self, telefono):
        # Valida que tenga exactamente 10 dígitos
        if not telefono.isdigit() or len(telefono) != 10:
            raise ErrorValidacion(f"El teléfono '{telefono}' debe tener 10 dígitos.")
        self._telefono = telefono

    def obtener_detalles(self):
        return f"Cliente: {self._nombre} | Correo: {self._correo} | Tel: {self._telefono}"

# ==========================================
# 5. CLASE ABSTRACTA SERVICIO Y DERIVADOS (Polimorfismo)
# ==========================================
class Servicio(Entidad, ABC):
    """Clase abstracta para los servicios ofrecidos por Software FJ."""
    def __init__(self, id_servicio, nombre, costo_base):
        super().__init__(id_servicio)
        self.nombre = nombre
        self.costo_base = costo_base # El costo base ahora entra por el constructor

    @abstractmethod
    def calcular_costo(self, duracion_horas, impuesto=0.0, descuento=0.0):
        """Método abstracto para calcular el costo según el tipo de servicio."""
        pass

    def obtener_detalles(self):
        return f"Servicio: {self.nombre} | Costo Base por hora: ${self.costo_base}"

class ReservaSala(Servicio):
    def calcular_costo(self, duracion_horas, impuesto=0.0, descuento=0.0):
        # Cálculo específico para reserva de salas
        return (self.costo_base * duracion_horas * (1 + impuesto)) - descuento

class AlquilerEquipo(Servicio):
    def calcular_costo(self, duracion_horas, impuesto=0.0, descuento=0.0):
        # Cálculo específico para alquiler de equipos
        return (self.costo_base * duracion_horas * (1 + impuesto)) - descuento

class AsesoriaEspecializada(Servicio):
    def calcular_costo(self, duracion_horas, impuesto=0.0, descuento=0.0):
        # Cálculo específico para asesorías
        return (self.costo_base * duracion_horas * (1 + impuesto)) - descuento

# ==========================================
# 6. CLASE RESERVA (Manejo de Excepciones Completo)
# ==========================================
class Reserva:
    """Integra cliente, servicio y duración, gestionando los errores."""
    def __init__(self, cliente, servicio):
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"
    
    def procesar(self, duracion, estado_servicio="activo"):
        try:
            # Registro de inicio
            logging.info(f"Iniciando reserva de {self.cliente._nombre} para {self.servicio.nombre}")
            
            # Validación de duración
            if duracion <= 0:
                raise ErrorValidacion("La duración debe ser mayor a 0 horas.")
            
            # Simulación de caída de servicio con encadenamiento de excepciones
            if estado_servicio == "caido":
                try:
                    raise ConnectionError("Error 504 - Timeout de red")
                except ConnectionError as e:
                    raise ServicioNoDisponible("El servicio de reservas está fuera de línea.") from e
            
            # Si todo está bien, se calcula el costo (impuesto 19% y descuento fijo de 5000)
            costo = self.servicio.calcular_costo(duracion, impuesto=0.19, descuento=5000)
            self.estado = "Confirmada"
        
        except ErrorValidacion as e:
            logging.error(f"Error de validación: {e}")
            self.estado = "Fallida"
        except ServicioNoDisponible as e:
            logging.error(f"Error de servicio: {e} | Causa raíz: {e.__cause__}")
            self.estado = "Fallida"
        except Exception as e:
            # Captura de errores inesperados
            logging.critical(f"Error inesperado en el sistema: {e}")
            self.estado = "Fallida"
        else:
            # Se ejecuta solo si no hubo errores
            logging.info(f"Reserva exitosa. Costo total: ${costo}")
        finally:
            # Se ejecuta siempre al final
            logging.info(f"Finalizado proceso de reserva. Estado final: {self.estado}\n")

# ==========================================
# 7. SIMULACIONES (10 OPERACIONES COMPLETAS)
# ==========================================
if __name__ == "__main__":
    print("=== SISTEMA INTEGRAL SOFTWARE FJ ===\n")
    
    # 1. Creación de clientes (Válido e Inválido)
    try:
        # Cliente válido con todos los datos
        c1 = Cliente(1, "Ana", "ana@correo.com", "3001234567") 
        # Cliente inválido (correo mal formado)
        c2 = Cliente(2, "Pedro", "pedro_correo.com", "3109876543") 
    except ErrorValidacion as e:
        logging.error(f"Fallo al crear cliente: {e}")
        # Se corrige el error para continuar con las pruebas
        c2 = Cliente(2, "Pedro", "pedro@correo.com", "3109876543") 

    # 2. Creación de servicios pasando el costo base por constructor
    s1 = ReservaSala(1, "Sala VIP", 50000)
    s2 = AlquilerEquipo(2, "Laptop Gamer", 30000)
    s3 = AsesoriaEspecializada(3, "Asesoría en Python", 80000)

    # 3. Ejecución de las 10 simulaciones (Válidas e Inválidas)
    Reserva(c1, s1).procesar(2)               # 1. Válida
    Reserva(c1, s2).procesar(5)               # 2. Válida
    Reserva(c2, s3).procesar(0)               # 3. Inválida (Duración 0)
    Reserva(c2, s1).procesar(3, "caido")      # 4. Inválida (Servicio caído)
    Reserva(c1, s3).procesar(1)               # 5. Válida
    Reserva(c2, s2).procesar(10)              # 6. Válida
    Reserva(c1, s1).procesar(-2)              # 7. Inválida (Duración negativa)
    Reserva(c1, s2).procesar(2, "caido")      # 8. Inválida (Servicio caído)
    Reserva(c2, s3).procesar(4)               # 9. Válida
    Reserva(c1, s1).procesar(8)               # 10. Válida

    print("\n=== SIMULACIONES COMPLETADAS. REVISA EL ARCHIVO sistema_fj.log ===")
