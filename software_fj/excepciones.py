
class ErrorSistemaFJ(Exception):
    """Excepcion base para todos los errores del sistema."""
    pass


class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando un dato ingresado no cumple las validaciones."""
    pass


class DatosFaltantesError(ErrorSistemaFJ):
    """Se lanza cuando falta un parametro obligatorio."""
    pass


class ClienteInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando el cliente no existe o esta mal registrado."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando el servicio solicitado no esta disponible."""
    pass


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando una reserva no se puede crear o procesar."""
    pass


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza cuando se intenta una operacion que no esta permitida
    en el estado actual del objeto (ej: cancelar una reserva ya cancelada)."""
    pass
