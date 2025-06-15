import unittest
from src.models.medico import Medico
from src.models.especialidad import Especialidad
from src.errors.custom_exception import ValidacionError, TipoDeDatoInvalidoError


class TestMedico(unittest.TestCase):
    def test_creacion_medico_valido(self):
        medico = Medico("Ana Gómez", "12345")
        self.assertEqual(medico.obtener_matricula(), "12345")
        self.assertIn("Ana Gómez", str(medico))
        self.assertIn("12345", str(medico))

    def test_nombre_no_texto(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Medico(123, "12345")

    def test_nombre_vacio(self):
        with self.assertRaises(ValidacionError):
            Medico("   ", "12345")

    def test_nombre_largo(self):
        with self.assertRaises(ValidacionError):
            Medico("a" * 51, "12345")

    def test_matricula_no_texto(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Medico("Ana Gómez", 12345)

    def test_matricula_vacia(self):
        with self.assertRaises(ValidacionError):
            Medico("Ana Gómez", "   ")

    def test_matricula_larga(self):
        with self.assertRaises(ValidacionError):
            Medico("Ana Gómez", "1" * 21)

    def test_agregar_especialidad_valida(self):
        medico = Medico("Ana Gómez", "12345")
        esp = Especialidad("Pediatría", ["lunes"])
        medico.agregar_especialidad(esp)
        self.assertIn("Pediatría", str(medico))

    def test_agregar_especialidad_invalida(self):
        medico = Medico("Ana Gómez", "12345")
        with self.assertRaises(TipoDeDatoInvalidoError):
            medico.agregar_especialidad("no_es_especialidad")

    def test_obtener_especialidad_para_dia(self):
        medico = Medico("Ana Gómez", "12345")
        esp = Especialidad("Pediatría", ["lunes", "martes"])
        medico.agregar_especialidad(esp)
        self.assertEqual(medico.obtener_especialidad_para_dia("LUNES"), "Pediatría")
        self.assertIsNone(medico.obtener_especialidad_para_dia("viernes"))


if __name__ == "__main__":
    unittest.main()
