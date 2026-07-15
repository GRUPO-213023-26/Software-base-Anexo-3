
from datetime import datetime

from entidades import Cliente
from servicios import Servicio
from excepciones import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    ClienteInvalidoError,
)
from gestor_logs import registrar_evento, registrar_error


class Reserva:
    """Representa una reserva de un cliente sobre un servicio especifico."""

    ESTADOS_VALIDOS = ("pendiente", "confirmada", "cancelada")

    def __init__(self, id_reserva, cliente, servicio, duracion):
        # Validamos que cliente y servicio sean del tipo correcto
        if not isinstance(cliente, Cliente):
            raise ClienteInvalidoError("La reserva requiere un objeto Cliente valido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un objeto Servicio valido.")
        if duracion is None or duracion <= 0:
            raise ReservaInvalidaError("La duracion de la reserva debe ser mayor a cero.")

        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self._estado = "pendiente"
        self.fecha_creacion = datetime.now()

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        """
        Confirma la reserva, verificando primero que el servicio
        siga disponible. Usa try/except/else/finally.
        """
        try:
            if self._estado != "pendiente":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva en estado '{self._estado}'."
                )
            self.servicio.verificar_disponibilidad()
        except ServicioNoDisponibleError as error:
            registrar_error(f"Reserva {self.id_reserva}: {error}")
            # Encadenamos la excepcion original dentro de una mas especifica de Reserva
            raise ReservaInvalidaError(
                f"No se pudo confirmar la reserva {self.id_reserva} porque el servicio no esta disponible."
            ) from error
        except OperacionNoPermitidaError as error:
            registrar_error(f"Reserva {self.id_reserva}: {error}")
            raise
        else:
            # Este bloque solo se ejecuta si NO hubo ninguna excepcion
            self._estado = "confirmada"
            registrar_evento(f"Reserva {self.id_reserva} confirmada correctamente.")
        finally:
            # Esto se ejecuta siempre, haya habido error o no
            registrar_evento(f"Intento de confirmacion procesado para la reserva {self.id_reserva}.")

    def cancelar(self):
        """Cancela la reserva si no ha sido cancelada previamente."""
        try:
            if self._estado == "cancelada":
                raise OperacionNoPermitidaError(
                    f"La reserva {self.id_reserva} ya se encuentra cancelada."
                )
        except OperacionNoPermitidaError as error:
            registrar_error(str(error))
            raise
        else:
            self._estado = "cancelada"
            registrar_evento(f"Reserva {self.id_reserva} cancelada correctamente.")
        finally:
            registrar_evento(f"Intento de cancelacion procesado para la reserva {self.id_reserva}.")

    def procesar(self, impuesto=0.0, descuento=0.0):
        """
        Procesa la reserva calculando el costo final.
        Solo se puede procesar si la reserva esta confirmada.
        """
        try:
            if self._estado != "confirmada":
                raise OperacionNoPermitidaError(
                    "Solo se pueden procesar reservas que ya esten confirmadas."
                )
            costo = self.servicio.calcular_costo(impuesto=impuesto, descuento=descuento)
        except OperacionNoPermitidaError as error:
            registrar_error(f"Reserva {self.id_reserva}: {error}")
            raise
        except Exception as error:
            # Cualquier otro error inesperado al calcular el costo
            registrar_error(f"Error inesperado procesando la reserva {self.id_reserva}: {error}")
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva {self.id_reserva} por un error en el calculo del costo."
            ) from error
        else:
            registrar_evento(f"Reserva {self.id_reserva} procesada. Costo total: ${costo:,.2f}")
            return costo
        finally:
            registrar_evento(f"Fin del intento de procesamiento de la reserva {self.id_reserva}.")

    def mostrar_informacion(self):
        return (f"Reserva [{self.id_reserva}] Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre_servicio} | Duracion: {self.duracion} | "
                f"Estado: {self._estado}")

    def __str__(self):
        return self.mostrar_informacion()
