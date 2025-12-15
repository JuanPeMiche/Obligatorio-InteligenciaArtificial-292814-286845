"""
Script principal para ejecutar TODOS los experimentos del obligatorio.

Estructura de experimentos:
- 3 Agentes: Minimax, Minimax+AlphaBeta, Expectimax
- 3 Heurísticas: Simple, Intermediate, Complex
- 2 Profundidades: 3, 4
Total: 3 × 3 × 2 = 18 experimentos

Cada experimento ejecuta 20 partidas y guarda resultados en CSV.
"""

import sys
import os
import time
import pandas as pd
from datetime import datetime
from typing import Dict, List

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Experiments import GameExperiment
from Minimax_Agent import MinimaxAgent
from Expectimax_Agent import ExpectimaxAgent
from Heuristics import get_heuristic


def print_header(text: str):
    """Imprime un header formateado"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")


def run_complete_experiments(num_games: int = 20):
    """
    Ejecuta la suite COMPLETA de experimentos según el obligatorio.
    
    Args:
        num_games: Número de partidas por experimento
    """
    print_header("EXPERIMENTOS COMPLETOS - OBLIGATORIO 2048")
    
    # Crear directorio de resultados si no existe
    os.makedirs("results", exist_ok=True)
    
    # Configuración de experimentos
    depths = [3, 4]
    heuristics = ['simple', 'intermediate', 'complex']
    configs = [1, 2]  # Dos configuraciones de pesos por heurística
    
    # Registro de todos los experimentos
    all_experiments = []
    experiment_number = 1
    total_experiments = len(depths) * len(heuristics) * len(configs) * 3  # 2 depths × 3 heurísticas × 2 configs × 3 agentes
    
    print(f"Total de experimentos a ejecutar: {total_experiments}")
    print(f"Partidas por experimento: {num_games}")
    print(f"Total de partidas: {total_experiments * num_games}")
    print(f"\nTiempo estimado: 6-12 horas\n")
    
    try:
        input("Presiona ENTER para comenzar...")
    except EOFError:
        print("Iniciando automáticamente...")
    
    start_time = time.time()
    
    # Iterar por cada profundidad PRIMERO
    for depth in depths:
        print_header(f"PROFUNDIDAD: {depth}")
        
        # Iterar por cada heurística
        for heuristic_name in heuristics:
            
            # Iterar por cada configuración de pesos
            for config_num in configs:
                print(f"\n{'#' * 80}")
                print(f"  HEURÍSTICA: {heuristic_name.upper()} - CONFIG {config_num}")
                print(f"{'#' * 80}\n")
                
                heuristic_func = get_heuristic(heuristic_name)
                
                # Crear función wrapper que incluye el parámetro config
                def make_heuristic_with_config(heur_func, cfg):
                    return lambda board: heur_func(board, config=cfg)
                
                heuristic_with_config = make_heuristic_with_config(heuristic_func, config_num)
                heuristic_with_config = make_heuristic_with_config(heuristic_func, config_num)
            
                # ========== EXPERIMENTO 1: Minimax SIN Alpha-Beta ==========
                print(f"\n[{experiment_number}/{total_experiments}] Minimax (sin AB) - {heuristic_name} - config{config_num} - depth={depth}")
                
                agent_minimax = MinimaxAgent(
                    depth=depth,
                    use_alpha_beta=False,
                    weights_config=None,
                    weights=None
                )
                agent_minimax.heuristic_func = heuristic_with_config
                agent_name = f"Minimax_NoAB_{heuristic_name}_c{config_num}_d{depth}"
                
                experiment = GameExperiment(agent_minimax, agent_name, num_games)
                df = experiment.run_experiment(verbose=True)
                df['heuristic'] = heuristic_name
                df['config'] = config_num
                df['depth'] = depth
                df['alpha_beta'] = False
                df['algorithm'] = 'minimax'
                
                # Guardar resultado individual
                filename = f"results/{agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(filename, index=False)
                print(f"Guardado: {filename}")
                
                all_experiments.append(df)
                experiment_number += 1
                
                # ========== EXPERIMENTO 2: Minimax CON Alpha-Beta ==========
                print(f"\n[{experiment_number}/{total_experiments}] Minimax (con AB) - {heuristic_name} - config{config_num} - depth={depth}")
                
                agent_minimax_ab = MinimaxAgent(
                    depth=depth,
                    use_alpha_beta=True,
                    weights_config=None,
                    weights=None
                )
                agent_minimax_ab.heuristic_func = heuristic_with_config
                agent_name_ab = f"Minimax_AB_{heuristic_name}_c{config_num}_d{depth}"
                
                experiment_ab = GameExperiment(agent_minimax_ab, agent_name_ab, num_games)
                df_ab = experiment_ab.run_experiment(verbose=True)
                df_ab['heuristic'] = heuristic_name
                df_ab['config'] = config_num
                df_ab['depth'] = depth
                df_ab['alpha_beta'] = True
                df_ab['algorithm'] = 'minimax'
                
                # Guardar resultado individual
                filename_ab = f"results/{agent_name_ab}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df_ab.to_csv(filename_ab, index=False)
                print(f"Guardado: {filename_ab}")
                
                all_experiments.append(df_ab)
                experiment_number += 1
                
                # ========== EXPERIMENTO 3: Expectimax ==========
                print(f"\n[{experiment_number}/{total_experiments}] Expectimax - {heuristic_name} - config{config_num} - depth={depth}")
                
                agent_expectimax = ExpectimaxAgent(
                    depth=depth,
                    weights_config=None,
                    weights=None
                )
                agent_expectimax.heuristic_func = heuristic_with_config
                agent_name_exp = f"Expectimax_{heuristic_name}_c{config_num}_d{depth}"
                
                experiment_exp = GameExperiment(agent_expectimax, agent_name_exp, num_games)
                df_exp = experiment_exp.run_experiment(verbose=True)
                df_exp['heuristic'] = heuristic_name
                df_exp['config'] = config_num
                df_exp['depth'] = depth
                df_exp['alpha_beta'] = False
                df_exp['algorithm'] = 'expectimax'
                
                # Guardar resultado individual
                filename_exp = f"results/{agent_name_exp}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df_exp.to_csv(filename_exp, index=False)
                print(f"Guardado: {filename_exp}")
                
                all_experiments.append(df_exp)
                experiment_number += 1
                
                # Progreso
                elapsed = time.time() - start_time
                avg_time_per_exp = elapsed / (experiment_number - 1)
                remaining_exp = total_experiments - (experiment_number - 1)
                eta = avg_time_per_exp * remaining_exp
                
                print(f"\nProgreso: {experiment_number-1}/{total_experiments} completados")
                print(f"Tiempo transcurrido: {elapsed/60:.1f} min")
                print(f"ETA: {eta/60:.1f} min")
    
    # ========== GUARDAR RESULTADOS COMBINADOS ==========
    print_header("GUARDANDO RESULTADOS COMBINADOS")
    
    combined_df = pd.concat(all_experiments, ignore_index=True)
    combined_filename = f"results/all_experiments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    combined_df.to_csv(combined_filename, index=False)
    print(f"Todos los resultados guardados en: {combined_filename}")
    
    # ========== RESUMEN FINAL ==========
    total_time = time.time() - start_time
    print_header("EXPERIMENTOS COMPLETADOS")
    print(f"{total_experiments} experimentos completados")
    print(f"{total_experiments * num_games} partidas jugadas")
    print(f"Tiempo total: {total_time/60:.1f} minutos ({total_time/3600:.2f} horas)")
    print(f"Resultados en carpeta: results/")
    print(f"\nPara analizar los resultados, ejecuta: jupyter notebook Analysis.ipynb")


def run_quick_test():
    """
    Ejecuta un test rápido con menos partidas para verificar que todo funciona.
    """
    print_header("TEST RÁPIDO (5 partidas por experimento)")
    print("Tiempo estimado: 1-2 horas")
    print("\nEsto ejecutará todos los experimentos con solo 5 partidas cada uno.")
    
    try:
        response = input("\n¿Continuar? (S/N): ")
    except EOFError:
        response = "S"
        print("S")
    
    if response.lower() != 's':
        print("Test cancelado")
        return
    
    run_complete_experiments(num_games=5)


def main():
    """Punto de entrada principal"""
    print("\n" + "=" * 80)
    print("EXPERIMENTOS 2048 - OBLIGATORIO MEC")
    print("=" * 80)
    print("\nModos disponibles:")
    print("1. Quick Test (5 partidas/experimento) - 1-2 horas")
    print("2. Standard (20 partidas/experimento) - 6-12 horas")
    print("3. Salir")
    
    choice = input("\nSelecciona una opción (1-3): ")
    
    if choice == "1":
        run_quick_test()
    elif choice == "2":
        print_header("MODO STANDARD")
        print("ADVERTENCIA: Esto tomará 6-12 horas")
        print("Asegúrate de que:")
        print("   - El ordenador NO se suspenda automáticamente")
        print("   - Tengas al menos 1 GB de espacio libre")
        print("   - Otros programas pesados estén cerrados")
        
        try:
            response = input("\n¿Continuar? (S/N): ")
        except EOFError:
            response = "S"
            print("S")
        
        if response.lower() == 's':
            run_complete_experiments(num_games=20)
        else:
            print("Experimentos cancelados")
    else:
        print("Saliendo...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExperimentos interrumpidos por el usuario")
        print("Los resultados parciales se han guardado en 'results/'")
    except Exception as e:
        print(f"\n\nError durante los experimentos: {e}")
        import traceback
        traceback.print_exc()
