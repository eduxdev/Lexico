# Implementation Plan

- [x] 1. Crear estructura de directorios para ejemplos





  - Crear carpeta `ejemplos/` en la raíz del proyecto
  - Preparar archivos para los 4 ejemplos
  - _Requirements: 5.1, 5.3_

- [x] 2. Implementar Ejemplo 1: Sistema de Gestión de Estudiantes






  - [x] 2.1 Escribir código Python para operaciones CRUD con listas





    - Crear listas para estudiantes, nombres y calificaciones
    - Implementar operación de alta (append)
    - Implementar operación de lectura (acceso por índice)
    - Implementar operación de actualización (asignación por índice)
    - Implementar operación de baja (asignación a 0)
    - Agregar prints para visualización
    - _Requirements: 1.1, 1.5_

  - [x] 2.2 Write property test for validación de código Python


    - **Property 1: Código Python válido genera tokens sin errores**
    - **Validates: Requirements 1.1**


  - [x] 2.3 Write property test para operaciones con listas

    - **Property 4: Operaciones con listas generan instrucciones TAC correctas**
    - **Validates: Requirements 1.5**


- [x] 3. Implementar Ejemplo 2: Sistema de Inventario










  - [x] 3.1 Escribir código Python para gestión de inventario





    - Declarar variables para productos y precios
    - Implementar cálculo de totales con operaciones aritméticas
    - Implementar cálculo de valor total con expresiones complejas
    - Implementar actualización de inventario
    - Implementar cálculo de promedio con división
    - Agregar prints para resultados
    - _Requirements: 2.1, 2.5_

  - [x] 3.2 Write property test para plegado de constantes


    - **Property 5: Plegado de constantes optimiza expresiones aritméticas**
    - **Validates: Requirements 2.2**

  - [x] 3.3 Write property test para tabla de símbolos


    - **Property 6: Tabla de símbolos mantiene todas las variables**
    - **Validates: Requirements 2.5**

- [x] 4. Implementar Ejemplo 3: Procesamiento de Cadenas





  - [x] 4.1 Escribir código Python para operaciones con strings


    - Declarar variables de tipo string
    - Usar función len() para calcular longitudes
    - Implementar comparaciones con strings
    - Usar condicionales if-else
    - Crear listas de strings
    - Agregar prints para visualización
    - _Requirements: 3.1, 3.2, 3.5_

  - [x] 4.2 Write property test para función len()


    - **Property 7: Función len() genera llamadas TAC correctas**
    - **Validates: Requirements 3.2**

  - [x] 4.3 Write property test para operaciones con strings


    - **Property 8: Concatenación y comparación de strings genera código correcto**
    - **Validates: Requirements 3.3, 3.5**

- [x] 5. Implementar Ejemplo 4: Cálculo de Factorial Recursivo






  - [x] 5.1 Escribir código Python con función recursiva

    - Definir función factorial con parámetro n
    - Implementar caso base (n == 0 retorna 1)
    - Implementar caso recursivo (n * factorial(n-1))
    - Crear variables temporales para claridad
    - Agregar llamadas de prueba con diferentes valores
    - Agregar prints para resultados
    - _Requirements: 4.1, 4.2_

  - [x] 5.2 Write property test para funciones recursivas


    - **Property 9: Funciones recursivas generan etiquetas y llamadas correctas**
    - **Validates: Requirements 4.2**


  - [x] 5.3 Write property test para stack frames

    - **Property 10: Stack frames en código ensamblador para funciones**
    - **Validates: Requirements 4.3**

- [x] 6. Checkpoint - Verificar que todos los ejemplos compilan





  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Crear script de procesamiento de ejemplos




  - [x] 7.1 Implementar función para procesar un ejemplo completo


    - Leer código fuente Python
    - Ejecutar Lexer y guardar tokens
    - Ejecutar Parser y guardar AST
    - Ejecutar Semantic Analyzer y guardar tabla de símbolos
    - Ejecutar TAC Generator y guardar código intermedio
    - Ejecutar TAC Optimizer y guardar TAC optimizado
    - Ejecutar Machine Code Generator y guardar código ensamblador
    - _Requirements: 6.1, 6.2, 6.3_

  - [x] 7.2 Implementar función de visualización de resultados


    - Mostrar código fuente original
    - Mostrar tokens generados
    - Mostrar AST formateado
    - Mostrar TAC generado
    - Mostrar TAC optimizado
    - Mostrar código ensamblador
    - _Requirements: 6.1, 6.2, 6.3_

  - [x] 7.3 Write property test para visualización completa


    - **Property 11: Visualización completa del proceso de compilación**
    - **Validates: Requirements 6.1, 6.2, 6.3**

