"""
Módulo de funciones heurísticas para evaluar estados del tablero 2048.

Contiene 3 heurísticas de complejidad creciente, cada una con 2 configuraciones:
1. simple_heuristic: Muy sencilla (celdas vacías + max tile)
2. intermediate_heuristic: Intermedia (5 componentes balanceados)
3. complex_heuristic: Compleja (7+ componentes optimizados)
"""
import numpy as np
from GameBoard import GameBoard


# ============================================================
# HEURÍSTICA 1: SIMPLE
# ============================================================

def simple_heuristic(board: GameBoard, config: int = 1) -> float:
    """
    Heurística MUY SIMPLE con solo 2 componentes básicos.
    
    Componentes:
    - Celdas vacías (más espacio = mejor)
    - Valor máximo del tablero (tile más grande)
    
    Args:
        board: Estado del tablero
        config: 1 o 2 (configuración de pesos)
    """
    empty = len(board.get_available_cells())
    max_tile = board.get_max_tile()
    
    if config == 1:
        # Configuración 1: Balance igual
        return empty * 10.0 + max_tile
    else:
        # Configuración 2: Prioriza celdas vacías
        return empty * 20.0 + max_tile * 0.5


# ============================================================
# HEURÍSTICA 2: INTERMEDIA
# ============================================================

def intermediate_heuristic(board: GameBoard, config: int = 1) -> float:
    """
    Heurística INTERMEDIA con 5 componentes clave.
    
    H = w1*monotonicity + w2*empty_cells + w3*max_corner - w4*smoothness + w5*positional
    
    Args:
        board: Estado del tablero
        config: 1 o 2 (configuración de pesos)
    """
    grid = board.grid
    
    # ===== COMPONENTE 1: Monotonía =====
    monotonicity_score = _monotonicity(board)
    
    # ===== COMPONENTE 2: Celdas vacías =====
    empty_score = len(board.get_available_cells())
    
    # ===== COMPONENTE 3: Max tile en esquina =====
    max_tile = board.get_max_tile()
    max_positions = np.where(grid == max_tile)
    
    if len(max_positions[0]) > 0:
        max_row, max_col = max_positions[0][0], max_positions[1][0]
        corners = {(0, 0): 1.0, (0, 3): 0.9, (3, 0): 0.9, (3, 3): 0.8}
        
        if (max_row, max_col) in corners:
            max_corner_score = max_tile * corners[(max_row, max_col)]
        else:
            min_dist = min(abs(max_row - c[0]) + abs(max_col - c[1]) for c in corners.keys())
            max_corner_score = -max_tile * min_dist * 0.5
    else:
        max_corner_score = 0.0
    
    # ===== COMPONENTE 4: Suavidad =====
    smoothness_score = _smoothness(board)
    
    # ===== COMPONENTE 5: Peso posicional =====
    position_weights = np.array([
        [4, 3, 2, 1],
        [3, 2, 1, 0],
        [2, 1, 0, -1],
        [1, 0, -1, -2]
    ])
    
    positional_score = 0.0
    for i in range(4):
        for j in range(4):
            if grid[i][j] > 0:
                tile_value = np.log2(grid[i][j])
                positional_score += tile_value * position_weights[i][j]
    
    # ===== COMBINACIÓN CON PESOS =====
    if config == 1:
        # Configuración 1: Balanceada
        W1, W2, W3, W4, W5 = 1.0, 2.7, 1.0, 0.1, 0.5
    else:
        # Configuración 2: Agresiva (prioriza esquina y posición)
        W1, W2, W3, W4, W5 = 0.5, 1.5, 2.0, 0.05, 1.0
    
    return (W1 * monotonicity_score + 
            W2 * empty_score + 
            W3 * max_corner_score - 
            W4 * smoothness_score + 
            W5 * positional_score)


# ============================================================
# HEURÍSTICA 3: COMPLEJA
# ============================================================

