import unittest
from datetime import datetime, timedelta
from src.models.paciente import Paciente
from src.errors.custom_exception import ValidacionError, TipoDeDatoInvalidoError


class TestPaciente(unittest.TestCase):
    def test_creacion_paciente_valido(self):
        paciente = Paciente("Juan Perez", "12345678", datetime(1990, 1, 1))
        self.assertEqual(paciente.obtener_dni(), "12345678")
        self.assertIn("Juan Perez", str(paciente))
        self.assertIn("12345678", str(paciente))

    def test_nombre_no_texto(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Paciente(123, "12345678", datetime(1990, 1, 1))

    def test_nombre_vacio(self):
        with self.assertRaises(ValidacionError):
            Paciente("   ", "12345678", datetime(1990, 1, 1))

    def test_nombre_largo(self):
        with self.assertRaises(ValidacionError):
            Paciente("a" * 51, "12345678", datetime(1990, 1, 1))

    def test_dni_no_texto(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Paciente("Juan Perez", 12345678, datetime(1990, 1, 1))

    def test_dni_vacio(self):
        with self.assertRaises(ValidacionError):
            Paciente("Juan Perez", "   ", datetime(1990, 1, 1))

    def test_dni_no_numerico(self):
        with self.assertRaises(ValidacionError):
            Paciente("Juan Perez", "abc123", datetime(1990, 1, 1))

    def test_fecha_nacimiento_no_datetime(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Paciente("Juan Perez", "12345678", "1990-01-01")

    def test_fecha_nacimiento_futura(self):
        fecha_futura = datetime.now() + timedelta(days=1)
        with self.assertRaises(ValidacionError):
            Paciente("Juan Perez", "12345678", fecha_futura)


if __name__ == "__main__":
    unittest.main()
