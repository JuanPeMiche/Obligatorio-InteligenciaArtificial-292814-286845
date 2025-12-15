"""
Agente que utiliza el algoritmo Minimax con Alpha-Beta Pruning para jugar 2048.
Aunque Minimax es típico para juegos adversariales, se puede adaptar para 2048.
"""
from Agent import Agent
from GameBoard import GameBoard
import numpy as np


class MinimaxAgent(Agent):
    """
    Agente que usa búsqueda Minimax con Alpha-Beta Pruning.
    - Nodos MAX: el jugador busca maximizar el valor
    - Nodos MIN: simula el "oponente" (aparición de fichas en peor posición)
    """
    
    def __init__(self, depth=4, use_alpha_beta=True, weights=None, weights_config=None):
        """
        Args:
            depth: Profundidad máxima de búsqueda
            use_alpha_beta: Si True, usa poda Alpha-Beta; si False, Minimax básico
            weights: DEPRECATED - No se usa
            weights_config: DEPRECATED - No se usa
        """
        self.depth = depth
        self.use_alpha_beta = use_alpha_beta
        self.heuristic_func = None  # Se asigna externamente
        
        self.nodes_explored = 0
        self.pruned_nodes = 0
        self.use_adaptive_depth = True  # Activar profundidad adaptativa
    
    def get_adaptive_depth(self, board: GameBoard) -> int:
        """Ajusta profundidad según número de celdas vacías para evitar explosión combinatoria."""
        if not self.use_adaptive_depth:
            return self.depth
        
        empty_cells = len(board.get_available_cells())
        
        if empty_cells <= 3:
            return self.depth + 1  # Más profundo con pocas opciones
        elif empty_cells <= 6:
            return self.depth
        elif empty_cells <= 10:
            return max(2, self.depth - 1)
        else:
            return max(2, self.depth - 2)  # Menos profundo al inicio
    
    def play(self, board: GameBoard) -> int:
        """
        Elige la mejor acción usando Minimax con profundidad adaptativa.
        
        Returns:
            Acción a tomar (0=UP, 1=DOWN, 2=LEFT, 3=RIGHT)
        """
        self.nodes_explored = 0
        self.pruned_nodes = 0
        
        # Usar profundidad adaptativa
        depth = self.get_adaptive_depth(board)
        
        best_action = None
        best_value = -np.inf
        alpha = -np.inf
        beta = np.inf
        
        available_moves = board.get_available_moves()
        
        if not available_moves:
            return 0
        
        # Ordenar movimientos por heurística rápida (mejor poda)
        move_values = []
        for move in available_moves:
            board_copy = board.clone()
            board_copy.move(move)
            quick_val = len(board_copy.get_available_cells()) * 10 + board_copy.get_max_tile()
            move_values.append((move, quick_val))
        
        move_values.sort(key=lambda x: x[1], reverse=True)
        
        for move, _ in move_values:
            board_copy = board.clone()
            board_copy.move(move)
            
            if self.use_alpha_beta:
                value = self.minimax(board_copy, depth - 1, False, alpha, beta)
                alpha = max(alpha, value)
            else:
                value = self.minimax(board_copy, depth - 1, False, -np.inf, np.inf)
            
            if value > best_value:
                best_value = value
                best_action = move
        
        return best_action if best_action is not None else available_moves[0]
    
    def minimax(self, board: GameBoard, depth: int, is_maximizing: bool, 
                alpha: float, beta: float) -> float:
        """
        Algoritmo Minimax con poda Alpha-Beta opcional.
        
        Args:
            board: Estado actual del tablero
            depth: Profundidad restante
            is_maximizing: True para nodo MAX, False para nodo MIN
            alpha: Mejor valor para el maximizador
            beta: Mejor valor para el minimizador
        
        Returns:
            Valor del estado
        """
        self.nodes_explored += 1
        
        # Caso base
        if depth == 0 or len(board.get_available_moves()) == 0:
            return self.heuristic_utility(board)
        
        if is_maximizing:
            return self.max_node(board, depth, alpha, beta)
        else:
            return self.min_node(board, depth, alpha, beta)
    
    def max_node(self, board: GameBoard, depth: int, alpha: float, beta: float) -> float:
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
            
            value = self.minimax(board_copy, depth - 1, False, alpha, beta)
            max_value = max(max_value, value)
            
            if self.use_alpha_beta:
                alpha = max(alpha, value)
                if beta <= alpha:
                    self.pruned_nodes += 1
                    break  # Poda Beta
        
        return max_value
    
    def min_node(self, board: GameBoard, depth: int, alpha: float, beta: float) -> float:
        """
        Nodo minimizador: simula el peor caso (ficha en peor posición).
        Optimizado con muestreo adaptativo según profundidad.
        """
        min_value = np.inf
        available_cells = board.get_available_cells()
        
        if not available_cells:
            return self.heuristic_utility(board)
        
        # Muestreo adaptativo según profundidad (OPTIMIZACIÓN CLAVE)
        if depth >= 2:
            max_cells = 3  # Solo 3 celdas en niveles altos
        elif depth == 1:
            max_cells = 5  # 5 celdas en nivel medio
        else:
            max_cells = len(available_cells)  # Todas en hojas
        
        if len(available_cells) > max_cells:
            cells_to_evaluate = self._select_critical_cells(board, available_cells, max_cells)
        else:
            cells_to_evaluate = available_cells
        
        for cell in cells_to_evaluate:
            # Solo evaluar ficha 2 en niveles profundos (simplificación estocástica)
            if depth >= 2:
                board_copy = board.clone()
                board_copy.insert_tile(cell, 2)
                value = self.minimax(board_copy, depth, True, alpha, beta)
            else:
                # Evaluar ambos valores solo cerca de hojas
                board_copy = board.clone()
                board_copy.insert_tile(cell, 2)
                value_2 = self.minimax(board_copy, depth, True, alpha, beta)
                
                board_copy = board.clone()
                board_copy.insert_tile(cell, 4)
                value_4 = self.minimax(board_copy, depth, True, alpha, beta)
                
                value = min(value_2, value_4)
            
            min_value = min(min_value, value)
            
            if self.use_alpha_beta:
                beta = min(beta, value)
                if beta <= alpha:
                    self.pruned_nodes += 1
                    break  # Poda Alpha
        
        return min_value
    
    def _select_critical_cells(self, board: GameBoard, available_cells: list, count: int) -> list:
        """
        Selecciona las celdas más críticas para evaluar.
        Prioriza celdas cerca de fichas grandes o en posiciones estratégicas.
        """
        grid = board.grid
        cell_scores = []
        
        for cell in available_cells:
            i, j = cell
            score = 0
            
            # Penalizar celdas cerca de fichas grandes (peor para el jugador)
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 4 and 0 <= nj < 4:
                        score += grid[ni][nj]
            
            # Priorizar esquinas y bordes (generalmente peor para el jugador)
            if i in [0, 3] and j in [0, 3]:
                score += 1000  # Esquina
            elif i in [0, 3] or j in [0, 3]:
                score += 500   # Borde
            
            cell_scores.append((cell, score))
        
        # Ordenar por score descendente y tomar las 'count' más críticas
        cell_scores.sort(key=lambda x: x[1], reverse=True)
        return [cell for cell, _ in cell_scores[:count]]
    
    def heuristic_utility(self, board: GameBoard) -> float:
        """
        Evalúa un estado del tablero usando la función heurística asignada.
        """
        if self.heuristic_func is None:
            # Fallback simple si no se asignó heurística
            return len(board.get_available_cells()) * 10.0 + board.get_max_tile()
        return self.heuristic_func(board)


