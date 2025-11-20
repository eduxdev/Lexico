# Guía de Compilación - Compilador Python a Ensamblador x86

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Proceso de Compilación](#proceso-de-compilación)
4. [Comandos de Ejecución](#comandos-de-ejecución)
5. [Ubicación de Archivos Generados](#ubicación-de-archivos-generados)
6. [Ejemplos Incluidos](#ejemplos-incluidos)
7. [Ejecución en EMU8086/DOSBox](#ejecución-en-emu8086dosbox)
8. [Resultados Esperados](#resultados-esperados)
9. [Troubleshooting](#troubleshooting)

---

## Introducción

Este compilador procesa código Python simplificado y lo transforma en código ensamblador x86 ejecutable en EMU8086 o DOSBox. El proceso de compilación consta de 7 fases principales:

1. **Análisis Léxico** - Tokenización del código fuente
2. **Análisis Sintáctico** - Construcción del AST (Abstract Syntax Tree)
3. **Análisis Semántico** - Validación de tipos y tabla de símbolos
4. **Generación TAC** - Código intermedio de tres direcciones
5. **Optimización TAC** - Optimizaciones sobre el código intermedio
6. **Generación de Código Máquina** - Código ensamblador x86
7. **Ejecución** - En EMU8086 o DOSBox

---

## Requisitos Previos

### Software Necesario

- **Python 3.7+** - Para ejecutar el compilador
- **EMU8086** o **DOSBox** - Para ejecutar el código ensamblador generado

### Archivos del Compilador

Asegúrese de tener los siguientes archivos en el directorio del proyecto:

```
proyecto/
├── python_compiler.py          # Lexer y Parser
├── semantic_analyzer.py        # Analizador semántico
├── tac_generator.py           # Generador de código intermedio
├── tac_optimizer.py           # Optimizador TAC
├── machine_code_generator.py  # Generador de código ensamblador
├── process_examples.py        # Script de procesamiento
├── verify_compilation.py      # Script de verificación
└── ejemplos/                  # Directorio de ejemplos
    ├── ejemplo1_estudiantes.py
    ├── ejemplo2_inventario.py
    ├── ejemplo3_cadenas.py
    └── ejemplo4_factorial.py
```

---

## Proceso de Compilación

### Descripción de las Fases

#### Fase 1: Análisis Léxico
El **Lexer** lee el código fuente carácter por carácter y lo convierte en una secuencia de tokens.

**Entrada:** Código Python (`.py`)  
**Salida:** Lista de tokens (`.tokens`)

**Ejemplo de tokens:**
```
1. Token(type='KEYWORD', value='def', line=1, column=1)
2. Token(type='IDENTIFIER', value='factorial', line=1, column=5)
3. Token(type='LPAREN', value='(', line=1, column=14)
```

#### Fase 2: Análisis Sintáctico
El **Parser** toma los tokens y construye un árbol de sintaxis abstracta (AST) que representa la estructura del programa.

**Entrada:** Lista de tokens  
**Salida:** AST (`.ast`)

**Ejemplo de AST:**
```
ProgramNode
  statements:
    FunctionDefNode
      name: factorial
      params: ['n']
      body:
        IfNode
          condition: BinaryOpNode
```

#### Fase 3: Análisis Semántico
El **Semantic Analyzer** valida el AST, verifica tipos, y construye la tabla de símbolos.

**Entrada:** AST  
**Salida:** AST validado + Tabla de símbolos (`.symbols`)

**Ejemplo de tabla de símbolos:**
```
Variable             Tipo            Inicializada    Línea
--------------------------------------------------------------------------------
n                    int             Sí              1
temp                 int             Sí              3
result               int             Sí              4
```

#### Fase 4: Generación de Código Intermedio (TAC)
El **TAC Generator** convierte el AST en código intermedio de tres direcciones.

**Entrada:** AST validado  
**Salida:** Código TAC (`.tac`)

**Ejemplo de TAC:**
```
1. LABEL func_factorial
2. PARAM n
3. t1 = n == 0
4. IF_FALSE t1 GOTO L1
5. RETURN 1
6. LABEL L1
```

#### Fase 5: Optimización TAC
El **TAC Optimizer** aplica optimizaciones al código intermedio:
- Plegado de constantes
- Propagación de constantes
- Eliminación de código muerto
- Eliminación de asignaciones redundantes
- Simplificación algebraica
- Reducción de fuerza

**Entrada:** Código TAC  
**Salida:** Código TAC optimizado (`.tac.opt`)

#### Fase 6: Generación de Código Ensamblador
El **Machine Code Generator** traduce el TAC optimizado a código ensamblador x86.

**Entrada:** Código TAC optimizado  
**Salida:** Código ensamblador (`.asm`)

**Ejemplo de código ensamblador:**
```asm
.data
    n DW 0
    temp DW 0
    result DW 0

.text
    MOV AX, @DATA
    MOV DS, AX
    
func_factorial:
    ; Código de la función
    RET
```

---

## Comandos de Ejecución

### Opción 1: Procesar Todos los Ejemplos

Para compilar todos los ejemplos de una vez:

```bash
python process_examples.py
```

Este comando:
- Procesa los 4 ejemplos incluidos
- Genera todos los archivos intermedios
- Guarda las salidas en el directorio `output/`
- Muestra un resumen del procesamiento

**Salida esperada:**
```
====================================================================================================
Procesando: ejemplo1_estudiantes
====================================================================================================

Fase 1: Leyendo código fuente...
✓ Código fuente leído correctamente

Fase 2: Análisis Léxico...
✓ 45 tokens generados
  Guardado en: output/ejemplo1_estudiantes.tokens

Fase 3: Análisis Sintáctico...
✓ AST generado correctamente
  Guardado en: output/ejemplo1_estudiantes.ast

...

====================================================================================================
✓ Procesamiento completo exitoso para ejemplo1_estudiantes
====================================================================================================
```

### Opción 2: Procesar un Ejemplo Específico

Para compilar un solo ejemplo:

```bash
python process_examples.py ejemplos/ejemplo1_estudiantes.py
```

Este comando procesa únicamente el ejemplo especificado y muestra toda la información de compilación.

### Opción 3: Verificar Compilación

Para verificar que todos los ejemplos compilan correctamente sin generar archivos:

```bash
python verify_compilation.py
```

Este comando:
- Ejecuta todas las fases de compilación
- Verifica que no hay errores
- Muestra un resumen de éxito/fallo
- No genera archivos de salida

**Salida esperada:**
```
============================================================
COMPILATION VERIFICATION FOR ALL EXAMPLES
============================================================

============================================================
Verifying: ejemplos/ejemplo1_estudiantes.py
============================================================
✓ Source code loaded
✓ Lexer: 45 tokens generated
✓ Parser: AST generated
✓ Semantic Analyzer: 6 variables in symbol table
✓ TAC Generator: 28 TAC instructions generated
✓ TAC Optimizer: 25 optimized TAC instructions
✓ Machine Code Generator: 87 lines of assembly code

✅ SUCCESS: ejemplos/ejemplo1_estudiantes.py compiled successfully!

...

============================================================
SUMMARY
============================================================
✅ PASS: ejemplos/ejemplo1_estudiantes.py
✅ PASS: ejemplos/ejemplo2_inventario.py
✅ PASS: ejemplos/ejemplo3_cadenas.py
✅ PASS: ejemplos/ejemplo4_factorial.py

Total: 4/4 examples compiled successfully

🎉 All examples compile correctly!
```

### Opción 4: Usar el IDE Completo

Para usar la interfaz gráfica:

```bash
python python_ide_complete.py
```

El IDE proporciona:
- Editor de código con resaltado de sintaxis
- Botones para ejecutar cada fase de compilación
- Visualización de resultados en tiempo real
- Manejo de errores con información detallada

---

## Ubicación de Archivos Generados

Todos los archivos generados se guardan en el directorio `output/` con la siguiente estructura:

```
output/
├── ejemplo1_estudiantes.tokens      # Tokens del análisis léxico
├── ejemplo1_estudiantes.ast         # Árbol de sintaxis abstracta
├── ejemplo1_estudiantes.symbols     # Tabla de símbolos
├── ejemplo1_estudiantes.tac         # Código intermedio TAC
├── ejemplo1_estudiantes.tac.opt     # Código TAC optimizado
├── ejemplo1_estudiantes.asm         # Código ensamblador x86
├── ejemplo2_inventario.tokens
├── ejemplo2_inventario.ast
├── ejemplo2_inventario.symbols
├── ejemplo2_inventario.tac
├── ejemplo2_inventario.tac.opt
├── ejemplo2_inventario.asm
├── ejemplo3_cadenas.tokens
├── ejemplo3_cadenas.ast
├── ejemplo3_cadenas.symbols
├── ejemplo3_cadenas.tac
├── ejemplo3_cadenas.tac.opt
├── ejemplo3_cadenas.asm
├── ejemplo4_factorial.tokens
├── ejemplo4_factorial.ast
├── ejemplo4_factorial.symbols
├── ejemplo4_factorial.tac
├── ejemplo4_factorial.tac.opt
└── ejemplo4_factorial.asm
```

### Descripción de Archivos

| Extensión | Descripción | Fase |
|-----------|-------------|------|
| `.tokens` | Lista de tokens generados por el Lexer | Fase 1 |
| `.ast` | Representación textual del AST | Fase 2 |
| `.symbols` | Tabla de símbolos con variables y tipos | Fase 3 |
| `.tac` | Código intermedio de tres direcciones | Fase 4 |
| `.tac.opt` | Código TAC después de optimizaciones | Fase 5 |
| `.asm` | Código ensamblador x86 ejecutable | Fase 6 |

---

## Ejemplos Incluidos

### Ejemplo 1: Sistema de Gestión de Estudiantes
**Archivo:** `ejemplos/ejemplo1_estudiantes.py`

**Propósito:** Demostrar operaciones CRUD con listas

**Características:**
- Creación de listas vacías
- Operación `append()` para agregar elementos
- Acceso por índice `lista[i]`
- Actualización de elementos
- Simulación de eliminación

**Código:**
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

# Baja (Delete)
calificaciones[0] = 0
print(calificaciones[0])
```

### Ejemplo 2: Sistema de Inventario
**Archivo:** `ejemplos/ejemplo2_inventario.py`

**Propósito:** Demostrar operaciones aritméticas y optimización

**Características:**
- Múltiples variables relacionadas
- Operaciones aritméticas: `+`, `-`, `*`, `/`
- Expresiones complejas
- Plegado de constantes en optimización

**Código:**
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

# Actualización
producto1 = producto1 - 5
print(producto1)

# Promedio
suma_precios = precio1 + precio2 + precio3
promedio = suma_precios / 3
print(promedio)
```

### Ejemplo 3: Procesamiento de Cadenas
**Archivo:** `ejemplos/ejemplo3_cadenas.py`

**Propósito:** Demostrar manejo de strings y función `len()`

**Características:**
- Literales de string
- Función `len()` para strings y listas
- Comparaciones con strings
- Condicionales `if-else`
- Listas de strings

**Código:**
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

# Listas de strings
palabras = []
palabras.append(nombre)
palabras.append(apellido)
print(len(palabras))
```

### Ejemplo 4: Cálculo de Factorial Recursivo
**Archivo:** `ejemplos/ejemplo4_factorial.py`

**Propósito:** Demostrar funciones recursivas y manejo de pila

**Características:**
- Definición de funciones con `def`
- Parámetros de función
- Llamadas recursivas
- Instrucción `return`
- Manejo de stack frames

**Código:**
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

---

## Ejecución en EMU8086/DOSBox

### Opción A: Usar EMU8086

EMU8086 es un emulador de procesador 8086 con entorno de desarrollo integrado.

#### Paso 1: Instalar EMU8086
1. Descargar EMU8086 desde el sitio oficial
2. Instalar siguiendo las instrucciones del instalador
3. Ejecutar EMU8086

#### Paso 2: Cargar el Código Ensamblador
1. Abrir EMU8086
2. Ir a **File → Open**
3. Navegar al directorio `output/`
4. Seleccionar el archivo `.asm` deseado (ej: `ejemplo1_estudiantes.asm`)
5. Click en **Open**

#### Paso 3: Compilar en EMU8086
1. Click en el botón **Compile** (o presionar F5)
2. EMU8086 generará el archivo ejecutable
3. Verificar que no hay errores en la ventana de compilación

#### Paso 4: Ejecutar el Programa
1. Click en el botón **Emulate** (o presionar F9)
2. En el emulador, click en **Run** (o presionar F5)
3. Observar la salida en la pantalla del emulador

#### Paso 5: Ver Resultados
- Los valores impresos aparecerán en la pantalla del emulador
- Puede usar **Step** (F7) para ejecutar instrucción por instrucción
- Puede ver los registros y memoria en tiempo real

### Opción B: Usar DOSBox

DOSBox es un emulador de DOS que puede ejecutar programas compilados.

#### Paso 1: Instalar DOSBox
1. Descargar DOSBox desde www.dosbox.com
2. Instalar siguiendo las instrucciones
3. Ejecutar DOSBox

#### Paso 2: Montar el Directorio
```
mount c: C:\ruta\a\tu\proyecto
c:
cd output
```

#### Paso 3: Compilar con MASM/TASM
Si tiene MASM o TASM instalado en DOSBox:

```
masm ejemplo1_estudiantes.asm;
link ejemplo1_estudiantes.obj;
```

O con TASM:
```
tasm ejemplo1_estudiantes.asm
tlink ejemplo1_estudiantes.obj
```

#### Paso 4: Ejecutar el Programa
```
ejemplo1_estudiantes.exe
```

### Configuración de DOSBox

Editar el archivo `dosbox.conf` para optimizar la experiencia:

```ini
[cpu]
core=auto
cputype=auto
cycles=max

[dosbox]
memsize=16

[autoexec]
# Montar automáticamente el directorio del proyecto
mount c: C:\ruta\a\tu\proyecto
c:
```

---

## Resultados Esperados

### Ejemplo 1: Sistema de Gestión de Estudiantes

**Salida esperada en EMU8086/DOSBox:**
```
1
Juan
85
90
0
```

**Explicación:**
- `1` - ID del primer estudiante
- `Juan` - Nombre del primer estudiante
- `85` - Calificación inicial
- `90` - Calificación actualizada
- `0` - Calificación después de "eliminación"

### Ejemplo 2: Sistema de Inventario

**Salida esperada:**
```
45
8500
5
150
```

**Explicación:**
- `45` - Total de productos (10 + 15 + 20)
- `8500` - Valor total del inventario
- `5` - Producto1 después de restar 5
- `150` - Promedio de precios

### Ejemplo 3: Procesamiento de Cadenas

**Salida esperada:**
```
6
8
1
2
```

**Explicación:**
- `6` - Longitud de "Python"
- `8` - Longitud de "Compiler"
- `1` - Resultado de la comparación (len_nombre > 5 es verdadero)
- `2` - Número de elementos en la lista de palabras

### Ejemplo 4: Cálculo de Factorial

**Salida esperada:**
```
1
1
120
```

**Explicación:**
- `1` - factorial(0) = 1
- `1` - factorial(1) = 1
- `120` - factorial(5) = 5 × 4 × 3 × 2 × 1 = 120

---

## Troubleshooting

### Problema 1: Error "ModuleNotFoundError"

**Síntoma:**
```
ModuleNotFoundError: No module named 'python_compiler'
```

**Solución:**
- Asegúrese de estar en el directorio correcto del proyecto
- Verifique que todos los archivos del compilador estén presentes
- Ejecute el comando desde el directorio raíz del proyecto

### Problema 2: Error "FileNotFoundError" al procesar ejemplos

**Síntoma:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'ejemplos/ejemplo1_estudiantes.py'
```

**Solución:**
- Verifique que el directorio `ejemplos/` existe
- Verifique que los archivos de ejemplo están presentes
- Use rutas relativas desde el directorio raíz del proyecto

### Problema 3: Errores de Compilación en el Lexer

**Síntoma:**
```
❌ Error Léxico: Invalid character '@' at line 5, column 10
```

**Solución:**
- El código Python contiene caracteres no soportados
- Revise la sintaxis del código fuente
- Asegúrese de usar solo las características soportadas por el compilador
- Consulte la sección "Características NO Soportadas" en el diseño

### Problema 4: Errores de Compilación en el Parser

**Síntoma:**
```
❌ Error Sintáctico: Unexpected token 'IDENTIFIER' at line 3
```

**Solución:**
- Verifique la sintaxis del código Python
- Asegúrese de que la indentación es correcta
- Verifique que todos los paréntesis, corchetes y llaves están balanceados
- Use solo estructuras de control soportadas

### Problema 5: Errores Semánticos

**Síntoma:**
```
❌ Error Semántico: Variable 'x' used before initialization at line 10
```

**Solución:**
- Inicialice todas las variables antes de usarlas
- Verifique que los nombres de variables son consistentes
- Asegúrese de que las operaciones son compatibles con los tipos

### Problema 6: El directorio `output/` no se crea

**Síntoma:**
Los archivos generados no aparecen

**Solución:**
- El script crea automáticamente el directorio `output/`
- Verifique permisos de escritura en el directorio del proyecto
- Ejecute el script con permisos adecuados

### Problema 7: Código ensamblador no se ejecuta en EMU8086

**Síntoma:**
EMU8086 muestra errores al compilar el archivo `.asm`

**Solución:**
- Verifique que el archivo `.asm` se generó correctamente
- Abra el archivo y verifique que tiene las secciones `.data` y `.text`
- Asegúrese de que EMU8086 está configurado para sintaxis Intel
- Verifique que no hay caracteres especiales en el archivo

### Problema 8: DOSBox no encuentra el archivo

**Síntoma:**
```
File not found: ejemplo1_estudiantes.asm
```

**Solución:**
- Verifique que montó correctamente el directorio en DOSBox
- Use el comando `dir` para listar archivos y confirmar la ubicación
- Asegúrese de estar en el directorio correcto (`cd output`)

### Problema 9: Resultados incorrectos en la ejecución

**Síntoma:**
Los valores impresos no coinciden con los esperados

**Solución:**
- Verifique que el código fuente Python es correcto
- Revise el archivo `.tac` para verificar el código intermedio
- Revise el archivo `.tac.opt` para ver si las optimizaciones son correctas
- Compare con los resultados esperados en esta guía

### Problema 10: Python no reconoce el comando

**Síntoma:**
```
'python' is not recognized as an internal or external command
```

**Solución:**
- Instale Python 3.7 o superior
- Agregue Python al PATH del sistema
- Use `python3` en lugar de `python` en sistemas Unix/Linux
- Verifique la instalación con `python --version`

### Problema 11: Errores de codificación de caracteres

**Síntoma:**
```
UnicodeDecodeError: 'charmap' codec can't decode byte...
```

**Solución:**
- Los archivos deben estar en codificación UTF-8
- Guarde los archivos con codificación UTF-8 en su editor
- Verifique que no hay caracteres especiales no soportados

### Problema 12: Optimizador elimina código necesario

**Síntoma:**
El código optimizado no produce los mismos resultados

**Solución:**
- Esto puede indicar un bug en el optimizador
- Compare los archivos `.tac` y `.tac.opt`
- Reporte el problema con el ejemplo específico
- Como workaround, use el TAC sin optimizar

---

## Recursos Adicionales

### Documentos del Proyecto

- `ANALISIS_REQUERIMIENTOS.md` - Análisis detallado de requerimientos
- `.kiro/specs/ejemplos-compilador/requirements.md` - Especificación de requerimientos
- `.kiro/specs/ejemplos-compilador/design.md` - Documento de diseño
- `.kiro/specs/ejemplos-compilador/tasks.md` - Plan de implementación

### Comandos Útiles

```bash
# Ver ayuda de un script
python process_examples.py --help

# Procesar todos los ejemplos
python process_examples.py

# Procesar un ejemplo específico
python process_examples.py ejemplos/ejemplo1_estudiantes.py

# Verificar compilación de todos los ejemplos
python verify_compilation.py

# Ejecutar tests
python test_ejemplos.py

# Abrir el IDE
python python_ide_complete.py
```

### Estructura del Proyecto

```
proyecto/
├── python_compiler.py          # Lexer y Parser
├── semantic_analyzer.py        # Analizador semántico
├── tac_generator.py           # Generador TAC
├── tac_optimizer.py           # Optimizador
├── machine_code_generator.py  # Generador de código máquina
├── tac_interpreter.py         # Intérprete TAC
├── process_examples.py        # Procesamiento de ejemplos
├── verify_compilation.py      # Verificación de compilación
├── test_ejemplos.py           # Tests automatizados
├── python_ide_complete.py     # IDE gráfico
├── GUIA_COMPILACION.md        # Esta guía
├── ejemplos/                  # Ejemplos de código
│   ├── ejemplo1_estudiantes.py
│   ├── ejemplo2_inventario.py
│   ├── ejemplo3_cadenas.py
│   └── ejemplo4_factorial.py
└── output/                    # Archivos generados
    ├── *.tokens
    ├── *.ast
    ├── *.symbols
    ├── *.tac
    ├── *.tac.opt
    └── *.asm
```

---

## Contacto y Soporte

Para reportar problemas o solicitar ayuda:

1. Verifique esta guía de troubleshooting
2. Revise los archivos de salida generados (`.tokens`, `.ast`, `.tac`, etc.)
3. Ejecute `verify_compilation.py` para diagnóstico
4. Documente el error con el mensaje completo y el ejemplo que lo causa

---

**Última actualización:** 2025-11-20  
**Versión del compilador:** 1.0
