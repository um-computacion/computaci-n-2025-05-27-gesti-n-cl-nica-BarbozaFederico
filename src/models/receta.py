from datetime import datetime
from .paciente import Paciente
from .medico import Medico
from ..errors.custom_exception import TipoDeDatoInvalidoError, ValidacionError
from ..utils.fechas import formatear_fecha


class Receta:
    """
    Representa una receta médica emitida por un médico a un paciente, incluyendo los medicamentos recetados y la fecha de emisión.
    """

    def __init__(self, paciente: Paciente, medico: Medico, medicamentos: list[str]):
        self.__asegurar_paciente_es_valido__(paciente)
        self.__asegurar_medico_es_valido__(medico)
        self.__asegurar_medicamentos_es_valido__(medicamentos)
        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__medicamentos__ = medicamentos
        self.__fecha__ = datetime.now()

    def __str__(self) -> str:
        medicamentos_str = ", ".join(self.__medicamentos__)
        return (
            f"Receta - Paciente: {self.__paciente__} | "
            f"Médico: {self.__medico__} | "
            f"Medicamentos: {medicamentos_str} | "
            f"Fecha: {formatear_fecha(self.__fecha__)}"
        )

    def __asegurar_paciente_es_valido__(self, paciente):
        if not isinstance(paciente, Paciente):
            raise TipoDeDatoInvalidoError("Paciente no es valido")

    def __asegurar_medico_es_valido__(self, medico):
        if not isinstance(medico, Medico):
            raise TipoDeDatoInvalidoError("Medico no es valido")

    def __asegurar_medicamentos_es_valido__(self, medicamentos):
        if not isinstance(medicamentos, list):
            raise TipoDeDatoInvalidoError("Los medicamentos deben estar en una lista")
        if not medicamentos:
            raise ValidacionError("Debe haber al menos un medicamento recetado")
        for medicamento in medicamentos:
            if not isinstance(medicamento, str):
                raise TipoDeDatoInvalidoError("Cada medicamento debe ser texto")
            if not medicamento.strip():
                raise ValidacionError("El nombre del medicamento no puede estar vacío")
