"""
Módulo de funciones heurísticas para evaluar estados del tablero 2048
"""
import numpy as np
from GameBoard import GameBoard


def smoothness(board: GameBoard) -> float:
    """
    Calcula la 'suavidad' del tablero.
    Un tablero más suave tiene menores diferencias entre celdas adyacentes.
    Valores más altos son mejores (menos negativos).
    """
    grid = board.grid
    smoothness_value = 0.0
    
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                value = np.log2(grid[i][j])
                
                # Comparar con celda derecha
                if j < 3 and grid[i][j+1] != 0:
                    target_value = np.log2(grid[i][j+1])
                    smoothness_value -= abs(value - target_value)
                
                # Comparar con celda abajo
                if i < 3 and grid[i+1][j] != 0:
                    target_value = np.log2(grid[i+1][j])
                    smoothness_value -= abs(value - target_value)
    
    return smoothness_value


def monotonicity(board: GameBoard) -> float:
    """
    Calcula la monotonicidad del tablero.
    Prefiere filas y columnas que sean monótonas (ascendentes o descendentes).
    Valores más altos son mejores.
    """
    grid = board.grid
    totals = [0, 0, 0, 0]  # up, down, left, right
    
    # Monotonicity para cada fila
    for i in range(4):
        current = 0
        next_pos = current + 1
        while next_pos < 4:
            while next_pos < 4 and grid[i][next_pos] == 0:
                next_pos += 1
            if next_pos >= 4:
                next_pos -= 1
            
            current_value = np.log2(grid[i][current]) if grid[i][current] != 0 else 0
            next_value = np.log2(grid[i][next_pos]) if grid[i][next_pos] != 0 else 0
            
            if current_value > next_value:
                totals[2] += next_value - current_value  # left
            elif next_value > current_value:
                totals[3] += current_value - next_value  # right
            
            current = next_pos
            next_pos += 1
    
    # Monotonicity para cada columna
    for j in range(4):
        current = 0
        next_pos = current + 1
        while next_pos < 4:
            while next_pos < 4 and grid[next_pos][j] == 0:
                next_pos += 1
            if next_pos >= 4:
                next_pos -= 1
            
            current_value = np.log2(grid[current][j]) if grid[current][j] != 0 else 0
            next_value = np.log2(grid[next_pos][j]) if grid[next_pos][j] != 0 else 0
            
            if current_value > next_value:
                totals[0] += next_value - current_value  # up
            elif next_value > current_value:
                totals[1] += current_value - next_value  # down
            
            current = next_pos
            next_pos += 1
    
    return max(totals[0], totals[1]) + max(totals[2], totals[3])


def empty_cells(board: GameBoard) -> float:
    """
    Cuenta el número de celdas vacías.
    Más celdas vacías = mejor (más espacio para maniobrar).
    """
    return len(board.get_available_cells())


def max_tile_position(board: GameBoard) -> float:
    """
    Evalúa si la ficha máxima está en una esquina (estrategia óptima).
    Retorna un valor positivo si está en esquina, negativo si no.
    """
    grid = board.grid
    max_value = board.get_max_tile()
    
    # Posiciones de las esquinas
    corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
    
    for corner in corners:
        if grid[corner[0]][corner[1]] == max_value:
            return 10000.0  # Bonus grande por tener max en esquina
    
    # Penalización si no está en esquina
    return -5000.0


def merge_potential(board: GameBoard) -> float:
    """
    Evalúa cuántas fichas adyacentes tienen el mismo valor (potencial de merge).
    Más merges posibles = mejor.
    """
    grid = board.grid
    potential = 0
    
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                # Verificar derecha
                if j < 3 and grid[i][j] == grid[i][j+1]:
                    potential += grid[i][j]
                
                # Verificar abajo
                if i < 3 and grid[i][j] == grid[i+1][j]:
                    potential += grid[i][j]
    
    return potential


def board_value(board: GameBoard) -> float:
    """
    Calcula el valor total del tablero.
    Suma ponderada de todas las fichas (fichas más grandes valen más).
    """
    grid = board.grid
    value = 0.0
    
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                # Usar potencia para dar más peso a fichas grandes
                value += grid[i][j] ** 2
    
    return value


def corner_strategy(board: GameBoard) -> float:
    """
    Premia mantener las fichas más grandes en las esquinas y bordes.
    """
    grid = board.grid
    score = 0.0
    
    # Pesos para posiciones (esquinas y bordes tienen más valor)
    weights = np.array([
        [16, 8, 8, 16],
        [8,  4, 4, 8],
        [8,  4, 4, 8],
        [16, 8, 8, 16]
    ])
    
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                score += grid[i][j] * weights[i][j]
    
    return score


def combined_heuristic(board: GameBoard, weights: dict = None) -> float:
    """
    Combina todas las heurísticas con pesos configurables.
    
    Args:
        board: Estado del tablero
        weights: Diccionario con pesos para cada heurística
    
    Returns:
        Score combinado del tablero
    """
    if weights is None:
        # Pesos por defecto (optimizados empíricamente)
        weights = {
            'smoothness': 1.0,
            'monotonicity': 2.0,
            'empty_cells': 2.7,
            'max_position': 0.1,
            'merge_potential': 0.5,
            'board_value': 0.1,
            'corner_strategy': 1.0
        }
    
    score = 0.0
    
    if 'smoothness' in weights:
        score += weights['smoothness'] * smoothness(board)
    
    if 'monotonicity' in weights:
        score += weights['monotonicity'] * monotonicity(board)
    
    if 'empty_cells' in weights:
        score += weights['empty_cells'] * empty_cells(board)
    
    if 'max_position' in weights:
        score += weights['max_position'] * max_tile_position(board)
    
    if 'merge_potential' in weights:
        score += weights['merge_potential'] * merge_potential(board)
    
    if 'board_value' in weights:
        score += weights['board_value'] * board_value(board)
    
    if 'corner_strategy' in weights:
        score += weights['corner_strategy'] * corner_strategy(board)
    
    return score


# Configuraciones de pesos predefinidas para experimentación
WEIGHT_CONFIGS = {
    'balanced': {
        'smoothness': 1.0,
        'monotonicity': 2.0,
        'empty_cells': 2.7,
        'max_position': 0.1,
        'merge_potential': 0.5,
        'board_value': 0.1,
        'corner_strategy': 1.0
    },
    'aggressive': {
        'smoothness': 0.5,
        'monotonicity': 1.0,
        'empty_cells': 1.0,
        'max_position': 0.0,
        'merge_potential': 2.0,
        'board_value': 1.5,
        'corner_strategy': 0.5
    },
    'defensive': {
        'smoothness': 2.0,
        'monotonicity': 3.0,
        'empty_cells': 5.0,
        'max_position': 0.5,
        'merge_potential': 0.3,
        'board_value': 0.05,
        'corner_strategy': 2.0
    },
    'corner_focused': {
        'smoothness': 0.5,
        'monotonicity': 2.5,
        'empty_cells': 2.0,
        'max_position': 1.0,
        'merge_potential': 0.3,
        'board_value': 0.1,
        'corner_strategy': 3.0
    }
}
