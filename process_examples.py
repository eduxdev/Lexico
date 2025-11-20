"""
Script de Procesamiento de Ejemplos
Procesa ejemplos de Python a través de todas las fases del compilador
"""

import os
from python_compiler import Lexer, Parser, LexerError, ParserError
from semantic_analyzer import SemanticAnalyzer, SemanticError
from tac_generator import TACGenerator
from tac_optimizer import TACOptimizer
from machine_code_generator import MachineCodeGenerator


class ExampleProcessor:
    """Procesa un ejemplo completo a través de todas las fases del compilador"""
    
    def __init__(self, example_path):
        self.example_path = example_path
        self.example_name = os.path.basename(example_path).replace('.py', '')
        self.source_code = None
        self.tokens = None
        self.ast = None
        self.symbol_table = None
        self.tac_instructions = None
        self.tac_optimized = None
        self.assembly_code = None
        self.errors = []
    
    def read_source(self):
        """Lee el código fuente del ejemplo"""
        try:
            with open(self.example_path, 'r', encoding='utf-8') as f:
                self.source_code = f.read()
            return True
        except Exception as e:
            self.errors.append(f"Error al leer archivo: {e}")
            return False
    
    def run_lexer(self):
        """Ejecuta el análisis léxico"""
        try:
            lexer = Lexer(self.source_code)
            self.tokens = lexer.tokenize()
            return True
        except LexerError as e:
            # Extraer información de línea del mensaje de error
            error_msg = str(e)
            self.errors.append(f"❌ Error Léxico: {error_msg}")
            return False
        except Exception as e:
            self.errors.append(f"❌ Error inesperado en análisis léxico: {e}")
            return False
    
    def run_parser(self):
        """Ejecuta el análisis sintáctico"""
        try:
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            return True
        except ParserError as e:
            # Extraer información de línea del mensaje de error
            error_msg = str(e)
            self.errors.append(f"❌ Error Sintáctico: {error_msg}")
            return False
        except Exception as e:
            self.errors.append(f"❌ Error inesperado en análisis sintáctico: {e}")
            return False
    
    def run_semantic_analyzer(self):
        """Ejecuta el análisis semántico"""
        try:
            analyzer = SemanticAnalyzer()
            success = analyzer.analyze(self.ast)
            self.symbol_table = analyzer.symbol_table
            
            if not success:
                for error in analyzer.errors:
                    # Los errores semánticos ya incluyen información de línea
                    self.errors.append(f"❌ Error Semántico: {error}")
                return False
            
            return True
        except SemanticError as e:
            # Extraer información de línea del mensaje de error
            error_msg = str(e)
            self.errors.append(f"❌ Error Semántico: {error_msg}")
            return False
        except Exception as e:
            self.errors.append(f"❌ Error inesperado en análisis semántico: {e}")
            return False
    
    def run_tac_generator(self):
        """Ejecuta el generador de código intermedio"""
        try:
            generator = TACGenerator()
            self.tac_instructions = generator.generate(self.ast)
            return True
        except Exception as e:
            self.errors.append(f"Error en generación TAC: {e}")
            return False
    
    def run_tac_optimizer(self):
        """Ejecuta el optimizador de código TAC"""
        try:
            optimizer = TACOptimizer()
            self.tac_optimized = optimizer.optimize(self.tac_instructions)
            return True
        except Exception as e:
            self.errors.append(f"Error en optimización TAC: {e}")
            return False
    
    def run_machine_code_generator(self):
        """Ejecuta el generador de código ensamblador"""
        try:
            generator = MachineCodeGenerator()
            self.assembly_code = generator.generate(self.tac_optimized)
            return True
        except Exception as e:
            self.errors.append(f"Error en generación de código máquina: {e}")
            return False
    
    def save_tokens(self, output_dir='output'):
        """Guarda los tokens en un archivo"""
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{self.example_name}.tokens")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("TOKENS\n")
            f.write("=" * 100 + "\n\n")
            for i, token in enumerate(self.tokens, 1):
                f.write(f"{i:4d}. {token}\n")
        
        return output_path
    
    def save_ast(self, output_dir='output'):
        """Guarda el AST en un archivo"""
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{self.example_name}.ast")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("ABSTRACT SYNTAX TREE (AST)\n")
            f.write("=" * 100 + "\n\n")
            f.write(self._format_ast(self.ast))
        
        return output_path
    
    def save_symbol_table(self, output_dir='output'):
        """Guarda la tabla de símbolos en un archivo"""
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{self.example_name}.symbols")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("TABLA DE SÍMBOLOS\n")
            f.write("=" * 100 + "\n\n")
            f.write(f"{'Variable':<20} {'Tipo':<15} {'Inicializada':<15} {'Línea':<10}\n")
            f.write("-" * 100 + "\n")
            
            for name, info in self.symbol_table.items():
                f.write(f"{name:<20} {info['type']:<15} {'Sí' if info['initialized'] else 'No':<15} {info['line']:<10}\n")
        
        return output_path
    
    def save_tac(self, output_dir='output'):
        """Guarda el código TAC en un archivo"""
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{self.example_name}.tac")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("CÓDIGO INTERMEDIO (TAC)\n")
            f.write("=" * 100 + "\n\n")
            for i, instr in enumerate(self.tac_instructions, 1):
                f.write(f"{i:4d}. {str(instr)}\n")
        
        return output_path
    
    def save_tac_optimized(self, output_dir='output'):
        """Guarda el código TAC optimizado en un archivo"""
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{self.example_name}.tac.opt")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("CÓDIGO INTERMEDIO OPTIMIZADO (TAC)\n")
            f.write("=" * 100 + "\n\n")
            for i, instr in enumerate(self.tac_optimized, 1):
                f.write(f"{i:4d}. {str(instr)}\n")
        
        return output_path
    
    def save_assembly(self, output_dir='output'):
        """Guarda el código ensamblador en un archivo"""
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{self.example_name}.asm")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("; CÓDIGO ENSAMBLADOR\n")
            f.write("; " + "=" * 98 + "\n\n")
            for line in self.assembly_code:
                f.write(f"{line}\n")
        
        return output_path
    
    def format_error_report(self):
        """Formatea un reporte de errores con información detallada"""
        if not self.errors:
            return ""
        
        report = "\n" + "=" * 100 + "\n"
        report += "REPORTE DE ERRORES\n"
        report += "=" * 100 + "\n\n"
        
        for i, error in enumerate(self.errors, 1):
            report += f"{i}. {error}\n"
        
        report += "\n" + "=" * 100 + "\n"
        return report
    
    def process_complete(self, output_dir='output'):
        """Procesa el ejemplo completo a través de todas las fases"""
        print(f"\n{'=' * 100}")
        print(f"Procesando: {self.example_name}")
        print(f"{'=' * 100}\n")
        
        # Fase 1: Leer código fuente
        print("Fase 1: Leyendo código fuente...")
        if not self.read_source():
            print(f"❌ Error: {self.errors[-1]}")
            print(self.format_error_report())
            return False
        print("✓ Código fuente leído correctamente")
        
        # Fase 2: Análisis Léxico
        print("\nFase 2: Análisis Léxico...")
        if not self.run_lexer():
            print(self.format_error_report())
            return False
        print(f"✓ {len(self.tokens)} tokens generados")
        tokens_path = self.save_tokens(output_dir)
        print(f"  Guardado en: {tokens_path}")
        
        # Fase 3: Análisis Sintáctico
        print("\nFase 3: Análisis Sintáctico...")
        if not self.run_parser():
            print(self.format_error_report())
            return False
        print("✓ AST generado correctamente")
        ast_path = self.save_ast(output_dir)
        print(f"  Guardado en: {ast_path}")
        
        # Fase 4: Análisis Semántico
        print("\nFase 4: Análisis Semántico...")
        if not self.run_semantic_analyzer():
            print(self.format_error_report())
            return False
        print(f"✓ {len(self.symbol_table)} variables en tabla de símbolos")
        symbols_path = self.save_symbol_table(output_dir)
        print(f"  Guardado en: {symbols_path}")
        
        # Fase 5: Generación de Código Intermedio
        print("\nFase 5: Generación de Código Intermedio (TAC)...")
        if not self.run_tac_generator():
            print(self.format_error_report())
            return False
        print(f"✓ {len(self.tac_instructions)} instrucciones TAC generadas")
        tac_path = self.save_tac(output_dir)
        print(f"  Guardado en: {tac_path}")
        
        # Fase 6: Optimización de Código TAC
        print("\nFase 6: Optimización de Código TAC...")
        if not self.run_tac_optimizer():
            print(self.format_error_report())
            return False
        print(f"✓ {len(self.tac_optimized)} instrucciones TAC optimizadas")
        tac_opt_path = self.save_tac_optimized(output_dir)
        print(f"  Guardado en: {tac_opt_path}")
        
        # Fase 7: Generación de Código Ensamblador
        print("\nFase 7: Generación de Código Ensamblador...")
        if not self.run_machine_code_generator():
            print(self.format_error_report())
            return False
        print(f"✓ {len(self.assembly_code)} líneas de código ensamblador generadas")
        asm_path = self.save_assembly(output_dir)
        print(f"  Guardado en: {asm_path}")
        
        print(f"\n{'=' * 100}")
        print(f"✓ Procesamiento completo exitoso para {self.example_name}")
        print(f"{'=' * 100}\n")
        
        return True
    
    def _format_ast(self, node, indent=0):
        """Formatea el AST para visualización"""
        result = ""
        indent_str = "  " * indent
        
        node_name = node.__class__.__name__
        result += f"{indent_str}{node_name}\n"
        
        if hasattr(node, '__dict__'):
            for attr, value in node.__dict__.items():
                if attr.startswith('_'):
                    continue
                
                if isinstance(value, list):
                    if value:
                        result += f"{indent_str}  {attr}:\n"
                        for item in value:
                            if hasattr(item, '__class__') and hasattr(item.__class__, '__name__'):
                                result += self._format_ast(item, indent + 2)
                            else:
                                result += f"{indent_str}    {item}\n"
                elif hasattr(value, '__class__') and hasattr(value.__class__, '__name__') and value.__class__.__module__ == 'python_compiler':
                    result += f"{indent_str}  {attr}:\n"
                    result += self._format_ast(value, indent + 2)
                else:
                    result += f"{indent_str}  {attr}: {value}\n"
        
        return result


