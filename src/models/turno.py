from datetime import datetime
from .paciente import Paciente
from .medico import Medico
from ..errors.custom_exception import TipoDeDatoInvalidoError, ValidacionError
from ..utils.fechas import formatear_fecha

class Turno:
    """
    Representa un turno médico entre un paciente y un médico para una especialidad específica en una fecha y hora determinada.
    """

    def __init__(self, paciente: Paciente, medico: Medico, fecha_hora: datetime, especialidad: str):
        self.__asegurar_paciente_es_valido__(paciente)
        self.__asegurar_medico_es_valido__(medico)
        self.__asegurar_fecha_hora_es_valida__(fecha_hora)
        self.__asegurar_especialidad_es_valida__(especialidad)
        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__fecha_hora__ = fecha_hora
        self.__especialidad__ = especialidad

    def obtener_medico(self) -> Medico:
        return self.__medico__

    def obtener_fecha_hora(self) -> datetime:
        return self.__fecha_hora__

    def __str__(self) -> str:
        return (
            f"Turno: Paciente: {self.__paciente__} | "
            f"Médico: {self.__medico__} | "
            f"Especialidad: {self.__especialidad__} | "
            f"Fecha y hora: {formatear_fecha(self.__fecha_hora__)} {self.__fecha_hora__.strftime('%H:%M')}"
        )

    def __asegurar_paciente_es_valido__(self, paciente):
        if not isinstance(paciente, Paciente):
            raise TipoDeDatoInvalidoError("Paciente no es valido")

    def __asegurar_medico_es_valido__(self, medico):
        if not isinstance(medico, Medico):
            raise TipoDeDatoInvalidoError("MedIco no es valido :]")

    def __asegurar_fecha_hora_es_valida__(self, fecha_hora):
        if not isinstance(fecha_hora, datetime):
            raise TipoDeDatoInvalidoError("La fecha y hora debe ser valida")
        if fecha_hora < datetime.now():
            raise ValidacionError("La fecha y hora del turno no puede ser en el pasado")

    def __asegurar_especialidad_es_valida__(self, especialidad):
        if not isinstance(especialidad, str):
            raise TipoDeDatoInvalidoError("La especialidad debe ser texto")
        if not especialidad.strip():
            raise ValidacionError("La especialidad no puede estar vacía")
        if len(especialidad) > 50:
            raise ValidacionError("La especialidad debe tener menos de 50 caracteres")
        