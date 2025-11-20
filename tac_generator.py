"""
Generador de Código Intermedio (TAC - Three Address Code)
Convierte el AST en código de tres direcciones
"""

from python_compiler import *


class TACInstruction:
    """Representa una instrucción TAC"""
    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
    
    def __str__(self):
        if self.op == 'ASSIGN':
            return f"{self.result} = {self.arg1}"
        elif self.op in ['ADD', 'SUB', 'MUL', 'DIV', 'MOD']:
            op_symbol = {
                'ADD': '+', 'SUB': '-', 'MUL': '*', 'DIV': '/', 'MOD': '%'
            }[self.op]
            return f"{self.result} = {self.arg1} {op_symbol} {self.arg2}"
        elif self.op in ['EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE']:
            op_symbol = {
                'EQ': '==', 'NEQ': '!=', 'LT': '<', 'GT': '>', 'LTE': '<=', 'GTE': '>='
            }[self.op]
            return f"{self.result} = {self.arg1} {op_symbol} {self.arg2}"
        elif self.op == 'NEG':
            return f"{self.result} = -{self.arg1}"
        elif self.op == 'PRINT':
            return f"print({self.arg1})"
        elif self.op == 'LABEL':
            return f"{self.arg1}:"
        elif self.op == 'GOTO':
            return f"goto {self.arg1}"
        elif self.op == 'IF_FALSE':
            return f"if_false {self.arg1} goto {self.arg2}"
        elif self.op == 'LIST_CREATE':
            return f"{self.result} = []"
        elif self.op == 'LIST_APPEND':
            return f"{self.arg1}.append({self.arg2})"
        elif self.op == 'LIST_GET':
            return f"{self.result} = {self.arg1}[{self.arg2}]"
        elif self.op == 'LIST_SET':
            return f"{self.arg1}[{self.arg2}] = {self.result}"
        elif self.op == 'DICT_CREATE':
            return f"{self.result} = {{}}"
        elif self.op == 'DICT_SET':
            return f"{self.arg1}[{self.arg2}] = {self.result}"
        elif self.op == 'CALL':
            if self.arg2:
                return f"{self.result} = {self.arg1}({self.arg2})"
            else:
                return f"{self.result} = {self.arg1}()"
        elif self.op == 'RETURN':
            if self.arg1:
                return f"return {self.arg1}"
            else:
                return "return"
        elif self.op == 'DEL':
            if self.arg2:
                return f"del {self.arg1}[{self.arg2}]"
            else:
                return f"del {self.arg1}"
        elif self.op == 'BREAK':
            return "break"
        elif self.op == 'CONTINUE':
            return "continue"
        else:
            return f"{self.op} {self.arg1} {self.arg2} {self.result}"


