"""
Script to verify that all examples compile correctly through all phases
"""

from python_compiler import Lexer, Parser
from semantic_analyzer import SemanticAnalyzer
from tac_generator import TACGenerator
from tac_optimizer import TACOptimizer
from machine_code_generator import MachineCodeGenerator

def verify_example(filepath):
    """Verify a single example compiles through all phases"""
    print(f"\n{'='*60}")
    print(f"Verifying: {filepath}")
    print('='*60)
    
    try:
        # Read source code
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        print("✓ Source code loaded")
        
        # Lexical analysis
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print(f"✓ Lexer: {len(tokens)} tokens generated")
        
        # Syntax analysis
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"✓ Parser: AST generated")
        
        # Semantic analysis
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print(f"✓ Semantic Analyzer: {len(analyzer.symbol_table)} variables in symbol table")
        
        # TAC generation
        tac_gen = TACGenerator()
        tac_instructions = tac_gen.generate(ast)
        print(f"✓ TAC Generator: {len(tac_instructions)} TAC instructions generated")
        
        # TAC optimization
        optimizer = TACOptimizer()
        optimized_tac = optimizer.optimize(tac_instructions)
        print(f"✓ TAC Optimizer: {len(optimized_tac)} optimized TAC instructions")
        
        # Machine code generation
        mcg = MachineCodeGenerator()
        assembly_code = mcg.generate(optimized_tac)
        asm_lines = len(assembly_code) if isinstance(assembly_code, list) else len(assembly_code.split('\n'))
        print(f"✓ Machine Code Generator: {asm_lines} lines of assembly code")
        
        print(f"\n✅ SUCCESS: {filepath} compiled successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: {filepath}")
        print(f"Error: {type(e).__name__}: {e}")
        return False

def main():
    """Verify all examples"""
    examples = [
        'ejemplos/ejemplo1_estudiantes.py',
        'ejemplos/ejemplo2_inventario.py',
        'ejemplos/ejemplo3_cadenas.py',
        'ejemplos/ejemplo4_factorial.py'
    ]
    
    print("="*60)
    print("COMPILATION VERIFICATION FOR ALL EXAMPLES")
    print("="*60)
    
    results = []
    for example in examples:
        success = verify_example(example)
        results.append((example, success))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for example, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {example}")
    
    print(f"\nTotal: {passed}/{total} examples compiled successfully")
    
    if passed == total:
        print("\n🎉 All examples compile correctly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} example(s) failed to compile")
        return 1

if __name__ == "__main__":
    exit(main())
