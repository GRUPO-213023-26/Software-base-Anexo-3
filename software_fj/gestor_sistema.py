
from entidades import Cliente
from servicios import ServicioSalas, ServicioEquipos, ServicioAsesoria
from reserva import Reserva
from excepciones import ErrorSistemaFJ, ClienteInvalidoError, ReservaInvalidaError
from gestor_logs import registrar_evento, registrar_error


class GestorSistema:
    """Administra clientes, servicios y reservas usando listas en memoria."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self._contador_reservas = 1

    # ---------------------- CLIENTES ----------------------

    def registrar_cliente(self, id_cliente, nombre, documento, telefono, email):
        try:
            cliente = Cliente(id_cliente, nombre, documento, telefono, email)
        except ErrorSistemaFJ as error:
            registrar_error(f"No se pudo registrar el cliente '{nombre}': {error}")
            raise
        else:
            self.clientes.append(cliente)
            registrar_evento(f"Cliente registrado: {cliente.mostrar_informacion()}")
            return cliente
        finally:
            registrar_evento(f"Intento de registro de cliente procesado (nombre recibido: '{nombre}').")

    def buscar_cliente(self, id_cliente):
        for cliente in self.clientes:
            if cliente.id_entidad == id_cliente:
                return cliente
        raise ClienteInvalidoError(f"No existe un cliente con id '{id_cliente}'.")

    # ---------------------- SERVICIOS ----------------------

    def registrar_servicio_sala(self, id_servicio, nombre, precio_hora, horas):
        try:
            servicio = ServicioSalas(id_servicio, nombre, precio_hora, horas)
        except ErrorSistemaFJ as error:
            registrar_error(f"No se pudo crear el servicio de sala '{nombre}': {error}")
            raise
        else:
            self.servicios.append(servicio)
            registrar_evento(f"Servicio de sala creado: {servicio.describir_servicio()}")
            return servicio
        finally:
            registrar_evento(f"Intento de creacion de servicio de sala procesado ('{nombre}').")

    def registrar_servicio_equipo(self, id_servicio, nombre, precio_dia, dias, deposito=0):
        try:
            servicio = ServicioEquipos(id_servicio, nombre, precio_dia, dias, deposito)
        except ErrorSistemaFJ as error:
            registrar_error(f"No se pudo crear el servicio de equipo '{nombre}': {error}")
            raise
        else:
            self.servicios.append(servicio)
            registrar_evento(f"Servicio de equipo creado: {servicio.describir_servicio()}")
            return servicio
        finally:
            registrar_evento(f"Intento de creacion de servicio de equipo procesado ('{nombre}').")

    def registrar_servicio_asesoria(self, id_servicio, nombre, tarifa_hora, horas, especialista):
        try:
            servicio = ServicioAsesoria(id_servicio, nombre, tarifa_hora, horas, especialista)
        except ErrorSistemaFJ as error:
            registrar_error(f"No se pudo crear el servicio de asesoria '{nombre}': {error}")
            raise
        else:
            self.servicios.append(servicio)
            registrar_evento(f"Servicio de asesoria creado: {servicio.describir_servicio()}")
            return servicio
        finally:
            registrar_evento(f"Intento de creacion de servicio de asesoria procesado ('{nombre}').")

    def buscar_servicio(self, id_servicio):
        for servicio in self.servicios:
            if servicio.id_servicio == id_servicio:
                return servicio
        raise ReservaInvalidaError(f"No existe un servicio con id '{id_servicio}'.")

    # ---------------------- RESERVAS ----------------------

    def crear_reserva(self, id_cliente, id_servicio, duracion):
        try:
            cliente = self.buscar_cliente(id_cliente)
            servicio = self.buscar_servicio(id_servicio)
            reserva = Reserva(self._contador_reservas, cliente, servicio, duracion)
        except ErrorSistemaFJ as error:
            registrar_error(f"No se pudo crear la reserva: {error}")
            raise
        else:
            self.reservas.append(reserva)
            self._contador_reservas += 1
            registrar_evento(f"Reserva creada: {reserva.mostrar_informacion()}")
            return reserva
        finally:
            registrar_evento("Intento de creacion de reserva procesado.")

    def listar_clientes(self):
        return [c.mostrar_informacion() for c in self.clientes]

    def listar_servicios(self):
        return [s.describir_servicio() for s in self.servicios]

    def listar_reservas(self):
        return [r.mostrar_informacion() for r in self.reservas]
