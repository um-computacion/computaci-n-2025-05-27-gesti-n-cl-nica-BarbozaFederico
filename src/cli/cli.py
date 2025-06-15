from datetime import datetime
from src.models.clinica import Clinica
from src.models.paciente import Paciente
from src.models.medico import Medico
from src.models.especialidad import Especialidad
from src.errors.custom_exception import CustomException, TipoDeDatoInvalidoError, ValidacionError

class CLI:
    def __init__(self, clinica: Clinica):
        self.clinica = clinica

    def mostrar_menu(self):
        print("\n--- Menú Clínica ---")
        print("1) Agregar paciente")
        print("2) Agregar médico")
        print("3) Agendar turno")
        print("4) Agregar especialidad a médico")
        print("5) Emitir receta")
        print("6) Ver historia clínica")
        print("7) Ver todos los turnos")
        print("8) Ver todos los pacientes")
        print("9) Ver todos los médicos")
        print("0) Salir")

    def solicitar_fecha(self, mensaje="Ingrese fecha (dd-mm-yyyy): "):
        while True:
            fecha_str = input(mensaje).strip()
            if not fecha_str:
                print(" Error: La fecha no puede estar vacía. Formato esperado: dd-mm-yyyy")
                continue
            try:
                return datetime.strptime(fecha_str, "%d-%m-%Y")
            except ValueError:
                print(" Error: Formato de fecha inválido. Use el formato dd-mm-yyyy (ejemplo: 25-12-2000)")

    def solicitar_fecha_hora(self, mensaje="Ingrese fecha y hora (dd-mm-yyyy hh-mm): "):
        while True:
            fecha_str = input(mensaje).strip()
            if not fecha_str:
                print(" Error: La fecha y hora no pueden estar vacías. Formato esperado: dd-mm-yyyy hh-mm")
                continue
            try:
                return datetime.strptime(fecha_str, "%d-%m-%Y %H-%M")
            except ValueError:
                print(" Error: Formato de fecha y hora inválido. Use el formato dd-mm-yyyy hh-mm (ejemplo: 25-12-2024 14-30)")

    def solicitar_entrada_no_vacia(self, mensaje):
        while True:
            entrada = input(mensaje).strip()
            if entrada:
                return entrada
            print(" Error: Este campo no puede estar vacío.")

    def run(self):
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()
            try:
                if opcion == "1":
                    self.agregar_paciente()
                elif opcion == "2":
                    self.agregar_medico()
                elif opcion == "3":
                    self.agendar_turno()
                elif opcion == "4":
                    self.agregar_especialidad_a_medico()
                elif opcion == "5":
                    self.emitir_receta()
                elif opcion == "6":
                    self.ver_historia_clinica()
                elif opcion == "7":
                    self.ver_todos_los_turnos()
                elif opcion == "8":
                    self.ver_todos_los_pacientes()
                elif opcion == "9":
                    self.ver_todos_los_medicos()
                elif opcion == "0":
                    print("Hasta luego!")
                    break
                else:
                    print(" Opción inválida. Por favor, seleccione una opción del 0 al 9.")
            except CustomException as e:
                print(f" Error: {e}")
            except Exception as e:
                print(" Error inesperado: Algo salió mal. Por favor, intente nuevamente.")

    def agregar_paciente(self):
        print("\n--- Agregar Paciente ---")
        nombre = self.solicitar_entrada_no_vacia("Nombre: ")
        dni = self.solicitar_entrada_no_vacia("DNI: ")
        fecha_nac = self.solicitar_fecha("Fecha de nacimiento (dd-mm-yyyy): ")
        paciente = Paciente(nombre, dni, fecha_nac)
        self.clinica.agregar_paciente(paciente)
        print("✓ Paciente agregado correctamente.")

    def agregar_medico(self):
        print("\n--- Agregar Médico ---")
        nombre = self.solicitar_entrada_no_vacia("Nombre: ")
        matricula = self.solicitar_entrada_no_vacia("Matrícula: ").lower()
        medico = Medico(nombre, matricula)
        
        print("Agregue especialidades (deje vacío para terminar):")
        while True:
            tipo = input("Especialidad: ").strip()
            if not tipo:
                break
            
            while True:
                dias = input("Días de atención (separados por coma,sin tildes y en plural, ej: lunes,martes,miercoles,sabados,domingos): ").strip()
                if not dias:
                    print(" Error: Debe ingresar al menos un día de atención.")
                    continue
                    
                dias_lista = []
                for dia in dias.split(","):
                    dia_limpio = dia.strip().lower()
                    if dia_limpio:
                        dias_lista.append(dia_limpio)
                
                if dias_lista:
                    break
                print(" Error: No se encontraron días válidos. Intente nuevamente.")
            
            especialidad = Especialidad(tipo.lower(), dias_lista)
            medico.agregar_especialidad(especialidad)
            print(f"✓ Especialidad '{tipo}' agregada.")
        
        self.clinica.agregar_medico(medico)
        print("✓ Médico agregado correctamente.")

    def agendar_turno(self):
        print("\n--- Agendar Turno ---")
        dni = self.solicitar_entrada_no_vacia("DNI del paciente: ")
        matricula = self.solicitar_entrada_no_vacia("Matrícula del médico: ").lower()
        especialidad = self.solicitar_entrada_no_vacia("Especialidad: ").lower()
        fecha_hora = self.solicitar_fecha_hora("Fecha y hora (dd-mm-yyyy hh-mm): ")
        self.clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
        print("✓ Turno agendado correctamente.")

    def agregar_especialidad_a_medico(self):
        print("\n--- Agregar Especialidad a Médico ---")
        matricula = self.solicitar_entrada_no_vacia("Matrícula del médico: ").lower()
        medico = self.clinica.obtener_medico_por_matricula(matricula)
        tipo = self.solicitar_entrada_no_vacia("Especialidad: ").lower()
        
        while True:
            dias = input("Días de atención (separados por coma,sin tildes y en plural, ej: lunes,martes,miercoles,sabados,domingos): ").strip()
            if not dias:
                print(" Error: Debe ingresar al menos un día de atención.")
                continue
                
            dias_lista = []
            for dia in dias.split(","):
                dia_limpio = dia.strip().lower()
                if dia_limpio:
                    dias_lista.append(dia_limpio)
            
            if dias_lista:
                break
            print(" Error: No se encontraron días válidos. Intente nuevamente.")
        
        especialidad = Especialidad(tipo, dias_lista)
        medico.agregar_especialidad(especialidad)
        print("✓ Especialidad agregada correctamente.")

    def emitir_receta(self):
        print("\n--- Emitir Receta ---")
        dni = self.solicitar_entrada_no_vacia("DNI del paciente: ")
        matricula = self.solicitar_entrada_no_vacia("Matrícula del médico: ").lower()
        
        while True:
            medicamentos = input("Medicamentos (separados por coma): ").strip()
            if not medicamentos:
                print(" Error: Debe ingresar al menos un medicamento.")
                continue
                
            lista_medicamentos = []
            for med in medicamentos.split(","):
                med_limpio = med.strip()
                if med_limpio:
                    lista_medicamentos.append(med_limpio)
            
            if lista_medicamentos:
                break
            print(" Error: No se encontraron medicamentos válidos. Intente nuevamente.")
        
        self.clinica.emitir_receta(dni, matricula, lista_medicamentos)
        print("✓ Receta emitida correctamente.")

    def ver_historia_clinica(self):
        print("\n--- Ver Historia Clínica ---")
        dni = self.solicitar_entrada_no_vacia("DNI del paciente: ")
        historia = self.clinica.obtener_historia_clinica(dni)
        print(historia)

    def ver_todos_los_turnos(self):
        print("\n--- Todos los Turnos ---")
        turnos = self.clinica.obtener_turnos()
        if not turnos:
            print("No hay turnos registrados.")
        else:
            for t in turnos:
                print(t)

    def ver_todos_los_pacientes(self):
        print("\n--- Todos los Pacientes ---")
        pacientes = self.clinica.obtener_pacientes()
        if not pacientes:
            print("No hay pacientes registrados.")
        else:
            for p in pacientes:
                print(p)

    def ver_todos_los_medicos(self):
        print("\n--- Todos los Médicos ---")
        medicos = self.clinica.obtener_medicos()
        if not medicos:
            print("No hay médicos registrados.")
        else:
            for m in medicos:
                print(m)
