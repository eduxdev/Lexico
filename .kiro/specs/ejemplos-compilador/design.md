# Design Document

## Overview

Este documento describe el diseño para crear 4 ejemplos básicos en Python que demuestren las capacidades del compilador existente. Cada ejemplo será procesado a través de todas las fases del compilador: análisis léxico, sintáctico, semántico, generación de código intermedio (TAC), optimización y generación de código ensamblador x86.

Los ejemplos están diseñados para ser simples, educativos y ejecutables en EMU8086 o DOSBox, demostrando diferentes aspectos del compilador sin usar características avanzadas de Python.

## Architecture

### Componentes Existentes

El sistema de compilación ya implementado incluye:

1. **Lexer** (`python_compiler.py`): Análisis léxico con AFD
2. **Parser** (`python_compiler.py`): Análisis sintáctico LL(1) descendente recursivo
3. **Semantic Analyzer** (`semantic_analyzer.py`): Análisis semántico con tabla de símbolos
4. **TAC Generator** (`tac_generator.py`): Generador de código intermedio de tres direcciones
5. **TAC Optimizer** (`tac_optimizer.py`): Optimizador con 6 tipos de optimizaciones
6. **Machine Code Generator** (`machine_code_generator.py`): Generador de código ensamblador
7. **TAC Interpreter** (`tac_interpreter.py`): Intérprete para ejecutar TAC
8. **IDE** (`python_ide_complete.py`): Interfaz gráfica completa

### Flujo de Procesamiento

```
Código Python → Lexer → Tokens
              ↓
           Parser → AST
              ↓
    Semantic Analyzer → AST Validado + Tabla de Símbolos
              ↓
      TAC Generator → Código Intermedio (TAC)
              ↓
      TAC Optimizer → TAC Optimizado
              ↓
  Machine Code Gen → Código Ensamblador x86
              ↓
    EMU8086/DOSBox → Ejecución
```

## Components and Interfaces

### Ejemplo 1: Sistema de Gestión de Estudiantes

**Propósito**: Demostrar operaciones CRUD con listas

**Estructura**:
```python
# Inicialización
estudiantes = []
nombres = []
calificaciones = []

# Alta (Create)
estudiantes.append(1)
nombres.append("Juan")
calificaciones.append(85)

# Visualización (Read)
print(estudiantes[0])
print(nombres[0])
print(calificaciones[0])

# Actualización (Update)
calificaciones[0] = 90
print(calificaciones[0])

# Baja (Delete) - simulada con valor especial
calificaciones[0] = 0
print(calificaciones[0])
```

**Operaciones soportadas**:
- Creación de listas vacías
- Operación `append()` para agregar elementos
- Acceso por índice `lista[i]`
- Asignación por índice `lista[i] = valor`
- Función `print()` para visualización

### Ejemplo 2: Sistema de Inventario

**Propósito**: Demostrar operaciones aritméticas y múltiples variables

**Estructura**:
```python
# Variables de inventario
producto1 = 10
producto2 = 15
producto3 = 20

precio1 = 100
precio2 = 150
precio3 = 200

# Cálculo de total
total_productos = producto1 + producto2 + producto3
print(total_productos)

# Cálculo de valor total
valor_total = producto1 * precio1 + producto2 * precio2 + producto3 * precio3
print(valor_total)

# Actualización de inventario
producto1 = producto1 - 5
print(producto1)

# Promedio de precios
suma_precios = precio1 + precio2 + precio3
promedio = suma_precios / 3
print(promedio)
```

**Operaciones soportadas**:
- Asignación de variables
- Operaciones aritméticas: `+`, `-`, `*`, `/`
- Expresiones aritméticas complejas
- Optimización de plegado de constantes

### Ejemplo 3: Procesamiento de Cadenas

**Propósito**: Demostrar manejo de strings y función len()

**Estructura**:
```python
# Definición de cadenas
nombre = "Python"
apellido = "Compiler"

# Longitud de cadenas
len_nombre = len(nombre)
len_apellido = len(apellido)
print(len_nombre)
print(len_apellido)

# Comparaciones
if len_nombre > 5:
    print(1)
else:
    print(0)

# Uso de strings en listas
palabras = []
palabras.append(nombre)
palabras.append(apellido)
print(len(palabras))
```