def process_all_examples(examples_dir='ejemplos', output_dir='output'):
    """Procesa todos los ejemplos en el directorio"""
    examples = [
        'ejemplo1_estudiantes.py',
        'ejemplo2_inventario.py',
        'ejemplo3_cadenas.py',
        'ejemplo4_factorial.py'
    ]
    
    results = []
    
    for example in examples:
        example_path = os.path.join(examples_dir, example)
        if os.path.exists(example_path):
            processor = ExampleProcessor(example_path)
            success = processor.process_complete(output_dir)
            results.append((example, success))
        else:
            print(f"⚠ Advertencia: No se encontró {example_path}")
            results.append((example, False))
    
    # Resumen final
    print(f"\n{'=' * 100}")
    print("RESUMEN DE PROCESAMIENTO")
    print(f"{'=' * 100}\n")
    
    for example, success in results:
        status = "✓ EXITOSO" if success else "❌ FALLIDO"
        print(f"{example:<40} {status}")
    
    successful = sum(1 for _, success in results if success)
    print(f"\nTotal: {successful}/{len(results)} ejemplos procesados exitosamente")
    print(f"{'=' * 100}\n")


class ResultsVisualizer:
    """Visualiza los resultados del procesamiento de un ejemplo"""
    
    def __init__(self, processor):
        self.processor = processor
    
    def show_source_code(self):
        """Muestra el código fuente original"""
        print(f"\n{'=' * 100}")
        print("CÓDIGO FUENTE ORIGINAL")
        print(f"{'=' * 100}\n")
        print(self.processor.source_code)
    
    def show_tokens(self):
        """Muestra los tokens generados"""
        print(f"\n{'=' * 100}")
        print("TOKENS GENERADOS")
        print(f"{'=' * 100}\n")
        
        for i, token in enumerate(self.processor.tokens, 1):
            print(f"{i:4d}. {token}")
    
    def show_ast(self):
        """Muestra el AST formateado"""
        print(f"\n{'=' * 100}")
        print("ABSTRACT SYNTAX TREE (AST)")
        print(f"{'=' * 100}\n")
        print(self.processor._format_ast(self.processor.ast))
    
    def show_symbol_table(self):
        """Muestra la tabla de símbolos"""
        print(f"\n{'=' * 100}")
        print("TABLA DE SÍMBOLOS")
        print(f"{'=' * 100}\n")
        print(f"{'Variable':<20} {'Tipo':<15} {'Inicializada':<15} {'Línea':<10}")
        print("-" * 100)
        
        for name, info in self.processor.symbol_table.items():
            print(f"{name:<20} {info['type']:<15} {'Sí' if info['initialized'] else 'No':<15} {info['line']:<10}")
    
    def show_tac(self):
        """Muestra el código TAC generado"""
        print(f"\n{'=' * 100}")
        print("CÓDIGO INTERMEDIO (TAC)")
        print(f"{'=' * 100}\n")
        
        for i, instr in enumerate(self.processor.tac_instructions, 1):
            print(f"{i:4d}. {str(instr)}")
    
    def show_tac_optimized(self):
        """Muestra el código TAC optimizado"""
        print(f"\n{'=' * 100}")
        print("CÓDIGO INTERMEDIO OPTIMIZADO (TAC)")
        print(f"{'=' * 100}\n")
        
        for i, instr in enumerate(self.processor.tac_optimized, 1):
            print(f"{i:4d}. {str(instr)}")
        
        # Mostrar comparación
        original_count = len(self.processor.tac_instructions)
        optimized_count = len(self.processor.tac_optimized)
        reduction = original_count - optimized_count
        
        print(f"\n{'=' * 100}")
        print(f"Instrucciones originales: {original_count}")
        print(f"Instrucciones optimizadas: {optimized_count}")
        print(f"Reducción: {reduction} instrucciones ({reduction/original_count*100:.1f}%)")
        print(f"{'=' * 100}")
    
    def show_assembly(self):
        """Muestra el código ensamblador"""
        print(f"\n{'=' * 100}")
        print("CÓDIGO ENSAMBLADOR")
        print(f"{'=' * 100}\n")
        
        for line in self.processor.assembly_code:
            print(line)
    
    def show_all(self):
        """Muestra todos los resultados"""
        self.show_source_code()
        self.show_tokens()
        self.show_ast()
        self.show_symbol_table()
        self.show_tac()
        self.show_tac_optimized()
        self.show_assembly()
        
        print(f"\n{'=' * 100}")
        print(f"VISUALIZACIÓN COMPLETA DE: {self.processor.example_name}")
        print(f"{'=' * 100}\n")


