# Ejemplo 4: Cálculo de Factorial Recursivo
# Demuestra funciones recursivas y manejo de pila

def factorial(n):
    # Caso base: factorial de 0 es 1
    if n == 0:
        return 1
    else:
        # Caso recursivo: n * factorial(n-1)
        temp = n - 1
        result = factorial(temp)
        return n * result

# Caso de prueba 1: factorial de 0 (caso base)
resultado1 = factorial(0)
print(resultado1)

# Caso de prueba 2: factorial de 1
resultado2 = factorial(1)
print(resultado2)

# Caso de prueba 3: factorial de 3
resultado3 = factorial(3)
print(resultado3)

# Caso de prueba 4: factorial de 5
resultado4 = factorial(5)
print(resultado4)
