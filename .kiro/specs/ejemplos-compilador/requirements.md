# Requirements Document

## Introduction

Este documento especifica los requerimientos para crear 4 ejemplos básicos en Python que serán procesados por el compilador existente. Los ejemplos deben generar código intermedio (TAC) y código ensamblador que pueda ejecutarse en EMU8086 o DOSBox. Los ejemplos deben ser simples, sin funciones complejas, y demostrar diferentes capacidades del compilador.

## Glossary

- **Sistema de Compilación**: El conjunto de componentes que incluye el analizador léxico, sintáctico, semántico, generador TAC, optimizador y generador de código máquina
- **TAC (Three Address Code)**: Código intermedio de tres direcciones generado por el compilador
- **Código Ensamblador**: Código en lenguaje ensamblador x86 generado a partir del TAC
- **EMU8086**: Emulador de procesador 8086 para ejecutar código ensamblador
- **DOSBox**: Emulador de DOS para ejecutar programas compilados
- **Ejemplo Python**: Código fuente en Python simplificado que será procesado por el compilador

## Requirements

### Requirement 1

**User Story:** Como usuario del compilador, quiero un ejemplo de sistema de gestión de estudiantes con operaciones CRUD, para que pueda verificar que el compilador maneja correctamente variables, listas y operaciones básicas.

#### Acceptance Criteria

1. WHEN el usuario ejecuta el ejemplo de gestión de estudiantes THEN el Sistema de Compilación SHALL generar código Python válido con operaciones de alta, baja, actualización y visualización de estudiantes
2. WHEN el código Python es procesado THEN el Sistema de Compilación SHALL generar código TAC que represente todas las operaciones CRUD
3. WHEN el código TAC es procesado THEN el Sistema de Compilación SHALL generar código ensamblador x86 ejecutable
4. WHEN el código ensamblador es ejecutado en EMU8086 o DOSBox THEN el Sistema de Compilación SHALL producir resultados correctos para todas las operaciones CRUD
5. WHERE el ejemplo usa listas THEN el Sistema de Compilación SHALL manejar operaciones de append y acceso por índice correctamente

### Requirement 2

**User Story:** Como usuario del compilador, quiero un ejemplo de sistema de inventario usando estructuras de datos simples, para que pueda verificar que el compilador maneja correctamente múltiples variables relacionadas y operaciones aritméticas.

#### Acceptance Criteria

1. WHEN el usuario ejecuta el ejemplo de inventario THEN el Sistema de Compilación SHALL generar código Python válido con operaciones de gestión de productos y cantidades
2. WHEN el código Python incluye operaciones aritméticas THEN el Sistema de Compilación SHALL generar TAC optimizado con plegado de constantes
3. WHEN el código TAC es procesado THEN el Sistema de Compilación SHALL generar código ensamblador que maneje correctamente operaciones aritméticas
4. WHEN el código ensamblador es ejecutado THEN el Sistema de Compilación SHALL calcular correctamente totales, promedios y operaciones de inventario
5. WHERE el ejemplo usa múltiples variables THEN el Sistema de Compilación SHALL mantener correctamente la tabla de símbolos

### Requirement 3

**User Story:** Como usuario del compilador, quiero un ejemplo de procesamiento de cadenas, para que pueda verificar que el compilador maneja correctamente strings, concatenación y operaciones de longitud.

#### Acceptance Criteria

1. WHEN el usuario ejecuta el ejemplo de procesamiento de cadenas THEN el Sistema de Compilación SHALL generar código Python válido con operaciones de strings
2. WHEN el código Python usa la función len THEN el Sistema de Compilación SHALL generar TAC correcto para calcular longitud de cadenas
3. WHEN el código Python concatena strings THEN el Sistema de Compilación SHALL generar código ensamblador que maneje correctamente la concatenación
4. WHEN el código ensamblador es ejecutado THEN el Sistema de Compilación SHALL mostrar correctamente las cadenas procesadas
5. WHERE el ejemplo usa comparaciones de strings THEN el Sistema de Compilación SHALL generar código correcto para comparaciones

### Requirement 4

**User Story:** Como usuario del compilador, quiero un ejemplo de cálculo de factorial con recursión, para que pueda verificar que el compilador maneja correctamente llamadas recursivas y condiciones de parada.

#### Acceptance Criteria

1. WHEN el usuario ejecuta el ejemplo de factorial recursivo THEN el Sistema de Compilación SHALL generar código Python válido con función recursiva
2. WHEN el código Python incluye recursión THEN el Sistema de Compilación SHALL generar TAC que maneje correctamente la pila de llamadas
3. WHEN el código TAC es procesado THEN el Sistema de Compilación SHALL generar código ensamblador con manejo correcto de stack frames
4. WHEN el código ensamblador es ejecutado con valores de entrada válidos THEN el Sistema de Compilación SHALL calcular correctamente el factorial
5. WHERE el valor de entrada es 0 o 1 THEN el Sistema de Compilación SHALL retornar 1 como caso base

### Requirement 5

**User Story:** Como usuario del compilador, quiero que todos los ejemplos sean simples y sin código complicado, para que pueda entender fácilmente el proceso de compilación completo.

#### Acceptance Criteria

1. WHEN se crean los ejemplos THEN el Sistema de Compilación SHALL usar únicamente sintaxis básica de Python sin funciones avanzadas
2. WHEN se crean los ejemplos THEN el Sistema de Compilación SHALL evitar el uso de clases, decoradores o características avanzadas
3. WHEN se crean los ejemplos THEN el Sistema de Compilación SHALL usar únicamente operaciones soportadas por el compilador existente
4. WHEN se visualiza el código THEN el Sistema de Compilación SHALL mantener los ejemplos con menos de 50 líneas cada uno
5. WHERE se requieren estructuras de datos THEN el Sistema de Compilación SHALL usar únicamente listas y variables simples

### Requirement 6

**User Story:** Como usuario del compilador, quiero que el proceso de compilación sea completo y verificable, para que pueda confirmar que cada fase funciona correctamente.

#### Acceptance Criteria

1. WHEN se procesa un ejemplo THEN el Sistema de Compilación SHALL mostrar el código fuente Python original
2. WHEN se genera código intermedio THEN el Sistema de Compilación SHALL mostrar el TAC generado de forma legible
3. WHEN se genera código ensamblador THEN el Sistema de Compilación SHALL mostrar el código ASM completo
4. WHEN se ejecuta el código THEN el Sistema de Compilación SHALL proporcionar instrucciones claras para ejecutar en EMU8086 o DOSBox
5. WHERE ocurren errores THEN el Sistema de Compilación SHALL reportar errores con número de línea y descripción clara
