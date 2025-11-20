"""
Intérprete de Código TAC
Ejecuta el código de tres direcciones y genera la salida
"""

from tac_generator import TACInstruction


class TACInterpreter:
    """Intérprete para código TAC"""
    
    def __init__(self):
        self.variables = {}
        self.output = []
        self.pc = 0
        self.labels = {}
        self.call_stack = []
        self.function_params = []
    
    def interpret(self, instructions):
        """Ejecuta las instrucciones TAC"""
        self.variables = {}
        self.output = []
        self.pc = 0
        self.labels = {}
        self.call_stack = []
        self.function_params = []
        
        # Primera pasada: identificar etiquetas y funciones
        for i, instr in enumerate(instructions):
            if instr.op == 'LABEL':
                self.labels[instr.arg1] = i
        
        # Encontrar el inicio del código principal (después de las definiciones de función)
        # Buscar la última instrucción RETURN que no tiene argumentos (fin de función)
        main_start = 0
        for i, instr in enumerate(instructions):
            if instr.op == 'LABEL' and instr.arg1.startswith('func_'):
                # Encontrar el final de esta función (RETURN sin argumentos)
                for j in range(i + 1, len(instructions)):
                    if instructions[j].op == 'RETURN' and instructions[j].arg1 is None:
                        main_start = j + 1
                        break
                break  # Solo procesamos la primera función
        
        # Comenzar desde el código principal
        self.pc = main_start
        
        while self.pc < len(instructions):
            instr = instructions[self.pc]
            self.execute_instruction(instr)
            self.pc += 1
        
        return '\n'.join(self.output)
    
    def execute_instruction(self, instr):
        """Ejecuta una instrucción individual"""
        
        if instr.op == 'ASSIGN':
            value = self.get_value(instr.arg1)
            self.variables[instr.result] = value
        
        elif instr.op == 'ADD':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left + right
        
        elif instr.op == 'SUB':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left - right
        
        elif instr.op == 'MUL':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left * right
        
        elif instr.op == 'DIV':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            if right == 0:
                raise Exception("Error de ejecución: División por cero")
            self.variables[instr.result] = left / right
        
        elif instr.op == 'MOD':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            if right == 0:
                raise Exception("Error de ejecución: Módulo por cero")
            self.variables[instr.result] = left % right
        
        elif instr.op == 'NEG':
            value = self.get_value(instr.arg1)
            self.variables[instr.result] = -value
        
        elif instr.op == 'EQ':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left == right
        
        elif instr.op == 'NEQ':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left != right
        
        elif instr.op == 'LT':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left < right
        
        elif instr.op == 'GT':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left > right
        
        elif instr.op == 'LTE':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left <= right
        
        elif instr.op == 'GTE':
            left = self.get_value(instr.arg1)
            right = self.get_value(instr.arg2)
            self.variables[instr.result] = left >= right
        
        elif instr.op == 'PRINT':
            value = self.get_value(instr.arg1)
            self.output.append(str(value))
        
        elif instr.op == 'LABEL':
            pass
        
        elif instr.op == 'GOTO':
            if instr.arg1 in self.labels:
                self.pc = self.labels[instr.arg1] - 1
            else:
                raise Exception(f"Error de ejecución: Etiqueta no encontrada: {instr.arg1}")
        
        elif instr.op == 'IF_FALSE':
            condition = self.get_value(instr.arg1)
            if not condition:
                if instr.arg2 in self.labels:
                    self.pc = self.labels[instr.arg2] - 1
                else:
                    raise Exception(f"Error de ejecución: Etiqueta no encontrada: {instr.arg2}")
        
        elif instr.op == 'LIST_CREATE':
            self.variables[instr.result] = []
        
        elif instr.op == 'LIST_APPEND':
            list_var = self.variables.get(instr.arg1, [])
            value = self.get_value(instr.arg2)
            if isinstance(list_var, list):
                list_var.append(value)
            else:
                raise Exception(f"Error de ejecución: {instr.arg1} no es una lista")
        
        elif instr.op == 'LIST_GET':
            container = self.get_value(instr.arg1)
            key = self.get_value(instr.arg2)
            
            if isinstance(container, list):
                if isinstance(key, (int, float)):
                    index = int(key)
                    if 0 <= index < len(container):
                        self.variables[instr.result] = container[index]
                    else:
                        raise Exception(f"Error de ejecución: Índice fuera de rango: {index}")
                else:
                    raise Exception(f"Error de ejecución: Índice debe ser número: {key}")
            elif isinstance(container, dict):
                if key in container:
                    self.variables[instr.result] = container[key]
                else:
                    raise Exception(f"Error de ejecución: Clave '{key}' no existe en el diccionario")
            else:
                raise Exception(f"Error de ejecución: {instr.arg1} no es una lista o diccionario")
        
        elif instr.op == 'LIST_SET':
            # Obtener el contenedor (puede ser el nombre de una variable o un temporal)
            if instr.arg1 in self.variables:
                container = self.variables[instr.arg1]
            else:
                # Puede ser un valor directo (caso raro)
                container = self.get_value(instr.arg1)
            
            key = self.get_value(instr.arg2)
            value = self.get_value(instr.result)
            
            if isinstance(container, list):
                if isinstance(key, (int, float)):
                    index = int(key)
                    if 0 <= index < len(container):
                        container[index] = value
                    else:
                        raise Exception(f"Error de ejecución: Índice fuera de rango: {index}")
                else:
                    raise Exception(f"Error de ejecución: Índice debe ser número")
            elif isinstance(container, dict):
                container[key] = value
            else:
                raise Exception(f"Error de ejecución: {instr.arg1} no es una lista o diccionario")
        
        elif instr.op == 'DICT_CREATE':
            self.variables[instr.result] = {}
        
        elif instr.op == 'DICT_SET':
            dict_var = self.variables.get(instr.arg1, None)
            if isinstance(dict_var, dict):
                key = self.get_value(instr.arg2)
                value = self.get_value(instr.result)
                dict_var[key] = value
            else:
                raise Exception(f"Error de ejecución: {instr.arg1} no es un diccionario")
        
        elif instr.op == 'CALL':
            func_name = instr.arg1
            
            # Verificar si es una función built-in
            if func_name == 'len':
                arg_value = self.get_value(instr.arg2)
                if isinstance(arg_value, (list, str, dict)):
                    self.variables[instr.result] = len(arg_value)
                else:
                    raise Exception(f"Error de ejecución: len() requiere una lista, string o diccionario")
            elif func_name == 'input':
                prompt = self.get_value(instr.arg2) if instr.arg2 else ""
                if prompt:
                    user_input = input(prompt)
                else:
                    user_input = input()
                self.variables[instr.result] = user_input
            elif instr.arg1 == 'int':
                arg_value = self.get_value(instr.arg2) if instr.arg2 else None
                if arg_value is not None:
                    try:
                        self.variables[instr.result] = int(arg_value)
                    except:
                        raise Exception(f"Error de ejecución: int() requiere un valor convertible a entero")
                else:
                    raise Exception(f"Error de ejecución: int() requiere un argumento")
            elif instr.arg1 == 'float':
                arg_value = self.get_value(instr.arg2) if instr.arg2 else None
                if arg_value is not None:
                    try:
                        self.variables[instr.result] = float(arg_value)
                    except:
                        raise Exception(f"Error de ejecución: float() requiere un valor convertible a float")
                else:
                    raise Exception(f"Error de ejecución: float() requiere un argumento")
            elif func_name == 'str':
                arg_value = self.get_value(instr.arg2) if instr.arg2 else None
                if arg_value is not None:
                    self.variables[instr.result] = str(arg_value)
                else:
                    raise Exception(f"Error de ejecución: str() requiere un argumento")
            else:
                # Función definida por el usuario
                func_label = f"func_{func_name}"
                if func_label in self.labels:
                    # Guardar contexto actual
                    saved_vars = self.variables.copy()
                    saved_pc = self.pc
                    
                    self.call_stack.append({
                        'return_pc': saved_pc,
                        'variables': saved_vars,
                        'result_var': instr.result
                    })
                    
                    # Obtener argumentos (pueden estar separados por comas)
                    if instr.arg2:
                        # Parsear argumentos (pueden ser "temp" o "0, 1" etc)
                        args_str = str(instr.arg2)
                        if ',' in args_str:
                            args = [arg.strip() for arg in args_str.split(',')]
                        else:
                            args = [args_str]
                        
                        # Evaluar cada argumento y asignarlo a parámetros
                        param_names = ['n', 'x', 'y', 'z', 'a', 'b', 'c']
                        for i, arg in enumerate(args):
                            if i < len(param_names):
                                self.variables[param_names[i]] = self.get_value(arg)
                    
                    # Saltar a la función
                    self.pc = self.labels[func_label]
                else:
                    raise Exception(f"Error de ejecución: Función '{func_name}' no implementada")
        
        elif instr.op == 'DEL':
            if instr.arg2:
                container = self.variables.get(instr.arg1, None)
                key = self.get_value(instr.arg2)
                if isinstance(container, dict):
                    if key in container:
                        del container[key]
                    else:
                        raise Exception(f"Error de ejecución: Clave '{key}' no existe")
                elif isinstance(container, list):
                    if isinstance(key, (int, float)):
                        index = int(key)
                        if 0 <= index < len(container):
                            del container[index]
                        else:
                            raise Exception(f"Error de ejecución: Índice fuera de rango")
                    else:
                        raise Exception(f"Error de ejecución: Índice debe ser número")
            else:
                if instr.arg1 in self.variables:
                    del self.variables[instr.arg1]
                else:
                    raise Exception(f"Error de ejecución: Variable '{instr.arg1}' no existe")
        
        elif instr.op == 'PARAM':
            # Guardar parámetro para la próxima llamada a función
            value = self.get_value(instr.arg1)
            self.function_params.append(value)
        
        elif instr.op == 'FUNCTION_CALL':
            # Llamada a función definida por el usuario
            func_name = instr.arg1
            num_params = int(instr.arg2) if instr.arg2 else 0
            
            # Guardar contexto actual
            saved_vars = self.variables.copy()
            self.call_stack.append({
                'return_pc': self.pc,
                'variables': saved_vars,
                'result_var': instr.result
            })
            
            # Asignar parámetros a variables locales
            # Los parámetros se pasan en orden inverso (último en entrar, primero en salir)
            params = []
            for _ in range(num_params):
                if self.function_params:
                    params.insert(0, self.function_params.pop())
            
            # Buscar la función y sus parámetros
            func_label = f"func_{func_name}"
            if func_label in self.labels:
                # Saltar a la función
                self.pc = self.labels[func_label]
                
                # Asignar parámetros (asumiendo que la función espera 'n', 'x', etc.)
                # Por simplicidad, usamos nombres genéricos
                param_names = ['n', 'x', 'y', 'z']  # Nombres comunes de parámetros
                for i, param_value in enumerate(params):
                    if i < len(param_names):
                        self.variables[param_names[i]] = param_value
            else:
                raise Exception(f"Error de ejecución: Función '{func_name}' no encontrada")
        
        elif instr.op == 'RETURN':
            # Retornar de una función
            if self.call_stack:
                # IMPORTANTE: Evaluar el valor de retorno ANTES de restaurar el contexto
                # para que las variables temporales estén disponibles
                return_value = self.get_value(instr.arg1) if instr.arg1 else None
                
                context = self.call_stack.pop()
                
                # Restaurar contexto
                self.variables = context['variables']
                self.pc = context['return_pc']
                
                # Guardar valor de retorno
                if context['result_var'] and return_value is not None:
                    self.variables[context['result_var']] = return_value
            else:
                # Return en el programa principal - terminar ejecución
                self.pc = len(self.variables) + 1000  # Forzar salida
        
        elif instr.op == 'BREAK':
            pass
        
        elif instr.op == 'CONTINUE':
            pass
    
    def get_value(self, operand):
        """Obtiene el valor de un operando (constante o variable)"""
        if operand is None:
            return None
        
        if isinstance(operand, str) and operand.startswith('"') and operand.endswith('"'):
            return operand[1:-1]
        
        try:
            if '.' in str(operand):
                return float(operand)
            else:
                return int(operand)
        except:
            pass
        
        if operand == 'True':
            return True
        if operand == 'False':
            return False
        
        if operand in self.variables:
            return self.variables[operand]
        
        raise Exception(f"Error de ejecución: Variable no definida: {operand}")
