# Diseño General del Sistema de Gestión de Clínica

## Arquitectura

El sistema está organizado en **capas** para separar responsabilidades y facilitar el mantenimiento:

- **Capa de Presentación:**  
  Implementada por la clase `CLI` (`src/cli/cli.py`). Es la interfaz de consola que interactúa con el usuario, mostrando menús, solicitando datos y mostrando resultados o errores.

- **Capa de Lógica de Negocio:**  
  Implementada por la clase `Clinica` (`src/models/clinica.py`). Centraliza la gestión de pacientes, médicos, turnos, recetas e historias clínicas, aplicando todas las reglas de negocio y validaciones.

- **Capa de Modelo:**  
  Incluye las clases de dominio como `Paciente`, `Medico`, `Especialidad`, `Turno`, `Receta` e `HistoriaClinica` (en `src/models/`). Cada clase valida sus propios datos y encapsula su comportamiento.

- **Capa de Errores:**  
  Excepciones personalizadas en `src/errors/` para manejar errores de validación, datos inválidos y reglas de negocio, permitiendo mensajes claros y controlados.

## Principios de Diseño

- **Separación de responsabilidades:**  
  La CLI solo interactúa con el usuario; la lógica de negocio está en `Clinica`; los modelos validan y representan entidades.

- **Validación exhaustiva:**  
  Todos los datos se validan tanto en la entrada por consola como en los modelos y la lógica de negocio.

- **Manejo centralizado de errores:**  
  Las excepciones personalizadas permiten capturar y mostrar mensajes claros al usuario final.

- **Acceso eficiente:**  
  Pacientes y médicos se almacenan en diccionarios para búsquedas rápidas por DNI o matrícula.

- **Normalización de datos:**  
  Los datos sensibles a mayúsculas/minúsculas (como especialidades y días) se almacenan en minúsculas para evitar inconsistencias.

## Flujo de Uso

1. El usuario navega por el menú de la CLI.
2. La CLI solicita y valida datos básicos.
3. La CLI llama a métodos de la clase `Clinica` para realizar operaciones.
4. `Clinica` valida reglas de negocio y actualiza los modelos.
5. Los resultados o errores se muestran al usuario por consola.

## Ventajas del diseño

- **Fácil de mantener y extender** gracias a la separación de capas.
- **Robusto ante errores** por el uso de excepciones personalizadas.
- **Escalable**: se pueden agregar nuevas funcionalidades o interfaces (por ejemplo, web) reutilizando la lógica de negocio y los modelos.


