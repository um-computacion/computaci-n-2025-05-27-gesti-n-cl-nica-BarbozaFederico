import unittest
from datetime import datetime
from src.models.receta import Receta
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.errors.custom_exception import ValidacionError, TipoDeDatoInvalidoError

class TestReceta(unittest.TestCase):
    def setUp(self):
        self.paciente = Paciente("Juan Perez", "12345678", datetime(1990, 1, 1))
        self.medico = Medico("Ana Gómez", "12345")

    def test_creacion_receta_valida(self):
        receta = Receta(self.paciente, self.medico, ["Paracetamol", "Ibuprofeno"])
        self.assertIn("Paracetamol", str(receta))
        self.assertIn("Ibuprofeno", str(receta))
        self.assertIn("Juan Perez", str(receta))
        self.assertIn("Ana Gómez", str(receta))

    def test_paciente_no_valido(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Receta("no_paciente", self.medico, ["Paracetamol"])

    def test_medico_no_valido(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Receta(self.paciente, "no_medico", ["Paracetamol"])

    def test_medicamentos_no_lista(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Receta(self.paciente, self.medico, "Paracetamol")

    def test_medicamentos_lista_vacia(self):
        with self.assertRaises(ValidacionError):
            Receta(self.paciente, self.medico, [])

    def test_medicamento_no_texto(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Receta(self.paciente, self.medico, ["Paracetamol", 123])

    def test_medicamento_vacio(self):
        with self.assertRaises(ValidacionError):
            Receta(self.paciente, self.medico, ["Paracetamol", ""])

if __name__ == "__main__":
    unittest.main()