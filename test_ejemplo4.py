"""
Script de prueba para el ejemplo 4 (Factorial)
"""

from python_compiler import Lexer, Parser
from semantic_analyzer import SemanticAnalyzer
from tac_generator import TACGenerator
from tac_optimizer import TACOptimizer
from tac_interpreter import TACInterpreter

# Leer el código del ejemplo 4
with open('ejemplos/ejemplo4_factorial.py', 'r', encoding='utf-8') as f:
    code = f.read()

print("=" * 80)
print("PROBANDO EJEMPLO 4: FACTORIAL RECURSIVO")
print("=" * 80)

try:
    # Fase 1: Análisis Léxico
    print("\n1. Análisis Léxico...")
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print(f"   ✓ {len(tokens)} tokens generados")
    
    # Fase 2: Análisis Sintáctico
    print("\n2. Análisis Sintáctico...")
    parser = Parser(tokens)
    ast = parser.parse()
    print("   ✓ AST generado")
    
    # Fase 3: Análisis Semántico
    print("\n3. Análisis Semántico...")
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    print(f"   ✓ {len(analyzer.symbol_table)} variables en tabla de símbolos")
    
    if analyzer.errors:
        print("\n   ⚠️ Errores semánticos encontrados:")
        for error in analyzer.errors:
            print(f"      - {error}")
    
    # Fase 4: Generación TAC
    print("\n4. Generación de Código Intermedio (TAC)...")
    tac_gen = TACGenerator()
    tac_instructions = tac_gen.generate(ast)
    print(f"   ✓ {len(tac_instructions)} instrucciones TAC generadas")
    
    # Mostrar TAC
    print("\n   Código TAC:")
    for i, instr in enumerate(tac_instructions[:15]):
        print(f"      {i}: {str(instr)}")
    if len(tac_instructions) > 15:
        print(f"      ... ({len(tac_instructions) - 15} instrucciones más)")
    
    # Fase 5: Optimización
    print("\n5. Optimización...")
    optimizer = TACOptimizer()
    optimized_tac = optimizer.optimize(tac_instructions)
    print(f"   ✓ {len(optimized_tac)} instrucciones optimizadas")
    
    # Fase 6: Ejecución
    print("\n6. Ejecución con Intérprete TAC...")
    interpreter = TACInterpreter()
    output = interpreter.interpret(optimized_tac)
    
    print("\n" + "=" * 80)
    print("SALIDA DE LA EJECUCIÓN:")
    print("=" * 80)
    print(output)
    print("=" * 80)
    
    print("\n✅ PRUEBA EXITOSA")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
