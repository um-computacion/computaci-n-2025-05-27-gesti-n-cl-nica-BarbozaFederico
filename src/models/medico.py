from .especialidad import Especialidad
from ..errors.custom_exception import TipoDeDatoInvalidoError, ValidacionError

class Medico:
    """
    Representa a un médico del sistema, con sus especialidades y matrícula profesional.
    """

    def __init__(self, nombre: str, matricula: str):
        self.__asegurar_nombre_es_valido__(nombre)
        self.__asegurar_matricula_es_valida__(matricula)
        self.__nombre__ = nombre
        self.__matricula__ = matricula
        self.__especialidades__:list[Especialidad]= []

    def agregar_especialidad(self, especialidad: Especialidad):
        if not isinstance(especialidad, Especialidad):
            raise TipoDeDatoInvalidoError("Debe agregar una instancia de Especialidad")
        self.__especialidades__.append(especialidad)

    def obtener_matricula(self) -> str:
        return self.__matricula__

    def obtener_especialidad_para_dia(self, dia: str) -> str | None:
        for esp in self.__especialidades__:
            if esp.verificar_dia(dia):
                return esp.obtener_especialidad()
        return None

    def __str__(self) -> str:
        especialidades_str = ", ".join([esp.obtener_especialidad() for esp in self.__especialidades__])
        return f"Médico: {self.__nombre__} - Matrícula: {self.__matricula__} - Especialidades: {especialidades_str}"

    def __asegurar_nombre_es_valido__(self, nombre: str) -> None:
        if not isinstance(nombre, str):
            raise TipoDeDatoInvalidoError("El nombre del médico debe ser texto")
        if not nombre.strip():
            raise ValidacionError("El nombre del médico no puede estar vacío")
        if len(nombre) > 50:
            raise ValidacionError("El nombre del médico debe tener menos de 50 caracteres")

    def __asegurar_matricula_es_valida__(self, matricula: str) -> None:
        if not isinstance(matricula, str):
            raise TipoDeDatoInvalidoError("La matrícula debe ser texto")
        if not matricula.strip():
            raise ValidacionError("La matrícula no puede estar vacía")
        if len(matricula) > 20:
            raise ValidacionError("La matrícula debe tener menos de 20 caracteres")