# Guía de Ejecución en EMU8086 y DOSBox

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Opción A: EMU8086](#opción-a-emu8086)
3. [Opción B: DOSBox](#opción-b-dosbox)
4. [Resultados Esperados por Ejemplo](#resultados-esperados-por-ejemplo)
5. [Troubleshooting Específico](#troubleshooting-específico)
6. [Comparación EMU8086 vs DOSBox](#comparación-emu8086-vs-dosbox)

---

## Introducción

Esta guía proporciona instrucciones detalladas para ejecutar el código ensamblador generado por el compilador en dos entornos diferentes:

- **EMU8086**: Emulador con IDE integrado (recomendado para principiantes)
- **DOSBox**: Emulador de DOS (recomendado para usuarios avanzados)

Ambos entornos son capaces de ejecutar código ensamblador x86 de 16 bits generado por nuestro compilador.

---

## Opción A: EMU8086

### ¿Qué es EMU8086?

EMU8086 es un emulador de microprocesador 8086 con un entorno de desarrollo integrado que incluye:
- Editor de código con resaltado de sintaxis
- Ensamblador integrado
- Depurador visual
- Visualización de registros y memoria en tiempo real
- Interfaz gráfica amigable

### Instalación de EMU8086

#### Windows

1. **Descargar EMU8086**
   - Visitar: http://www.emu8086.com/
   - Click en "Download" o "Free Download"
   - Descargar el instalador (aproximadamente 5 MB)

2. **Instalar EMU8086**
   - Ejecutar el archivo descargado (`emu8086_setup.exe`)
   - Seguir el asistente de instalación
   - Aceptar los términos de licencia
   - Seleccionar el directorio de instalación (por defecto: `C:\emu8086`)
   - Click en "Install"
   - Click en "Finish" al completar

3. **Verificar la Instalación**
   - Buscar "EMU8086" en el menú de inicio
   - Ejecutar la aplicación
   - Debe aparecer la ventana principal del IDE

#### Linux (usando Wine)

```bash
# Instalar Wine
sudo apt-get install wine

# Descargar EMU8086
wget http://www.emu8086.com/dl/emu8086_setup.exe

# Instalar con Wine
wine emu8086_setup.exe

# Ejecutar EMU8086
wine ~/.wine/drive_c/emu8086/emu8086.exe
```

### Uso de EMU8086

#### Paso 1: Abrir EMU8086

1. Ejecutar EMU8086 desde el menú de inicio o escritorio
2. Aparecerá la ventana principal del IDE

#### Paso 2: Cargar el Código Ensamblador

**Método 1: Abrir archivo existente**

1. Click en **File → Open** (o presionar `Ctrl+O`)
2. Navegar al directorio `output/` de su proyecto
3. Seleccionar el archivo `.asm` deseado:
   - `ejemplo1_estudiantes.asm`
   - `ejemplo2_inventario.asm`
   - `ejemplo3_cadenas.asm`
   - `ejemplo4_factorial.asm`
4. Click en **Open**
5. El código aparecerá en el editor

**Método 2: Copiar y pegar**

1. Abrir el archivo `.asm` con un editor de texto
2. Copiar todo el contenido (`Ctrl+A`, `Ctrl+C`)
3. En EMU8086, crear un nuevo archivo (**File → New**)
4. Pegar el código (`Ctrl+V`)
5. Guardar el archivo (**File → Save As**)

#### Paso 3: Compilar el Código

1. Click en el botón **Compile** en la barra de herramientas (o presionar `F5`)
2. EMU8086 mostrará el progreso de compilación
3. Si hay errores:
   - Aparecerán en la ventana de mensajes en la parte inferior
   - Hacer doble click en el error para ir a la línea correspondiente
   - Corregir el error y volver a compilar
4. Si la compilación es exitosa:
   - Aparecerá el mensaje "Compiled successfully"
   - Se generará el archivo ejecutable

#### Paso 4: Ejecutar el Programa

1. Click en el botón **Emulate** (o presionar `F9`)
2. Se abrirá la ventana del emulador con:
   - **Pantalla virtual**: Muestra la salida del programa
   - **Registros**: Muestra el estado de AX, BX, CX, DX, etc.
   - **Flags**: Muestra los flags del procesador (ZF, CF, SF, etc.)
   - **Memoria**: Muestra el contenido de la memoria
   - **Stack**: Muestra el estado de la pila

3. Click en el botón **Run** (o presionar `F5` en el emulador)
4. El programa se ejecutará y mostrará los resultados

#### Paso 5: Depuración (Opcional)

EMU8086 ofrece herramientas de depuración avanzadas:

**Ejecución Paso a Paso:**
- **Step Into** (`F7`): Ejecuta una instrucción y entra en funciones
- **Step Over** (`F8`): Ejecuta una instrucción sin entrar en funciones
- **Run to Cursor** (`F4`): Ejecuta hasta la línea del cursor

**Breakpoints:**
1. Click en el margen izquierdo del editor para establecer un breakpoint
2. El programa se detendrá en esa línea durante la ejecución
3. Click nuevamente para remover el breakpoint

**Inspección de Valores:**
- Hover sobre variables para ver sus valores
- Ver registros en tiempo real en el panel de registros
- Ver memoria en el panel de memoria
- Ver la pila en el panel de stack

#### Paso 6: Ver Resultados

Los resultados se mostrarán en la pantalla virtual del emulador:

- **Números**: Se mostrarán en formato decimal o hexadecimal
- **Strings**: Se mostrarán como texto
- **Saltos de línea**: Aparecerán como nuevas líneas

### Ejemplo Completo: Ejecutar ejemplo1_estudiantes.asm

```
1. Abrir EMU8086
2. File → Open → output/ejemplo1_estudiantes.asm
3. Click en "Compile" (F5)
4. Verificar mensaje "Compiled successfully"
5. Click en "Emulate" (F9)
6. Click en "Run" (F5)
7. Observar la salida en la pantalla virtual:
   1
   Juan
   85
   90
   0
```

### Características Útiles de EMU8086

#### 1. Calculadora Integrada
- **Tools → Calculator**
- Convierte entre decimal, hexadecimal, binario y octal
- Útil para verificar valores

#### 2. Tabla ASCII
- **Help → ASCII Table**
- Muestra todos los caracteres ASCII
- Útil para trabajar con strings

#### 3. Referencia de Instrucciones
- **Help → Instruction Set**
- Documentación completa de todas las instrucciones x86
- Incluye ejemplos y flags afectados

#### 4. Ejemplos Incluidos
- **File → Examples**
- EMU8086 incluye ejemplos de código
- Útil para aprender sintaxis

---

## Opción B: DOSBox

### ¿Qué es DOSBox?

DOSBox es un emulador de DOS que permite ejecutar programas antiguos de DOS en sistemas modernos. A diferencia de EMU8086, DOSBox:
- No tiene IDE integrado
- Requiere un ensamblador externo (MASM, TASM, NASM)
- Es más cercano a la experiencia real de DOS
- Es multiplataforma (Windows, Linux, macOS)

### Instalación de DOSBox

#### Windows

1. **Descargar DOSBox**
   - Visitar: https://www.dosbox.com/download.php?main=1
   - Descargar el instalador para Windows
   - Ejecutar el instalador
   - Seguir el asistente de instalación

2. **Verificar la Instalación**
   ```
   Buscar "DOSBox" en el menú de inicio
   Ejecutar DOSBox
   Debe aparecer una ventana con el prompt de DOS
   ```

#### Linux

```bash
# Ubuntu/Debian
sudo apt-get install dosbox

# Fedora
sudo dnf install dosbox

# Arch Linux
sudo pacman -S dosbox

# Verificar instalación
dosbox --version
```

#### macOS

```bash
# Usando Homebrew
brew install dosbox

# Verificar instalación
dosbox --version
```

### Instalación de MASM en DOSBox

Para compilar código ensamblador en DOSBox, necesita un ensamblador. Recomendamos MASM (Microsoft Macro Assembler).

#### Paso 1: Descargar MASM

1. Descargar MASM 6.11 (disponible en varios sitios de archivo)
2. Extraer los archivos a una carpeta (ej: `C:\MASM`)

Los archivos necesarios son:
- `MASM.EXE` - El ensamblador
- `LINK.EXE` - El linker
- `ML.EXE` - Macro assembler (opcional)

#### Paso 2: Configurar DOSBox

Editar el archivo de configuración de DOSBox (`dosbox.conf`):

**Ubicación del archivo:**
- Windows: `C:\Users\[Usuario]\AppData\Local\DOSBox\dosbox-[version].conf`
- Linux: `~/.dosbox/dosbox-[version].conf`
- macOS: `~/Library/Preferences/DOSBox [version] Preferences`

**Agregar al final del archivo (sección [autoexec]):**

```ini
[autoexec]
# Montar el directorio de MASM
mount d: C:\MASM
# Montar el directorio del proyecto
mount c: C:\ruta\a\tu\proyecto
# Agregar MASM al PATH
set PATH=%PATH%;D:\
# Cambiar a la unidad C
c:
```

### Uso de DOSBox

#### Paso 1: Iniciar DOSBox

1. Ejecutar DOSBox
2. Aparecerá una ventana con el prompt de DOS: `Z:\>`

#### Paso 2: Montar Directorios

Si no configuró el autoexec, montar manualmente:

```dos
mount c: C:\ruta\a\tu\proyecto
mount d: C:\MASM
set PATH=%PATH%;D:\
c:
```

#### Paso 3: Navegar al Directorio de Salida

```dos
cd output
dir
```

Debe ver los archivos `.asm` generados por el compilador.

#### Paso 4: Compilar con MASM

**Para ejemplo1_estudiantes.asm:**

```dos
masm ejemplo1_estudiantes.asm;
```

Esto genera `ejemplo1_estudiantes.obj`

**Si hay errores:**
- MASM mostrará los errores con números de línea
- Editar el archivo `.asm` para corregir
- Volver a compilar

#### Paso 5: Enlazar (Link)

```dos
link ejemplo1_estudiantes.obj;
```

Esto genera `ejemplo1_estudiantes.exe`

**Opciones de link:**
- Si pide "Run File [ejemplo1_estudiantes.exe]:", presionar Enter
- Si pide "List File [NUL.MAP]:", presionar Enter
- Si pide "Libraries [.LIB]:", presionar Enter

#### Paso 6: Ejecutar el Programa

```dos
ejemplo1_estudiantes.exe
```

El programa se ejecutará y mostrará los resultados en la pantalla.

### Ejemplo Completo: Compilar y Ejecutar en DOSBox

```dos
Z:\> mount c: C:\mi_proyecto
Z:\> mount d: C:\MASM
Z:\> set PATH=%PATH%;D:\
Z:\> c:
C:\> cd output
C:\OUTPUT> dir
 EJEMPLO1~1.ASM
 EJEMPLO2~1.ASM
 EJEMPLO3~1.ASM
 EJEMPLO4~1.ASM
C:\OUTPUT> masm ejemplo1_estudiantes.asm;
Microsoft (R) Macro Assembler Version 6.11
Copyright (C) Microsoft Corp 1981-1993. All rights reserved.

 Assembling: ejemplo1_estudiantes.asm

C:\OUTPUT> link ejemplo1_estudiantes.obj;
Microsoft (R) Segmented-Executable Linker Version 5.31.009
Copyright (C) Microsoft Corp 1984-1992. All rights reserved.

C:\OUTPUT> ejemplo1_estudiantes.exe
1
Juan
85
90
0
C:\OUTPUT>
```

### Alternativa: Usar TASM

Si prefiere usar TASM (Turbo Assembler) en lugar de MASM:

```dos
tasm ejemplo1_estudiantes.asm
tlink ejemplo1_estudiantes.obj
ejemplo1_estudiantes.exe
```

### Alternativa: Usar NASM

NASM es un ensamblador moderno que funciona en DOSBox:

```dos
nasm -f obj ejemplo1_estudiantes.asm -o ejemplo1_estudiantes.obj
link ejemplo1_estudiantes.obj
ejemplo1_estudiantes.exe
```

**Nota:** El código generado por nuestro compilador está optimizado para MASM/TASM. Puede requerir ajustes para NASM.

### Configuración Avanzada de DOSBox

#### Optimizar Rendimiento

Editar `dosbox.conf`:

```ini
[cpu]
core=auto          # Usar el core más rápido disponible
cputype=auto       # Detectar automáticamente el tipo de CPU
cycles=max         # Usar el máximo de ciclos disponibles

[dosbox]
memsize=16         # 16 MB de memoria (suficiente para nuestros ejemplos)

[render]
aspect=true        # Mantener relación de aspecto
scaler=normal2x    # Escalado 2x para mejor visualización
```

#### Crear Acceso Directo

**Windows:**
1. Click derecho en el escritorio → Nuevo → Acceso directo
2. Ubicación: `"C:\Program Files (x86)\DOSBox\dosbox.exe" -conf "C:\ruta\a\dosbox.conf"`
3. Nombre: "DOSBox - Compilador"

**Linux:**
```bash
#!/bin/bash
dosbox -conf ~/.dosbox/compilador.conf
```

#### Script de Compilación Automática

Crear un archivo `compile.bat` en el directorio `output/`:

```batch
@echo off
echo Compilando %1.asm...
masm %1.asm;
if errorlevel 1 goto error
echo Enlazando %1.obj...
link %1.obj;
if errorlevel 1 goto error
echo Ejecutando %1.exe...
%1.exe
goto end
:error
echo Error en la compilacion
:end
```

Uso:
```dos
compile ejemplo1_estudiantes
```

---

## Resultados Esperados por Ejemplo

### Ejemplo 1: Sistema de Gestión de Estudiantes

**Archivo:** `output/ejemplo1_estudiantes.asm`

**Comando de compilación:**
```dos
# EMU8086: Compile → Emulate → Run
# DOSBox:
masm ejemplo1_estudiantes.asm;
link ejemplo1_estudiantes.obj;
ejemplo1_estudiantes.exe
```

**Salida esperada:**
```
1
Juan
85
90
0
```

**Explicación línea por línea:**
1. `1` - ID del estudiante agregado (estudiantes[0])
2. `Juan` - Nombre del estudiante (nombres[0])
3. `85` - Calificación inicial (calificaciones[0])
4. `90` - Calificación después de actualización
5. `0` - Calificación después de "eliminación" (baja lógica)

**Tiempo de ejecución:** < 1 segundo

### Ejemplo 2: Sistema de Inventario

**Archivo:** `output/ejemplo2_inventario.asm`

**Comando de compilación:**
```dos
# EMU8086: Compile → Emulate → Run
# DOSBox:
masm ejemplo2_inventario.asm;
link ejemplo2_inventario.obj;
ejemplo2_inventario.exe
```

**Salida esperada:**
```
45
8500
5
150
```

**Explicación línea por línea:**
1. `45` - Total de productos (10 + 15 + 20)
2. `8500` - Valor total del inventario (10×100 + 15×150 + 20×200)
3. `5` - Producto1 después de restar 5 unidades (10 - 5)
4. `150` - Promedio de precios ((100 + 150 + 200) / 3)

**Tiempo de ejecución:** < 1 segundo

**Nota sobre optimización:**
- El TAC optimizado debe haber plegado las constantes
- Compare `.tac` y `.tac.opt` para ver las optimizaciones

### Ejemplo 3: Procesamiento de Cadenas

**Archivo:** `output/ejemplo3_cadenas.asm`

**Comando de compilación:**
```dos
# EMU8086: Compile → Emulate → Run
# DOSBox:
masm ejemplo3_cadenas.asm;
link ejemplo3_cadenas.obj;
ejemplo3_cadenas.exe
```

**Salida esperada:**
```
6
8
1
2
```

**Explicación línea por línea:**
1. `6` - Longitud de "Python" (len(nombre))
2. `8` - Longitud de "Compiler" (len(apellido))
3. `1` - Resultado de comparación: len_nombre > 5 es verdadero
4. `2` - Número de elementos en la lista palabras

**Tiempo de ejecución:** < 1 segundo

**Nota sobre strings:**
- Los strings se almacenan en la sección `.data`
- La función `len()` cuenta caracteres hasta el null terminator

### Ejemplo 4: Cálculo de Factorial Recursivo

**Archivo:** `output/ejemplo4_factorial.asm`

**Comando de compilación:**
```dos
# EMU8086: Compile → Emulate → Run
# DOSBox:
masm ejemplo4_factorial.asm;
link ejemplo4_factorial.obj;
ejemplo4_factorial.exe
```

**Salida esperada:**
```
1
1
120
```

**Explicación línea por línea:**
1. `1` - factorial(0) = 1 (caso base)
2. `1` - factorial(1) = 1 (caso base)
3. `120` - factorial(5) = 5! = 5 × 4 × 3 × 2 × 1 = 120

**Tiempo de ejecución:** < 1 segundo

**Nota sobre recursión:**
- La función usa la pila para guardar el contexto
- Cada llamada recursiva hace push de registros
- El return hace pop para restaurar el contexto
- Puede usar el depurador de EMU8086 para ver la pila

**Verificación manual:**
```
factorial(5) = 5 × factorial(4)
             = 5 × 4 × factorial(3)
             = 5 × 4 × 3 × factorial(2)
             = 5 × 4 × 3 × 2 × factorial(1)
             = 5 × 4 × 3 × 2 × 1
             = 120
```

---

## Troubleshooting Específico

### Problemas con EMU8086

#### Error: "Cannot open file"

**Causa:** El archivo no existe o la ruta es incorrecta

**Solución:**
1. Verificar que el archivo `.asm` existe en `output/`
2. Usar rutas absolutas si es necesario
3. Verificar permisos de lectura del archivo

#### Error: "Invalid instruction"

**Causa:** Sintaxis no compatible con EMU8086

**Solución:**
1. Verificar que el código usa sintaxis Intel
2. Revisar el archivo `.asm` generado
3. Asegurarse de que las directivas son correctas (`.data`, `.text`)

#### Error: "Undefined symbol"

**Causa:** Variable o etiqueta no definida

**Solución:**
1. Verificar que todas las variables están en la sección `.data`
2. Verificar que todas las etiquetas están definidas
3. Revisar el archivo `.symbols` para ver las variables

#### El programa no muestra salida

**Causa:** Las instrucciones de salida no están correctas

**Solución:**
1. Verificar que hay instrucciones `INT 21h` para imprimir
2. Usar el depurador para ver qué está pasando
3. Verificar que el programa no termina prematuramente

#### EMU8086 se congela

**Causa:** Loop infinito en el código

**Solución:**
1. Click en "Stop" o cerrar el emulador
2. Revisar el código para loops infinitos
3. Usar breakpoints para identificar el problema

### Problemas con DOSBox

#### Error: "Drive C does not exist"

**Causa:** No se montó el directorio

**Solución:**
```dos
mount c: C:\ruta\a\tu\proyecto
c:
```

#### Error: "Bad command or file name" al ejecutar MASM

**Causa:** MASM no está en el PATH

**Solución:**
```dos
mount d: C:\MASM
set PATH=%PATH%;D:\
```

O usar ruta completa:
```dos
D:\MASM.EXE ejemplo1_estudiantes.asm;
```

#### Error: "Out of memory"

**Causa:** DOSBox no tiene suficiente memoria asignada

**Solución:**
Editar `dosbox.conf`:
```ini
[dosbox]
memsize=16
```

#### Error: "Cannot open file" en MASM

**Causa:** El archivo no existe o el nombre es incorrecto

**Solución:**
1. Usar `dir` para listar archivos
2. DOSBox usa nombres cortos (8.3): `EJEMPL~1.ASM`
3. Usar el nombre corto o renombrar el archivo

#### El programa se ejecuta muy lento

**Causa:** Ciclos de CPU muy bajos

**Solución:**
Editar `dosbox.conf`:
```ini
[cpu]
cycles=max
```

O presionar `Ctrl+F12` para aumentar ciclos en tiempo real

#### No se ve la salida del programa

**Causa:** El programa termina muy rápido

**Solución:**
Agregar al final del código `.asm`:
```asm
; Esperar tecla antes de salir
MOV AH, 01h
INT 21h
```

### Problemas Comunes en Ambos Entornos

#### Los números se muestran como caracteres extraños

**Causa:** El código imprime valores binarios en lugar de ASCII

**Solución:**
- El compilador debe convertir números a ASCII antes de imprimir
- Verificar el archivo `.asm` generado
- Buscar rutinas de conversión decimal-a-ASCII

#### Los strings no se muestran correctamente

**Causa:** Strings no terminan con null o '$'

**Solución:**
- Verificar que los strings en `.data` terminan correctamente
- MASM/TASM usan '$' como terminador para INT 21h función 09h
- Verificar la función de impresión de strings

#### El programa termina con error

**Causa:** Instrucción de salida incorrecta

**Solución:**
Verificar que el código termina con:
```asm
MOV AH, 4Ch    ; Función de salida
MOV AL, 0      ; Código de retorno
INT 21h        ; Llamada a DOS
```

#### Resultados incorrectos en operaciones aritméticas

**Causa:** Overflow o división por cero

**Solución:**
1. Verificar rangos de valores (16 bits: -32768 a 32767)
2. Usar registros de 32 bits si es necesario (EAX, EBX, etc.)
3. Verificar divisiones por cero

---

## Comparación EMU8086 vs DOSBox

### Tabla Comparativa

| Característica | EMU8086 | DOSBox |
|----------------|---------|--------|
| **Facilidad de uso** | ⭐⭐⭐⭐⭐ Muy fácil | ⭐⭐⭐ Moderado |
| **IDE integrado** | ✅ Sí | ❌ No |
| **Depurador visual** | ✅ Sí | ❌ No |
| **Ensamblador incluido** | ✅ Sí | ❌ Requiere MASM/TASM |
| **Multiplataforma** | ❌ Solo Windows | ✅ Windows/Linux/macOS |
| **Velocidad** | ⭐⭐⭐ Buena | ⭐⭐⭐⭐⭐ Excelente |
| **Visualización de registros** | ✅ Tiempo real | ❌ No disponible |
| **Visualización de memoria** | ✅ Tiempo real | ❌ No disponible |
| **Ejecución paso a paso** | ✅ Sí | ❌ No |
| **Breakpoints** | ✅ Sí | ❌ No |
| **Curva de aprendizaje** | ⭐⭐ Baja | ⭐⭐⭐⭐ Alta |
| **Documentación** | ⭐⭐⭐⭐ Buena | ⭐⭐⭐ Moderada |
| **Compatibilidad** | ⭐⭐⭐⭐ Alta | ⭐⭐⭐⭐⭐ Muy alta |
| **Costo** | 💰 Shareware | 🆓 Gratis y open source |

### Recomendaciones

**Use EMU8086 si:**
- Es principiante en ensamblador
- Quiere depurar visualmente el código
- Necesita ver registros y memoria en tiempo real
- Prefiere una interfaz gráfica
- Está en Windows

**Use DOSBox si:**
- Es usuario avanzado
- Necesita compatibilidad multiplataforma
- Quiere una experiencia más cercana a DOS real
- Prefiere herramientas de línea de comandos
- Necesita ejecutar otros programas de DOS

**Use ambos si:**
- Quiere desarrollar en EMU8086 y probar en DOSBox
- Necesita verificar compatibilidad
- Quiere aprender ambos entornos

---

## Recursos Adicionales

### Tutoriales en Video

**EMU8086:**
- Búsqueda en YouTube: "EMU8086 tutorial"
- Canales recomendados: Programación en ensamblador

**DOSBox:**
- Búsqueda en YouTube: "DOSBox MASM tutorial"
- Documentación oficial: https://www.dosbox.com/wiki/

### Documentación Oficial

- **EMU8086**: http://www.emu8086.com/
- **DOSBox**: https://www.dosbox.com/
- **MASM**: Documentación de Microsoft (archivada)
- **x86 Assembly**: https://en.wikibooks.org/wiki/X86_Assembly

### Comunidades

- **Stack Overflow**: Tag [assembly] [x86]
- **Reddit**: r/asm, r/dosbox
- **Foros de EMU8086**: http://www.emu8086.com/forum/

### Libros Recomendados

- "Assembly Language for x86 Processors" - Kip Irvine
- "The Art of Assembly Language" - Randall Hyde
- "Programming from the Ground Up" - Jonathan Bartlett

---

## Apéndice: Comandos Rápidos

### EMU8086

```
Ctrl+O          Abrir archivo
Ctrl+S          Guardar archivo
F5              Compilar
F9              Emular
F5 (emulador)   Ejecutar
F7              Step Into
F8              Step Over
F4              Run to Cursor
Ctrl+F2         Reset
```

### DOSBox

```dos
mount c: [ruta]     Montar directorio
c:                  Cambiar a unidad C
cd [dir]            Cambiar directorio
dir                 Listar archivos
masm [file].asm;    Compilar con MASM
link [file].obj;    Enlazar
[file].exe          Ejecutar programa
exit                Salir de DOSBox
```

### MASM

```dos
masm [file].asm;                    Compilar
masm /Zi [file].asm;                Compilar con info de depuración
link [file].obj;                    Enlazar
link /DEBUG [file].obj;             Enlazar con depuración
```

---

**Última actualización:** 2025-11-20  
**Versión:** 1.0
