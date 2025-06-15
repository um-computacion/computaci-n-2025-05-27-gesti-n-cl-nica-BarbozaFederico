from .custom_exception import CustomException



class PacienteNoEncontradoError(CustomException):
    def __init__(self, dni: str):
        self.dni = dni
        self.message = f"El paciente con dni {dni} no se encuentra registrado"
        super().__init__(self.message)

class PacienteYaRegistradoError(CustomException):
    def __init__(self, dni: str):
        self.dni = dni
        self.message = f"El paciente con dni {dni} ya se encuentra registrado"
        super().__init__(self.message)

class MedicoNoEncontradoError(CustomException):
    def __init__(self, matricula: str):
        self.matricula = matricula
        self.message = f"El médico con matricula {matricula} no se encuentra registrado"
        super().__init__(self.message)

class MedicoYaRegistradoError(CustomException):
    def __init__(self, matricula: str):
        self.matricula = matricula
        self.message = f"El médico con matricula {matricula} ya se encuentra registrado"
        super().__init__(self.message)  

class TurnoOcupadoError(CustomException):
    def __init__(self):
        self.message = f"Ya existe un turno para esa fecha y hora"
        super().__init__(self.message)

class MedicoNoDisponibleError(CustomException):
    def __init__(self, matricula: str, dia_semana: str):
        self.matricula = matricula
        self.dia_semana = dia_semana
        self.message = f"El médico con matricula {matricula} no está disponible para la semana {dia_semana}"
        super().__init__(self.message)