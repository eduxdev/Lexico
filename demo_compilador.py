#!/usr/bin/env python3
"""
Script Principal de Demostración del Compilador
Procesa ejemplos de Python a través de todas las fases del compilador con opciones de línea de comandos
"""

import argparse
import os
import sys
from process_examples import ExampleProcessor, ResultsVisualizer


class CompilerDemo:
    """Clase principal para la demostración del compilador"""
    
    def __init__(self, verbose=False, output_dir='output'):
        self.verbose = verbose
        self.output_dir = output_dir
        self.examples = {
            '1': ('ejemplos/ejemplo1_estudiantes.py', 'Sistema de Gestión de Estudiantes'),
            '2': ('ejemplos/ejemplo2_inventario.py', 'Sistema de Inventario'),
            '3': ('ejemplos/ejemplo3_cadenas.py', 'Procesamiento de Cadenas'),
            '4': ('ejemplos/ejemplo4_factorial.py', 'Cálculo de Factorial Recursivo')
        }
    
    def process_single_example(self, example_num, phase=None, save_output=False):
        """Procesa un ejemplo individual"""
        if example_num not in self.examples:
            print(f"❌ Error: Ejemplo '{example_num}' no existe")
            print(f"Ejemplos disponibles: {', '.join(self.examples.keys())}")
            return False
        
        example_path, description = self.examples[example_num]
        
        if not os.path.exists(example_path):
            print(f"❌ Error: No se encontró el archivo {example_path}")
            return False
        
        print(f"\n{'=' * 100}")
        print(f"Ejemplo {example_num}: {description}")
        print(f"{'=' * 100}\n")
        
        processor = ExampleProcessor(example_path)
        
        # Leer código fuente
        if not processor.read_source():
            print(f"❌ Error al leer el archivo: {processor.errors[-1]}")
            return False
        
        if phase is None or phase == 'all':
            # Procesar todas las fases
            success = self._process_all_phases(processor, save_output)
        else:
            # Procesar solo una fase específica
            success = self._process_specific_phase(processor, phase, save_output)
        
        return success
    
    def _process_all_phases(self, processor, save_output):
        """Procesa todas las fases del compilador"""
        phases = [
            ('lexer', 'Análisis Léxico', processor.run_lexer),
            ('parser', 'Análisis Sintáctico', processor.run_parser),
            ('semantic', 'Análisis Semántico', processor.run_semantic_analyzer),
            ('tac', 'Generación de Código Intermedio (TAC)', processor.run_tac_generator),
            ('optimizer', 'Optimización de Código TAC', processor.run_tac_optimizer),
            ('codegen', 'Generación de Código Ensamblador', processor.run_machine_code_generator)
        ]
        
        for phase_name, phase_desc, phase_func in phases:
            if self.verbose:
                print(f"\n{'─' * 100}")
            print(f"Fase: {phase_desc}...")
            
            if not phase_func():
                print(f"❌ Error en {phase_desc}")
                print(processor.format_error_report())
                return False
            
            # Mostrar resultados según la fase
            self._show_phase_results(processor, phase_name)
        
        # Guardar salidas si se solicita
        if save_output:
            self._save_all_outputs(processor)
        
        print(f"\n{'=' * 100}")
        print(f"✓ Procesamiento completo exitoso para {processor.example_name}")
        print(f"{'=' * 100}\n")
        
        return True
    
    def _process_specific_phase(self, processor, phase, save_output):
        """Procesa solo una fase específica del compilador"""
        phase_map = {
            'lexer': ('Análisis Léxico', [processor.run_lexer]),
            'parser': ('Análisis Sintáctico', [processor.run_lexer, processor.run_parser]),
            'semantic': ('Análisis Semántico', [processor.run_lexer, processor.run_parser, processor.run_semantic_analyzer]),
            'tac': ('Generación TAC', [processor.run_lexer, processor.run_parser, processor.run_semantic_analyzer, processor.run_tac_generator]),
            'optimizer': ('Optimización TAC', [processor.run_lexer, processor.run_parser, processor.run_semantic_analyzer, processor.run_tac_generator, processor.run_tac_optimizer]),
            'codegen': ('Generación de Código', [processor.run_lexer, processor.run_parser, processor.run_semantic_analyzer, processor.run_tac_generator, processor.run_tac_optimizer, processor.run_machine_code_generator])
        }
        
        if phase not in phase_map:
            print(f"❌ Error: Fase '{phase}' no válida")
            print(f"Fases disponibles: {', '.join(phase_map.keys())}")
            return False
        
        phase_desc, phase_funcs = phase_map[phase]
        print(f"\nProcesando hasta fase: {phase_desc}...")
        
        # Ejecutar todas las fases necesarias hasta la solicitada
        for phase_func in phase_funcs:
            if not phase_func():
                print(f"❌ Error en procesamiento")
                print(processor.format_error_report())
                return False
        
        # Mostrar solo los resultados de la fase solicitada
        self._show_phase_results(processor, phase)
        
        # Guardar salida si se solicita
        if save_output:
            self._save_phase_output(processor, phase)
        
        print(f"\n✓ Fase {phase_desc} completada exitosamente\n")
        return True
    
    def _show_phase_results(self, processor, phase):
        """Muestra los resultados de una fase específica"""
        if phase == 'lexer' and processor.tokens:
            print(f"✓ {len(processor.tokens)} tokens generados")
            if self.verbose:
                print("\nTokens:")
                for i, token in enumerate(processor.tokens[:10], 1):  # Mostrar primeros 10
                    print(f"  {i}. {token}")
                if len(processor.tokens) > 10:
                    print(f"  ... ({len(processor.tokens) - 10} tokens más)")
        
        elif phase == 'parser' and processor.ast:
            print(f"✓ AST generado correctamente")
            if self.verbose:
                print("\nAST (primeras líneas):")
                ast_str = processor._format_ast(processor.ast)
                lines = ast_str.split('\n')[:15]
                for line in lines:
                    print(f"  {line}")
                if len(ast_str.split('\n')) > 15:
                    print(f"  ... ({len(ast_str.split('\n')) - 15} líneas más)")
        
        elif phase == 'semantic' and processor.symbol_table:
            print(f"✓ {len(processor.symbol_table)} variables en tabla de símbolos")
            if self.verbose:
                print("\nTabla de Símbolos:")
                print(f"  {'Variable':<20} {'Tipo':<15} {'Inicializada':<15}")
                print(f"  {'-' * 50}")
                for name, info in list(processor.symbol_table.items())[:10]:
                    init = 'Sí' if info['initialized'] else 'No'
                    print(f"  {name:<20} {info['type']:<15} {init:<15}")
                if len(processor.symbol_table) > 10:
                    print(f"  ... ({len(processor.symbol_table) - 10} variables más)")
        
        elif phase == 'tac' and processor.tac_instructions:
            print(f"✓ {len(processor.tac_instructions)} instrucciones TAC generadas")
            if self.verbose:
                print("\nCódigo TAC (primeras instrucciones):")
                for i, instr in enumerate(processor.tac_instructions[:10], 1):
                    print(f"  {i}. {str(instr)}")
                if len(processor.tac_instructions) > 10:
                    print(f"  ... ({len(processor.tac_instructions) - 10} instrucciones más)")
        
        elif phase == 'optimizer' and processor.tac_optimized:
            original = len(processor.tac_instructions) if processor.tac_instructions else 0
            optimized = len(processor.tac_optimized)
            reduction = original - optimized
            print(f"✓ {optimized} instrucciones TAC optimizadas (reducción: {reduction} instrucciones)")
            if self.verbose:
                print("\nCódigo TAC Optimizado (primeras instrucciones):")
                for i, instr in enumerate(processor.tac_optimized[:10], 1):
                    print(f"  {i}. {str(instr)}")
                if len(processor.tac_optimized) > 10:
                    print(f"  ... ({len(processor.tac_optimized) - 10} instrucciones más)")
        
        elif phase == 'codegen' and processor.assembly_code:
            print(f"✓ {len(processor.assembly_code)} líneas de código ensamblador generadas")
            if self.verbose:
                print("\nCódigo Ensamblador (primeras líneas):")
                for i, line in enumerate(processor.assembly_code[:15], 1):
                    print(f"  {line}")
                if len(processor.assembly_code) > 15:
                    print(f"  ... ({len(processor.assembly_code) - 15} líneas más)")
    
    def _save_all_outputs(self, processor):
        """Guarda todas las salidas del procesamiento"""
        print(f"\n{'─' * 100}")
        print("Guardando archivos de salida...")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        saved_files = []
        if processor.tokens:
            saved_files.append(processor.save_tokens(self.output_dir))
        if processor.ast:
            saved_files.append(processor.save_ast(self.output_dir))
        if processor.symbol_table:
            saved_files.append(processor.save_symbol_table(self.output_dir))
        if processor.tac_instructions:
            saved_files.append(processor.save_tac(self.output_dir))
        if processor.tac_optimized:
            saved_files.append(processor.save_tac_optimized(self.output_dir))
        if processor.assembly_code:
            saved_files.append(processor.save_assembly(self.output_dir))
        
        print(f"✓ {len(saved_files)} archivos guardados en '{self.output_dir}/':")
        for filepath in saved_files:
            print(f"  - {filepath}")
    
    def _save_phase_output(self, processor, phase):
        """Guarda la salida de una fase específica"""
        print(f"\n{'─' * 100}")
        print("Guardando archivo de salida...")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        phase_save_map = {
            'lexer': processor.save_tokens,
            'parser': processor.save_ast,
            'semantic': processor.save_symbol_table,
            'tac': processor.save_tac,
            'optimizer': processor.save_tac_optimized,
            'codegen': processor.save_assembly
        }
        
        if phase in phase_save_map:
            filepath = phase_save_map[phase](self.output_dir)
            print(f"✓ Guardado en: {filepath}")
    
    def process_all_examples(self, save_output=False):
        """Procesa todos los ejemplos y genera un reporte resumen"""
        print(f"\n{'=' * 100}")
        print("DEMOSTRACIÓN COMPLETA DEL COMPILADOR")
        print(f"{'=' * 100}\n")
        
        results = []
        
        for example_num in sorted(self.examples.keys()):
            example_path, description = self.examples[example_num]
            
            if not os.path.exists(example_path):
                print(f"⚠ Advertencia: No se encontró {example_path}")
                results.append((example_num, description, False, "Archivo no encontrado"))
                continue
            
            print(f"\n{'=' * 100}")
            print(f"Ejemplo {example_num}: {description}")
            print(f"Archivo: {example_path}")
            print(f"{'=' * 100}\n")
            
            processor = ExampleProcessor(example_path)
            
            # Procesar el ejemplo
            if save_output:
                success = processor.process_complete(self.output_dir)
            else:
                # Procesar sin guardar archivos
                success = self._process_without_saving(processor)
            
            if success:
                results.append((example_num, description, True, "Exitoso"))
            else:
                error_msg = processor.errors[-1] if processor.errors else "Error desconocido"
                results.append((example_num, description, False, error_msg))
        
        # Generar reporte resumen
        self._generate_summary_report(results)
        
        return all(success for _, _, success, _ in results)
    
    def _process_without_saving(self, processor):
        """Procesa un ejemplo sin guardar archivos"""
        # Leer código fuente primero
        if not processor.read_source():
            print(f"❌ Error al leer el archivo: {processor.errors[-1]}")
            return False
        
        # Fase 1: Análisis Léxico
        print("Fase 1: Análisis Léxico...")
        if not processor.run_lexer():
            print(processor.format_error_report())
            return False
        print(f"✓ {len(processor.tokens)} tokens generados")
        
        # Fase 2: Análisis Sintáctico
        print("\nFase 2: Análisis Sintáctico...")
        if not processor.run_parser():
            print(processor.format_error_report())
            return False
        print("✓ AST generado correctamente")
        
        # Fase 3: Análisis Semántico
        print("\nFase 3: Análisis Semántico...")
        if not processor.run_semantic_analyzer():
            print(processor.format_error_report())
            return False
        print(f"✓ {len(processor.symbol_table)} variables en tabla de símbolos")
        
        # Fase 4: Generación de Código Intermedio
        print("\nFase 4: Generación de Código Intermedio (TAC)...")
        if not processor.run_tac_generator():
            print(processor.format_error_report())
            return False
        print(f"✓ {len(processor.tac_instructions)} instrucciones TAC generadas")
        
        # Fase 5: Optimización de Código TAC
        print("\nFase 5: Optimización de Código TAC...")
        if not processor.run_tac_optimizer():
            print(processor.format_error_report())
            return False
        print(f"✓ {len(processor.tac_optimized)} instrucciones TAC optimizadas")
        
        # Fase 6: Generación de Código Ensamblador
        print("\nFase 6: Generación de Código Ensamblador...")
        if not processor.run_machine_code_generator():
            print(processor.format_error_report())
            return False
        print(f"✓ {len(processor.assembly_code)} líneas de código ensamblador generadas")
        
        print(f"\n{'=' * 100}")
        print(f"✓ Procesamiento completo exitoso para {processor.example_name}")
        print(f"{'=' * 100}\n")
        
        return True
    
    def _generate_summary_report(self, results):
        """Genera un reporte resumen del procesamiento"""
        print(f"\n{'=' * 100}")
        print("REPORTE RESUMEN")
        print(f"{'=' * 100}\n")
        
        print(f"{'Ejemplo':<10} {'Descripción':<45} {'Estado':<15}")
        print(f"{'-' * 100}")
        
        for example_num, description, success, message in results:
            status = "✓ EXITOSO" if success else "❌ FALLIDO"
            print(f"{example_num:<10} {description:<45} {status:<15}")
            if not success and self.verbose:
                print(f"           Error: {message}")
        
        successful = sum(1 for _, _, success, _ in results if success)
        total = len(results)
        
        print(f"\n{'-' * 100}")
        print(f"Total: {successful}/{total} ejemplos procesados exitosamente")
        
        if successful == total:
            print("\n🎉 ¡Todos los ejemplos se compilaron correctamente!")
        else:
            print(f"\n⚠️  {total - successful} ejemplo(s) fallaron")
        
        print(f"{'=' * 100}\n")
        
        # Información adicional
        if self.output_dir and os.path.exists(self.output_dir):
            print(f"📁 Archivos de salida guardados en: {self.output_dir}/")
            print(f"{'=' * 100}\n")


