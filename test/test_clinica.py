import unittest
from datetime import datetime, timedelta
from src.models.clinica import Clinica
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.models.especialidad import Especialidad
from src.errors.excepciones_clinica import (
    PacienteNoEncontradoError,
    PacienteYaRegistradoError,
    MedicoNoEncontradoError,
    MedicoYaRegistradoError,
    TurnoOcupadoError,
    MedicoNoDisponibleError,
)
from src.errors.custom_exception import TipoDeDatoInvalidoError


class TestClinica(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica({}, {}, [], {})
        self.paciente = Paciente("Juan Perez", "12345678", datetime(1990, 1, 1))
        self.medico = Medico("Ana Gómez", "12345")
        self.especialidad = Especialidad("Pediatría", ["lunes", "miércoles"])

    def test_registro_exitoso_paciente(self):
        self.clinica.agregar_paciente(self.paciente)
        pacientes = self.clinica.obtener_pacientes()
        self.assertEqual(len(pacientes), 1)
        self.assertEqual(pacientes[0].obtener_dni(), "12345678")

    def test_registro_exitoso_medico(self):
        self.clinica.agregar_medico(self.medico)
        medicos = self.clinica.obtener_medicos()
        self.assertEqual(len(medicos), 1)
        self.assertEqual(medicos[0].obtener_matricula(), "12345")

    def test_prevencion_registro_duplicado_paciente(self):
        self.clinica.agregar_paciente(self.paciente)
        with self.assertRaises(PacienteYaRegistradoError):
            self.clinica.agregar_paciente(self.paciente)

    def test_prevencion_registro_duplicado_medico(self):
        self.clinica.agregar_medico(self.medico)
        with self.assertRaises(MedicoYaRegistradoError):
            self.clinica.agregar_medico(self.medico)

    def test_verificacion_parametros_invalidos_clinica(self):
        with self.assertRaises(TipoDeDatoInvalidoError):
            Clinica("no_es_dict", {}, [], {})
        with self.assertRaises(TipoDeDatoInvalidoError):
            Clinica({}, "no_es_dict", [], {})
        with self.assertRaises(TipoDeDatoInvalidoError):
            Clinica({}, {}, "no_es_lista", {})
        with self.assertRaises(TipoDeDatoInvalidoError):
            Clinica({}, {}, [], "no_es_dict")

    def test_agregar_especialidad_a_medico_registrado(self):
        self.clinica.agregar_medico(self.medico)
        self.medico.agregar_especialidad(self.especialidad)
        medico_recuperado = self.clinica.obtener_medico_por_matricula("12345")
        self.assertEqual(
            medico_recuperado.obtener_especialidad_para_dia("lunes"), "Pediatría"
        )

    def test_error_medico_no_registrado(self):
        with self.assertRaises(MedicoNoEncontradoError):
            self.clinica.obtener_medico_por_matricula("99999")

    def test_agendamiento_turno_correcto(self):
        self.clinica.agregar_paciente(self.paciente)
        self.medico.agregar_especialidad(self.especialidad)
        self.clinica.agregar_medico(self.medico)

        fecha = datetime.now() + timedelta(days=1)
        while fecha.weekday() != 0:
            fecha += timedelta(days=1)

        self.clinica.agendar_turno("12345678", "12345", "Pediatría", fecha)
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0].obtener_fecha_hora(), fecha)

    def test_evitar_turno_duplicado(self):
        self.clinica.agregar_paciente(self.paciente)
        self.medico.agregar_especialidad(self.especialidad)
        self.clinica.agregar_medico(self.medico)

        fecha = datetime.now() + timedelta(days=1)
        while fecha.weekday() != 0:  # 0 = lunes
            fecha += timedelta(days=1)

        self.clinica.agendar_turno("12345678", "12345", "Pediatría", fecha)
        with self.assertRaises(TurnoOcupadoError):
            self.clinica.agendar_turno("12345678", "12345", "Pediatría", fecha)

    def test_error_paciente_no_existe(self):
        self.medico.agregar_especialidad(self.especialidad)
        self.clinica.agregar_medico(self.medico)

        fecha = datetime.now() + timedelta(days=1)
        with self.assertRaises(PacienteNoEncontradoError):
            self.clinica.agendar_turno("99999999", "12345", "Pediatría", fecha)

    def test_error_medico_no_existe_turno(self):
        self.clinica.agregar_paciente(self.paciente)

        fecha = datetime.now() + timedelta(days=1)
        with self.assertRaises(MedicoNoEncontradoError):
            self.clinica.agendar_turno("12345678", "99999", "Pediatría", fecha)

    def test_error_medico_no_atiende_especialidad(self):
        self.clinica.agregar_paciente(self.paciente)
        self.medico.agregar_especialidad(Especialidad("Cardiología", ["lunes"]))
        self.clinica.agregar_medico(self.medico)

        fecha = datetime.now() + timedelta(days=1)
        while fecha.weekday() != 0:  # 0 = lunes
            fecha += timedelta(days=1)

        with self.assertRaises(MedicoNoDisponibleError):
            self.clinica.agendar_turno("12345678", "12345", "Pediatría", fecha)

    def test_error_medico_no_trabaja_ese_dia(self):
        self.clinica.agregar_paciente(self.paciente)
        self.medico.agregar_especialidad(self.especialidad)
        self.clinica.agregar_medico(self.medico)

        fecha = datetime.now() + timedelta(days=1)
        while fecha.weekday() != 1:
            fecha += timedelta(days=1)

        with self.assertRaises(MedicoNoDisponibleError):
            self.clinica.agendar_turno("12345678", "12345", "Pediatría", fecha)

    def test_emision_receta_exitosa(self):
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)

        self.clinica.emitir_receta("12345678", "12345", ["Paracetamol"])
        historia = self.clinica.obtener_historia_clinica("12345678")
        recetas = historia.obtener_recetas()
        self.assertEqual(len(recetas), 1)

    def test_error_paciente_no_existe_receta(self):
        self.clinica.agregar_medico(self.medico)

        with self.assertRaises(PacienteNoEncontradoError):
            self.clinica.emitir_receta("99999999", "12345", ["Paracetamol"])

    def test_error_medico_no_existe_receta(self):
        self.clinica.agregar_paciente(self.paciente)

        with self.assertRaises(MedicoNoEncontradoError):
            self.clinica.emitir_receta("12345678", "99999", ["Paracetamol"])

    def test_turnos_y_recetas_guardados_en_historia(self):
        self.clinica.agregar_paciente(self.paciente)
        self.medico.agregar_especialidad(self.especialidad)
        self.clinica.agregar_medico(self.medico)

        fecha = datetime.now() + timedelta(days=1)
        while fecha.weekday() != 0:
            fecha += timedelta(days=1)

        self.clinica.agendar_turno("12345678", "12345", "Pediatría", fecha)

        self.clinica.emitir_receta("12345678", "12345", ["Paracetamol"])

        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_turnos()), 1)
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_obtener_historia_clinica_paciente_no_existente(self):
        with self.assertRaises(PacienteNoEncontradoError):
            self.clinica.obtener_historia_clinica("99999999")


if __name__ == "__main__":
    unittest.main()
