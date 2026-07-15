
from abc import ABC, abstractmethod

from excepciones import DatosInvalidosError, DatosFaltantesError, ServicioNoDisponibleError


class Servicio(ABC):
    """
    Clase abstracta que representa un servicio general de la empresa.
    """

    def __init__(self, id_servicio, nombre_servicio, disponible=True):
        self._id_servicio = id_servicio
        self._nombre_servicio = nombre_servicio
        self._disponible = disponible

    @property
    def id_servicio(self):
        return self._id_servicio

    @property
    def nombre_servicio(self):
        return self._nombre_servicio

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    def verificar_disponibilidad(self):
        """Metodo comun para todos los servicios: revisa si esta disponible."""
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._nombre_servicio}' no esta disponible en este momento."
            )

    @abstractmethod
    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        """Cada servicio calcula su costo de forma distinta (polimorfismo)."""
        pass

    @abstractmethod
    def describir_servicio(self):
        """Cada servicio da su propia descripcion."""
        pass

    @abstractmethod
    def validar_parametros(self):
        """Cada servicio valida sus propios parametros antes de usarse."""
        pass


class ServicioSalas(Servicio):
    """Servicio de reserva de salas, se cobra por hora."""

    def __init__(self, id_servicio, nombre_servicio, precio_hora, horas, disponible=True):
        super().__init__(id_servicio, nombre_servicio, disponible)
        self.precio_hora = precio_hora
        self.horas = horas
        self.validar_parametros()

    def validar_parametros(self):
        if self.precio_hora is None or self.horas is None:
            raise DatosFaltantesError("La sala requiere precio por hora y numero de horas.")
        if self.precio_hora <= 0 or self.horas <= 0:
            raise DatosInvalidosError("El precio por hora y las horas deben ser mayores a cero.")

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        # Variante "sobrecargada": si no se pasan impuesto/descuento, se calcula el costo simple.
        subtotal = self.precio_hora * self.horas
        subtotal = subtotal - (subtotal * descuento)
        total = subtotal + (subtotal * impuesto)
        return round(total, 2)

    def describir_servicio(self):
        return f"Sala '{self._nombre_servicio}': {self.horas} hora(s) a ${self.precio_hora:,.0f}/hora"


class ServicioEquipos(Servicio):
    """Servicio de alquiler de equipos, se cobra por dia y puede tener deposito."""

    def __init__(self, id_servicio, nombre_servicio, precio_dia, dias, deposito=0, disponible=True):
        super().__init__(id_servicio, nombre_servicio, disponible)
        self.precio_dia = precio_dia
        self.dias = dias
        self.deposito = deposito
        self.validar_parametros()

    def validar_parametros(self):
        if self.precio_dia is None or self.dias is None:
            raise DatosFaltantesError("El alquiler de equipos requiere precio por dia y numero de dias.")
        if self.precio_dia <= 0 or self.dias <= 0:
            raise DatosInvalidosError("El precio por dia y los dias deben ser mayores a cero.")
        if self.deposito < 0:
            raise DatosInvalidosError("El deposito no puede ser negativo.")

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        subtotal = (self.precio_dia * self.dias) + self.deposito
        subtotal = subtotal - (subtotal * descuento)
        total = subtotal + (subtotal * impuesto)
        return round(total, 2)

    def describir_servicio(self):
        return (f"Equipo '{self._nombre_servicio}': {self.dias} dia(s) a ${self.precio_dia:,.0f}/dia "
                f"+ deposito ${self.deposito:,.0f}")


class ServicioAsesoria(Servicio):
    """Servicio de asesoria especializada, se cobra por hora con una tarifa de especialista."""

    def __init__(self, id_servicio, nombre_servicio, tarifa_hora, horas, especialista, disponible=True):
        super().__init__(id_servicio, nombre_servicio, disponible)
        self.tarifa_hora = tarifa_hora
        self.horas = horas
        self.especialista = especialista
        self.validar_parametros()

    def validar_parametros(self):
        if self.tarifa_hora is None or self.horas is None:
            raise DatosFaltantesError("La asesoria requiere tarifa por hora y numero de horas.")
        if self.tarifa_hora <= 0 or self.horas <= 0:
            raise DatosInvalidosError("La tarifa por hora y las horas deben ser mayores a cero.")
        if not self.especialista or str(self.especialista).strip() == "":
            raise DatosFaltantesError("Se debe indicar el nombre del especialista.")

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        subtotal = self.tarifa_hora * self.horas
        subtotal = subtotal - (subtotal * descuento)
        total = subtotal + (subtotal * impuesto)
        return round(total, 2)

    def describir_servicio(self):
        return (f"Asesoria '{self._nombre_servicio}' con {self.especialista}: "
                f"{self.horas} hora(s) a ${self.tarifa_hora:,.0f}/hora")
