# Ejercicio MEC - 2048 con Minimax y Expectimax

Implementación completa de agentes inteligentes para el juego 2048 usando algoritmos de búsqueda adversaria.

## 📁 Estructura del Proyecto

```
2048/
├── Agent.py                    # Clase base abstracta
├── GameBoard.py                # Lógica del juego 2048
├── Random_Agent.py             # Agente aleatorio (baseline)
├── Heuristics.py               # ✨ Funciones heurísticas de evaluación
├── Expectimax_Agent.py         # ✨ Agente Expectimax (con optimización)
├── Minimax_Agent.py            # ✨ Agente Minimax con Alpha-Beta Pruning
├── Experiments.py              # ✨ Sistema de experimentación automática
├── run_experiments.py          # ✨ Script principal para ejecutar experimentos
├── Main.ipynb                  # Notebook para pruebas interactivas
├── Analysis.ipynb              # ✨ Análisis y visualización de resultados
├── results/                    # Carpeta con resultados de experimentos
│   ├── *.csv                   # Resultados en CSV
│   └── plots/                  # Gráficos generados
└── models/                     # Configuraciones óptimas guardadas
```

## 🚀 Inicio Rápido

### 1. Prueba Rápida (5 minutos)

Para verificar que todo funciona correctamente:

```bash
python run_experiments.py quick
```

Esto ejecutará:
- 10 partidas con agente aleatorio
- 5 partidas con Expectimax (profundidades 2 y 3)
- 5 partidas con Minimax (profundidades 2 y 3)

### 2. Ejecución Estándar (2-4 horas)

Para experimentos completos con buenos resultados:

```bash
python run_experiments.py standard
```

Esto ejecutará:
- 50 partidas baseline
- Comparación de profundidades (2, 3, 4) con 20 partidas c/u
- Comparación de heurísticas
- Análisis de Alpha-Beta Pruning
- Comparación Minimax vs Expectimax

### 3. Ejecución Nocturna (8-12 horas)

Para análisis exhaustivo con estadísticas robustas:

```bash
python run_experiments.py extensive
```

⚠️ **Recomendado para dejar durante la noche**

Esto ejecutará:
- 100 partidas baseline
- Profundidades 2, 3, 4, 5 con 50 partidas cada una
- Todas las configuraciones de heurísticas
- Comparaciones exhaustivas

## 📊 Análisis de Resultados

Una vez completados los experimentos:

1. Abre `Analysis.ipynb` en Jupyter/VS Code
2. Ejecuta todas las celdas
3. Se generarán automáticamente:
   - Gráficos comparativos
   - Estadísticas detalladas
   - Resumen ejecutivo para el informe

Los gráficos se guardarán en `results/plots/`

## 🎮 Probar Agentes Individualmente

Puedes probar agentes específicos usando `Main.ipynb`:

```python
from Expectimax_Agent import ExpectimaxAgentOptimized
from GameBoard import GameBoard

# Crear agente
agent = ExpectimaxAgentOptimized(depth=4, weights_config='balanced')

# Jugar una partida
board = GameBoard()
# ... (ver Main.ipynb para código completo)
```

## 🧠 Algoritmos Implementados

### 1. Expectimax
- **Archivo**: `Expectimax_Agent.py`
- **Características**:
  - Nodos MAX: jugador maximiza score
  - Nodos CHANCE: calcula valor esperado (90% ficha=2, 10% ficha=4)
  - Versión optimizada con memoización
  - Más adecuado para juegos estocásticos como 2048

### 2. Minimax con Alpha-Beta Pruning
- **Archivo**: `Minimax_Agent.py`
- **Características**:
  - Nodos MAX: jugador maximiza
  - Nodos MIN: simula peor caso (oponente)
  - Poda Alpha-Beta para optimizar búsqueda
  - Versión optimizada con memoización y ordenamiento de movimientos

## 📈 Funciones Heurísticas

Implementadas en `Heuristics.py`:

1. **Smoothness**: Mide diferencias entre celdas adyacentes
2. **Monotonicity**: Prefiere filas/columnas ordenadas
3. **Empty Cells**: Valora espacios vacíos
4. **Max Tile Position**: Premia ficha máxima en esquina
5. **Merge Potential**: Cuenta fichas adyacentes con mismo valor
6. **Board Value**: Suma ponderada de todas las fichas
7. **Corner Strategy**: Premia fichas grandes en esquinas/bordes

