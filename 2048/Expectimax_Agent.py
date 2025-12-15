"""
Agente que utiliza el algoritmo Expectimax para jugar 2048.
Expectimax es más adecuado para juegos con elementos aleatorios (estocásticos).
"""
from Agent import Agent
from GameBoard import GameBoard
import numpy as np


class ExpectimaxAgent(Agent):
    """
    Agente que usa búsqueda Expectimax.
    - Nodos MAX: elige la mejor acción del jugador
    - Nodos CHANCE: calcula el valor esperado de las fichas aleatorias
    """
    
    def __init__(self, depth=4, weights=None, weights_config=None):
        """
        Args:
            depth: Profundidad máxima de búsqueda
            weights: DEPRECATED - No se usa
            weights_config: DEPRECATED - No se usa
        """
        self.depth = depth
        self.heuristic_func = None  # Se asigna externamente
        
        self.nodes_explored = 0  # Para estadísticas
        self.use_adaptive_depth = True  # Activar profundidad adaptativa
    
    def get_adaptive_depth(self, board: GameBoard) -> int:
        """Ajusta profundidad según número de celdas vacías."""
        if not self.use_adaptive_depth:
            return self.depth
        
        empty_cells = len(board.get_available_cells())
        
        if empty_cells <= 3:
            return self.depth + 1
        elif empty_cells <= 6:
            return self.depth
        elif empty_cells <= 10:
            return max(2, self.depth - 1)
        else:
            return max(2, self.depth - 2)
    
    def play(self, board: GameBoard) -> int:
        """
        Elige la mejor acción usando Expectimax con profundidad adaptativa.
        
        Returns:
            Acción a tomar (0=UP, 1=DOWN, 2=LEFT, 3=RIGHT)
        """
        self.nodes_explored = 0
        
        # Usar profundidad adaptativa
        depth = self.get_adaptive_depth(board)
        
        best_action = None
        best_value = -np.inf
        
        available_moves = board.get_available_moves()
        
        if not available_moves:
            return 0  # No hay movimientos válidos
        
        # Evaluar cada movimiento posible
        for move in available_moves:
            board_copy = board.clone()
            board_copy.move(move)
            
            # Calcular valor esperado del movimiento
            value = self.expectimax(board_copy, depth - 1, False)
            
            if value > best_value:
                best_value = value
                best_action = move
        
        return best_action if best_action is not None else available_moves[0]
    
    def expectimax(self, board: GameBoard, depth: int, is_maximizing: bool) -> float:
        """
        Algoritmo Expectimax recursivo.
        
        Args:
            board: Estado actual del tablero
            depth: Profundidad restante
            is_maximizing: True si es turno del jugador (MAX), False si es nodo de chance
        
        Returns:
            Valor del estado
        """
        self.nodes_explored += 1
        
        # Caso base: profundidad 0 o juego terminado
        if depth == 0 or len(board.get_available_moves()) == 0:
            return self.heuristic_utility(board)
        
        if is_maximizing:
            # Nodo MAX: el jugador elige la mejor acción
            return self.max_node(board, depth)
        else:
            # Nodo CHANCE: se agrega una ficha aleatoria
            return self.chance_node(board, depth)
    
    def max_node(self, board: GameBoard, depth: int) -> float:
        """
        Nodo maximizador: el jugador elige la mejor acción.
        """
        max_value = -np.inf
        available_moves = board.get_available_moves()
        
        if not available_moves:
            return self.heuristic_utility(board)
        
        for move in available_moves:
            board_copy = board.clone()
            board_copy.move(move)
            
            # Después del movimiento del jugador, viene un nodo de chance
            value = self.expectimax(board_copy, depth - 1, False)
            max_value = max(max_value, value)
        
        return max_value
    
    def chance_node(self, board: GameBoard, depth: int) -> float:
        """
        Nodo de chance: calcula el valor esperado de agregar fichas aleatorias.
        Optimizado con muestreo adaptativo según profundidad.
        """
        available_cells = board.get_available_cells()
        
        if not available_cells:
            return self.heuristic_utility(board)
        
        expected_value = 0.0
        num_empty = len(available_cells)
        
        # Muestreo adaptativo según profundidad (OPTIMIZACIÓN CLAVE)
        if depth >= 2:
            max_cells = 3  # Solo 3 celdas en niveles altos
        elif depth == 1:
            max_cells = 5  # 5 celdas en nivel medio
        else:
            max_cells = num_empty  # Todas en hojas
        
        if num_empty > max_cells:
            sampled_indices = np.random.choice(num_empty, max_cells, replace=False)
            cells_to_evaluate = [available_cells[i] for i in sampled_indices]
            weight_per_cell = num_empty / len(cells_to_evaluate)
        else:
            cells_to_evaluate = available_cells
            weight_per_cell = 1.0
        
        # Evaluar cada posible ficha nueva
        for cell in cells_to_evaluate:
            # Solo evaluar ficha 2 en niveles profundos (simplificación estocástica)
            if depth >= 2:
                board_copy = board.clone()
                board_copy.insert_tile(cell, 2)
                cell_value = self.expectimax(board_copy, depth, True)
            else:
                # Evaluar ambos valores solo cerca de hojas
                board_copy = board.clone()
                board_copy.insert_tile(cell, 2)
                value_2 = self.expectimax(board_copy, depth, True)
                
                board_copy = board.clone()
                board_copy.insert_tile(cell, 4)
                value_4 = self.expectimax(board_copy, depth, True)
                
                cell_value = 0.9 * value_2 + 0.1 * value_4
            
            expected_value += cell_value * weight_per_cell
        
        # Promedio sobre todas las celdas evaluadas
        return expected_value / len(cells_to_evaluate)
    
    def heuristic_utility(self, board: GameBoard) -> float:
        """
        Evalúa un estado del tablero usando la función heurística asignada.
        """
        if self.heuristic_func is None:
            # Fallback simple si no se asignó heurística
            return len(board.get_available_cells()) * 10.0 + board.get_max_tile()
        return self.heuristic_func(board)


class ExpectimaxAgentOptimized(ExpectimaxAgent):
    """
    Versión optimizada del agente Expectimax con memoización.
    Cachea estados ya evaluados para evitar recalcularlos.
    """
    
    def __init__(self, depth=4, weights=None, weights_config='balanced'):
        super().__init__(depth, weights, weights_config)
        self.cache = {}
    
    def play(self, board: GameBoard) -> int:
        """
        Elige la mejor acción usando Expectimax con caché.
        """
        self.cache.clear()  # Limpiar caché para cada turno
        self.nodes_explored = 0
        return super().play(board)
    
    def expectimax(self, board: GameBoard, depth: int, is_maximizing: bool) -> float:
        """
        Expectimax con memoización.
        """
        # Crear clave única para este estado
        state_key = (board.grid.tobytes(), depth, is_maximizing)
        
        if state_key in self.cache:
            return self.cache[state_key]
        
        value = super().expectimax(board, depth, is_maximizing)
        self.cache[state_key] = value
        
        return value
