from tac_generator import TACInstruction


class MachineCodeGenerator:
    
    def __init__(self):
        self.code = []
        self.register_map = {}
        self.available_registers = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7']
        self.next_register = 0
        self.memory_offset = 0
        self.memory_map = {}
    
    def generate(self, tac_instructions):
        self.code = []
        self.code.append(".data")
        
        for instr in tac_instructions:
            if instr.op == 'ASSIGN' and not instr.result.startswith('t'):
                if instr.result not in self.memory_map:
                    self.memory_map[instr.result] = self.memory_offset
                    self.code.append(f"    {instr.result}: .word 0")
                    self.memory_offset += 4
        
        self.code.append("")
        self.code.append(".text")
        self.code.append("    .globl main")
        self.code.append("main:")
        self.code.append("")
        
        for instr in tac_instructions:
            self.generate_instruction(instr)
        
        self.code.append("")
        self.code.append("    MOV R0, #0")
        self.code.append("    B _exit")
        
        return self.code
    
    def get_register(self, var):
        if var in self.register_map:
            return self.register_map[var]
        
        reg = self.available_registers[self.next_register % len(self.available_registers)]
        self.next_register += 1
        self.register_map[var] = reg
        return reg
    
    def load_value(self, operand):
        if operand is None:
            return None
        
        try:
            num = int(operand) if '.' not in str(operand) else float(operand)
            reg = self.available_registers[self.next_register % len(self.available_registers)]
            self.next_register += 1
            self.code.append(f"    MOV {reg}, #{operand}")
            return reg
        except:
            pass
        
        if operand.startswith('t') or operand.startswith('_'):
            return self.get_register(operand)
        
        reg = self.available_registers[self.next_register % len(self.available_registers)]
        self.next_register += 1
        offset = self.memory_map.get(operand, 0)
        self.code.append(f"    LDR {reg}, [SP, #{offset}]")
        return reg
    
    def store_value(self, reg, var):
        if var.startswith('t') or var.startswith('_'):
            self.register_map[var] = reg
        else:
            offset = self.memory_map.get(var, 0)
            self.code.append(f"    STR {reg}, [SP, #{offset}]")
    
    def generate_instruction(self, instr):
        
        if instr.op == 'ASSIGN':
            reg_src = self.load_value(instr.arg1)
            if reg_src:
                self.store_value(reg_src, instr.result)
        
        elif instr.op == 'ADD':
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code.append(f"    ADD {reg_dest}, {reg1}, {reg2}")
            if not instr.result.startswith('t'):
                self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'SUB':
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code.append(f"    SUB {reg_dest}, {reg1}, {reg2}")
            if not instr.result.startswith('t'):
                self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'MUL':
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code.append(f"    MUL {reg_dest}, {reg1}, {reg2}")
            if not instr.result.startswith('t'):
                self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'DIV':
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code.append(f"    DIV {reg_dest}, {reg1}, {reg2}")
            if not instr.result.startswith('t'):
                self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'MOD':
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code.append(f"    MOD {reg_dest}, {reg1}, {reg2}")
            if not instr.result.startswith('t'):
                self.store_value(reg_dest, instr.result)
        
        elif instr.op == 'NEG':
            reg_src = self.load_value(instr.arg1)
            reg_dest = self.get_register(instr.result)
            self.code.append(f"    NEG {reg_dest}, {reg_src}")
            if not instr.result.startswith('t'):
                self.store_value(reg_dest, instr.result)
        
        elif instr.op in ['EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE']:
            op_map = {
                'EQ': 'EQ', 'NEQ': 'NE', 'LT': 'LT', 
                'GT': 'GT', 'LTE': 'LE', 'GTE': 'GE'
            }
            reg1 = self.load_value(instr.arg1)
            reg2 = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code.append(f"    CMP {reg1}, {reg2}")
            self.code.append(f"    MOV{op_map[instr.op]} {reg_dest}, #1")
            self.code.append(f"    MOVN{op_map[instr.op]} {reg_dest}, #0")
        
        elif instr.op == 'PRINT':
            reg = self.load_value(instr.arg1)
            self.code.append(f"    MOV R0, {reg}")
            self.code.append(f"    BL _print_int")
        
        elif instr.op == 'LABEL':
            self.code.append(f"{instr.arg1}:")
        
        elif instr.op == 'GOTO':
            self.code.append(f"    B {instr.arg1}")
        
        elif instr.op == 'IF_FALSE':
            reg = self.load_value(instr.arg1)
            self.code.append(f"    CMP {reg}, #0")
            self.code.append(f"    BEQ {instr.arg2}")
        
        elif instr.op == 'LIST_CREATE':
            self.code.append(f"    BL _list_create")
            reg_dest = self.get_register(instr.result)
            self.code.append(f"    MOV {reg_dest}, R0")
        
        elif instr.op == 'LIST_APPEND':
            reg_list = self.load_value(instr.arg1)
            reg_item = self.load_value(instr.arg2)
            self.code.append(f"    MOV R0, {reg_list}")
            self.code.append(f"    MOV R1, {reg_item}")
            self.code.append(f"    BL _list_append")
        
        elif instr.op == 'LIST_GET':
            reg_list = self.load_value(instr.arg1)
            reg_index = self.load_value(instr.arg2)
            reg_dest = self.get_register(instr.result)
            self.code.append(f"    MOV R0, {reg_list}")
            self.code.append(f"    MOV R1, {reg_index}")
            self.code.append(f"    BL _list_get")
            self.code.append(f"    MOV {reg_dest}, R0")
        
        elif instr.op == 'CALL':
            if instr.arg1 == 'len':
                reg_list = self.load_value(instr.arg2)
                reg_dest = self.get_register(instr.result)
                self.code.append(f"    MOV R0, {reg_list}")
                self.code.append(f"    BL _list_len")
                self.code.append(f"    MOV {reg_dest}, R0")
    
    def get_code_as_string(self):
        return '\n'.join(self.code)


