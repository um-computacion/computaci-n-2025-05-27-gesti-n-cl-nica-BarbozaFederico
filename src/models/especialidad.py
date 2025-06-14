from ..errors.custom_exception import TipoDeDatoInvalidoError, ValidacionError

class Especialidad:
    """
    Representa una especialidad médica junto con los días de atención asociados.
    """

    def __init__(self, tipo: str, dias: list[str]):
        self.__asegurar_tipo_es_valido__(tipo)
        self.__asegurar_dias_es_valido__(dias)
        self.__tipo__ = tipo
        self.__dias__ = []
        for d in dias:
            self.__dias__.append(d.lower())

    def obtener_especialidad(self) -> str:
        return self.__tipo__

    def verificar_dia(self, dia: str) -> bool:
        return dia.lower() in self.__dias__

    def __str__(self) -> str:
        dias_str = ", ".join(self.__dias__)
        return f"{self.__tipo__} (Días: {dias_str})"

    def __asegurar_tipo_es_valido__(self, tipo: str) -> None:
        """
        Verifica que el tipo de especialidad sea texto, no esté vacío y tenga menos de 50 caracteres.
        """
        if not isinstance(tipo, str):
            raise TipoDeDatoInvalidoError("El nombre de la especialidad debe ser texto")
        if not tipo.strip():
            raise ValidacionError("El nombre de la especialidad no puede estar vacío")
        if len(tipo) > 50:
            raise ValidacionError("El nombre de la especialidad debe tener menos de 50 caracteres")

    def __asegurar_dias_es_valido__(self, dias: list[str]) -> None:
        """
        Verifica que los días sean una lista de strings no vacía y que cada día sea texto no vacío.
        """
        if not isinstance(dias, list):
            raise TipoDeDatoInvalidoError("Los días deben estar en una lista")
        if not dias:
            raise ValidacionError("Debe haber al menos un día de atención")
        for dia in dias:
            if not isinstance(dia, str):
                raise TipoDeDatoInvalidoError("Cada día debe ser texto")
            if not dia.strip():
                raise ValidacionError("El nombre del día no puede estar vacío")