def main():
    """Función principal con manejo de argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Demostración del Compilador de Python a Ensamblador x86',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s                          # Procesar todos los ejemplos
  %(prog)s -e 1                     # Procesar solo el Ejemplo 1
  %(prog)s -e 2 -p tac              # Procesar Ejemplo 2 hasta fase TAC
  %(prog)s -e 3 -s                  # Procesar Ejemplo 3 y guardar salidas
  %(prog)s -v                       # Modo verbose con todos los ejemplos
  %(prog)s -e 4 -p codegen -s -v    # Ejemplo 4, hasta codegen, guardar, verbose

Fases disponibles:
  lexer      - Análisis Léxico
  parser     - Análisis Sintáctico
  semantic   - Análisis Semántico
  tac        - Generación de Código Intermedio (TAC)
  optimizer  - Optimización de Código TAC
  codegen    - Generación de Código Ensamblador
  all        - Todas las fases (por defecto)

Ejemplos disponibles:
  1 - Sistema de Gestión de Estudiantes
  2 - Sistema de Inventario
  3 - Procesamiento de Cadenas
  4 - Cálculo de Factorial Recursivo
        """
    )
    
    parser.add_argument(
        '-e', '--example',
        type=str,
        choices=['1', '2', '3', '4'],
        help='Número del ejemplo a procesar (1-4)'
    )
    
    parser.add_argument(
        '-p', '--phase',
        type=str,
        choices=['lexer', 'parser', 'semantic', 'tac', 'optimizer', 'codegen', 'all'],
        default='all',
        help='Fase específica del compilador a ejecutar (por defecto: all)'
    )
    
    parser.add_argument(
        '-s', '--save',
        action='store_true',
        help='Guardar salidas en archivos'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='output',
        help='Directorio de salida para archivos generados (por defecto: output)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Modo verbose - mostrar información detallada'
    )
    
    args = parser.parse_args()
    
    # Crear instancia del demo
    demo = CompilerDemo(verbose=args.verbose, output_dir=args.output)
    
    # Procesar según los argumentos
    if args.example:
        # Procesar un ejemplo específico
        success = demo.process_single_example(
            args.example,
            phase=args.phase if args.phase != 'all' else None,
            save_output=args.save
        )
    else:
        # Procesar todos los ejemplos
        if args.phase != 'all':
            print("⚠️  Advertencia: La opción --phase se ignora cuando se procesan todos los ejemplos")
        success = demo.process_all_examples(save_output=args.save)
    
    # Retornar código de salida apropiado
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