def complex_heuristic(board: GameBoard, config: int = 1) -> float:
    """
    Heurística COMPLEJA con 7+ componentes optimizados.
    
    Incluye: monotonía, suavidad, celdas vacías, posición max,
    potencial de merge, valor del tablero, estrategia de esquina,
    y bonus por milestones.
    
    Args:
        board: Estado del tablero
        config: 1 o 2 (configuración de pesos)
    """
    grid = board.grid
    max_tile = board.get_max_tile()
    
    # ===== COMPONENTE 1: Monotonía =====
    monotonicity_score = _monotonicity(board)
    
    # ===== COMPONENTE 2: Suavidad =====
    smoothness_score = _smoothness(board)
    
    # ===== COMPONENTE 3: Celdas vacías (escala exponencial) =====
    empty = len(board.get_available_cells())
    if empty >= 8:
        empty_score = empty * 100.0
    elif empty >= 6:
        empty_score = empty * 50.0
    elif empty >= 3:
        empty_score = empty * 30.0
    else:
        empty_score = empty * 15.0
    
    # ===== COMPONENTE 4: Max tile en esquina =====
    max_corner_score = _max_tile_corner(board)
    
    # ===== COMPONENTE 5: Potencial de merge =====
    merge_score = 0.0
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                # Merges normales
                if j < 3 and grid[i][j] == grid[i][j+1]:
                    merge_score += grid[i][j]
                if i < 3 and grid[i][j] == grid[i+1][j]:
                    merge_score += grid[i][j]
                
                # Bonus para merges grandes
                if grid[i][j] >= 256:
                    if j < 3 and grid[i][j] == grid[i][j+1]:
                        merge_score += grid[i][j] * 5.0
                    if i < 3 and grid[i][j] == grid[i+1][j]:
                        merge_score += grid[i][j] * 5.0
    
    # ===== COMPONENTE 6: Valor del tablero =====
    value_score = sum(grid[i][j] ** 2 for i in range(4) for j in range(4) if grid[i][j] != 0)
    
    # ===== COMPONENTE 7: Estrategia de esquina =====
    weights = np.array([
        [16, 8, 8, 16],
        [8,  4, 4, 8],
        [8,  4, 4, 8],
        [16, 8, 8, 16]
    ])
    corner_score = sum(grid[i][j] * weights[i][j] for i in range(4) for j in range(4) if grid[i][j] != 0)
    
    # ===== COMPONENTE 8: Bonus por milestones =====
    if max_tile >= 2048:
        milestone_bonus = 100000.0
    elif max_tile >= 1024:
        milestone_bonus = 50000.0
    elif max_tile >= 512:
        milestone_bonus = 10000.0
    elif max_tile >= 256:
        milestone_bonus = 2000.0
    else:
        milestone_bonus = 0.0
    
    # ===== COMBINACIÓN CON PESOS =====
    if config == 1:
        # Configuración 1: Equilibrada
        total = (monotonicity_score * 5.0 +
                smoothness_score * 2.0 +
                empty_score * 8.0 +
                max_corner_score * 0.1 +
                merge_score * 6.0 +
                value_score * 0.0001 +
                corner_score * 0.01 +
                milestone_bonus)
    else:
        # Configuración 2: Defensiva (más peso en vacías y monotonía)
        total = (monotonicity_score * 8.0 +
                smoothness_score * 3.0 +
                empty_score * 12.0 +
                max_corner_score * 0.15 +
                merge_score * 4.0 +
                value_score * 0.00005 +
                corner_score * 0.005 +
                milestone_bonus)
    
    return total


# ============================================================
# FUNCIONES AUXILIARES INTERNAS
# ============================================================

def _smoothness(board: GameBoard) -> float:
    """Calcula la suavidad del tablero."""
    grid = board.grid
    smoothness_value = 0.0
    
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                value = np.log2(grid[i][j])
                
                if j < 3 and grid[i][j+1] != 0:
                    target_value = np.log2(grid[i][j+1])
                    smoothness_value -= abs(value - target_value)
                
                if i < 3 and grid[i+1][j] != 0:
                    target_value = np.log2(grid[i+1][j])
                    smoothness_value -= abs(value - target_value)
    
    return smoothness_value


def _monotonicity(board: GameBoard) -> float:
    """Calcula la monotonicidad del tablero."""
    grid = board.grid
    totals = [0, 0, 0, 0]  # up, down, left, right
    
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
                totals[2] += next_value - current_value
            elif next_value > current_value:
                totals[3] += current_value - next_value
            
            current = next_pos
            next_pos += 1
    
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
                totals[0] += next_value - current_value
            elif next_value > current_value:
                totals[1] += current_value - next_value
            
            current = next_pos
            next_pos += 1
    
    return max(totals[0], totals[1]) + max(totals[2], totals[3])


def _max_tile_corner(board: GameBoard) -> float:
    """Evalúa si la ficha máxima está en esquina."""
    grid = board.grid
    max_value = board.get_max_tile()
    corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
    
    for corner in corners:
        if grid[corner[0]][corner[1]] == max_value:
            return 10000.0
    
    return -5000.0


# ============================================================
# DICCIONARIO Y HELPER
# ============================================================

HEURISTICS = {
    'simple': simple_heuristic,
    'intermediate': intermediate_heuristic,
    'complex': complex_heuristic
}


def get_heuristic(name: str):
    """
    Obtiene una función heurística por nombre.
    
    Args:
        name: 'simple', 'intermediate', o 'complex'
    
    Returns:
        Función heurística
    """
    if name not in HEURISTICS:
        print(f"⚠️  Heurística '{name}' no encontrada. Usando 'intermediate'.")
        return HEURISTICS['intermediate']
    
    return HEURISTICS[name]

