# Script de Demostración del Compilador

## Descripción

`demo_compilador.py` es el script principal de demostración que procesa ejemplos de Python a través de todas las fases del compilador: análisis léxico, sintáctico, semántico, generación de código intermedio (TAC), optimización y generación de código ensamblador x86.

## Uso Básico

### Procesar todos los ejemplos
```bash
python demo_compilador.py
```

### Procesar un ejemplo específico
```bash
python demo_compilador.py -e 1
```

### Procesar hasta una fase específica
```bash
python demo_compilador.py -e 2 -p tac
```

### Guardar salidas en archivos
```bash
python demo_compilador.py -e 3 -s
```

### Modo verbose (información detallada)
```bash
python demo_compilador.py -v
```

## Opciones de Línea de Comandos

| Opción | Descripción |
|--------|-------------|
| `-e, --example {1,2,3,4}` | Número del ejemplo a procesar (1-4) |
| `-p, --phase {lexer,parser,semantic,tac,optimizer,codegen,all}` | Fase específica del compilador a ejecutar |
| `-s, --save` | Guardar salidas en archivos |
| `-o, --output OUTPUT` | Directorio de salida para archivos generados (por defecto: output) |
| `-v, --verbose` | Modo verbose - mostrar información detallada |
| `-h, --help` | Mostrar ayuda |

## Fases Disponibles

1. **lexer** - Análisis Léxico
2. **parser** - Análisis Sintáctico
3. **semantic** - Análisis Semántico
4. **tac** - Generación de Código Intermedio (TAC)
5. **optimizer** - Optimización de Código TAC
6. **codegen** - Generación de Código Ensamblador
7. **all** - Todas las fases (por defecto)

## Ejemplos Disponibles

1. **Sistema de Gestión de Estudiantes** - Operaciones CRUD con listas
2. **Sistema de Inventario** - Operaciones aritméticas y múltiples variables
3. **Procesamiento de Cadenas** - Manejo de strings y función len()
4. **Cálculo de Factorial Recursivo** - Funciones recursivas y manejo de pila

## Ejemplos de Uso

### Procesar todos los ejemplos con salida detallada
```bash
python demo_compilador.py -v
```

### Procesar Ejemplo 1 y guardar todos los archivos
```bash
python demo_compilador.py -e 1 -s -v
```

### Procesar Ejemplo 2 hasta la fase TAC
```bash
python demo_compilador.py -e 2 -p tac
```

### Procesar Ejemplo 3 hasta análisis semántico y guardar
```bash
python demo_compilador.py -e 3 -p semantic -s
```

### Procesar Ejemplo 4 con salida en directorio personalizado
```bash
python demo_compilador.py -e 4 -s -o mi_salida
```

### Procesar todos los ejemplos y guardar archivos
```bash
python demo_compilador.py -s
```

## Archivos de Salida

Cuando se usa la opción `-s`, el script genera los siguientes archivos para cada ejemplo:

- `{ejemplo}.tokens` - Lista de tokens del análisis léxico
- `{ejemplo}.ast` - Árbol de sintaxis abstracta
- `{ejemplo}.symbols` - Tabla de símbolos
- `{ejemplo}.tac` - Código intermedio (TAC)
- `{ejemplo}.tac.opt` - Código intermedio optimizado
- `{ejemplo}.asm` - Código ensamblador x86

## Reporte Resumen

Al procesar todos los ejemplos, el script genera un reporte resumen que muestra:

- Estado de cada ejemplo (EXITOSO/FALLIDO)
- Total de ejemplos procesados exitosamente
- Ubicación de los archivos de salida

## Códigos de Salida

- `0` - Procesamiento exitoso
- `1` - Error en el procesamiento

## Notas

- El modo verbose (`-v`) muestra información detallada de cada fase
- Los archivos de salida se guardan en el directorio especificado con `-o` (por defecto: `output/`)
- Si se procesa un ejemplo específico con una fase específica, solo se ejecutan las fases necesarias hasta la solicitada
- La opción `--phase` se ignora cuando se procesan todos los ejemplos