- [x] 8. Implementar manejo de errores y validación





  - [x] 8.1 Agregar validación de errores en procesamiento


    - Capturar LexerError con información de línea
    - Capturar ParserError con información de línea
    - Capturar SemanticError con información de línea
    - Formatear mensajes de error claramente
    - _Requirements: 6.5_

  - [x] 8.2 Write property test para reporte de errores


    - **Property 12: Errores reportados con información de línea**
    - **Validates: Requirements 6.5**

- [x] 9. Crear documentación de ejecución





  - [x] 9.1 Documentar proceso de compilación


    - Escribir instrucciones paso a paso
    - Incluir comandos de ejecución
    - Documentar ubicación de archivos generados
    - _Requirements: 6.4_



  - [x] 9.2 Documentar ejecución en EMU8086/DOSBox





    - Escribir pasos para cargar código en EMU8086
    - Documentar configuración de DOSBox
    - Incluir resultados esperados para cada ejemplo
    - Agregar sección de troubleshooting
    - _Requirements: 6.4_


- [x] 10. Crear tests unitarios para validación




  - [x] 10.1 Implementar tests para Ejemplo 1 (Estudiantes)


    - Test de tokenización correcta
    - Test de parsing sin errores
    - Test de generación TAC con operaciones de listas
    - Test de código ensamblador generado
    - _Requirements: 1.1, 1.2, 1.3, 1.5_

  - [x] 10.2 Implementar tests para Ejemplo 2 (Inventario)

    - Test de operaciones aritméticas
    - Test de optimización de constantes
    - Test de tabla de símbolos completa
    - Test de código ensamblador con operaciones aritméticas
    - _Requirements: 2.1, 2.2, 2.3, 2.5_

  - [x] 10.3 Implementar tests para Ejemplo 3 (Cadenas)

    - Test de manejo de strings
    - Test de función len()
    - Test de comparaciones de strings
    - Test de código ensamblador con strings
    - _Requirements: 3.1, 3.2, 3.3, 3.5_

  - [x] 10.4 Implementar tests para Ejemplo 4 (Factorial)

    - Test de definición de función
    - Test de recursión en TAC
    - Test de stack frames en ensamblador
    - Test de casos base (0 y 1)
    - _Requirements: 4.1, 4.2, 4.3, 4.5_

- [x] 11. Implementar property-based tests adicionales





  - [x] 11.1 Write property test para TAC completo


    - **Property 2: TAC representa todas las operaciones del código fuente**
    - **Validates: Requirements 1.2**

  - [x] 11.2 Write property test para código ensamblador completo


    - **Property 3: Generación de código ensamblador es completa**
    - **Validates: Requirements 1.3, 2.3**

- [x] 12. Checkpoint Final - Verificar todo el sistema





  - Ensure all tests pass, ask the user if questions arise.

- [x] 13. Crear script principal de demostración





  - [x] 13.1 Implementar script que procesa todos los ejemplos


    - Procesar Ejemplo 1 y mostrar resultados
    - Procesar Ejemplo 2 y mostrar resultados
    - Procesar Ejemplo 3 y mostrar resultados
    - Procesar Ejemplo 4 y mostrar resultados
    - Generar reporte resumen
    - _Requirements: 5.4, 6.1, 6.2, 6.3_

  - [x] 13.2 Agregar opciones de línea de comandos

    - Opción para procesar ejemplo individual
    - Opción para mostrar solo una fase específica
    - Opción para guardar salidas en archivos
    - Opción para modo verbose
    - _Requirements: 6.1, 6.2, 6.3_