**Operaciones soportadas**:
- Literales de string
- Función `len()` para strings y listas
- Comparaciones con strings
- Condicionales `if-else`
- Listas de strings

### Ejemplo 4: Cálculo de Factorial con Recursión

**Propósito**: Demostrar funciones recursivas y manejo de pila

**Estructura**:
```python
def factorial(n):
    if n == 0:
        return 1
    else:
        temp = n - 1
        result = factorial(temp)
        return n * result

# Casos de prueba
resultado1 = factorial(0)
print(resultado1)

resultado2 = factorial(1)
print(resultado2)

resultado3 = factorial(5)
print(resultado3)
```

**Operaciones soportadas**:
- Definición de funciones con `def`
- Parámetros de función
- Condicionales `if-else`
- Llamadas recursivas
- Instrucción `return`
- Operaciones aritméticas en recursión

## Data Models

### Estructura de Archivos de Ejemplos

Cada ejemplo será almacenado en un archivo Python individual:

```
ejemplos/
├── ejemplo1_estudiantes.py
├── ejemplo2_inventario.py
├── ejemplo3_cadenas.py
└── ejemplo4_factorial.py
```

### Formato de Salida

Para cada ejemplo, el sistema generará:

1. **Código Fuente** (`.py`): El código Python original
2. **Tokens** (`.tokens`): Lista de tokens del análisis léxico
3. **AST** (`.ast`): Representación del árbol de sintaxis abstracta
4. **TAC** (`.tac`): Código intermedio de tres direcciones
5. **TAC Optimizado** (`.tac.opt`): Código intermedio optimizado
6. **Código Ensamblador** (`.asm`): Código ensamblador x86

### Estructura de Datos del Compilador

El compilador utiliza las siguientes estructuras:

- **Token**: `(type, value, line, column)`
- **ASTNode**: Jerarquía de nodos (ProgramNode, AssignmentNode, etc.)
- **TACInstruction**: `(op, arg1, arg2, result)`
- **Symbol Table**: `{variable: {type, initialized, line}}`

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Código Python válido genera tokens sin errores
*For any* código Python sintácticamente válido de los ejemplos, el Lexer debe completar el análisis sin lanzar excepciones LexerError y producir una lista de tokens que termina con EOF.
**Validates: Requirements 1.1, 2.1, 3.1, 4.1**

### Property 2: TAC representa todas las operaciones del código fuente
*For any* código Python válido procesado, cada operación en el código fuente (asignación, operación aritmética, llamada a función, etc.) debe tener una representación correspondiente en el código TAC generado.
**Validates: Requirements 1.2**

### Property 3: Generación de código ensamblador es completa
*For any* código TAC válido, el generador de código máquina debe producir código ensamblador que incluya secciones `.data` y `.text`, y termine con instrucciones de salida.
**Validates: Requirements 1.3, 2.3**

### Property 4: Operaciones con listas generan instrucciones TAC correctas
*For any* código que use operaciones de listas (append, acceso por índice), el TAC generado debe incluir instrucciones LIST_APPEND, LIST_GET o LIST_SET correspondientes.
**Validates: Requirements 1.5**

### Property 5: Plegado de constantes optimiza expresiones aritméticas
*For any* expresión aritmética que contenga únicamente constantes numéricas, el optimizador TAC debe reducirla a una única constante en el TAC optimizado.
**Validates: Requirements 2.2**

### Property 6: Tabla de símbolos mantiene todas las variables
*For any* código con múltiples variables, la tabla de símbolos del analizador semántico debe contener una entrada para cada variable declarada, sin duplicados ni pérdidas.
**Validates: Requirements 2.5**

### Property 7: Función len() genera llamadas TAC correctas
*For any* uso de la función len() en el código, el TAC generado debe incluir una instrucción CALL con arg1='len' y el argumento correspondiente.
**Validates: Requirements 3.2**

