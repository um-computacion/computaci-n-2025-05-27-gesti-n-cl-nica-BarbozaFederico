class CustomException(Exception):
    def __init__(self, message: str):
        self.is_custom = True
        self.message = message
        super().__init__(self.message)


class ValidacionError(CustomException):
    pass


class TipoDeDatoInvalidoError(CustomException):
    pass