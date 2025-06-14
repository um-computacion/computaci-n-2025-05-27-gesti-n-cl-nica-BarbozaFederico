from datetime import datetime
from ..errors.custom_exception import TipoDeDatoInvalidoError, ValidacionError
from ..utils.fechas import formatear_fecha


class Paciente:
    """
    Creacion de la clase paciente
    """

    def __init__(self, nombre: str, dni: str, fecha_nacimiento: datetime):
        self.__asegurar_nombre_es_valido__(nombre)
        self.__asegurar_dni_es_valido__(dni)
        self.__asegurar_fecha_nacimiento_es_valido__(fecha_nacimiento)
        self.__nombre__ = nombre
        self.__dni__ = dni
        self.__fecha_nacimiento__ = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self.__dni__

    def __str__(self) -> str:
        return (
            f"Paciente: {self.__nombre__} - "
            f"DNI: {self.__dni__} - "
            f"Fecha de nacimiento: {formatear_fecha(self.__fecha_nacimiento__)}"
        )

    def __asegurar_nombre_es_valido__(self, nombre: str) -> None:
        """
        Verifica que el nombre sea texto, no esté vacío y tenga menos de 50 caracteres.

        :param nombre: Nombre a validar.
        :raises TipoDeDatoInvalidoError: Si no es texto.
        :raises ValidacionError: Si está vacío o es muy largo.
        """
        if not isinstance(nombre, str):
            raise TipoDeDatoInvalidoError("El nombre debe ser texto")
        if not nombre.strip():
            raise ValidacionError("El nombre no puede estar vacío")
        if len(nombre) > 50:
            raise ValidacionError("El nombre debe tener menos de 50 caracteres")

    def __asegurar_dni_es_valido__(self, dni: str) -> None:
        """
        Verifica que el DNI sea texto numérico y no esté vacío.

        :param dni: DNI a validar.
        :raises TipoDeDatoInvalidoError: Si no es texto.
        :raises ValidacionError: Si está vacío o no es numérico.
        """
        if not isinstance(dni, str):
            raise TipoDeDatoInvalidoError("El DNI debe ser texto")
        if not dni.strip():
            raise ValidacionError("El DNI no puede estar vacío")
        if not dni.isdigit():
            raise ValidacionError("El DNI debe ser numérico")

    def __asegurar_fecha_nacimiento_es_valido__(
        self, fecha_nacimiento: datetime
    ) -> None:
        """
        Verifica que la fecha de nacimiento sea un datetime y no esté en el futuro.

        :param fecha_nacimiento: Fecha a validar.
        :raises TipoDeDatoInvalidoError: Si no es datetime.
        :raises ValidacionError: Si la fecha es posterior a la fecha actual.
        """
        if not isinstance(fecha_nacimiento, datetime):
            raise TipoDeDatoInvalidoError("La fecha de nacimiento es inválida")
        if fecha_nacimiento > datetime.now():
            raise ValidacionError("La fecha de nacimiento no puede ser mayor a hoy")


paciente_1 = Paciente("fede", "45724146", datetime(2004, 7, 6))
paciente_2 = Paciente("angel", "45724148", datetime(2004, 6, 3))
print(str(paciente_1))