### Property 8: Concatenación y comparación de strings genera código correcto
*For any* operación de concatenación o comparación de strings, el TAC debe generar instrucciones ADD (para concatenación) o instrucciones de comparación (EQ, NEQ, etc.) apropiadas.
**Validates: Requirements 3.3, 3.5**

### Property 9: Funciones recursivas generan etiquetas y llamadas correctas
*For any* función recursiva definida, el TAC debe incluir una etiqueta de función (LABEL func_nombre), instrucciones CALL para llamadas recursivas, y instrucciones RETURN.
**Validates: Requirements 4.2**

### Property 10: Stack frames en código ensamblador para funciones
*For any* código TAC que contenga definiciones de funciones, el código ensamblador generado debe incluir instrucciones de manejo de pila (push/pop o equivalentes) para preservar el contexto.
**Validates: Requirements 4.3**

### Property 11: Visualización completa del proceso de compilación
*For any* ejemplo procesado, el sistema debe generar y mostrar todas las representaciones intermedias: tokens, AST, TAC, TAC optimizado y código ensamblador.
**Validates: Requirements 6.1, 6.2, 6.3**

### Property 12: Errores reportados con información de línea
*For any* código con errores sintácticos o semánticos, el compilador debe lanzar una excepción que incluya el número de línea donde ocurrió el error.
**Validates: Requirements 6.5**

## Error Handling

### Tipos de Errores

1. **LexerError**: Caracteres inválidos, strings sin cerrar, números mal formados
2. **ParserError**: Sintaxis incorrecta, tokens inesperados, indentación inconsistente
3. **SemanticError**: Variables no declaradas, tipos incompatibles, operaciones inválidas

### Estrategia de Manejo

- **Panic Mode**: El lexer y parser lanzan excepciones inmediatamente al encontrar errores
- **Continuación**: El analizador semántico acumula múltiples errores antes de reportar
- **Mensajes Descriptivos**: Todos los errores incluyen línea, columna y descripción clara

### Validaciones Específicas por Ejemplo

**Ejemplo 1 (Estudiantes)**:
- Verificar que las listas existan antes de append
- Validar índices dentro de rango
- Confirmar tipos compatibles en asignaciones

**Ejemplo 2 (Inventario)**:
- Validar operaciones aritméticas con tipos numéricos
- Verificar división por cero
- Confirmar variables inicializadas antes de uso

**Ejemplo 3 (Cadenas)**:
- Validar que len() reciba un argumento
- Verificar tipos compatibles en comparaciones
- Confirmar strings bien formados

**Ejemplo 4 (Factorial)**:
- Validar definición de función antes de llamada
- Verificar número correcto de argumentos
- Confirmar return en todas las ramas

## Testing Strategy

### Enfoque Dual de Testing

Este proyecto utilizará tanto **unit tests** como **property-based tests** para garantizar la corrección:

- **Unit tests**: Verifican ejemplos específicos y casos edge
- **Property tests**: Verifican propiedades universales sobre todos los inputs posibles

Ambos tipos de tests son complementarios y necesarios para cobertura completa.

### Unit Testing

**Framework**: pytest

**Casos de prueba unitarios**:

1. **Test de Lexer**:
   - Tokenización correcta de cada ejemplo
   - Manejo de keywords, identificadores, números, strings
   - Detección de errores léxicos

2. **Test de Parser**:
   - Construcción correcta del AST para cada ejemplo
   - Manejo de precedencia de operadores
   - Detección de errores sintácticos

3. **Test de Semantic Analyzer**:
   - Validación de tabla de símbolos
   - Detección de variables no declaradas
   - Verificación de tipos

4. **Test de TAC Generator**:
   - Generación correcta de instrucciones TAC
   - Manejo de temporales y etiquetas
   - Representación de estructuras de control

5. **Test de Optimizer**:
   - Plegado de constantes funciona
   - Eliminación de código muerto
   - Propagación de constantes

6. **Test de Machine Code Generator**:
   - Generación de secciones .data y .text
   - Asignación de registros
   - Instrucciones de salto y comparación

### Property-Based Testing

