"""
Script principal para ejecutar todos los experimentos del ejercicio MEC.
Este script está diseñado para ejecutarse durante la noche/largo plazo.

Ejecuta una batería completa de experimentos que incluye:
- Baseline con agente aleatorio
- Comparación de profundidades (Minimax y Expectimax)
- Comparación de heurísticas
- Comparación Alpha-Beta Pruning
- Comparación directa Minimax vs Expectimax
"""

import sys
import argparse
from datetime import datetime
import time

from Experiments import ExperimentSuite
from Expectimax_Agent import ExpectimaxAgent, ExpectimaxAgentOptimized
from Minimax_Agent import MinimaxAgent, MinimaxAgentOptimized


def print_header(text):
    """Imprime un header formateado"""
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#  " + text.center(74) + "  #")
    print("#" + " " * 78 + "#")
    print("#" * 80 + "\n")


def run_quick_experiments():
    """
    Ejecuta experimentos rápidos (para pruebas).
    Menos partidas, profundidades menores.
    """
    print_header("MODO RÁPIDO - PRUEBAS")
    print("⚡ Ejecutando experimentos de prueba con configuración reducida...")
    print("   - 5 partidas por configuración")
    print("   - Profundidades: 2, 3")
    print("   - Tiempo estimado: 10-15 minutos\n")
    
    suite = ExperimentSuite(output_dir="results")
    
    # 1. Baseline
    print("\n" + "="*80)
    print("1/4: Baseline con Agente Aleatorio")
    print("="*80)
    suite.run_baseline_comparison(num_games=10)
    
    # 2. Expectimax - Profundidades
    print("\n" + "="*80)
    print("2/4: Expectimax - Comparación de Profundidades")
    print("="*80)
    suite.run_depth_comparison(
        ExpectimaxAgentOptimized, 
        "Expectimax", 
        depths=[2, 3],
        num_games=5,
        weights_config='balanced'
    )
    
    # 3. Minimax - Profundidades
    print("\n" + "="*80)
    print("3/4: Minimax - Comparación de Profundidades")
    print("="*80)
    suite.run_depth_comparison(
        MinimaxAgentOptimized,
        "Minimax",
        depths=[2, 3],
        num_games=5,
        weights_config='balanced'
    )
    
    # 4. Minimax vs Expectimax
    print("\n" + "="*80)
    print("4/4: Minimax vs Expectimax")
    print("="*80)
    suite.run_minimax_vs_expectimax(depth=3, num_games=10, weights_config='balanced')
    
    # Guardar resultados
    suite.save_best_configs()
    
    print_header("✓ EXPERIMENTOS RÁPIDOS COMPLETADOS")


def run_standard_experiments():
    """
    Ejecuta experimentos estándar (para trabajo normal).
    Configuración balanceada entre exhaustividad y tiempo.
    """
    print_header("MODO ESTÁNDAR - EXPERIMENTOS COMPLETOS")
    print("📊 Ejecutando suite completa de experimentos...")
    print("   - 20-30 partidas por configuración")
    print("   - Profundidades: 2, 3, 4")
    print("   - Tiempo estimado: 2-4 horas\n")
    
    suite = ExperimentSuite(output_dir="results")
    start_time = time.time()
    
    # 1. Baseline
    print("\n" + "="*80)
    print("1/6: Baseline con Agente Aleatorio")
    print("="*80)
    suite.run_baseline_comparison(num_games=50)
    
    # 2. Expectimax - Profundidades
    print("\n" + "="*80)
    print("2/6: Expectimax - Comparación de Profundidades")
    print("="*80)
    suite.run_depth_comparison(
        ExpectimaxAgentOptimized,
        "Expectimax",
        depths=[2, 3, 4],
        num_games=20,
        weights_config='balanced'
    )
    
    # 3. Minimax - Profundidades
    print("\n" + "="*80)
    print("3/6: Minimax - Comparación de Profundidades")
    print("="*80)
    suite.run_depth_comparison(
        MinimaxAgentOptimized,
        "Minimax",
        depths=[2, 3, 4],
        num_games=20,
        weights_config='balanced'
    )
    
    # 4. Alpha-Beta Pruning
    print("\n" + "="*80)
    print("4/6: Impacto de Alpha-Beta Pruning")
    print("="*80)
    suite.run_alpha_beta_comparison(depth=3, num_games=20, weights_config='balanced')
    
    # 5. Heurísticas - Expectimax
    print("\n" + "="*80)
    print("5/6: Expectimax - Comparación de Heurísticas")
    print("="*80)
    suite.run_heuristic_comparison(
        ExpectimaxAgentOptimized,
        "Expectimax",
        depth=3,
        num_games=15
    )
    
    # 6. Minimax vs Expectimax
    print("\n" + "="*80)
    print("6/6: Minimax vs Expectimax - Comparación Final")
    print("="*80)
    suite.run_minimax_vs_expectimax(depth=4, num_games=30, weights_config='balanced')
    
    # Guardar resultados
    suite.save_best_configs()
    
    elapsed_time = time.time() - start_time
    print_header(f"✓ EXPERIMENTOS COMPLETADOS en {elapsed_time/3600:.2f} horas")