def visualize_example(example_path, show_all=True):
    """Procesa y visualiza un ejemplo"""
    processor = ExampleProcessor(example_path)
    
    # Procesar el ejemplo
    if not processor.process_complete():
        print(f"\n❌ Error al procesar {example_path}")
        print(processor.format_error_report())
        return False
    
    # Visualizar resultados
    visualizer = ResultsVisualizer(processor)
    
    if show_all:
        visualizer.show_all()
    
    return True


def visualize_all_examples(examples_dir='ejemplos'):
    """Procesa y visualiza todos los ejemplos"""
    examples = [
        'ejemplo1_estudiantes.py',
        'ejemplo2_inventario.py',
        'ejemplo3_cadenas.py',
        'ejemplo4_factorial.py'
    ]
    
    for example in examples:
        example_path = os.path.join(examples_dir, example)
        if os.path.exists(example_path):
            visualize_example(example_path, show_all=True)
            print("\n" + "=" * 100)
            print("Presione Enter para continuar al siguiente ejemplo...")
            print("=" * 100)
            input()
        else:
            print(f"⚠ Advertencia: No se encontró {example_path}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # Modo: procesar un ejemplo específico
        example_path = sys.argv[1]
        visualize_example(example_path)
    else:
        # Modo: procesar todos los ejemplos
        process_all_examples()
