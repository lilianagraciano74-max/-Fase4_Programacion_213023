# ==========================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================

class ErrorReservaInvalida(Exception):
    """Excepción lanzada cuando los datos de la reserva no son válidos (ej. cantidad negativa o cero)."""
    pass

class ServicioNoDisponible(Exception):
    """Excepción lanzada cuando el sistema externo de reservas falla (ej. caída de red)."""
    pass