def run_extensive_experiments():
    """
    Ejecuta experimentos extensivos (para ejecución nocturna).
    Configuración exhaustiva con muchas partidas.
    """
    print_header("MODO EXTENSIVO - EJECUCIÓN NOCTURNA")
    print("🌙 Ejecutando suite exhaustiva de experimentos...")
    print("   - 50-100 partidas por configuración")
    print("   - Profundidades: 2, 3, 4, 5")
    print("   - Todas las configuraciones de heurísticas")
    print("   - Tiempo estimado: 8-12 horas (NOCTURNO)")
    print("\n⚠️  ASEGÚRATE DE:")
    print("   1. Tener suficiente espacio en disco")
    print("   2. Que el ordenador no se apague")
    print("   3. Cerrar otros programas pesados\n")
    
    input("Presiona ENTER para continuar o Ctrl+C para cancelar...")
    
    suite = ExperimentSuite(output_dir="results")
    start_time = time.time()
    
    # 1. Baseline
    print("\n" + "="*80)
    print("1/8: Baseline con Agente Aleatorio")
    print("="*80)
    suite.run_baseline_comparison(num_games=100)
    
    # 2. Expectimax - Profundidades
    print("\n" + "="*80)
    print("2/8: Expectimax - Comparación de Profundidades")
    print("="*80)
    suite.run_depth_comparison(
        ExpectimaxAgentOptimized,
        "Expectimax",
        depths=[2, 3, 4, 5],
        num_games=50,
        weights_config='balanced'
    )
    
    # 3. Minimax - Profundidades
    print("\n" + "="*80)
    print("3/8: Minimax - Comparación de Profundidades")
    print("="*80)
    suite.run_depth_comparison(
        MinimaxAgentOptimized,
        "Minimax",
        depths=[2, 3, 4, 5],
        num_games=50,
        weights_config='balanced'
    )
    
    # 4. Alpha-Beta Pruning
    print("\n" + "="*80)
    print("4/8: Impacto de Alpha-Beta Pruning")
    print("="*80)
    suite.run_alpha_beta_comparison(depth=4, num_games=50, weights_config='balanced')
    
    # 5. Heurísticas - Expectimax
    print("\n" + "="*80)
    print("5/8: Expectimax - Comparación de Heurísticas")
    print("="*80)
    suite.run_heuristic_comparison(
        ExpectimaxAgentOptimized,
        "Expectimax",
        depth=4,
        num_games=30
    )
    
    # 6. Heurísticas - Minimax
    print("\n" + "="*80)
    print("6/8: Minimax - Comparación de Heurísticas")
    print("="*80)
    suite.run_heuristic_comparison(
        MinimaxAgentOptimized,
        "Minimax",
        depth=4,
        num_games=30
    )
    
    # 7. Minimax vs Expectimax (profundidad 4)
    print("\n" + "="*80)
    print("7/8: Minimax vs Expectimax (depth=4)")
    print("="*80)
    suite.run_minimax_vs_expectimax(depth=4, num_games=50, weights_config='balanced')
    
    # 8. Minimax vs Expectimax (profundidad 5)
    print("\n" + "="*80)
    print("8/8: Minimax vs Expectimax (depth=5)")
    print("="*80)
    suite.run_minimax_vs_expectimax(depth=5, num_games=30, weights_config='balanced')
    
    # Guardar resultados
    suite.save_best_configs()
    
    elapsed_time = time.time() - start_time
    print_header(f"✓ EXPERIMENTOS EXTENSIVOS COMPLETADOS en {elapsed_time/3600:.2f} horas")
    
    print("\n📁 ARCHIVOS GENERADOS:")
    print("   - results/*.csv : Resultados de cada experimento")
    print("   - results/best_configurations_*.csv : Mejores configuraciones")
    print("   - models/ : Configuraciones óptimas guardadas")
    print("\n📊 SIGUIENTE PASO:")
    print("   Abre Analysis.ipynb para visualizar y analizar los resultados")


def main():
    parser = argparse.ArgumentParser(
        description='Ejecutar experimentos del ejercicio MEC (2048)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modos de ejecución:
  quick     : Pruebas rápidas (10-15 min) - para verificar que todo funciona
  standard  : Experimentos completos (2-4 horas) - para trabajo normal
  extensive : Experimentos exhaustivos (8-12 horas) - para ejecución nocturna

Ejemplos:
  python run_experiments.py quick      # Prueba rápida
  python run_experiments.py standard   # Ejecución estándar
  python run_experiments.py extensive  # Ejecución nocturna completa
        """
    )
    
    parser.add_argument(
        'mode',
        choices=['quick', 'standard', 'extensive'],
        nargs='?',
        default='standard',
        help='Modo de ejecución (default: standard)'
    )
    
    args = parser.parse_args()
    
    print_header(f"EXPERIMENTOS MEC - 2048")
    print(f"Fecha/Hora inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Modo: {args.mode.upper()}")
    
    try:
        if args.mode == 'quick':
            run_quick_experiments()
        elif args.mode == 'standard':
            run_standard_experiments()
        elif args.mode == 'extensive':
            run_extensive_experiments()
        
        print_header("🎉 ¡TODOS LOS EXPERIMENTOS FINALIZADOS CON ÉXITO! 🎉")
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Revisa los archivos CSV en la carpeta 'results/'")
        print("   2. Abre y ejecuta Analysis.ipynb para visualizar resultados")
        print("   3. Usa los gráficos y estadísticas para tu informe")
        print("\n✓ ¡Buen trabajo! Los experimentos se completaron correctamente.\n")
        
    except KeyboardInterrupt:
        print("\n\n❌ Experimentos interrumpidos por el usuario.")
        print("Los resultados parciales se han guardado en 'results/'")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error durante la ejecución: {str(e)}")
        print("Revisa los logs y los resultados parciales en 'results/'")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
