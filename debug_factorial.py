"""
Script de depuración para el factorial
"""
import sys
import importlib

# Forzar recarga de módulos
if 'tac_interpreter' in sys.modules:
    importlib.reload(sys.modules['tac_interpreter'])

from tac_interpreter import TACInterpreter
from tac_generator import TACGenerator
from python_compiler import Lexer, Parser

code = '''def factorial(n):
    if n == 0:
        return 1
    else:
        temp = n - 1
        result = factorial(temp)
        return n * result

resultado1 = factorial(0)
print(resultado1)

resultado2 = factorial(1)
print(resultado2)

resultado3 = factorial(3)
print(resultado3)

resultado4 = factorial(5)
print(resultado4)
'''

print("Generando TAC...")
lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
gen = TACGenerator()
tac = gen.generate(ast)

print("\nCódigo TAC generado:")
for i, instr in enumerate(tac):
    print(f"{i:3d}. {str(instr)}")

print("\n" + "="*80)
print("Ejecutando con intérprete TAC...")
print("="*80)

try:
    interp = TACInterpreter()
    
    # Debug: mostrar estado inicial
    print(f"Estado inicial:")
    print(f"  Variables: {interp.variables}")
    print(f"  Call stack: {interp.call_stack}")
    print(f"  PC: {interp.pc}")
    
    result = interp.interpret(tac)
    
    print("\n" + "="*80)
    print("RESULTADO:")
    print("="*80)
    print(result)
    print("="*80)
    print("\n✅ ÉXITO")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
