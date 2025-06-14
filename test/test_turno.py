import unittest
from datetime import datetime, timedelta
from src.models.turno import Turno
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.errors.custom_exception import ValidacionError, TipoDeDatoInvalidoError


class TestTurno(unittest.TestCase):
    def setUp(self):
        self.paciente = Paciente("Juan Perez", "12345678", datetime(1990, 1, 1))
        self.medico = Medico("Ana Gómez", "12345")
        self.fecha_futura = datetime.now() + timedelta(days=1)

    def test_creacion_turno_valido(self):
        turno = Turno(self.paciente, self.medico, self.fecha_futura, "Pediatría")
        self.assertEqual(turno.obtener_medico(), self.medico)
        self.assertEqual(turno.obtener_fecha_hora(), self.fecha_futura)
        self.assertIn("Pediatría", str(turno))
        self.assertIn("Juan Perez", str(turno))
        self.assertIn("Ana Gómez", str(turno))

    def test_paciente_no_valido(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Turno("no_paciente", self.medico, self.fecha_futura, "Pediatría")

    def test_medico_no_valido(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Turno(self.paciente, "no_medico", self.fecha_futura, "Pediatría")

    def test_fecha_no_datetime(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Turno(self.paciente, self.medico, "2025-06-15", "Pediatría")

    def test_fecha_pasada(self):
        fecha_pasada = datetime.now() - timedelta(days=1)
        with self.assertRaises(ValidacionError):
            Turno(self.paciente, self.medico, fecha_pasada, "Pediatría")

    def test_especialidad_no_texto(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Turno(self.paciente, self.medico, self.fecha_futura, 123)

    def test_especialidad_vacia(self):
        with self.assertRaises(ValidacionError):
            Turno(self.paciente, self.medico, self.fecha_futura, "   ")

    def test_especialidad_larga(self):
        with self.assertRaises(ValidacionError):
            Turno(self.paciente, self.medico, self.fecha_futura, "a" * 51)


if __name__ == "__main__":
    unittest.main()
