# Ejemplo 3: Procesamiento de Cadenas
# Demuestra manejo de strings y función len()

# Definición de cadenas
nombre = "Python"
apellido = "Compiler"

# Longitud de cadenas
len_nombre = len(nombre)
len_apellido = len(apellido)
print(len_nombre)
print(len_apellido)

# Comparaciones con longitudes
if len_nombre > 5:
    print(1)
else:
    print(0)

# Comparación de longitudes
if len_apellido > len_nombre:
    print(1)
else:
    print(0)

# Uso de strings en listas
palabras = []
palabras.append(nombre)
palabras.append(apellido)
print(len(palabras))

# Más operaciones con strings
saludo = "Hola"
len_saludo = len(saludo)
print(len_saludo)

# Comparación directa de strings
if nombre == "Python":
    print(1)
else:
    print(0)

# Verificación de longitud de lista
if len(palabras) == 2:
    print(1)
else:
    print(0)
