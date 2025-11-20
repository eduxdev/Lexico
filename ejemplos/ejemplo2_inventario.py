# Ejemplo 2: Sistema de Inventario
# Demuestra operaciones aritméticas y múltiples variables

# Variables de inventario
producto1 = 10
producto2 = 15
producto3 = 20

precio1 = 100
precio2 = 150
precio3 = 200

# Cálculo de total de productos
total_productos = producto1 + producto2 + producto3
print(total_productos)

# Cálculo de valor total del inventario
valor_total = producto1 * precio1 + producto2 * precio2 + producto3 * precio3
print(valor_total)

# Actualización de inventario (venta de 5 unidades del producto1)
producto1 = producto1 - 5
print(producto1)

# Cálculo de promedio de precios
suma_precios = precio1 + precio2 + precio3
promedio = suma_precios / 3
print(promedio)
