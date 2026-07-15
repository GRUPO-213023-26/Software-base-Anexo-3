from abc import ABC, abstractmethod
from datetime import datetime

from excepciones import DatosInvalidosError, DatosFaltantesError


class EntidadBase(ABC):

    def __init__(self, id_entidad, nombre):
        self._id_entidad = id_entidad
        self._nombre = nombre
        self._fecha_registro = datetime.now()

    @abstractmethod
    def mostrar_informacion(self):
        """Cada entidad debe poder mostrar su informacion basica."""
        pass

    @property
    def id_entidad(self):
        return self._id_entidad

    @property
    def nombre(self):
        return self._nombre


class Cliente(EntidadBase):

    def __init__(self, id_entidad, nombre, documento, telefono, email):
        # Se llama al constructor de la clase padre (EntidadBase)
        super().__init__(id_entidad, nombre)

        # Se usan los setters para que se validen los datos desde el inicio
        self.documento = documento
        self.telefono = telefono
        self.email = email

    # ---------- Validaciones con encapsulacion (getters y setters) ----------

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise DatosFaltantesError("El documento del cliente es obligatorio.")
        if not str(valor).isdigit():
            raise DatosInvalidosError(f"El documento '{valor}' no es valido, debe ser numerico.")
        self._documento = str(valor)

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None or str(valor).strip() == "":
            raise DatosFaltantesError("El telefono del cliente es obligatorio.")
        if not str(valor).isdigit():
            raise DatosInvalidosError(f"El telefono '{valor}' no es valido, debe ser numerico.")
        self._telefono = str(valor)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if valor is None or str(valor).strip() == "":
            raise DatosFaltantesError("El email del cliente es obligatorio.")
        if "@" not in valor or "." not in valor:
            raise DatosInvalidosError(f"El email '{valor}' no tiene un formato valido.")
        self._email = valor

    # ---------- Metodo obligatorio de la clase abstracta ----------

    def mostrar_informacion(self):
        return (f"Cliente [ID: {self._id_entidad}] {self._nombre} | "
                f"Doc: {self._documento} | Tel: {self._telefono} | Email: {self._email}")

    def __str__(self):
        return self.mostrar_informacion()
