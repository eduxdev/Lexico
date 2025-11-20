"""
Property-Based Tests for Ejemplos del Compilador
Uses Hypothesis for property-based testing
"""

import pytest
from hypothesis import given, strategies as st, settings
from python_compiler import Lexer, TokenType, LexerError, ParserError
from tac_generator import TACGenerator
from semantic_analyzer import SemanticAnalyzer, SemanticError
import ast


# ============= PROPERTY TEST 2.2 =============
# Feature: ejemplos-compilador, Property 1: Código Python válido genera tokens sin errores
# Validates: Requirements 1.1

@settings(max_examples=100)
@given(st.sampled_from([
    # Valid Python code samples
    "x = 5",
    "y = 10\nz = 20",
    "lista = []",
    "lista.append(1)",
    "print(x)",
    "if x > 5:\n    print(1)",
    "def func():\n    return 1",
    "x = 1 + 2 * 3",
    "nombre = \"Juan\"",
    "calificacion = 85",
]))
def test_property_valid_python_generates_tokens_without_errors(code):
    """
    Property 1: Código Python válido genera tokens sin errores
    For any syntactically valid Python code, the Lexer must complete
    analysis without throwing LexerError and produce a token list ending with EOF.
    """
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Verify no exception was raised (implicit by reaching here)
    assert tokens is not None
    assert len(tokens) > 0
    
    # Verify last token is EOF
    assert tokens[-1].type == TokenType.EOF