class TACGenerator:
    """Generador de Código de Tres Direcciones"""
    
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self):
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, op, arg1=None, arg2=None, result=None):
        instr = TACInstruction(op, arg1, arg2, result)
        self.instructions.append(instr)
        return instr
    
    def generate(self, ast):
        self.visit(ast)
        return self.instructions
    
    def visit(self, node):
        method_name = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise Exception(f'No hay método visit para {node.__class__.__name__}')
    
    def visit_ProgramNode(self, node):
        for statement in node.statements:
            self.visit(statement)
    
    def visit_AssignmentNode(self, node):
        expr_result = self.visit(node.expression)
        self.emit('ASSIGN', expr_result, None, node.identifier)
    
    def visit_IndexAssignmentNode(self, node):
        index_result = self.visit(node.index_expr)
        value_result = self.visit(node.value_expr)
        
        # Si target es un string simple
        if isinstance(node.target, str):
            self.emit('LIST_SET', node.target, index_result, value_result)
        else:
            # Si target es un IndexNode (acceso anidado)
            # Primero obtenemos el valor del contenedor
            container_result = self.visit(node.target)
            # Luego asignamos al índice de ese contenedor
            self.emit('LIST_SET', container_result, index_result, value_result)
    
    def visit_PrintNode(self, node):
        expr_result = self.visit(node.expression)
        self.emit('PRINT', expr_result)
    
    def visit_IfNode(self, node):
        cond_result = self.visit(node.condition)
        else_label = self.new_label()
        end_label = self.new_label()
        
        self.emit('IF_FALSE', cond_result, else_label)
        self.visit(node.then_block)
        self.emit('GOTO', end_label)
        
        self.emit('LABEL', else_label)
        for elif_cond, elif_block in node.elif_parts:
            next_label = self.new_label()
            elif_result = self.visit(elif_cond)
            self.emit('IF_FALSE', elif_result, next_label)
            self.visit(elif_block)
            self.emit('GOTO', end_label)
            self.emit('LABEL', next_label)
        
        if node.else_block:
            self.visit(node.else_block)
        
        self.emit('LABEL', end_label)
    
    def visit_WhileNode(self, node):
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.emit('LABEL', start_label)
        cond_result = self.visit(node.condition)
        self.emit('IF_FALSE', cond_result, end_label)
        self.visit(node.block)
        self.emit('GOTO', start_label)
        self.emit('LABEL', end_label)
    
    def visit_ForNode(self, node):
        if isinstance(node.iterable, CallNode) and node.iterable.function == 'range':
            limit_result = self.visit(node.iterable.args[0])
            counter = node.identifier
            
            self.emit('ASSIGN', '0', None, counter)
            start_label = self.new_label()
            end_label = self.new_label()
            
            self.emit('LABEL', start_label)
            temp_cond = self.new_temp()
            self.emit('LT', counter, limit_result, temp_cond)
            self.emit('IF_FALSE', temp_cond, end_label)
            
            self.visit(node.block)
            
            temp_inc = self.new_temp()
            self.emit('ADD', counter, '1', temp_inc)
            self.emit('ASSIGN', temp_inc, None, counter)
            self.emit('GOTO', start_label)
            self.emit('LABEL', end_label)
        else:
            list_result = self.visit(node.iterable)
            counter = f"_idx_{node.identifier}"
            list_len = self.new_temp()
            
            self.emit('CALL', 'len', list_result, list_len)
            self.emit('ASSIGN', '0', None, counter)
            
            start_label = self.new_label()
            end_label = self.new_label()
            
            self.emit('LABEL', start_label)
            temp_cond = self.new_temp()
            self.emit('LT', counter, list_len, temp_cond)
            self.emit('IF_FALSE', temp_cond, end_label)
            
            self.emit('LIST_GET', list_result, counter, node.identifier)
            self.visit(node.block)
            
            temp_inc = self.new_temp()
            self.emit('ADD', counter, '1', temp_inc)
            self.emit('ASSIGN', temp_inc, None, counter)
            self.emit('GOTO', start_label)
            self.emit('LABEL', end_label)
    
    def visit_BinaryOpNode(self, node):
        left_result = self.visit(node.left)
        right_result = self.visit(node.right)
        temp = self.new_temp()
        
        op_map = {
            '+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV', '%': 'MOD',
            '==': 'EQ', '!=': 'NEQ', '<': 'LT', '>': 'GT', '<=': 'LTE', '>=': 'GTE'
        }
        
        op_code = op_map.get(node.operator, 'UNKNOWN')
        self.emit(op_code, left_result, right_result, temp)
        
        return temp
    
    def visit_UnaryOpNode(self, node):
        operand_result = self.visit(node.operand)
        temp = self.new_temp()
        self.emit('NEG', operand_result, None, temp)
        return temp
    
    def visit_NumberNode(self, node):
        return str(node.value)
    
    def visit_StringNode(self, node):
        return f'"{node.value}"'
    
    def visit_IdentifierNode(self, node):
        return node.name
    
    def visit_ListNode(self, node):
        temp_list = self.new_temp()
        self.emit('LIST_CREATE', None, None, temp_list)
        for element in node.elements:
            elem_result = self.visit(element)
            self.emit('LIST_APPEND', temp_list, elem_result)
        return temp_list
    
    def visit_DictionaryNode(self, node):
        temp_dict = self.new_temp()
        self.emit('DICT_CREATE', None, None, temp_dict)
        for key, value in node.items:
            key_result = self.visit(key)
            value_result = self.visit(value)
            self.emit('DICT_SET', temp_dict, key_result, value_result)
        return temp_dict
    
    def visit_IndexNode(self, node):
        list_result = self.visit(node.list_expr)
        index_result = self.visit(node.index_expr)
        temp = self.new_temp()
        self.emit('LIST_GET', list_result, index_result, temp)
        return temp
    
    def visit_CallNode(self, node):
        if node.function == 'range':
            if node.args:
                return self.visit(node.args[0])
            return '0'
        elif node.function == 'len':
            arg_result = self.visit(node.args[0]) if node.args else None
            temp = self.new_temp()
            self.emit('CALL', 'len', arg_result, temp)
            return temp
        elif '.' in node.function:
            parts = node.function.split('.')
            list_name = parts[0]
            method = parts[1]
            if method == 'append' and node.args:
                arg_result = self.visit(node.args[0])
                self.emit('LIST_APPEND', list_name, arg_result)
            return list_name
        else:
            args_str = ', '.join([self.visit(arg) for arg in node.args]) if node.args else None
            temp = self.new_temp()
            self.emit('CALL', node.function, args_str, temp)
            return temp
    
    def visit_FunctionNode(self, node):
        self.emit('LABEL', f"func_{node.name}")
        self.visit(node.body)
        self.emit('RETURN')
    
    def visit_ReturnNode(self, node):
        if node.expression:
            expr_result = self.visit(node.expression)
            self.emit('RETURN', expr_result)
        else:
            self.emit('RETURN')
    
    def visit_GlobalNode(self, node):
        pass
    
    def visit_TryNode(self, node):
        try_label = self.new_label()
        except_label = self.new_label()
        end_label = self.new_label()
        
        self.emit('LABEL', try_label)
        self.visit(node.try_block)
        self.emit('GOTO', end_label)
        
        self.emit('LABEL', except_label)
        for exception_type, except_block in node.except_blocks:
            self.visit(except_block)
        
        self.emit('LABEL', end_label)
    
    def visit_DelNode(self, node):
        if isinstance(node.target, IndexNode):
            list_result = self.visit(node.target.list_expr)
            index_result = self.visit(node.target.index_expr)
            self.emit('DEL', list_result, index_result)
        else:
            target_name = node.target.name if isinstance(node.target, IdentifierNode) else str(node.target)
            self.emit('DEL', target_name)
    
    def visit_BreakNode(self, node):
        self.emit('BREAK')
    
    def visit_ContinueNode(self, node):
        self.emit('CONTINUE')
    
    def visit_BlockNode(self, node):
        for statement in node.statements:
            self.visit(statement)
