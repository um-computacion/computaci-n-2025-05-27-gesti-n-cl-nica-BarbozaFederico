from .paciente import Paciente
from .turno import Turno
from .receta import Receta
from ..errors.custom_exception import TipoDeDatoInvalidoError, ValidacionError


class HistoriaClinica:
    """
    Clase que almacena la información médica de un paciente: turnos y recetas.
    """

    def __init__(self, paciente: Paciente):
        self.__asegurar_paciente_es_valido__(paciente)
        self.__paciente__ = paciente
        self.__turnos__: list[Turno] = []
        self.__recetas__: list[Receta] = []

    def agregar_turno(self, turno: Turno) -> None:
        self.__asegurar_turno_es_valido__(turno)
        self.__turnos__.append(turno)

    def agregar_receta(self, receta: Receta) -> None:
        self.__asegurar_receta_es_valida__(receta)
        self.__recetas__.append(receta)

    def obtener_turnos(self) -> list:
        return list(self.__turnos__)

    def obtener_recetas(self) -> list:
        return list(self.__recetas__)

    def __str__(self) -> str:
        turnos_str = (
            "\n".join(str(t) for t in self.__turnos__)
            if self.__turnos__
            else "Sin turnos"
        )
        recetas_str = (
            "\n".join(str(r) for r in self.__recetas__)
            if self.__recetas__
            else "Sin recetas"
        )
        return (
            f"Historia Clínica de {self.__paciente__}\n"
            f"--- Turnos ---\n{turnos_str}\n"
            f"--- Recetas ---\n{recetas_str}"
        )

    def __asegurar_paciente_es_valido__(self, paciente):
        if not isinstance(paciente, Paciente):
            raise TipoDeDatoInvalidoError("El paciente es invalido")

    def __asegurar_turno_es_valido__(self, turno):
        if not isinstance(turno, Turno):
            raise TipoDeDatoInvalidoError("El turno es invalido")

    def __asegurar_receta_es_valida__(self, receta):
        if not isinstance(receta, Receta):
            raise TipoDeDatoInvalidoError("La receta es invalida")