class MinimaxAgentOptimized(MinimaxAgent):
    """
    Versión optimizada con memoización y ordenamiento de movimientos.
    """
    
    def __init__(self, depth=4, use_alpha_beta=True, weights=None, weights_config='balanced'):
        super().__init__(depth, use_alpha_beta, weights, weights_config)
        self.cache = {}
    
    def play(self, board: GameBoard) -> int:
        """
        Versión optimizada con caché.
        """
        self.cache.clear()
        self.nodes_explored = 0
        self.pruned_nodes = 0
        return super().play(board)
    
    def minimax(self, board: GameBoard, depth: int, is_maximizing: bool, 
                alpha: float, beta: float) -> float:
        """
        Minimax con memoización.
        """
        # Crear clave para el caché
        state_key = (board.grid.tobytes(), depth, is_maximizing)
        
        if state_key in self.cache:
            return self.cache[state_key]
        
        value = super().minimax(board, depth, is_maximizing, alpha, beta)
        self.cache[state_key] = value
        
        return value
    
    def max_node(self, board: GameBoard, depth: int, alpha: float, beta: float) -> float:
        """
        Nodo MAX optimizado con ordenamiento de movimientos.
        Evalúa primero los movimientos más prometedores.
        """
        available_moves = board.get_available_moves()
        
        if not available_moves:
            return self.heuristic_utility(board)
        
        # Ordenar movimientos por valor heurístico (para mejor poda)
        move_values = []
        for move in available_moves:
            board_copy = board.clone()
            board_copy.move(move)
            value = self.heuristic_utility(board_copy)
            move_values.append((move, value))
        
        # Ordenar de mejor a peor
        move_values.sort(key=lambda x: x[1], reverse=True)
        ordered_moves = [move for move, _ in move_values]
        
        max_value = -np.inf
        for move in ordered_moves:
            board_copy = board.clone()
            board_copy.move(move)
            
            value = self.minimax(board_copy, depth - 1, False, alpha, beta)
            max_value = max(max_value, value)
            
            if self.use_alpha_beta:
                alpha = max(alpha, value)
                if beta <= alpha:
                    self.pruned_nodes += 1
                    break
        
        return max_value
