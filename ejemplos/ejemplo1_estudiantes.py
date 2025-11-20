# Ejemplo 1: Sistema de Gestión de Estudiantes
# Demuestra operaciones CRUD con listas

# Inicialización de listas vacías
estudiantes = []
nombres = []
calificaciones = []

# Operación de ALTA (Create) - Agregar estudiante 1
estudiantes.append(1)
nombres.append("Juan")
calificaciones.append(85)

# Operación de ALTA (Create) - Agregar estudiante 2
estudiantes.append(2)
nombres.append("Maria")
calificaciones.append(92)

# Operación de ALTA (Create) - Agregar estudiante 3
estudiantes.append(3)
nombres.append("Pedro")
calificaciones.append(78)

# Operación de LECTURA (Read) - Visualizar estudiante 1
print(estudiantes[0])
print(nombres[0])
print(calificaciones[0])

# Operación de LECTURA (Read) - Visualizar estudiante 2
print(estudiantes[1])
print(nombres[1])
print(calificaciones[1])

# Operación de ACTUALIZACIÓN (Update) - Modificar calificación del estudiante 1
calificaciones[0] = 90
print(calificaciones[0])

# Operación de ACTUALIZACIÓN (Update) - Modificar calificación del estudiante 2
calificaciones[1] = 95
print(calificaciones[1])

# Operación de BAJA (Delete) - Marcar estudiante 3 como eliminado
calificaciones[2] = 0
print(calificaciones[2])

# Verificación final - Mostrar todos los estudiantes
print(estudiantes[0])
print(estudiantes[1])
print(estudiantes[2])
