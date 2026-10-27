# Fase 4 - Prácticas Simuladas: Manejo de Excepciones

**Curso:** Programación (213023)
**Programa:** Ingeniería de Sistemas
**Universidad:** UNAD

## Descripción del Proyecto
Este proyecto simula un sistema de reservas diseñado para ser robusto y estable. Implementa manejo avanzado de excepciones en Python para garantizar que la aplicación nunca se detenga ante fallos de usuario o de red, registrando todos los eventos en un archivo de logs.

## Características Implementadas (Nivel Alto)
*   **Excepciones Personalizadas:** `ErrorReservaInvalida` y `ServicioNoDisponible` (en `excepciones.py`).
*   **Bloques de Control:** Uso completo de `try`, `except`, `else`, `finally`.
*   **Encadenamiento:** Uso de `raise ... from ...` para rastrear la causa raíz de los errores de conexión.
*   **Logging:** Registro detallado de eventos y errores en el archivo `sistema_reservas.log`.
*   **Estabilidad:** 10 simulaciones (válidas e inválidas) que demuestran que el sistema continúa funcionando.

## Integrantes del Equipo
*   [Cristian Camilo Silva Graciano] - Lógica y Excepciones
*   [Nombre Integrante 2] - Logging y Pruebas
*   [Nombre Integrante 3] - Documentación y GitHub

## Instrucciones de Ejecución
1. Clonar el repositorio o descargar los archivos.
2. Abrir la terminal en la carpeta del proyecto.
3. Ejecutar el comando:
   ```bash
   python sistema_reservas.py