### Configuraciones Predefinidas

- `balanced`: Configuración equilibrada (recomendada)
- `aggressive`: Enfocada en merge y score
- `defensive`: Prioriza espacios vacíos y smoothness
- `corner_focused`: Estrategia de mantener max en esquina

## 📝 Resultados y Métricas

Cada experimento registra:

- **Max Tile**: Ficha más grande alcanzada
- **Final Score**: Puntuación total
- **Moves**: Número de movimientos
- **Time**: Tiempo de ejecución
- **Nodes Explored**: Nodos explorados en el árbol de búsqueda
- **Won**: Si alcanzó 2048 o más

## 🔧 Personalización

### Crear un Agente Personalizado

```python
from Expectimax_Agent import ExpectimaxAgent

# Pesos personalizados
custom_weights = {
    'smoothness': 1.5,
    'monotonicity': 2.5,
    'empty_cells': 3.0,
    'max_position': 0.5,
    'merge_potential': 1.0,
    'board_value': 0.2,
    'corner_strategy': 1.5
}

agent = ExpectimaxAgent(depth=4, weights=custom_weights)
```

### Ejecutar Experimentos Personalizados

```python
from Experiments import ExperimentSuite, GameExperiment
from Expectimax_Agent import ExpectimaxAgent

suite = ExperimentSuite(output_dir="results")

# Experimento personalizado
agent = ExpectimaxAgent(depth=5, weights_config='defensive')
experiment = GameExperiment(agent, "Mi_Experimento", num_games=50)
df = experiment.run_experiment()
```

## 📦 Dependencias

Instaladas con Poetry:
- `numpy`: Operaciones matriciales
- `numba`: Optimización JIT
- `pandas`: Manejo de datos
- `matplotlib`: Visualización
- `seaborn`: Gráficos estadísticos
- `tqdm`: Barras de progreso

## 💡 Tips para el Informe

1. **Gráficos**: Usa los generados en `results/plots/`
2. **Estadísticas**: La tabla en `results/summary_statistics.csv` tiene todo
3. **Resumen Ejecutivo**: La última celda de `Analysis.ipynb` genera un resumen completo
4. **Comparaciones**: Los experimentos automáticamente comparan algoritmos
5. **Conclusiones**: Expectimax generalmente supera a Minimax en 2048

## ⚠️ Consideraciones

- **Tiempo**: Profundidad 5+ puede ser muy lento (minutos por movimiento)
- **Memoria**: Los agentes optimizados usan caché (más RAM pero más rápido)
- **Profundidad recomendada**: 3-4 para balance tiempo/rendimiento
- **Partidas**: Mínimo 20 partidas para estadísticas confiables

## 🎯 Para Dejar Durante la Noche

```bash
# En terminal:
python run_experiments.py extensive

# O con nohup (Linux/Mac):
nohup python run_experiments.py extensive > experiments.log 2>&1 &

# En Windows (PowerShell):
Start-Process python -ArgumentList "run_experiments.py extensive" -RedirectStandardOutput "experiments.log" -NoNewWindow
```

## ✅ Checklist para el Informe

- [ ] Ejecutar `run_experiments.py extensive`
- [ ] Generar todos los gráficos con `Analysis.ipynb`
- [ ] Documentar configuraciones de heurísticas probadas
- [ ] Comparar Minimax vs Expectimax
- [ ] Analizar impacto de Alpha-Beta Pruning
- [ ] Mostrar evolución con profundidad
- [ ] Identificar mejor configuración
- [ ] Calcular estadísticas (media, std, max)
- [ ] Guardar mejores modelos en `models/`

## 📞 Troubleshooting

**Problema**: "ModuleNotFoundError"
- Solución: `poetry install`

**Problema**: Experimentos muy lentos
- Solución: Reducir profundidad o usar modo `quick`

**Problema**: Sin resultados en Analysis.ipynb
- Solución: Primero ejecutar `run_experiments.py`

**Problema**: Memoria insuficiente
- Solución: Reducir número de partidas o cerrar otros programas

---

**¡Buena suerte con el proyecto! 🚀**
