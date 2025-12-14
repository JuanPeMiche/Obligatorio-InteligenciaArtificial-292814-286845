"""
Sistema de experimentación para evaluar agentes de 2048.
Ejecuta múltiples partidas, registra métricas y guarda resultados.
"""
import sys
import numpy as np
import pandas as pd
from datetime import datetime
import time
import pickle
import json
from typing import Dict, List, Tuple
from tqdm import tqdm

from GameBoard import GameBoard
from Agent import Agent
from Random_Agent import RandomAgent
from Expectimax_Agent import ExpectimaxAgent, ExpectimaxAgentOptimized
from Minimax_Agent import MinimaxAgent, MinimaxAgentOptimized
from Heuristics import WEIGHT_CONFIGS


class GameExperiment:
    """
    Clase para ejecutar y registrar experimentos con agentes de 2048.
    """
    
    def __init__(self, agent: Agent, agent_name: str, num_games: int = 10):
        """
        Args:
            agent: Agente a evaluar
            agent_name: Nombre descriptivo del agente
            num_games: Número de partidas a ejecutar
        """
        self.agent = agent
        self.agent_name = agent_name
        self.num_games = num_games
        self.results = []
    
    def run_single_game(self, game_id: int, verbose: bool = False) -> Dict:
        """
        Ejecuta una sola partida y registra métricas.
        
        Returns:
            Diccionario con métricas de la partida
        """
        board = GameBoard()
        moves = 0
        start_time = time.time()
        total_nodes_explored = 0
        last_move_time = start_time
        
        done = False
        while not done:
            move_start = time.time()
            action = self.agent.play(board)
            move_time = time.time() - move_start
            
            # Log si un movimiento tarda más de 60 segundos
            if move_time > 60:
                print(f"\n⚠️  Movimiento {moves+1} tardó {move_time:.1f}s")
                sys.stdout.flush()
            
            # Registrar nodos explorados si el agente lo soporta
            if hasattr(self.agent, 'nodes_explored'):
                total_nodes_explored += self.agent.nodes_explored
            
            done = board.play(action)
            done = done or board.get_max_tile() >= 2048  # Win condition
            moves += 1
            
            if verbose and moves % 50 == 0:
                elapsed = time.time() - start_time
                print(f"  Move {moves}, Max tile: {board.get_max_tile()}, Elapsed: {elapsed:.1f}s")
                sys.stdout.flush()
        
        elapsed_time = time.time() - start_time
        
        # Recopilar métricas
        result = {
            'game_id': game_id,
            'agent_name': self.agent_name,
            'max_tile': int(board.get_max_tile()),
            'final_score': self._calculate_score(board),
            'moves': moves,
            'time_seconds': elapsed_time,
            'won': board.get_max_tile() >= 2048,
            'nodes_explored': total_nodes_explored,
            'avg_time_per_move': elapsed_time / moves if moves > 0 else 0,
            'timestamp': datetime.now().isoformat()
        }
        
        # Agregar info específica del agente si está disponible
        if hasattr(self.agent, 'depth'):
            result['depth'] = self.agent.depth
        if hasattr(self.agent, 'use_alpha_beta'):
            result['alpha_beta'] = self.agent.use_alpha_beta
        if hasattr(self.agent, 'pruned_nodes'):
            result['pruned_nodes'] = self.agent.pruned_nodes
        
        return result
    
    def run_experiment(self, verbose: bool = True) -> pd.DataFrame:
        """
        Ejecuta múltiples partidas y retorna resultados.
        
        Returns:
            DataFrame con resultados de todas las partidas
        """
        print(f"\n{'='*60}")
        print(f"Ejecutando experimento: {self.agent_name}")
        print(f"Número de partidas: {self.num_games}")
        print(f"{'='*60}\n")
        sys.stdout.flush()
        
        for game_id in tqdm(range(self.num_games), desc="Partidas", file=sys.stdout):
            result = self.run_single_game(game_id, verbose=False)
            self.results.append(result)
            
            if verbose and (game_id + 1) % max(1, self.num_games // 10) == 0:
                print(f"\nPartida {game_id + 1}/{self.num_games}")
                print(f"  Max tile: {result['max_tile']}")
                print(f"  Moves: {result['moves']}")
                print(f"  Time: {result['time_seconds']:.2f}s")
                sys.stdout.flush()
        
        df = pd.DataFrame(self.results)
        self._print_summary(df)
        sys.stdout.flush()
        
        return df
    
    def _calculate_score(self, board: GameBoard) -> int:
        """
        Calcula el score final del tablero.
        Suma de todas las fichas (se puede ajustar).
        """
        return int(np.sum(board.grid))
    
    def _print_summary(self, df: pd.DataFrame):
        """
        Imprime resumen estadístico de los resultados.
        """
        print(f"\n{'='*60}")
        print(f"RESUMEN - {self.agent_name}")
        print(f"{'='*60}")
        print(f"Partidas jugadas: {len(df)}")
        print(f"\nMax Tile alcanzado:")
        print(f"  Promedio: {df['max_tile'].mean():.1f}")
        print(f"  Mediana: {df['max_tile'].median():.1f}")
        print(f"  Máximo: {df['max_tile'].max()}")
        print(f"  Mínimo: {df['max_tile'].min()}")
        print(f"\nDistribución de max tiles:")
        for tile in sorted(df['max_tile'].unique(), reverse=True):
            count = len(df[df['max_tile'] == tile])
            pct = (count / len(df)) * 100
            print(f"  {tile}: {count} ({pct:.1f}%)")
        print(f"\nScore:")
        print(f"  Promedio: {df['final_score'].mean():.1f}")
        print(f"  Máximo: {df['final_score'].max()}")
        print(f"\nMovimientos:")
        print(f"  Promedio: {df['moves'].mean():.1f}")
        print(f"  Máximo: {df['moves'].max()}")
        print(f"\nTiempo:")
        print(f"  Total: {df['time_seconds'].sum():.1f}s ({df['time_seconds'].sum()/60:.1f} min)")
        print(f"  Promedio por partida: {df['time_seconds'].mean():.2f}s")
        print(f"  Promedio por movimiento: {df['avg_time_per_move'].mean()*1000:.2f}ms")
        
        if 'won' in df.columns:
            wins = df['won'].sum()
            print(f"\nVictorias (2048+): {wins} ({(wins/len(df))*100:.1f}%)")
        
        if 'nodes_explored' in df.columns and df['nodes_explored'].sum() > 0:
            print(f"\nNodos explorados:")
            print(f"  Promedio por partida: {df['nodes_explored'].mean():.0f}")
            print(f"  Total: {df['nodes_explored'].sum():.0f}")
        
        print(f"{'='*60}\n")
        sys.stdout.flush()


class ExperimentSuite:
    """
    Suite completa de experimentos para comparar múltiples agentes.
    """
    
    def __init__(self, output_dir: str = "results"):
        """
        Args:
            output_dir: Directorio donde guardar resultados
        """
        self.output_dir = output_dir
        self.all_results = []
    
    def run_depth_comparison(self, agent_class, agent_type: str, 
                            depths: List[int], num_games: int = 20,
                            weights_config: str = 'balanced'):
        """
        Compara el rendimiento a diferentes profundidades.
        """
        print(f"\n{'#'*60}")
        print(f"# EXPERIMENTO: Comparación de Profundidades - {agent_type}")
        print(f"{'#'*60}\n")
        sys.stdout.flush()
        
        results = []
        for i, depth in enumerate(depths):
            print(f"\n>>> Iniciando profundidad {depth} ({i+1}/{len(depths)})...")
            sys.stdout.flush()
            
            if agent_type == "Minimax":
                agent = agent_class(depth=depth, use_alpha_beta=True, 
                                   weights_config=weights_config)
            else:
                agent = agent_class(depth=depth, weights_config=weights_config)
            
            name = f"{agent_type}_depth{depth}"
            experiment = GameExperiment(agent, name, num_games)
            df = experiment.run_experiment(verbose=True)
            results.append(df)
            
            print(f"\n>>> Completada profundidad {depth} ({i+1}/{len(depths)})")
            sys.stdout.flush()
        
        # Combinar y guardar resultados
        print(f"\n>>> Combinando y guardando resultados...")
        sys.stdout.flush()
        combined_df = pd.concat(results, ignore_index=True)
        filename = f"{self.output_dir}/{agent_type.lower()}_depth_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        combined_df.to_csv(filename, index=False)
        print(f"\n✓ Resultados guardados en: {filename}")
        sys.stdout.flush()
        
        self.all_results.append(combined_df)
        return combined_df
    
    def run_heuristic_comparison(self, agent_class, agent_type: str,
                                depth: int, num_games: int = 20):
        """
        Compara el rendimiento con diferentes configuraciones de heurísticas.
        """
        print(f"\n{'#'*60}")
        print(f"# EXPERIMENTO: Comparación de Heurísticas - {agent_type}")
        print(f"{'#'*60}\n")
        
        results = []
        for config_name in WEIGHT_CONFIGS.keys():
            if agent_type == "Minimax":
                agent = agent_class(depth=depth, use_alpha_beta=True, 
                                   weights_config=config_name)
            else:
                agent = agent_class(depth=depth, weights_config=config_name)
            
            name = f"{agent_type}_{config_name}_d{depth}"
            experiment = GameExperiment(agent, name, num_games)
            df = experiment.run_experiment(verbose=True)
            df['heuristic_config'] = config_name
            results.append(df)
        
        # Combinar y guardar
        combined_df = pd.concat(results, ignore_index=True)
        filename = f"{self.output_dir}/{agent_type.lower()}_heuristic_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        combined_df.to_csv(filename, index=False)
        print(f"\n✓ Resultados guardados en: {filename}")
        
        self.all_results.append(combined_df)
        return combined_df
    
    def run_alpha_beta_comparison(self, depth: int = 4, num_games: int = 20,
                                  weights_config: str = 'balanced'):
        """
        Compara Minimax con y sin Alpha-Beta Pruning.
        """
        print(f"\n{'#'*60}")
        print(f"# EXPERIMENTO: Impacto de Alpha-Beta Pruning")
        print(f"{'#'*60}\n")
        
        results = []
        
        # Sin Alpha-Beta
        agent_no_ab = MinimaxAgent(depth=depth, use_alpha_beta=False, 
                                   weights_config=weights_config)
        exp_no_ab = GameExperiment(agent_no_ab, f"Minimax_NoAB_d{depth}", num_games)
        df_no_ab = exp_no_ab.run_experiment(verbose=True)
        results.append(df_no_ab)
        
        # Con Alpha-Beta
        agent_with_ab = MinimaxAgent(depth=depth, use_alpha_beta=True, 
                                     weights_config=weights_config)
        exp_with_ab = GameExperiment(agent_with_ab, f"Minimax_WithAB_d{depth}", num_games)
        df_with_ab = exp_with_ab.run_experiment(verbose=True)
        results.append(df_with_ab)
        
        # Combinar y guardar
        combined_df = pd.concat(results, ignore_index=True)
        filename = f"{self.output_dir}/alpha_beta_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        combined_df.to_csv(filename, index=False)
        print(f"\n✓ Resultados guardados en: {filename}")
        
        self.all_results.append(combined_df)
        return combined_df
    
    def run_minimax_vs_expectimax(self, depth: int = 4, num_games: int = 30,
                                  weights_config: str = 'balanced'):
        """
        Comparación directa entre Minimax y Expectimax.
        """
        print(f"\n{'#'*60}")
        print(f"# EXPERIMENTO: Minimax vs Expectimax")
        print(f"{'#'*60}\n")
        
        results = []
        
        # Minimax
        minimax_agent = MinimaxAgentOptimized(depth=depth, use_alpha_beta=True,
                                             weights_config=weights_config)
        minimax_exp = GameExperiment(minimax_agent, f"Minimax_d{depth}", num_games)
        df_minimax = minimax_exp.run_experiment(verbose=True)
        results.append(df_minimax)
        
        # Expectimax
        expectimax_agent = ExpectimaxAgentOptimized(depth=depth, 
                                                   weights_config=weights_config)
        expectimax_exp = GameExperiment(expectimax_agent, f"Expectimax_d{depth}", num_games)
        df_expectimax = expectimax_exp.run_experiment(verbose=True)
        results.append(df_expectimax)
        
        # Combinar y guardar
        combined_df = pd.concat(results, ignore_index=True)
        filename = f"{self.output_dir}/minimax_vs_expectimax_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        combined_df.to_csv(filename, index=False)
        print(f"\n✓ Resultados guardados en: {filename}")
        
        # Comparación estadística
        self._compare_agents(df_minimax, df_expectimax, "Minimax", "Expectimax")
        
        self.all_results.append(combined_df)
        return combined_df
    
    def run_baseline_comparison(self, num_games: int = 50):
        """
        Ejecuta baseline con agente aleatorio para comparación.
        """
        print(f"\n{'#'*60}")
        print(f"# EXPERIMENTO: Baseline (Agente Aleatorio)")
        print(f"{'#'*60}\n")
        
        agent = RandomAgent()
        experiment = GameExperiment(agent, "Random_Baseline", num_games)
        df = experiment.run_experiment(verbose=True)
        
        filename = f"{self.output_dir}/baseline_random_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        print(f"\n✓ Resultados guardados en: {filename}")
        
        self.all_results.append(df)
        return df
    
    def _compare_agents(self, df1: pd.DataFrame, df2: pd.DataFrame, 
                       name1: str, name2: str):
        """
        Imprime comparación estadística entre dos agentes.
        """
        print(f"\n{'='*60}")
        print(f"COMPARACIÓN: {name1} vs {name2}")
        print(f"{'='*60}")
        
        metrics = ['max_tile', 'final_score', 'moves', 'time_seconds']
        
        for metric in metrics:
            if metric in df1.columns and metric in df2.columns:
                avg1 = df1[metric].mean()
                avg2 = df2[metric].mean()
                diff_pct = ((avg2 - avg1) / avg1) * 100 if avg1 != 0 else 0
                
                print(f"\n{metric.upper()}:")
                print(f"  {name1}: {avg1:.2f}")
                print(f"  {name2}: {avg2:.2f}")
                print(f"  Diferencia: {diff_pct:+.1f}%")
        
        print(f"{'='*60}\n")
    
    def save_best_configs(self):
        """
        Guarda las mejores configuraciones encontradas.
        """
        if not self.all_results:
            print("No hay resultados para guardar.")
            return
        
        # Combinar todos los resultados
        all_df = pd.concat(self.all_results, ignore_index=True)
        
        # Encontrar mejores configuraciones por max_tile promedio
        best_configs = all_df.groupby('agent_name').agg({
            'max_tile': ['mean', 'std', 'max'],
            'final_score': 'mean',
            'moves': 'mean',
            'time_seconds': 'mean'
        }).round(2)
        
        best_configs = best_configs.sort_values(('max_tile', 'mean'), ascending=False)
        
        print(f"\n{'='*60}")
        print("MEJORES CONFIGURACIONES")
        print(f"{'='*60}")
        print(best_configs)
        
        # Guardar
        filename = f"{self.output_dir}/best_configurations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        best_configs.to_csv(filename)
        print(f"\n✓ Mejores configuraciones guardadas en: {filename}")
        
        # Guardar como pickle también
        pickle_file = f"{self.output_dir}/all_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
        with open(pickle_file, 'wb') as f:
            pickle.dump(self.all_results, f)
        print(f"✓ Resultados completos guardados en: {pickle_file}")


def run_quick_test():
    """
    Prueba rápida para verificar que todo funciona.
    """
    print("\n" + "="*60)
    print("PRUEBA RÁPIDA")
    print("="*60 + "\n")
    
    # Test con Expectimax
    agent = ExpectimaxAgent(depth=3, weights_config='balanced')
    experiment = GameExperiment(agent, "Expectimax_Quick_Test", num_games=3)
    df = experiment.run_experiment(verbose=True)
    
    return df


if __name__ == "__main__":
    # Prueba rápida
    run_quick_test()