**Framework**: Hypothesis (Python)

**Configuración**: Cada property test ejecutará mínimo 100 iteraciones

**Properties a implementar**:

Cada property-based test debe incluir un comentario con el formato:
`# Feature: ejemplos-compilador, Property {número}: {descripción}`

1. **Property Test 1**: Código válido no lanza errores léxicos
   - Generar código Python válido aleatorio
   - Verificar que Lexer completa sin excepciones

2. **Property Test 2**: TAC preserva semántica de operaciones
   - Generar código Python con operaciones variadas
   - Verificar que cada operación tiene representación TAC

3. **Property Test 3**: Código ensamblador es completo
   - Generar TAC aleatorio válido
   - Verificar estructura completa del código generado

4. **Property Test 4**: Listas mantienen consistencia
   - Generar código con operaciones de listas
   - Verificar instrucciones TAC correctas

5. **Property Test 5**: Optimización preserva semántica
   - Generar expresiones aritméticas
   - Verificar que TAC optimizado es equivalente

6. **Property Test 6**: Tabla de símbolos es completa
   - Generar código con múltiples variables
   - Verificar todas las variables están en la tabla

7. **Property Test 7**: len() genera código correcto
   - Generar código con llamadas a len()
   - Verificar instrucciones CALL en TAC

8. **Property Test 8**: Strings se manejan correctamente
   - Generar código con operaciones de strings
   - Verificar TAC correcto para strings

9. **Property Test 9**: Recursión genera estructura correcta
   - Generar funciones recursivas
   - Verificar etiquetas y llamadas en TAC

10. **Property Test 10**: Errores incluyen información de línea
    - Generar código con errores intencionales
    - Verificar que excepciones incluyen número de línea

### Estrategia de Ejecución

1. **Fase 1**: Crear los 4 ejemplos básicos
2. **Fase 2**: Procesar cada ejemplo a través del compilador
3. **Fase 3**: Verificar salidas intermedias (tokens, AST, TAC)
4. **Fase 4**: Verificar código ensamblador generado
5. **Fase 5**: Documentar instrucciones de ejecución en EMU8086/DOSBox
6. **Fase 6**: Ejecutar unit tests
7. **Fase 7**: Ejecutar property-based tests

### Criterios de Éxito

- Todos los ejemplos compilan sin errores
- Todas las fases de compilación producen salida válida
- Código ensamblador es sintácticamente correcto
- Unit tests pasan al 100%
- Property tests pasan al 100% (mínimo 100 iteraciones cada uno)
- Documentación de ejecución está completa

## Implementation Notes

### Restricciones de Sintaxis

Los ejemplos deben usar únicamente:
- Variables simples y listas
- Operaciones aritméticas básicas: +, -, *, /, %
- Comparaciones: ==, !=, <, >, <=, >=
- Estructuras de control: if-else, while, for
- Funciones: def, return
- Funciones built-in: print, len, range, append
- Literales: números, strings

### Características NO Soportadas

Los ejemplos NO deben usar:
- Clases y objetos
- Decoradores
- Comprensiones de listas
- Lambdas
- Imports
- Excepciones (try-except)
- Generadores
- Context managers (with)
- Operadores lógicos (and, or, not)

### Limitaciones del Compilador

El compilador existente tiene las siguientes limitaciones conocidas:
- No soporta funciones con valores de retorno complejos
- Recursión limitada por stack del ensamblador
- No hay garbage collection para listas
- Strings son inmutables
- No hay soporte para diccionarios en código ensamblador

### Formato de Salida para EMU8086

El código ensamblador generado debe:
- Usar sintaxis compatible con EMU8086
- Incluir directivas .data y .text
- Usar registros de 8086: AX, BX, CX, DX, SI, DI, SP, BP
- Terminar con instrucción de salida apropiada
- Incluir comentarios explicativos

### Instrucciones de Ejecución

Para cada ejemplo, se proporcionará:
1. Comando para ejecutar el compilador
2. Ubicación del archivo .asm generado
3. Pasos para cargar en EMU8086
4. Resultados esperados de la ejecución
5. Troubleshooting común