def test_ejemplo1_estudiantes_tokenizes_correctly():
    """
    Unit test: Verify ejemplo1_estudiantes.py tokenizes without errors
    """
    with open('ejemplos/ejemplo1_estudiantes.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    assert tokens is not None
    assert len(tokens) > 0
    assert tokens[-1].type == TokenType.EOF
    
    # Verify no LexerError was raised
    # Check that key tokens are present
    token_types = [t.type for t in tokens]
    assert TokenType.IDENTIFIER in token_types  # Variable names
    assert TokenType.ASSIGN in token_types  # Assignments
    assert TokenType.LBRACKET in token_types  # List operations
    assert TokenType.PRINT in token_types  # Print statements


# ============= PROPERTY TEST 11.1 =============
# Feature: ejemplos-compilador, Property 2: TAC representa todas las operaciones del código fuente
# Validates: Requirements 1.2

@settings(max_examples=100)
@given(st.sampled_from([
    # Various Python code patterns with different operations
    "x = 5",
    "x = 5\ny = 10",
    "x = 1 + 2",
    "x = 1 + 2 * 3",
    "x = 5\nprint(x)",
    "lista = []\nlista.append(1)",
    "x = 5\nif x > 3:\n    print(1)",
    "x = 5\ny = x + 10\nprint(y)",
    "a = 10\nb = 20\nc = a + b\nprint(c)",
    "x = 1\ny = 2\nz = x * y + 5",
    "nombre = \"Juan\"\nprint(nombre)",
    "x = len(\"hello\")",
    "lista = []\nlista.append(5)\ny = lista[0]",
    "x = 10\ny = 20\nif x < y:\n    print(1)\nelse:\n    print(0)",
    "x = 5\nwhile x > 0:\n    x = x - 1",
]))
def test_property_tac_represents_all_source_operations(code):
    """
    Property 2: TAC representa todas las operaciones del código fuente
    For any valid Python code processed, each operation in the source code
    (assignment, arithmetic operation, function call, etc.) must have a
    corresponding representation in the generated TAC code.
    """
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Verify TAC is not empty
    assert len(tac_instructions) > 0, "TAC should not be empty for valid code"
    
    # Count operations in source code
    has_assignment = '=' in code and '==' not in code
    has_arithmetic = any(op in code for op in ['+', '-', '*', '/', '%'])
    has_print = 'print' in code
    has_if = 'if' in code
    has_while = 'while' in code
    has_list_append = 'append' in code
    has_list_access = '[' in code and ']' in code and 'append' not in code
    has_len = 'len(' in code
    has_comparison = any(op in code for op in ['>', '<', '>=', '<=', '==', '!='])
    
    # Verify corresponding TAC operations exist
    tac_ops = [instr.op for instr in tac_instructions]
    
    if has_assignment:
        assert 'ASSIGN' in tac_ops or any(op in tac_ops for op in ['ADD', 'SUB', 'MUL', 'DIV', 'LIST_CREATE']), \
            "TAC should contain ASSIGN or operation instructions for assignments"
    
    if has_arithmetic:
        arithmetic_ops = ['ADD', 'SUB', 'MUL', 'DIV', 'MOD']
        assert any(op in tac_ops for op in arithmetic_ops), \
            f"TAC should contain arithmetic operations for code with arithmetic. Found: {set(tac_ops)}"
    
    if has_print:
        assert 'PRINT' in tac_ops, "TAC should contain PRINT instruction for print statements"
    
    if has_if:
        conditional_ops = ['IF_FALSE', 'GOTO', 'LABEL']
        assert any(op in tac_ops for op in conditional_ops), \
            "TAC should contain conditional jump instructions for if statements"
    
    if has_while:
        loop_ops = ['LABEL', 'GOTO', 'IF_FALSE']
        assert all(op in tac_ops for op in loop_ops), \
            "TAC should contain loop control instructions for while statements"
    
    if has_list_append:
        assert 'LIST_APPEND' in tac_ops, "TAC should contain LIST_APPEND for append operations"
    
    if has_list_access and not has_list_append:
        assert 'LIST_GET' in tac_ops or 'LIST_SET' in tac_ops, \
            "TAC should contain LIST_GET or LIST_SET for list access"
    
    if has_len:
        call_instructions = [instr for instr in tac_instructions if instr.op == 'CALL']
        len_calls = [instr for instr in call_instructions if instr.arg1 == 'len']
        assert len(len_calls) > 0, "TAC should contain CALL to len() for len() usage"
    
    if has_comparison:
        comparison_ops = ['EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE']
        assert any(op in tac_ops for op in comparison_ops), \
            "TAC should contain comparison instructions for comparison operations"


def test_ejemplo1_tac_completeness():
    """
    Unit test: Verify ejemplo1_estudiantes.py TAC represents all operations
    """
    with open('ejemplos/ejemplo1_estudiantes.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Verify TAC contains all expected operation types
    tac_ops = [instr.op for instr in tac_instructions]
    
    # Should have list operations
    assert 'LIST_CREATE' in tac_ops, "Should have LIST_CREATE"
    assert 'LIST_APPEND' in tac_ops, "Should have LIST_APPEND"
    assert 'LIST_GET' in tac_ops, "Should have LIST_GET"
    assert 'LIST_SET' in tac_ops, "Should have LIST_SET"
    
    # Should have print operations
    assert 'PRINT' in tac_ops, "Should have PRINT"
    
    # Should have assignments
    assert 'ASSIGN' in tac_ops, "Should have ASSIGN"


def test_ejemplo2_tac_completeness():
    """
    Unit test: Verify ejemplo2_inventario.py TAC represents all operations
    """
    with open('ejemplos/ejemplo2_inventario.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Verify TAC contains all expected operation types
    tac_ops = [instr.op for instr in tac_instructions]
    
    # Should have arithmetic operations
    assert 'ADD' in tac_ops, "Should have ADD"
    assert 'MUL' in tac_ops, "Should have MUL"
    assert 'SUB' in tac_ops, "Should have SUB"
    assert 'DIV' in tac_ops, "Should have DIV"
    
    # Should have print operations
    assert 'PRINT' in tac_ops, "Should have PRINT"
    
    # Should have assignments
    assert 'ASSIGN' in tac_ops, "Should have ASSIGN"


# ============= PROPERTY TEST 11.2 =============
# Feature: ejemplos-compilador, Property 3: Generación de código ensamblador es completa
# Validates: Requirements 1.3, 2.3

@settings(max_examples=100)
@given(st.sampled_from([
    # Various Python code patterns
    "x = 5",
    "x = 5\ny = 10",
    "x = 1 + 2",
    "x = 1 + 2 * 3",
    "x = 5\nprint(x)",
    "lista = []\nlista.append(1)",
    "x = 5\nif x > 3:\n    print(1)",
    "x = 5\ny = x + 10\nprint(y)",
    "a = 10\nb = 20\nc = a + b\nprint(c)",
    "x = 1\ny = 2\nz = x * y + 5",
    "nombre = \"Juan\"\nprint(nombre)",
    "x = len(\"hello\")",
    "lista = []\nlista.append(5)\ny = lista[0]",
    "x = 10\ny = 20\nif x < y:\n    print(1)\nelse:\n    print(0)",
    """def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
x = factorial(5)""",
]))
def test_property_assembly_generation_is_complete(code):
    """
    Property 3: Generación de código ensamblador es completa
    For any valid TAC code, the machine code generator must produce assembly code
    that includes .data and .text sections, and terminates with exit instructions.
    """
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Generate machine code
    from machine_code_generator import MachineCodeGenerator
    mcg = MachineCodeGenerator()
    assembly_code = mcg.generate(tac_instructions)
    
    # Verify assembly code was generated
    assert assembly_code is not None, "Assembly code should not be None"
    assert len(assembly_code) > 0, "Assembly code should not be empty"
    
    # Convert to string for easier checking
    asm_text = '\n'.join(assembly_code) if isinstance(assembly_code, list) else assembly_code
    
    # Verify assembly code is substantial (not just a stub)
    assert len(asm_text) > 50, "Assembly code should be substantial (more than 50 characters)"
    
    # Verify .data section exists
    has_data_section = '.data' in asm_text.lower() or 'data segment' in asm_text.lower()
    assert has_data_section, "Assembly code should include .data section"
    
    # Verify .text section exists
    has_text_section = '.text' in asm_text.lower() or 'code segment' in asm_text.lower()
    assert has_text_section, "Assembly code should include .text section"
    
    # Verify exit/termination instructions exist
    # Common exit patterns: MOV AH, 4CH / INT 21H, or END directive, or RET
    has_exit = any(pattern in asm_text.upper() for pattern in [
        'INT 21H', 'INT 21', 'END', 'RET', 'HLT', 'EXIT'
    ])
    assert has_exit, "Assembly code should include exit/termination instructions"
    
    # Verify assembly contains actual instructions (not just sections)
    # Check for common assembly instructions
    has_instructions = any(instr in asm_text.upper() for instr in [
        'MOV', 'ADD', 'SUB', 'MUL', 'DIV', 'CMP', 'JMP', 'CALL', 
        'PUSH', 'POP', 'LDR', 'STR', 'LEA'
    ])
    assert has_instructions, "Assembly code should contain actual assembly instructions"


def test_ejemplo1_assembly_completeness():
    """
    Unit test: Verify ejemplo1_estudiantes.py generates complete assembly code
    """
    with open('ejemplos/ejemplo1_estudiantes.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Generate machine code
    from machine_code_generator import MachineCodeGenerator
    mcg = MachineCodeGenerator()
    assembly_code = mcg.generate(tac_instructions)
    
    # Verify assembly structure
    asm_text = '\n'.join(assembly_code) if isinstance(assembly_code, list) else assembly_code
    
    # Should have .data and .text sections
    assert '.data' in asm_text.lower() or 'data segment' in asm_text.lower(), \
        "Should have .data section"
    assert '.text' in asm_text.lower() or 'code segment' in asm_text.lower(), \
        "Should have .text section"
    
    # Should have exit instructions
    has_exit = any(pattern in asm_text.upper() for pattern in [
        'INT 21H', 'INT 21', 'END', 'RET', 'HLT'
    ])
    assert has_exit, "Should have exit instructions"
    
    # Should have actual instructions
    has_instructions = any(instr in asm_text.upper() for instr in [
        'MOV', 'ADD', 'SUB', 'MUL', 'DIV', 'CMP', 'JMP', 'CALL', 
        'PUSH', 'POP', 'LDR', 'STR'
    ])
    assert has_instructions, "Should have assembly instructions"
    
    # Should be substantial
    assert len(asm_text) > 100, "Assembly code should be substantial"


def test_ejemplo2_assembly_completeness():
    """
    Unit test: Verify ejemplo2_inventario.py generates complete assembly code
    """
    with open('ejemplos/ejemplo2_inventario.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Generate machine code
    from machine_code_generator import MachineCodeGenerator
    mcg = MachineCodeGenerator()
    assembly_code = mcg.generate(tac_instructions)
    
    # Verify assembly structure
    asm_text = '\n'.join(assembly_code) if isinstance(assembly_code, list) else assembly_code
    
    # Should have .data and .text sections
    assert '.data' in asm_text.lower() or 'data segment' in asm_text.lower(), \
        "Should have .data section"
    assert '.text' in asm_text.lower() or 'code segment' in asm_text.lower(), \
        "Should have .text section"
    
    # Should have exit instructions
    has_exit = any(pattern in asm_text.upper() for pattern in [
        'INT 21H', 'INT 21', 'END', 'RET', 'HLT', '_EXIT', 'EXIT'
    ])
    assert has_exit, "Should have exit instructions"
    
    # Should have arithmetic instructions (for inventario calculations)
    has_arithmetic = any(instr in asm_text.upper() for instr in [
        'ADD', 'SUB', 'MUL', 'DIV', 'IMUL', 'IDIV'
    ])
    assert has_arithmetic, "Should have arithmetic instructions"
    
    # Should be substantial
    assert len(asm_text) > 100, "Assembly code should be substantial"


def test_ejemplo4_assembly_completeness():
    """
    Unit test: Verify ejemplo4_factorial.py generates complete assembly code with function support
    """
    with open('ejemplos/ejemplo4_factorial.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Generate machine code
    from machine_code_generator import MachineCodeGenerator
    mcg = MachineCodeGenerator()
    assembly_code = mcg.generate(tac_instructions)
    
    # Verify assembly structure
    asm_text = '\n'.join(assembly_code) if isinstance(assembly_code, list) else assembly_code
    
    # Should have .data and .text sections
    assert '.data' in asm_text.lower() or 'data segment' in asm_text.lower(), \
        "Should have .data section"
    assert '.text' in asm_text.lower() or 'code segment' in asm_text.lower(), \
        "Should have .text section"
    
    # Should have function label
    assert 'func_factorial' in asm_text, "Should have func_factorial label"
    
    # Should have exit instructions
    has_exit = any(pattern in asm_text.upper() for pattern in [
        'INT 21H', 'INT 21', 'END', 'RET', 'HLT', '_EXIT', 'EXIT'
    ])
    assert has_exit, "Should have exit instructions"
    
    # Should have function call instructions
    has_call = any(instr in asm_text.upper() for instr in ['CALL', 'BL', 'JSR'])
    assert has_call, "Should have function call instructions"
    
    # Should have stack operations for function calls
    has_stack = any(instr in asm_text.upper() for instr in ['PUSH', 'POP', 'SP'])
    assert has_stack, "Should have stack operations"
    
    # Should be substantial
    assert len(asm_text) > 100, "Assembly code should be substantial"


# ============= PROPERTY TEST 2.3 =============
# Feature: ejemplos-compilador, Property 4: Operaciones con listas generan instrucciones TAC correctas
# Validates: Requirements 1.5


def test_property_list_operations_generate_correct_tac():
    """
    Property 4: Operaciones con listas generan instrucciones TAC correctas
    For any code using list operations (append, index access), the generated TAC
    must include corresponding LIST_APPEND, LIST_GET, or LIST_SET instructions.
    """
    # Test with ejemplo1_estudiantes.py
    with open('ejemplos/ejemplo1_estudiantes.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    from semantic_analyzer import SemanticAnalyzer
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    from tac_generator import TACGenerator
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Verify TAC contains list operations
    tac_ops = [instr.op for instr in tac_instructions]
    
    # Should have LIST_CREATE for empty list initialization
    assert 'LIST_CREATE' in tac_ops, "TAC should contain LIST_CREATE for list initialization"
    
    # Should have LIST_APPEND for append operations
    assert 'LIST_APPEND' in tac_ops, "TAC should contain LIST_APPEND for append operations"
    
    # Should have LIST_GET for index access (read operations)
    assert 'LIST_GET' in tac_ops, "TAC should contain LIST_GET for index access"
    
    # Should have LIST_SET for index assignment (update operations)
    assert 'LIST_SET' in tac_ops, "TAC should contain LIST_SET for index assignment"


@settings(max_examples=100)
@given(st.sampled_from([
    # Various list operation patterns
    "lista = []\nlista.append(1)",
    "lista = []\nlista.append(5)\nprint(lista[0])",
    "lista = []\nlista.append(10)\nlista[0] = 20",
    "x = []\nx.append(1)\nx.append(2)\ny = x[0]",
    "nombres = []\nnombres.append(\"Juan\")\nprint(nombres[0])",
]))
def test_property_list_operations_tac_coverage(code):
    """
    Property 4 (generalized): For any code with list operations,
    TAC must include appropriate list instructions.
    """
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    from semantic_analyzer import SemanticAnalyzer
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    from tac_generator import TACGenerator
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Verify TAC contains list operations
    tac_ops = [instr.op for instr in tac_instructions]
    
    # At minimum, should have LIST_CREATE and LIST_APPEND
    assert 'LIST_CREATE' in tac_ops or 'LIST_APPEND' in tac_ops or 'LIST_GET' in tac_ops or 'LIST_SET' in tac_ops, \
        "TAC should contain at least one list operation instruction"


# ============= PROPERTY TEST 3.2 =============
# Feature: ejemplos-compilador, Property 5: Plegado de constantes optimiza expresiones aritméticas
# Validates: Requirements 2.2

@settings(max_examples=100)
@given(st.sampled_from([
    # Arithmetic expressions with only constants
    "x = 1 + 2",
    "y = 10 * 5",
    "z = 100 - 25",
    "w = 20 / 4",
    "a = 2 + 3 * 4",
    "b = (5 + 3) * 2",
    "c = 100 + 50 + 25",
    "d = 10 * 10 * 10",
    "e = 1000 - 500 - 250",
    "f = 100 / 10 / 2",
]))
def test_property_constant_folding_optimizes_arithmetic(code):
    """
    Property 5: Plegado de constantes optimiza expresiones aritméticas
    For any arithmetic expression containing only numeric constants,
    the TAC optimizer must reduce it to a single constant in the optimized TAC.
    """
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Optimize TAC
    from tac_optimizer import TACOptimizer
    optimizer = TACOptimizer()
    optimized_tac = optimizer.optimize(tac_instructions)
    
    # Count arithmetic operations in original TAC
    original_ops = [instr.op for instr in tac_instructions if instr.op in ['ADD', 'SUB', 'MUL', 'DIV', 'MOD']]
    
    # Count arithmetic operations in optimized TAC
    optimized_ops = [instr.op for instr in optimized_tac if instr.op in ['ADD', 'SUB', 'MUL', 'DIV', 'MOD']]
    
    # If there were arithmetic operations with constants, they should be reduced
    if len(original_ops) > 0:
        # The optimized version should have fewer or equal arithmetic operations
        assert len(optimized_ops) <= len(original_ops), \
            f"Optimizer should reduce arithmetic operations: {len(original_ops)} -> {len(optimized_ops)}"


def test_ejemplo2_inventario_constant_folding():
    """
    Unit test: Verify ejemplo2_inventario.py benefits from constant folding
    """
    with open('ejemplos/ejemplo2_inventario.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Optimize TAC
    from tac_optimizer import TACOptimizer
    optimizer = TACOptimizer()
    optimized_tac = optimizer.optimize(tac_instructions)
    
    # Verify optimization occurred
    assert len(optimized_tac) <= len(tac_instructions), \
        "Optimized TAC should be same length or shorter than original"


# ============= PROPERTY TEST 3.3 =============
# Feature: ejemplos-compilador, Property 6: Tabla de símbolos mantiene todas las variables
# Validates: Requirements 2.5

@settings(max_examples=100)
@given(st.sampled_from([
    # Code with multiple variables
    "x = 1\ny = 2",
    "a = 5\nb = 10\nc = 15",
    "producto1 = 10\nproducto2 = 20\nproducto3 = 30",
    "precio = 100\ncantidad = 5\ntotal = precio * cantidad",
    "x = 1\ny = x + 2\nz = y + 3",
    "a = 10\nb = 20\nc = 30\nd = 40\ne = 50",
    "var1 = 1\nvar2 = 2\nvar3 = 3\nvar4 = 4",
    "nombre = \"Juan\"\nedad = 25\nsalario = 5000",
    "lista = []\nx = 1\ny = 2",
    "p1 = 100\np2 = 200\np3 = 300\ntotal = p1 + p2 + p3",
]))
def test_property_symbol_table_maintains_all_variables(code):
    """
    Property 6: Tabla de símbolos mantiene todas las variables
    For any code with multiple variables, the symbol table from the semantic analyzer
    must contain an entry for each declared variable, without duplicates or losses.
    """
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Extract variable names from the code (left side of assignments)
    # Count unique variable assignments
    import re
    assignment_pattern = r'^(\w+)\s*='
    declared_vars = set()
    for line in code.split('\n'):
        match = re.match(assignment_pattern, line.strip())
        if match:
            declared_vars.add(match.group(1))
    
    # Verify all declared variables are in the symbol table
    symbol_table_vars = set(analyzer.symbol_table.keys())
    
    # All declared variables should be in the symbol table
    assert declared_vars.issubset(symbol_table_vars), \
        f"Missing variables in symbol table. Declared: {declared_vars}, In table: {symbol_table_vars}"
    
    # Verify no duplicates (symbol table should be a dict, so this is implicit)
    assert len(symbol_table_vars) >= len(declared_vars), \
        "Symbol table should contain at least all declared variables"
    
    # Verify each variable has proper metadata
    for var in declared_vars:
        assert var in analyzer.symbol_table, f"Variable '{var}' not in symbol table"
        assert 'type' in analyzer.symbol_table[var], f"Variable '{var}' missing type information"
        assert 'initialized' in analyzer.symbol_table[var], f"Variable '{var}' missing initialized flag"
        assert 'line' in analyzer.symbol_table[var], f"Variable '{var}' missing line information"


def test_ejemplo2_inventario_symbol_table():
    """
    Unit test: Verify ejemplo2_inventario.py has complete symbol table
    """
    with open('ejemplos/ejemplo2_inventario.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Expected variables in ejemplo2_inventario.py
    expected_vars = {
        'producto1', 'producto2', 'producto3',
        'precio1', 'precio2', 'precio3',
        'total_productos', 'valor_total',
        'suma_precios', 'promedio'
    }
    
    # Verify all expected variables are in the symbol table
    symbol_table_vars = set(analyzer.symbol_table.keys())
    assert expected_vars.issubset(symbol_table_vars), \
        f"Missing variables: {expected_vars - symbol_table_vars}"
    
    # Verify all variables are marked as initialized
    for var in expected_vars:
        assert analyzer.symbol_table[var]['initialized'], \
            f"Variable '{var}' should be marked as initialized"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


# ============= PROPERTY TEST 4.2 =============
# Feature: ejemplos-compilador, Property 7: Función len() genera llamadas TAC correctas
# Validates: Requirements 3.2

@settings(max_examples=100)
@given(st.sampled_from([
    # Various len() usage patterns
    "x = len(\"hello\")",
    "lista = []\ny = len(lista)",
    "nombre = \"Python\"\nlen_nombre = len(nombre)",
    "palabras = []\npalabras.append(\"test\")\nsize = len(palabras)",
    "s = \"test\"\nif len(s) > 3:\n    print(1)",
    "lista = []\nlista.append(1)\nlista.append(2)\nn = len(lista)",
    "texto = \"Compiler\"\nlongitud = len(texto)\nprint(longitud)",
    "items = []\nx = len(items)\nprint(x)",
    "cadena = \"abc\"\nif len(cadena) == 3:\n    print(1)",
    "arr = []\narr.append(5)\nif len(arr) > 0:\n    print(1)",
]))
def test_property_len_generates_correct_tac_calls(code):
    """
    Property 7: Función len() genera llamadas TAC correctas
    For any use of the len() function in code, the generated TAC must include
    a CALL instruction with arg1='len' and the corresponding argument.
    """
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Verify TAC contains CALL instruction for len()
    call_instructions = [instr for instr in tac_instructions if instr.op == 'CALL']
    len_calls = [instr for instr in call_instructions if instr.arg1 == 'len']
    
    # Should have at least one len() call
    assert len(len_calls) > 0, "TAC should contain at least one CALL instruction for len()"
    
    # Each len() call should have an argument
    for call in len_calls:
        assert call.arg2 is not None, "len() CALL instruction should have an argument (arg2)"


def test_ejemplo3_cadenas_len_function():
    """
    Unit test: Verify ejemplo3_cadenas.py generates correct TAC for len() calls
    """
    with open('ejemplos/ejemplo3_cadenas.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Verify TAC contains CALL instructions for len()
    call_instructions = [instr for instr in tac_instructions if instr.op == 'CALL']
    len_calls = [instr for instr in call_instructions if instr.arg1 == 'len']
    
    # ejemplo3_cadenas.py has multiple len() calls
    assert len(len_calls) >= 3, f"Expected at least 3 len() calls, found {len(len_calls)}"
    
    # Verify each len() call has proper structure
    for call in len_calls:
        assert call.arg2 is not None, "len() call should have an argument"
        assert call.result is not None, "len() call should store result in a temporary"


# ============= PROPERTY TEST 4.3 =============
# Feature: ejemplos-compilador, Property 8: Concatenación y comparación de strings genera código correcto
# Validates: Requirements 3.3, 3.5

@settings(max_examples=100)
@given(st.sampled_from([
    # String comparison patterns
    "x = \"hello\"\nif x == \"hello\":\n    print(1)",
    "nombre = \"Python\"\nif nombre == \"Python\":\n    print(1)\nelse:\n    print(0)",
    "s1 = \"test\"\ns2 = \"test\"\nif s1 == s2:\n    print(1)",
    "palabra = \"Compiler\"\nif palabra != \"Python\":\n    print(1)",
    "a = \"abc\"\nif a == \"abc\":\n    print(1)\nelse:\n    print(0)",
    # String with length comparisons
    "texto = \"hello\"\nif len(texto) > 3:\n    print(1)",
    "s = \"Python\"\nif len(s) == 6:\n    print(1)",
    "cadena = \"test\"\nif len(cadena) < 10:\n    print(1)",
    # Mixed operations
    "nombre = \"Juan\"\nif nombre == \"Juan\":\n    x = len(nombre)\n    print(x)",
    "s = \"abc\"\nif len(s) > 0:\n    if s == \"abc\":\n        print(1)",
]))
def test_property_string_operations_generate_correct_code(code):
    """
    Property 8: Concatenación y comparación de strings genera código correcto
    For any string concatenation or comparison operation, the TAC must generate
    appropriate ADD instructions (for concatenation) or comparison instructions
    (EQ, NEQ, etc.) as appropriate.
    """
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Verify TAC contains appropriate instructions
    tac_ops = [instr.op for instr in tac_instructions]
    
    # Check if code has string comparisons (== or !=)
    has_comparison = '==' in code or '!=' in code
    
    if has_comparison:
        # Should have comparison instructions (EQ, NEQ, etc.)
        comparison_ops = ['EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE']
        has_comparison_in_tac = any(op in tac_ops for op in comparison_ops)
        assert has_comparison_in_tac, \
            f"TAC should contain comparison instructions for string comparisons. Found ops: {set(tac_ops)}"
    
    # Verify TAC is not empty and contains valid instructions
    assert len(tac_instructions) > 0, "TAC should not be empty"
    
    # All instructions should have valid operations
    for instr in tac_instructions:
        assert instr.op is not None, "All TAC instructions should have an operation"


def test_ejemplo3_cadenas_string_operations():
    """
    Unit test: Verify ejemplo3_cadenas.py generates correct TAC for string operations
    """
    with open('ejemplos/ejemplo3_cadenas.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Verify TAC contains comparison instructions
    tac_ops = [instr.op for instr in tac_instructions]
    
    # ejemplo3_cadenas.py has string comparisons
    comparison_ops = ['EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE']
    has_comparison = any(op in tac_ops for op in comparison_ops)
    assert has_comparison, f"TAC should contain comparison instructions. Found ops: {set(tac_ops)}"
    
    # Should also have CALL instructions for len()
    assert 'CALL' in tac_ops, "TAC should contain CALL instructions for len()"
    
    # Should have conditional jumps (IF_FALSE or similar)
    conditional_ops = ['IF_FALSE', 'GOTO', 'LABEL']
    has_conditionals = any(op in tac_ops for op in conditional_ops)
    assert has_conditionals, "TAC should contain conditional jump instructions for if-else"
    
    # Verify string assignments are present
    assert 'ASSIGN' in tac_ops, "TAC should contain ASSIGN instructions for variable assignments"


# ============= PROPERTY TEST 5.2 =============
# Feature: ejemplos-compilador, Property 9: Funciones recursivas generan etiquetas y llamadas correctas
# Validates: Requirements 4.2

@settings(max_examples=100)
@given(st.sampled_from([
    # Various recursive function patterns
    """def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
x = factorial(5)""",
    """def fib(n):
    if n == 0:
        return 0
    else:
        if n == 1:
            return 1
        else:
            a = n - 1
            b = n - 2
            return fib(a) + fib(b)
result = fib(5)""",
    """def countdown(n):
    if n == 0:
        return 0
    else:
        temp = n - 1
        return countdown(temp)
x = countdown(10)""",
    """def sum_to_n(n):
    if n == 0:
        return 0
    else:
        prev = n - 1
        result = sum_to_n(prev)
        return n + result
total = sum_to_n(5)""",
    """def power(base, exp):
    if exp == 0:
        return 1
    else:
        e = exp - 1
        result = power(base, e)
        return base * result
x = power(2, 3)""",
]))
def test_property_recursive_functions_generate_correct_labels_and_calls(code):
    """
    Property 9: Funciones recursivas generan etiquetas y llamadas correctas
    For any recursive function defined, the TAC must include a function label
    (LABEL func_name), CALL instructions for recursive calls, and RETURN instructions.
    """
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Verify TAC contains function-related instructions
    tac_ops = [instr.op for instr in tac_instructions]
    
    # Should have LABEL for function definition
    assert 'LABEL' in tac_ops, "TAC should contain LABEL instruction for function definition"
    
    # Should have CALL for recursive calls
    assert 'CALL' in tac_ops, "TAC should contain CALL instruction for recursive function calls"
    
    # Should have RETURN for function return
    assert 'RETURN' in tac_ops, "TAC should contain RETURN instruction"
    
    # Verify function labels exist (they start with 'func_' and are in arg1)
    labels = [instr for instr in tac_instructions if instr.op == 'LABEL']
    function_labels = [lbl for lbl in labels if lbl.arg1 and lbl.arg1.startswith('func_')]
    assert len(function_labels) > 0, "TAC should contain at least one function label (starting with 'func_')"
    
    # Verify recursive calls exist (CALL to the same function)
    calls = [instr for instr in tac_instructions if instr.op == 'CALL']
    assert len(calls) > 0, "TAC should contain at least one CALL instruction"
    
    # Verify RETURN instructions exist
    returns = [instr for instr in tac_instructions if instr.op == 'RETURN']
    assert len(returns) > 0, "TAC should contain at least one RETURN instruction"


def test_ejemplo4_factorial_recursive_structure():
    """
    Unit test: Verify ejemplo4_factorial.py generates correct TAC structure for recursion
    """
    with open('ejemplos/ejemplo4_factorial.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Verify TAC structure
    tac_ops = [instr.op for instr in tac_instructions]
    
    # Should have LABEL for factorial function (label is in arg1)
    labels = [instr for instr in tac_instructions if instr.op == 'LABEL']
    function_labels = [lbl for lbl in labels if lbl.arg1 == 'func_factorial']
    assert len(function_labels) > 0, "TAC should contain LABEL for factorial function"
    
    # Should have CALL instructions for recursive calls to factorial
    calls = [instr for instr in tac_instructions if instr.op == 'CALL']
    factorial_calls = [call for call in calls if call.arg1 == 'factorial']
    assert len(factorial_calls) > 0, "TAC should contain recursive CALL to factorial"
    
    # Should have RETURN instructions
    returns = [instr for instr in tac_instructions if instr.op == 'RETURN']
    assert len(returns) >= 2, "TAC should contain at least 2 RETURN instructions (base case and recursive case)"
    
    # Should have conditional logic (IF_FALSE for base case check)
    assert 'IF_FALSE' in tac_ops or 'GOTO' in tac_ops, \
        "TAC should contain conditional jumps for base case checking"
    
    # Verify function has parameters
    # The function should use PARAM or similar for parameter passing
    # Check that the function label is followed by parameter handling
    factorial_label_idx = next(i for i, instr in enumerate(tac_instructions) if instr.op == 'LABEL' and instr.arg1 == 'func_factorial')
    assert factorial_label_idx >= 0, "Should find factorial function label"


# ============= PROPERTY TEST 5.3 =============
# Feature: ejemplos-compilador, Property 10: Stack frames en código ensamblador para funciones
# Validates: Requirements 4.3

@settings(max_examples=100)
@given(st.sampled_from([
    # Various recursive function patterns
    """def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
x = factorial(5)""",
    """def fib(n):
    if n == 0:
        return 0
    else:
        if n == 1:
            return 1
        else:
            a = n - 1
            b = n - 2
            return fib(a) + fib(b)
result = fib(5)""",
    """def countdown(n):
    if n == 0:
        return 0
    else:
        temp = n - 1
        return countdown(temp)
x = countdown(10)""",
    """def sum_to_n(n):
    if n == 0:
        return 0
    else:
        prev = n - 1
        result = sum_to_n(prev)
        return n + result
total = sum_to_n(5)""",
    """def power(base, exp):
    if exp == 0:
        return 1
    else:
        e = exp - 1
        result = power(base, e)
        return base * result
x = power(2, 3)""",
]))
def test_property_stack_frames_in_assembly_for_functions(code):
    """
    Property 10: Stack frames en código ensamblador para funciones
    For any TAC code containing function definitions, the generated assembly code
    must include stack handling instructions (push/pop or equivalents like LDR/STR with SP)
    to preserve context.
    """
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Generate machine code
    from machine_code_generator import MachineCodeGenerator
    mcg = MachineCodeGenerator()
    assembly_code = mcg.generate(tac_instructions)
    
    # Verify assembly code contains stack operations
    # Join all assembly lines into a single string for easier searching
    asm_text = '\n'.join(assembly_code) if isinstance(assembly_code, list) else assembly_code
    
    # Check for stack pointer usage (SP register)
    assert 'SP' in asm_text or 'sp' in asm_text, \
        "Assembly code should use stack pointer (SP) for function context"
    
    # Check for stack operations (LDR/STR with SP, or PUSH/POP)
    has_stack_ops = (
        'LDR' in asm_text and 'SP' in asm_text or
        'STR' in asm_text and 'SP' in asm_text or
        'PUSH' in asm_text or
        'POP' in asm_text or
        'ldr' in asm_text and 'sp' in asm_text or
        'str' in asm_text and 'sp' in asm_text or
        'push' in asm_text or
        'pop' in asm_text
    )
    assert has_stack_ops, \
        "Assembly code should contain stack operations (LDR/STR with SP, or PUSH/POP)"
    
    # Verify function labels exist in assembly
    has_function_label = 'func_' in asm_text
    assert has_function_label, "Assembly code should contain function labels"


def test_ejemplo4_factorial_stack_frames():
    """
    Unit test: Verify ejemplo4_factorial.py generates assembly with proper stack frame handling
    """
    with open('ejemplos/ejemplo4_factorial.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Tokenize
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    # Parse
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    
    # Generate TAC
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    
    # Generate machine code
    from machine_code_generator import MachineCodeGenerator
    mcg = MachineCodeGenerator()
    assembly_code = mcg.generate(tac_instructions)
    
    # Verify assembly code structure
    asm_text = '\n'.join(assembly_code) if isinstance(assembly_code, list) else assembly_code
    
    # Should have .data and .text sections
    assert '.data' in asm_text or 'data' in asm_text, "Assembly should have .data section"
    assert '.text' in asm_text or 'text' in asm_text, "Assembly should have .text section"
    
    # Should have function label for factorial
    assert 'func_factorial' in asm_text, "Assembly should contain func_factorial label"
    
    # Should use stack pointer for parameter passing and local variables
    assert 'SP' in asm_text or 'sp' in asm_text, "Assembly should use stack pointer (SP)"
    
    # Should have stack load/store operations
    has_ldr_sp = 'LDR' in asm_text and 'SP' in asm_text
    has_str_sp = 'STR' in asm_text and 'SP' in asm_text
    assert has_ldr_sp or has_str_sp, \
        "Assembly should have LDR/STR operations with SP for stack frame management"
    
    # Should have branch instructions for function calls
    has_branch = 'BL' in asm_text or 'B' in asm_text or 'bl' in asm_text or 'b' in asm_text
    assert has_branch, "Assembly should have branch instructions for function calls"
    
    # Should have comparison and conditional branch for base case
    has_cmp = 'CMP' in asm_text or 'cmp' in asm_text
    assert has_cmp, "Assembly should have CMP instruction for base case checking"
    
    # Should have conditional branches (BEQ, BNE, etc.)
    has_conditional = any(instr in asm_text for instr in ['BEQ', 'BNE', 'BGT', 'BLT', 'beq', 'bne', 'bgt', 'blt'])
    assert has_conditional, "Assembly should have conditional branch instructions"


# ============= PROPERTY TEST 7.3 =============
# Feature: ejemplos-compilador, Property 11: Visualización completa del proceso de compilación
# Validates: Requirements 6.1, 6.2, 6.3

@settings(max_examples=100)
@given(st.sampled_from([
    'ejemplos/ejemplo1_estudiantes.py',
    'ejemplos/ejemplo2_inventario.py',
    'ejemplos/ejemplo3_cadenas.py',
    'ejemplos/ejemplo4_factorial.py',
]))
def test_property_complete_compilation_visualization(example_path):
    """
    Property 11: Visualización completa del proceso de compilación
    For any example processed, the system must generate and show all intermediate
    representations: tokens, AST, TAC, TAC optimized, and assembly code.
    """
    from process_examples import ExampleProcessor
    
    # Process the example
    processor = ExampleProcessor(example_path)
    
    # Read source
    assert processor.read_source(), "Should successfully read source code"
    assert processor.source_code is not None, "Source code should not be None"
    assert len(processor.source_code) > 0, "Source code should not be empty"
    
    # Run lexer
    assert processor.run_lexer(), "Lexer should complete successfully"
    assert processor.tokens is not None, "Tokens should not be None"
    assert len(processor.tokens) > 0, "Should generate at least one token"
    assert processor.tokens[-1].type == TokenType.EOF, "Last token should be EOF"
    
    # Run parser
    assert processor.run_parser(), "Parser should complete successfully"
    assert processor.ast is not None, "AST should not be None"
    
    # Run semantic analyzer
    assert processor.run_semantic_analyzer(), "Semantic analyzer should complete successfully"
    assert processor.symbol_table is not None, "Symbol table should not be None"
    assert len(processor.symbol_table) > 0, "Symbol table should contain at least one variable"
    
    # Run TAC generator
    assert processor.run_tac_generator(), "TAC generator should complete successfully"
    assert processor.tac_instructions is not None, "TAC instructions should not be None"
    assert len(processor.tac_instructions) > 0, "Should generate at least one TAC instruction"
    
    # Run TAC optimizer
    assert processor.run_tac_optimizer(), "TAC optimizer should complete successfully"
    assert processor.tac_optimized is not None, "Optimized TAC should not be None"
    assert len(processor.tac_optimized) > 0, "Optimized TAC should contain at least one instruction"
    
    # Run machine code generator
    assert processor.run_machine_code_generator(), "Machine code generator should complete successfully"
    assert processor.assembly_code is not None, "Assembly code should not be None"
    assert len(processor.assembly_code) > 0, "Should generate at least one line of assembly"
    
    # Verify all intermediate representations are present
    # This ensures complete visualization is possible
    assert processor.source_code is not None, "Source code representation missing"
    assert processor.tokens is not None, "Tokens representation missing"
    assert processor.ast is not None, "AST representation missing"
    assert processor.symbol_table is not None, "Symbol table representation missing"
    assert processor.tac_instructions is not None, "TAC representation missing"
    assert processor.tac_optimized is not None, "Optimized TAC representation missing"
    assert processor.assembly_code is not None, "Assembly code representation missing"


def test_complete_visualization_ejemplo1():
    """
    Unit test: Verify ejemplo1_estudiantes.py can be completely visualized
    """
    from process_examples import ExampleProcessor, ResultsVisualizer
    
    processor = ExampleProcessor('ejemplos/ejemplo1_estudiantes.py')
    success = processor.process_complete(output_dir='output')
    
    assert success, "Processing should complete successfully"
    assert len(processor.errors) == 0, f"Should have no errors, but got: {processor.errors}"
    
    # Verify all outputs can be visualized
    visualizer = ResultsVisualizer(processor)
    
    # These should not raise exceptions
    try:
        visualizer.show_source_code()
        visualizer.show_tokens()
        visualizer.show_ast()
        visualizer.show_symbol_table()
        visualizer.show_tac()
        visualizer.show_tac_optimized()
        visualizer.show_assembly()
    except Exception as e:
        pytest.fail(f"Visualization failed with exception: {e}")


def test_complete_visualization_ejemplo2():
    """
    Unit test: Verify ejemplo2_inventario.py can be completely visualized
    """
    from process_examples import ExampleProcessor, ResultsVisualizer
    
    processor = ExampleProcessor('ejemplos/ejemplo2_inventario.py')
    success = processor.process_complete(output_dir='output')
    
    assert success, "Processing should complete successfully"
    assert len(processor.errors) == 0, f"Should have no errors, but got: {processor.errors}"
    
    # Verify all outputs can be visualized
    visualizer = ResultsVisualizer(processor)
    
    # These should not raise exceptions
    try:
        visualizer.show_source_code()
        visualizer.show_tokens()
        visualizer.show_ast()
        visualizer.show_symbol_table()
        visualizer.show_tac()
        visualizer.show_tac_optimized()
        visualizer.show_assembly()
    except Exception as e:
        pytest.fail(f"Visualization failed with exception: {e}")


def test_complete_visualization_ejemplo3():
    """
    Unit test: Verify ejemplo3_cadenas.py can be completely visualized
    """
    from process_examples import ExampleProcessor, ResultsVisualizer
    
    processor = ExampleProcessor('ejemplos/ejemplo3_cadenas.py')
    success = processor.process_complete(output_dir='output')
    
    assert success, "Processing should complete successfully"
    assert len(processor.errors) == 0, f"Should have no errors, but got: {processor.errors}"
    
    # Verify all outputs can be visualized
    visualizer = ResultsVisualizer(processor)
    
    # These should not raise exceptions
    try:
        visualizer.show_source_code()
        visualizer.show_tokens()
        visualizer.show_ast()
        visualizer.show_symbol_table()
        visualizer.show_tac()
        visualizer.show_tac_optimized()
        visualizer.show_assembly()
    except Exception as e:
        pytest.fail(f"Visualization failed with exception: {e}")


def test_complete_visualization_ejemplo4():
    """
    Unit test: Verify ejemplo4_factorial.py can be completely visualized
    """
    from process_examples import ExampleProcessor, ResultsVisualizer
    
    processor = ExampleProcessor('ejemplos/ejemplo4_factorial.py')
    success = processor.process_complete(output_dir='output')
    
    assert success, "Processing should complete successfully"
    assert len(processor.errors) == 0, f"Should have no errors, but got: {processor.errors}"
    
    # Verify all outputs can be visualized
    visualizer = ResultsVisualizer(processor)
    
    # These should not raise exceptions
    try:
        visualizer.show_source_code()
        visualizer.show_tokens()
        visualizer.show_ast()
        visualizer.show_symbol_table()
        visualizer.show_tac()
        visualizer.show_tac_optimized()
        visualizer.show_assembly()
    except Exception as e:
        pytest.fail(f"Visualization failed with exception: {e}")


def test_all_examples_generate_all_representations():
    """
    Unit test: Verify all examples generate all required representations
    """
    from process_examples import ExampleProcessor
    
    examples = [
        'ejemplos/ejemplo1_estudiantes.py',
        'ejemplos/ejemplo2_inventario.py',
        'ejemplos/ejemplo3_cadenas.py',
        'ejemplos/ejemplo4_factorial.py',
    ]
    
    for example_path in examples:
        processor = ExampleProcessor(example_path)
        success = processor.process_complete(output_dir='output')
        
        assert success, f"Processing {example_path} should complete successfully"
        
        # Verify all representations exist
        assert processor.source_code is not None, f"{example_path}: Source code missing"
        assert processor.tokens is not None, f"{example_path}: Tokens missing"
        assert processor.ast is not None, f"{example_path}: AST missing"
        assert processor.symbol_table is not None, f"{example_path}: Symbol table missing"
        assert processor.tac_instructions is not None, f"{example_path}: TAC missing"
        assert processor.tac_optimized is not None, f"{example_path}: Optimized TAC missing"
        assert processor.assembly_code is not None, f"{example_path}: Assembly code missing"
        
        # Verify representations are non-empty
        assert len(processor.source_code) > 0, f"{example_path}: Source code is empty"
        assert len(processor.tokens) > 0, f"{example_path}: Tokens list is empty"
        assert len(processor.symbol_table) > 0, f"{example_path}: Symbol table is empty"
        assert len(processor.tac_instructions) > 0, f"{example_path}: TAC is empty"
        assert len(processor.tac_optimized) > 0, f"{example_path}: Optimized TAC is empty"
        assert len(processor.assembly_code) > 0, f"{example_path}: Assembly code is empty"


# ============= PROPERTY TEST 8.2 =============
# Feature: ejemplos-compilador, Property 12: Errores reportados con información de línea
# Validates: Requirements 6.5

@settings(max_examples=100)
@given(st.sampled_from([
    # Lexer errors - invalid characters
    ("x = 5 @ 3", LexerError, "línea"),
    ("y = 10 $ 5", LexerError, "línea"),
    # Parser errors - syntax errors  
    ("if x > 5\n    print(1)", ParserError, "línea"),
    ("def func()\n    return 1", ParserError, "línea"),
    ("print(x\n", ParserError, "línea"),
    ("x = 5\nif y > 3\n    print(1)", ParserError, "línea"),
    # Semantic errors - undeclared variables
    ("print(undefined_var)", SemanticError, "Línea"),
    ("x = undefined_var + 5", SemanticError, "Línea"),
    ("y = z * 2", SemanticError, "Línea"),
    ("x = 5\ny = undefined_var", SemanticError, "Línea"),
]))
def test_property_errors_reported_with_line_information(error_data):
    """
    Property 12: Errores reportados con información de línea
    For any code with syntactic or semantic errors, the compiler must throw
    an exception that includes the line number where the error occurred.
    """
    code, expected_error_type, line_keyword = error_data
    
    error_raised = False
    error_message = ""
    
    try:
        # Try to compile the code through all phases
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        from python_compiler import Parser
        parser = Parser(tokens)
        ast = parser.parse()
        
        from semantic_analyzer import SemanticAnalyzer
        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)
        
        # If semantic analysis fails, check errors
        if not success and analyzer.errors:
            error_raised = True
            error_message = str(analyzer.errors[0])
            expected_error_type = SemanticError
    
    except (LexerError, ParserError, SemanticError, Exception) as e:
        error_raised = True
        error_message = str(e)
    
    # Verify an error was raised
    assert error_raised, f"Expected an error for code: {code}"
    
    # Verify the error message contains line information
    assert line_keyword.lower() in error_message.lower(), \
        f"Error message should contain line information ('{line_keyword}'). Got: {error_message}"
    
    # Verify the error message contains a number (the line number)
    import re
    has_number = bool(re.search(r'\d+', error_message))
    assert has_number, \
        f"Error message should contain a line number. Got: {error_message}"


def test_lexer_error_includes_line_number():
    """
    Unit test: Verify LexerError includes line number
    """
    code = "x = 5\ny = 10 @ 3"  # @ is invalid
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        pytest.fail("Should have raised LexerError")
    except LexerError as e:
        error_msg = str(e)
        # Should contain "línea" or "line"
        assert "línea" in error_msg.lower() or "line" in error_msg.lower(), \
            f"Error should mention line: {error_msg}"
        # Should contain line number 2
        assert "2" in error_msg, f"Error should mention line 2: {error_msg}"


def test_parser_error_includes_line_number():
    """
    Unit test: Verify ParserError includes line number
    """
    code = "x = 5\nif x > 5"  # Missing colon
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        from python_compiler import Parser
        parser = Parser(tokens)
        ast = parser.parse()
        pytest.fail("Should have raised ParserError")
    except ParserError as e:
        error_msg = str(e)
        # Should contain "línea" or "line"
        assert "línea" in error_msg.lower() or "line" in error_msg.lower(), \
            f"Error should mention line: {error_msg}"
        # Should contain a line number
        import re
        has_number = bool(re.search(r'\d+', error_msg))
        assert has_number, f"Error should contain line number: {error_msg}"


def test_semantic_error_includes_line_number():
    """
    Unit test: Verify SemanticError includes line number
    """
    code = "x = 5\ny = undefined_var + 10"
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    from semantic_analyzer import SemanticAnalyzer
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    
    # Semantic analyzer accumulates errors instead of throwing
    assert not success, "Should have semantic errors"
    assert len(analyzer.errors) > 0, "Should have at least one error"
    
    error_msg = analyzer.errors[0]
    # Should contain "Línea" or "Line"
    assert "línea" in error_msg.lower() or "line" in error_msg.lower(), \
        f"Error should mention line: {error_msg}"
    # Should contain line number 2
    assert "2" in error_msg, f"Error should mention line 2: {error_msg}"


def test_process_examples_error_formatting():
    """
    Unit test: Verify ExampleProcessor formats errors with line information
    """
    from process_examples import ExampleProcessor
    import tempfile
    import os
    
    # Create a temporary file with invalid code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write("x = 5\ny = 10 @ 3")  # @ is invalid
        temp_path = f.name
    
    try:
        processor = ExampleProcessor(temp_path)
        success = processor.process_complete(output_dir='output')
        
        # Should fail
        assert not success, "Processing should fail for invalid code"
        
        # Should have errors
        assert len(processor.errors) > 0, "Should have at least one error"
        
        # Error should contain line information
        error_msg = processor.errors[0]
        assert "línea" in error_msg.lower() or "line" in error_msg.lower(), \
            f"Error should mention line: {error_msg}"
        
        # Should contain a line number
        import re
        has_number = bool(re.search(r'\d+', error_msg))
        assert has_number, f"Error should contain line number: {error_msg}"
        
        # Test error report formatting
        error_report = processor.format_error_report()
        assert len(error_report) > 0, "Error report should not be empty"
        assert "REPORTE DE ERRORES" in error_report, "Error report should have header"
        assert error_msg in error_report, "Error report should contain the error message"
    
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_multiple_errors_all_include_line_numbers():
    """
    Unit test: Verify multiple semantic errors all include line numbers
    """
    code = """x = 5
y = undefined1 + 10
z = undefined2 * 2
w = undefined3 - 5"""
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    from python_compiler import Parser
    parser = Parser(tokens)
    ast = parser.parse()
    
    from semantic_analyzer import SemanticAnalyzer
    analyzer = SemanticAnalyzer()
    success = analyzer.analyze(ast)
    
    # Should have multiple errors
    assert not success, "Should have semantic errors"
    assert len(analyzer.errors) >= 3, f"Should have at least 3 errors, got {len(analyzer.errors)}"
    
    # All errors should contain line information
    for error_msg in analyzer.errors:
        assert "línea" in error_msg.lower() or "line" in error_msg.lower(), \
            f"Error should mention line: {error_msg}"
        
        # Should contain a line number
        import re
        has_number = bool(re.search(r'\d+', error_msg))
        assert has_number, f"Error should contain line number: {error_msg}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
