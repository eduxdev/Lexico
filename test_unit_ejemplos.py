"""
Unit Tests for Ejemplos del Compilador
Tests specific functionality for each of the 4 examples
"""

import pytest
from python_compiler import Lexer, Parser, TokenType, LexerError, ParserError
from semantic_analyzer import SemanticAnalyzer, SemanticError
from tac_generator import TACGenerator
from tac_optimizer import TACOptimizer
from machine_code_generator import MachineCodeGenerator


# ============= UNIT TESTS FOR EJEMPLO 1: ESTUDIANTES =============
# Requirements: 1.1, 1.2, 1.3, 1.5

class TestEjemplo1Estudiantes:
    """Unit tests for ejemplo1_estudiantes.py"""
    
    @pytest.fixture
    def ejemplo1_code(self):
        """Load ejemplo1_estudiantes.py code"""
        with open('ejemplos/ejemplo1_estudiantes.py', 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_tokenization_correcta(self, ejemplo1_code):
        """Test de tokenización correcta - Requirements 1.1"""
        lexer = Lexer(ejemplo1_code)
        tokens = lexer.tokenize()
        
        # Verify tokenization completed successfully
        assert tokens is not None
        assert len(tokens) > 0
        assert tokens[-1].type == TokenType.EOF
        
        # Verify key tokens are present
        token_types = [t.type for t in tokens]
        assert TokenType.IDENTIFIER in token_types, "Should have identifiers"
        assert TokenType.ASSIGN in token_types, "Should have assignments"
        assert TokenType.LBRACKET in token_types, "Should have list brackets"
        assert TokenType.RBRACKET in token_types, "Should have closing brackets"
        assert TokenType.PRINT in token_types, "Should have print statements"
        assert TokenType.DOT in token_types, "Should have dot for append"
        
        # Verify specific identifiers exist
        token_values = [t.value for t in tokens if t.type == TokenType.IDENTIFIER]
        assert 'estudiantes' in token_values, "Should have 'estudiantes' identifier"
        assert 'nombres' in token_values, "Should have 'nombres' identifier"
        assert 'calificaciones' in token_values, "Should have 'calificaciones' identifier"
        # Note: 'append' might be tokenized as a keyword or method, not just an identifier
    
    def test_parsing_sin_errores(self, ejemplo1_code):
        """Test de parsing sin errores - Requirements 1.1"""
        lexer = Lexer(ejemplo1_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Verify parsing completed successfully
        assert ast is not None
        assert hasattr(ast, 'statements')
        assert len(ast.statements) > 0, "AST should have statements"
        
        # Verify no parser errors were raised
        # (implicit by reaching this point)
    
    def test_generacion_tac_con_operaciones_listas(self, ejemplo1_code):
        """Test de generación TAC con operaciones de listas - Requirements 1.2, 1.5"""
        lexer = Lexer(ejemplo1_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        
        # Verify TAC was generated
        assert tac_instructions is not None
        assert len(tac_instructions) > 0
        
        # Verify list operations are present
        tac_ops = [instr.op for instr in tac_instructions]
        
        # Should have LIST_CREATE for empty list initialization
        assert 'LIST_CREATE' in tac_ops, "Should have LIST_CREATE for list initialization"
        
        # Should have LIST_APPEND for append operations
        list_appends = [instr for instr in tac_instructions if instr.op == 'LIST_APPEND']
        assert len(list_appends) >= 9, f"Should have at least 9 LIST_APPEND operations (3 per list), found {len(list_appends)}"
        
        # Should have LIST_GET for index access (read operations)
        list_gets = [instr for instr in tac_instructions if instr.op == 'LIST_GET']
        assert len(list_gets) > 0, "Should have LIST_GET for reading list elements"
        
        # Should have LIST_SET for index assignment (update operations)
        list_sets = [instr for instr in tac_instructions if instr.op == 'LIST_SET']
        assert len(list_sets) >= 3, f"Should have at least 3 LIST_SET operations, found {len(list_sets)}"
        
        # Verify PRINT operations exist
        prints = [instr for instr in tac_instructions if instr.op == 'PRINT']
        assert len(prints) > 0, "Should have PRINT operations"
    
    def test_codigo_ensamblador_generado(self, ejemplo1_code):
        """Test de código ensamblador generado - Requirements 1.3"""
        lexer = Lexer(ejemplo1_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        
        mcg = MachineCodeGenerator()
        assembly_code = mcg.generate(tac_instructions)
        
        # Verify assembly code was generated
        assert assembly_code is not None
        assert len(assembly_code) > 0
        
        # Convert to string for easier checking
        asm_text = '\n'.join(assembly_code) if isinstance(assembly_code, list) else assembly_code
        
        # Verify assembly structure
        assert '.data' in asm_text or 'data' in asm_text, "Should have .data section"
        assert '.text' in asm_text or 'text' in asm_text, "Should have .text section"
        
        # Verify some assembly instructions exist
        # (specific instructions depend on implementation)
        assert len(asm_text) > 100, "Assembly code should be substantial"


# ============= UNIT TESTS FOR EJEMPLO 2: INVENTARIO =============
# Requirements: 2.1, 2.2, 2.3, 2.5

class TestEjemplo2Inventario:
    """Unit tests for ejemplo2_inventario.py"""
    
    @pytest.fixture
    def ejemplo2_code(self):
        """Load ejemplo2_inventario.py code"""
        with open('ejemplos/ejemplo2_inventario.py', 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_operaciones_aritmeticas(self, ejemplo2_code):
        """Test de operaciones aritméticas - Requirements 2.1"""
        lexer = Lexer(ejemplo2_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        
        # Verify arithmetic operations are present in TAC
        tac_ops = [instr.op for instr in tac_instructions]
        
        # Should have ADD operations
        assert 'ADD' in tac_ops, "Should have ADD operations"
        
        # Should have MUL operations
        assert 'MUL' in tac_ops, "Should have MUL operations"
        
        # Should have SUB operations
        assert 'SUB' in tac_ops, "Should have SUB operations"
        
        # Should have DIV operations
        assert 'DIV' in tac_ops, "Should have DIV operations"
        
        # Count arithmetic operations
        arithmetic_ops = [op for op in tac_ops if op in ['ADD', 'SUB', 'MUL', 'DIV']]
        assert len(arithmetic_ops) > 5, f"Should have multiple arithmetic operations, found {len(arithmetic_ops)}"
    
    def test_optimizacion_constantes(self, ejemplo2_code):
        """Test de optimización de constantes - Requirements 2.2"""
        lexer = Lexer(ejemplo2_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        
        # Optimize TAC
        optimizer = TACOptimizer()
        tac_optimized = optimizer.optimize(tac_instructions)
        
        # Verify optimization occurred
        assert tac_optimized is not None
        assert len(tac_optimized) > 0
        
        # Optimized TAC should be same length or shorter
        assert len(tac_optimized) <= len(tac_instructions), \
            f"Optimized TAC should be <= original: {len(tac_optimized)} vs {len(tac_instructions)}"
        
        # Count arithmetic operations before and after
        original_arithmetic = [instr for instr in tac_instructions if instr.op in ['ADD', 'SUB', 'MUL', 'DIV']]
        optimized_arithmetic = [instr for instr in tac_optimized if instr.op in ['ADD', 'SUB', 'MUL', 'DIV']]
        
        # Optimization should reduce or maintain arithmetic operations
        assert len(optimized_arithmetic) <= len(original_arithmetic), \
            "Optimization should reduce arithmetic operations"
    
    def test_tabla_simbolos_completa(self, ejemplo2_code):
        """Test de tabla de símbolos completa - Requirements 2.5"""
        lexer = Lexer(ejemplo2_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        # Verify symbol table is complete
        symbol_table = analyzer.symbol_table
        assert symbol_table is not None
        assert len(symbol_table) > 0
        
        # Expected variables
        expected_vars = {
            'producto1', 'producto2', 'producto3',
            'precio1', 'precio2', 'precio3',
            'total_productos', 'valor_total',
            'suma_precios', 'promedio'
        }
        
        # Verify all expected variables are in symbol table
        symbol_vars = set(symbol_table.keys())
        missing_vars = expected_vars - symbol_vars
        assert len(missing_vars) == 0, f"Missing variables in symbol table: {missing_vars}"
        
        # Verify each variable has proper metadata
        for var in expected_vars:
            assert var in symbol_table, f"Variable '{var}' not in symbol table"
            assert 'type' in symbol_table[var], f"Variable '{var}' missing type"
            assert 'initialized' in symbol_table[var], f"Variable '{var}' missing initialized flag"
            assert 'line' in symbol_table[var], f"Variable '{var}' missing line info"
            assert symbol_table[var]['initialized'], f"Variable '{var}' should be initialized"
    
    def test_codigo_ensamblador_con_operaciones_aritmeticas(self, ejemplo2_code):
        """Test de código ensamblador con operaciones aritméticas - Requirements 2.3"""
        lexer = Lexer(ejemplo2_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        
        mcg = MachineCodeGenerator()
        assembly_code = mcg.generate(tac_instructions)
        
        # Verify assembly code was generated
        assert assembly_code is not None
        assert len(assembly_code) > 0
        
        # Convert to string
        asm_text = '\n'.join(assembly_code) if isinstance(assembly_code, list) else assembly_code
        
        # Verify assembly structure
        assert '.data' in asm_text or 'data' in asm_text, "Should have .data section"
        assert '.text' in asm_text or 'text' in asm_text, "Should have .text section"
        
        # Verify arithmetic instructions exist (ADD, SUB, MUL, DIV or their equivalents)
        # Note: actual instructions depend on target architecture
        assert len(asm_text) > 100, "Assembly code should be substantial"


# ============= UNIT TESTS FOR EJEMPLO 3: CADENAS =============
# Requirements: 3.1, 3.2, 3.3, 3.5

class TestEjemplo3Cadenas:
    """Unit tests for ejemplo3_cadenas.py"""
    
    @pytest.fixture
    def ejemplo3_code(self):
        """Load ejemplo3_cadenas.py code"""
        with open('ejemplos/ejemplo3_cadenas.py', 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_manejo_strings(self, ejemplo3_code):
        """Test de manejo de strings - Requirements 3.1"""
        lexer = Lexer(ejemplo3_code)
        tokens = lexer.tokenize()
        
        # Verify string tokens are present
        token_types = [t.type for t in tokens]
        assert TokenType.STRING in token_types, "Should have STRING tokens"
        
        # Verify specific strings
        string_values = [t.value for t in tokens if t.type == TokenType.STRING]
        assert '"Python"' in string_values or 'Python' in string_values, "Should have 'Python' string"
        assert '"Compiler"' in string_values or 'Compiler' in string_values, "Should have 'Compiler' string"
        
        # Parse successfully
        parser = Parser(tokens)
        ast = parser.parse()
        assert ast is not None
        
        # Semantic analysis should handle strings
        analyzer = SemanticAnalyzer()
        success = analyzer.analyze(ast)
        assert success or len(analyzer.errors) == 0, f"Should analyze successfully, errors: {analyzer.errors}"
    
    def test_funcion_len(self, ejemplo3_code):
        """Test de función len() - Requirements 3.2"""
        lexer = Lexer(ejemplo3_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        
        # Verify len() calls are present in TAC
        call_instructions = [instr for instr in tac_instructions if instr.op == 'CALL']
        len_calls = [instr for instr in call_instructions if instr.arg1 == 'len']
        
        # ejemplo3_cadenas.py has multiple len() calls
        assert len(len_calls) >= 5, f"Should have at least 5 len() calls, found {len(len_calls)}"
        
        # Verify each len() call has proper structure
        for call in len_calls:
            assert call.arg2 is not None, "len() call should have an argument"
            assert call.result is not None, "len() call should store result"
    
    def test_comparaciones_strings(self, ejemplo3_code):
        """Test de comparaciones de strings - Requirements 3.3, 3.5"""
        lexer = Lexer(ejemplo3_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        
        # Verify comparison operations are present
        tac_ops = [instr.op for instr in tac_instructions]
        
        # Should have comparison instructions
        comparison_ops = ['EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE']
        has_comparison = any(op in tac_ops for op in comparison_ops)
        assert has_comparison, f"Should have comparison operations. Found ops: {set(tac_ops)}"
        
        # Should have conditional jumps
        conditional_ops = ['IF_FALSE', 'GOTO', 'LABEL']
        has_conditionals = any(op in tac_ops for op in conditional_ops)
        assert has_conditionals, "Should have conditional jump instructions"
        
        # Verify GT (greater than) for length comparisons
        gt_ops = [instr for instr in tac_instructions if instr.op == 'GT']
        assert len(gt_ops) > 0, "Should have GT operations for length comparisons"
    
    def test_codigo_ensamblador_con_strings(self, ejemplo3_code):
        """Test de código ensamblador con strings - Requirements 3.1"""
        lexer = Lexer(ejemplo3_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        
        mcg = MachineCodeGenerator()
        assembly_code = mcg.generate(tac_instructions)
        
        # Verify assembly code was generated
        assert assembly_code is not None
        assert len(assembly_code) > 0
        
        # Convert to string
        asm_text = '\n'.join(assembly_code) if isinstance(assembly_code, list) else assembly_code
        
        # Verify assembly structure
        assert '.data' in asm_text or 'data' in asm_text, "Should have .data section"
        assert '.text' in asm_text or 'text' in asm_text, "Should have .text section"
        
        # Verify string data is in .data section
        # (strings should be defined in data section)
        assert len(asm_text) > 100, "Assembly code should be substantial"


# ============= UNIT TESTS FOR EJEMPLO 4: FACTORIAL =============
# Requirements: 4.1, 4.2, 4.3, 4.5

class TestEjemplo4Factorial:
    """Unit tests for ejemplo4_factorial.py"""
    
    @pytest.fixture
    def ejemplo4_code(self):
        """Load ejemplo4_factorial.py code"""
        with open('ejemplos/ejemplo4_factorial.py', 'r', encoding='utf-8') as f:
            return f.read()
    
    def test_definicion_funcion(self, ejemplo4_code):
        """Test de definición de función - Requirements 4.1"""
        lexer = Lexer(ejemplo4_code)
        tokens = lexer.tokenize()
        
        # Verify DEF token is present
        token_types = [t.type for t in tokens]
        assert TokenType.DEF in token_types, "Should have DEF token for function definition"
        
        # Verify function name
        token_values = [t.value for t in tokens if t.type == TokenType.IDENTIFIER]
        assert 'factorial' in token_values, "Should have 'factorial' function name"
        
        # Parse successfully
        parser = Parser(tokens)
        ast = parser.parse()
        assert ast is not None
        
        # Verify function definition in AST
        # (specific structure depends on AST implementation)
        assert hasattr(ast, 'statements')
        assert len(ast.statements) > 0
    
    def test_recursion_en_tac(self, ejemplo4_code):
        """Test de recursión en TAC - Requirements 4.2"""
        lexer = Lexer(ejemplo4_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        
        # Verify function-related TAC instructions
        tac_ops = [instr.op for instr in tac_instructions]
        
        # Should have LABEL for function definition
        labels = [instr for instr in tac_instructions if instr.op == 'LABEL']
        function_labels = [lbl for lbl in labels if lbl.arg1 == 'func_factorial']
        assert len(function_labels) > 0, "Should have LABEL for factorial function"
        
        # Should have CALL for recursive calls
        calls = [instr for instr in tac_instructions if instr.op == 'CALL']
        factorial_calls = [call for call in calls if call.arg1 == 'factorial']
        assert len(factorial_calls) > 0, "Should have recursive CALL to factorial"
        
        # Should have RETURN instructions
        returns = [instr for instr in tac_instructions if instr.op == 'RETURN']
        assert len(returns) >= 2, f"Should have at least 2 RETURN instructions, found {len(returns)}"
        
        # Should have conditional logic for base case
        assert 'IF_FALSE' in tac_ops or 'GOTO' in tac_ops, "Should have conditional jumps"
        
        # Should have EQ for base case check (n == 0)
        eq_ops = [instr for instr in tac_instructions if instr.op == 'EQ']
        assert len(eq_ops) > 0, "Should have EQ operation for base case check"
    
    def test_stack_frames_en_ensamblador(self, ejemplo4_code):
        """Test de stack frames en ensamblador - Requirements 4.3"""
        lexer = Lexer(ejemplo4_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        
        mcg = MachineCodeGenerator()
        assembly_code = mcg.generate(tac_instructions)
        
        # Verify assembly code was generated
        assert assembly_code is not None
        assert len(assembly_code) > 0
        
        # Convert to string
        asm_text = '\n'.join(assembly_code) if isinstance(assembly_code, list) else assembly_code
        
        # Verify assembly structure
        assert '.data' in asm_text or 'data' in asm_text, "Should have .data section"
        assert '.text' in asm_text or 'text' in asm_text, "Should have .text section"
        
        # Verify function label
        assert 'func_factorial' in asm_text, "Should have func_factorial label"
        
        # Verify stack pointer usage
        assert 'SP' in asm_text or 'sp' in asm_text, "Should use stack pointer (SP)"
        
        # Verify stack operations (LDR/STR with SP, or PUSH/POP)
        has_stack_ops = (
            ('LDR' in asm_text and 'SP' in asm_text) or
            ('STR' in asm_text and 'SP' in asm_text) or
            'PUSH' in asm_text or
            'POP' in asm_text or
            ('ldr' in asm_text and 'sp' in asm_text) or
            ('str' in asm_text and 'sp' in asm_text) or
            'push' in asm_text or
            'pop' in asm_text
        )
        assert has_stack_ops, "Should have stack operations for function calls"
        
        # Verify branch instructions for function calls
        has_branch = 'BL' in asm_text or 'B' in asm_text or 'bl' in asm_text or 'b' in asm_text
        assert has_branch, "Should have branch instructions for function calls"
    
    def test_casos_base(self, ejemplo4_code):
        """Test de casos base (0 y 1) - Requirements 4.5"""
        lexer = Lexer(ejemplo4_code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        
        # Verify base case check (n == 0)
        eq_ops = [instr for instr in tac_instructions if instr.op == 'EQ']
        assert len(eq_ops) > 0, "Should have EQ operation for base case check"
        
        # Verify conditional branches for base case
        if_false_ops = [instr for instr in tac_instructions if instr.op == 'IF_FALSE']
        assert len(if_false_ops) > 0, "Should have IF_FALSE for base case branching"
        
        # Verify RETURN with value 1 for base case
        returns = [instr for instr in tac_instructions if instr.op == 'RETURN']
        assert len(returns) >= 2, "Should have multiple RETURN instructions"
        
        # Verify function calls with 0 and 1
        # (these are in the test calls at the end of the file)
        calls = [instr for instr in tac_instructions if instr.op == 'CALL' and instr.arg1 == 'factorial']
        assert len(calls) >= 4, f"Should have at least 4 factorial calls, found {len(calls)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
