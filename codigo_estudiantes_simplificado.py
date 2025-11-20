estudiantes = {}

aid = 1

def agregar_estudiante():
    global aid
    print("Nombre: ")
    nombre = input("")
    print("Apellidos: ")
    apellidos = input("")
    print("Grupo: ")
    grupo = input("")
    estudiantes[aid] = {"nombre": nombre, "apellidos": apellidos, "grupo": grupo}
    print("Estudiante registrado con AID: ")
    print(aid)
    aid = aid + 1

def eliminar_estudiante():
    print("AID del estudiante a eliminar: ")
    id_borrar_str = input("")
    id_borrar = int(id_borrar_str)
    del estudiantes[id_borrar]
    print("Estudiante eliminado correctamente.")

def actualizar_estudiante():
    print("AID del estudiante a actualizar: ")
    id_act_str = input("")
    id_act = int(id_act_str)
    print("Deja vacio cualquier campo que no quieras modificar.")
    print("Nuevo nombre: ")
    nombre = input("")
    print("Nuevos apellidos: ")
    apellidos = input("")
    print("Nuevo grupo: ")
    grupo = input("")
    if nombre != "":
        estudiantes[id_act]["nombre"] = nombre
    if apellidos != "":
        estudiantes[id_act]["apellidos"] = apellidos
    if grupo != "":
        estudiantes[id_act]["grupo"] = grupo
    print("Datos actualizados correctamente.")

def mostrar_estudiantes():
    tam = len(estudiantes)
    if tam == 0:
        print("No hay estudiantes registrados.")
        return
    print("Lista de estudiantes:")

def menu():
    while True:
        print("")
        print("1. Alta de estudiante")
        print("2. Baja de estudiante")
        print("3. Actualizar estudiante")
        print("4. Mostrar estudiantes")
        print("5. Salir")
        print("Selecciona una opcion: ")
        opcion = input("")
        if opcion == "1":
            agregar_estudiante()
        elif opcion == "2":
            eliminar_estudiante()
        elif opcion == "3":
            actualizar_estudiante()
        elif opcion == "4":
            mostrar_estudiantes()
        elif opcion == "5":
            break
        else:
            print("Opcion invalida.")

menu()

