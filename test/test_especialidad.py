import unittest
from src.models.especialidad import Especialidad
from src.errors.custom_exception import ValidacionError, TipoDeDatoInvalidoError


class TestEspecialidad(unittest.TestCase):
    def test_creacion_especialidad_valida(self):
        esp = Especialidad("Pediatría", ["lunes", "miércoles", "viernes"])
        self.assertEqual(esp.obtener_especialidad(), "Pediatría")
        self.assertIn("Pediatría", str(esp))
        self.assertIn("lunes", str(esp))

    def test_tipo_no_texto(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Especialidad(123, ["lunes"])

    def test_tipo_vacio(self):
        with self.assertRaises(ValidacionError):
            Especialidad("   ", ["lunes"])

    def test_tipo_largo(self):
        with self.assertRaises(ValidacionError):
            Especialidad("a" * 51, ["lunes"])

    def test_dias_no_lista(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Especialidad("Cardiología", "lunes")

    def test_dias_lista_vacia(self):
        with self.assertRaises(ValidacionError):
            Especialidad("Cardiología", [])

    def test_dia_no_texto(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Especialidad("Cardiología", ["lunes", 2])

    def test_dia_vacio(self):
        with self.assertRaises(ValidacionError):
            Especialidad("Cardiología", ["lunes", ""])

    def test_verificar_dia_true(self):
        esp = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.assertTrue(esp.verificar_dia("LUNES"))
        self.assertTrue(esp.verificar_dia("miércoles"))

    def test_verificar_dia_false(self):
        esp = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.assertFalse(esp.verificar_dia("viernes"))


if __name__ == "__main__":
    unittest.main()
