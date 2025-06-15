from datetime import datetime
from .paciente import Paciente
from .medico import Medico
from .turno import Turno
from .historia_clinica import HistoriaClinica
from .receta import Receta
from ..errors.custom_exception import TipoDeDatoInvalidoError
from ..errors.excepciones_clinica import (
    PacienteNoEncontradoError,
    PacienteYaRegistradoError,
    MedicoNoEncontradoError,
    MedicoYaRegistradoError,
    TurnoOcupadoError,
    MedicoNoDisponibleError,
)


class Clinica:
    """
    Clase principal que representa el sistema de gestión de la clínica.
    """

    def __init__(
        self,
        pacientes: dict[str, Paciente],
        medicos: dict[str, Medico],
        turnos: list[Turno],
        historias_clinicas: dict[str, HistoriaClinica],
    ):
        if not isinstance(pacientes, dict):
            raise TipoDeDatoInvalidoError("pacientes debe ser un diccionario")
        if not isinstance(medicos, dict):
            raise TipoDeDatoInvalidoError("medicos debe ser un diccionario")
        if not isinstance(turnos, list):
            raise TipoDeDatoInvalidoError("turnos debe ser una lista")
        if not isinstance(historias_clinicas, dict):
            raise TipoDeDatoInvalidoError("historias_clinicas debe ser un diccionario")
        self.__pacientes__ = pacientes
        self.__medicos__ = medicos
        self.__turnos__ = turnos
        self.__historias_clinicas__ = historias_clinicas

    def agregar_paciente(self, paciente: Paciente):
        dni = paciente.obtener_dni()
        if dni in self.__pacientes__:
            raise PacienteYaRegistradoError(dni)
        self.__pacientes__[dni] = paciente
        self.__historias_clinicas__[dni] = HistoriaClinica(paciente)

    def agregar_medico(self, medico: Medico):
        matricula = medico.obtener_matricula()
        if matricula in self.__medicos__:
            raise MedicoYaRegistradoError(matricula)
        self.__medicos__[matricula] = medico

    def obtener_pacientes(self) -> list[Paciente]:
        return list(self.__pacientes__.values())

    def obtener_medicos(self) -> list[Medico]:
        return list(self.__medicos__.values())

    def obtener_medico_por_matricula(self, matricula: str) -> Medico:
        self.validar_existencia_medico(matricula)
        return self.__medicos__[matricula]

    def agendar_turno(
        self, dni: str, matricula: str, especialidad: str, fecha_hora: datetime
    ):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        self.validar_turno_no_duplicado(matricula, fecha_hora)
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)
        self.validar_especialidad_en_dia(medico, especialidad, dia_semana)
        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos__.append(turno)
        self.__historias_clinicas__[dni].agregar_turno(turno)

    def obtener_turnos(self) -> list[Turno]:
        return list(self.__turnos__)

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]):
        self.validar_existencia_paciente(dni)
        self.validar_existencia_medico(matricula)
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        receta = Receta(paciente, medico, medicamentos)
        self.__historias_clinicas__[dni].agregar_receta(receta)

    def obtener_historia_clinica(self, dni: str) -> HistoriaClinica:
        self.validar_existencia_paciente(dni)
        return self.__historias_clinicas__[dni]

    def validar_existencia_paciente(self, dni: str):
        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoError(dni)

    def validar_existencia_medico(self, matricula: str):
        if matricula not in self.__medicos__:
            raise MedicoNoEncontradoError(matricula)

    def validar_turno_no_duplicado(self, matricula: str, fecha_hora: datetime):
        for turno in self.__turnos__:
            if (
                turno.obtener_medico().obtener_matricula() == matricula
                and turno.obtener_fecha_hora() == fecha_hora
            ):
                raise TurnoOcupadoError()

    def obtener_dia_semana_en_espanol(self, fecha_hora: datetime) -> str:
        dias = [
            "lunes",
            "martes",
            "miercoles",
            "jueves",
            "viernes",
            "sabados",
            "domingos",
        ]
        return dias[fecha_hora.weekday()]

    def obtener_especialidad_disponible(self, medico: Medico, dia_semana: str) -> str:
        especialidad = medico.obtener_especialidad_para_dia(dia_semana)
        if especialidad is None:
            raise MedicoNoDisponibleError(medico.obtener_matricula(), dia_semana)
        return especialidad

    def validar_especialidad_en_dia(
        self, medico: Medico, especialidad_solicitada: str, dia_semana: str
    ):
        especialidad = medico.obtener_especialidad_para_dia(dia_semana)
        if especialidad is None or especialidad != especialidad_solicitada:
            raise MedicoNoDisponibleError(medico.obtener_matricula(), dia_semana)
