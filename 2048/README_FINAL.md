# 🎮 Experimentos 2048 - Obligatorio MEC

## 📋 Resumen del Sistema

Este proyecto implementa y evalúa **3 algoritmos de búsqueda** con **3 heurísticas** de complejidad creciente para el juego 2048.

### Algoritmos Implementados
1. **Minimax (sin Alpha-Beta)** - Búsqueda adversarial clásica
2. **Minimax con Alpha-Beta Pruning** - Optimización con poda
3. **Expectimax** - Manejo de aleatoriedad

### Heurísticas Implementadas
Cada heurística tiene **2 configuraciones de pesos**:

1. **Simple** (2 componentes)
   - Config 1: Balance igual entre celdas vacías y max tile
   - Config 2: Prioriza celdas vacías

2. **Intermediate** (5 componentes)
   - Config 1: Balanceada (monotonía, vacías, esquina, suavidad, posicional)
   - Config 2: Agresiva (más peso en esquina y posición)

3. **Complex** (7+ componentes)
   - Config 1: Equilibrada (todos los componentes + milestones)
   - Config 2: Defensiva (más peso en vacías y monotonía)

### Estructura de Experimentos
**Total: 36 experimentos**
- 2 profundidades (depth=3, depth=4)
- 3 heurísticas × 2 configs = 6 variantes
- 3 algoritmos por variante
- 20 partidas por experimento (modo standard)

## 🚀 Ejecución

### Opción 1: Script Automático (RECOMENDADO)

**Windows:**
```bash
START_EXPERIMENTS.bat
```

**Linux/Mac:**
```bash
chmod +x START_EXPERIMENTS.sh
./START_EXPERIMENTS.sh
```

### Opción 2: Ejecución Directa

```bash
python run_experiments.py
```

Luego selecciona:
- **Opción 1**: Quick Test (5 partidas/experimento) - 1-2 horas
- **Opción 2**: Standard (20 partidas/experimento) - 6-12 horas

## 📊 Resultados

Los resultados se guardan en la carpeta `results/`:

### Archivos Individuales
```
Minimax_NoAB_simple_c1_d3_20241214_143022.csv
Minimax_AB_intermediate_c2_d4_20241214_150145.csv
Expectimax_complex_c1_d3_20241214_153301.csv
...
```

### Archivo Combinado
```
all_experiments_20241214_180000.csv
```

Contiene columnas:
- `game_id`: ID de la partida
- `max_tile`: Tile máxima alcanzada
- `score`: Puntuación final
- `moves`: Número de movimientos
- `time`: Tiempo de ejecución
- `heuristic`: Heurística usada (simple/intermediate/complex)
- `config`: Configuración de pesos (1/2)
- `depth`: Profundidad de búsqueda (3/4)
- `algorithm`: Algoritmo usado (minimax/expectimax)
- `alpha_beta`: Si se usó poda (True/False)

## 📈 Análisis

Después de ejecutar los experimentos, analiza los resultados:

```bash
jupyter notebook Analysis.ipynb
```

## ⚙️ Configuración del Sistema

### Estructura de Archivos
```
2048/
├── run_experiments.py         # Script principal de experimentos
├── Heuristics.py             # 3 heurísticas con 2 configs cada una
├── Minimax_Agent.py          # Agente Minimax
├── Expectimax_Agent.py       # Agente Expectimax
├── Experiments.py            # Framework de experimentación
├── GameBoard.py              # Lógica del juego
├── START_EXPERIMENTS.bat     # Launcher Windows
├── START_EXPERIMENTS.sh      # Launcher Linux/Mac
└── results/                  # Carpeta de resultados
```

### Dependencias
```bash
poetry install
```

O manualmente:
```bash
pip install numpy pandas tqdm matplotlib seaborn
```

## 🔍 Detalles de las Heurísticas

### 1. Simple Heuristic
```python
# Config 1: Balance igual
score = empty_cells * 10.0 + max_tile

# Config 2: Prioriza espacio
score = empty_cells * 20.0 + max_tile * 0.5
```

### 2. Intermediate Heuristic
```python
H = w1*monotonicity + w2*empty_cells + w3*max_corner 
    - w4*smoothness + w5*positional

# Config 1: Balanceada
w1=1.0, w2=2.7, w3=1.0, w4=0.1, w5=0.5

# Config 2: Agresiva
w1=0.5, w2=1.5, w3=2.0, w4=0.05, w5=1.0
```

### 3. Complex Heuristic
7+ componentes:
- Monotonía (orden de valores)
- Suavidad (diferencias adyacentes)
- Celdas vacías (escala exponencial)
- Posición max tile (bonus esquina)
- Potencial de merge
- Valor del tablero
- Estrategia de esquina
- Bonus por milestones (512, 1024, 2048)

## ⏱️ Estimación de Tiempos

**Quick Test (5 partidas/experimento):**
- Depth 3: ~30 seg/experimento → 18 min total
- Depth 4: ~2 min/experimento → 1 hora total
- **Total: 1-2 horas**

**Standard (20 partidas/experimento):**
- Depth 3: ~2 min/experimento → 1 hora total
- Depth 4: ~10 min/experimento → 6 horas total
- **Total: 6-12 horas**

## ⚠️ Notas Importantes

1. **Depth 4 es lento**: Si un experimento se atasca (>5 min/partida), considera interrumpir con Ctrl+C. Los resultados parciales se guardan.

2. **Monitoreo**: El script muestra progreso en tiempo real:
   ```
   [3/36] Minimax (sin AB) - intermediate - config1 - depth=3
   Partida 15/20: Max=512, Score=1204, Movimientos=156
   ⏱️  Progreso: 3/36 completados
   ⏱️  Tiempo transcurrido: 45.2 min
   ⏱️  ETA: 498.3 min
   ```

3. **Suspensión**: Desactiva la suspensión automática del PC antes de ejecutar.

4. **Espacio**: Asegúrate de tener al menos 1 GB libre.

## 📝 Para el Informe

Los experimentos generan datos para analizar:

1. **Comparación de algoritmos**: ¿Minimax vs Expectimax?
2. **Impacto de Alpha-Beta**: ¿Mejora o empeora el rendimiento?
3. **Efectividad de heurísticas**: ¿Simple vs Complex?
4. **Efecto de profundidad**: ¿Depth 3 vs 4?
5. **Configuraciones de pesos**: ¿Balance vs Agresivo?

## 🆘 Troubleshooting

**Error: ModuleNotFoundError**
```bash
poetry install
# O
pip install numpy pandas tqdm
```

**Experimentos muy lentos**
- Usa Quick Test primero
- Considera ejecutar solo depth=3
- Modifica `depths = [3]` en run_experiments.py

**No se crean archivos CSV**
- Verifica permisos en carpeta `results/`
- Asegúrate de que pandas está instalado

## 📧 Contacto

Obligatorio - Inteligencia Artificial - ORT
Estudiantes: 292814, 286845
