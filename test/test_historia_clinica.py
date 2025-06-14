import unittest
from datetime import datetime, timedelta
from src.models.historia_clinica import HistoriaClinica
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.models.turno import Turno
from src.models.receta import Receta
from src.errors.custom_exception import TipoDeDatoInvalidoError


class TestHistoriaClinica(unittest.TestCase):
    def setUp(self):
        self.paciente = Paciente("Juan Perez", "12345678", datetime(1990, 1, 1))
        self.medico = Medico("Ana Gómez", "12345")
        self.turno = Turno(
            self.paciente, self.medico, datetime.now() + timedelta(days=1), "Pediatría"
        )
        self.receta = Receta(self.paciente, self.medico, ["Paracetamol"])

    def test_creacion_historia_clinica_valida(self):
        hc = HistoriaClinica(self.paciente)
        self.assertIn("Historia Clínica de", str(hc))
        self.assertIn("Sin turnos", str(hc))
        self.assertIn("Sin recetas", str(hc))

    def test_paciente_no_valido(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            HistoriaClinica("no_paciente")

    def test_agregar_turno_valido(self):
        hc = HistoriaClinica(self.paciente)
        hc.agregar_turno(self.turno)
        self.assertIn(str(self.turno), str(hc))
        self.assertEqual(len(hc.obtener_turnos()), 1)

    def test_agregar_turno_invalido(self):
        hc = HistoriaClinica(self.paciente)
        with self.assertRaises(TipoDeDatoInvalidoError):
            hc.agregar_turno("no_turno")

    def test_agregar_receta_valida(self):
        hc = HistoriaClinica(self.paciente)
        hc.agregar_receta(self.receta)
        self.assertIn(str(self.receta), str(hc))
        self.assertEqual(len(hc.obtener_recetas()), 1)

    def test_agregar_receta_invalida(self):
        hc = HistoriaClinica(self.paciente)
        with self.assertRaises(TipoDeDatoInvalidoError):
            hc.agregar_receta("no_receta")


if __name__ == "__main__":
    unittest.main()
