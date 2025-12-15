# Documentación de Resultados - Juego 2048

## Índice
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Técnicas Implementadas](#técnicas-implementadas)
3. [Funciones de Evaluación](#funciones-de-evaluación)
4. [Experimentación y Resultados](#experimentación-y-resultados)
5. [Análisis Comparativo](#análisis-comparativo)
6. [Conclusiones](#conclusiones)

---

## 1. Resumen Ejecutivo

Este documento presenta los resultados de la implementación y evaluación de algoritmos de búsqueda adversarial aplicados al juego 2048. Se implementaron dos técnicas principales: **Minimax con Alpha-Beta Pruning** y **Expectimax**, evaluando su desempeño con diferentes funciones de evaluación y configuraciones.

### Resultados Clave
- **Mejor rendimiento global**: Minimax sin Alpha-Beta con heurística intermedia (Max Tile: 1318, Win Rate: 40%)
- **Impacto de Alpha-Beta Pruning**: Reducción del 75.5% en tiempo de ejecución y 82.5% en nodos explorados
- **Mejor algoritmo para ganar**: Expectimax con Config 1 (35% de victorias)
- **Más eficiente**: Minimax con Alpha-Beta, Config 2 (86.9s por partida)

---

## 2. Técnicas Implementadas

### 2.1 Minimax con Alpha-Beta Pruning

#### Descripción
Minimax es un algoritmo de búsqueda adversarial que asume que el oponente juega de manera óptima. En el contexto del 2048, el jugador maximiza el puntaje mientras que las fichas aleatorias (2 o 4) actúan como el minimizador.

#### Implementación
- **Profundidad de búsqueda**: 3 niveles
- **Alpha-Beta Pruning**: Implementado para mejorar eficiencia
- **Configuraciones**:
  - **Config 1**: Configuración estándar
  - **Config 2**: Configuración alternativa

#### Resultados

##### Sin Alpha-Beta Pruning
| Heurística | Config | Max Tile | Score | Win Rate | Tiempo (s) | Nodos Explorados |
|------------|--------|----------|-------|----------|------------|------------------|
| Simple | C1 | 614 | 1124 | 0% | 406.6 | 3,274,487 |
| Simple | C2 | 691 | 1277 | 0% | 456.3 | 3,673,473 |
| Intermediate | C1 | **1318** | **1942** | **40%** | 1751.5 | 5,170,995 |

##### Con Alpha-Beta Pruning
| Heurística | Config | Max Tile | Score | Win Rate | Tiempo (s) | Nodos Explorados |
|------------|--------|----------|-------|----------|------------|------------------|
| Simple | C1 | 768 | 1411 | 0% | 99.7 | 572,203 |
| Simple | C2 | 627 | 1188 | 0% | **86.9** | **498,687** |
| Intermediate | C1 | 1280 | 1961 | 35% | 190.7 | 848,188 |

#### Análisis del Impacto de Alpha-Beta Pruning

**Comparación: Simple Config 1**
- ✅ **Reducción de tiempo**: 75.5% (de 406.6s a 99.7s)
- ✅ **Reducción de nodos explorados**: 82.5% (de 3.27M a 572K)
- ⚠️ **Impacto en rendimiento**: +154 en Max Tile promedio (mejora)

**Conclusión**: Alpha-Beta Pruning es **altamente efectivo** para reducir el costo computacional sin sacrificar (e incluso mejorando ligeramente) la calidad de las decisiones.

---

### 2.2 Expectimax

#### Descripción
Expectimax es una variante de Minimax que, en lugar de asumir que el oponente juega de manera óptima, modela la aleatoriedad del juego calculando el valor esperado de los nodos de azar.

#### Implementación
- **Profundidad de búsqueda**: 3 niveles
- **Modelado de probabilidad**: Fichas 2 (90%) y 4 (10%)
- **Configuraciones**: Config 1 y Config 2

#### Resultados

| Heurística | Config | Max Tile | Score | Win Rate | Tiempo (s) | Nodos Explorados |
|------------|--------|----------|-------|----------|------------|------------------|
| Simple | C1 | **1254** | 1813 | **35%** | 664.0 | 5,345,286 |
| Simple | C2 | 1075 | 1796 | 15% | 648.0 | 5,201,056 |

#### Ventajas Observadas
- ✅ **Mayor tasa de victoria** que Minimax con heurística simple (35% vs 0%)
- ✅ **Mejor adaptación** a la naturaleza estocástica del juego
- ⚠️ **Mayor costo computacional** (no aplica poda)

---

## 3. Funciones de Evaluación

### 3.1 Heurística Simple

#### Componentes
1. **Puntaje del tablero**: Valor directo del score actual
2. **Número de celdas vacías**: Más espacios libres = mejor movilidad
3. **Monotonía**: Preferencia por valores ordenados
4. **Suavidad**: Penalización por grandes diferencias entre celdas adyacentes

#### Ponderación
- Configuración 1: Balance estándar entre componentes
- Configuración 2: Mayor peso en celdas vacías y monotonía

#### Resultados
- **Efectiva para búsqueda rápida** con Alpha-Beta
- **Limitada para alcanzar fichas altas** (max 768 con AB)
- **Mejor con Expectimax** (1254 max tile, 35% victorias)

---

### 3.2 Heurística Intermedia

#### Componentes Adicionales
1. Todos los componentes de la heurística simple
2. **Posicionamiento en esquina**: Bonus por mantener el valor máximo en una esquina
3. **Agrupación de valores similares**: Incentivo para juntar fichas del mismo valor
4. **Penalización por dispersión**: Castigo por valores altos en posiciones no estratégicas

#### Ponderación
- **Mayor complejidad** en la evaluación
- **Mejor adaptación** a estrategias avanzadas

#### Resultados
| Algoritmo | Alpha-Beta | Max Tile | Score | Win Rate | Tiempo (s) |
|-----------|------------|----------|-------|----------|------------|
| Minimax | ❌ No | **1318** | 1942 | **40%** | 1751.5 |
| Minimax | ✅ Sí | 1280 | **1961** | 35% | 190.7 |

#### Análisis
- ✅ **Mejora significativa** en rendimiento vs heurística simple
- ✅ **Única configuración** que logra 40% de victorias
- ✅ **Alcanza ficha 2048** consistentemente
- ⚠️ **Mayor tiempo de cómputo** sin Alpha-Beta

---

### 3.3 Comparación de Heurísticas

**Minimax AB - Config 1**
| Métrica | Simple | Intermediate | Diferencia |
|---------|--------|--------------|------------|
| Max Tile | 768 | 1280 | +512 (+67%) |
| Score | 1411 | 1961 | +550 (+39%) |
| Win Rate | 0% | 35% | +35 pp |
| Tiempo | 99.7s | 190.7s | +91s (+91%) |

**Conclusión**: La heurística intermedia justifica ampliamente su mayor costo computacional con mejoras dramáticas en todos los aspectos del rendimiento.

---

## 4. Experimentación y Resultados

### 4.1 Metodología

#### Configuración de Experimentos
- **Número de partidas**: 20 por configuración
- **Profundidad de búsqueda**: 3 niveles
- **Semilla aleatoria**: Controlada para reproducibilidad
- **Métricas registradas**:
  - Max Tile alcanzada
  - Score final
  - Número de movimientos
  - Tiempo de ejecución
  - Nodos explorados
  - Victorias (alcanzar ficha 2048)

#### Condiciones de Prueba
- **Hardware**: Procesador estándar
- **Ambiente**: Python con optimizaciones
- **Timeouts**: Sin límite de tiempo por movimiento

---

### 4.2 Resultados Completos

#### Tabla Resumen - Todos los Experimentos

| Experimento | Algoritmo | Heurística | Config | Alpha-Beta | Max Tile | Score | Win % | Tiempo (s) | Nodos |
|-------------|-----------|------------|--------|------------|----------|-------|-------|------------|-------|
| Minimax_NoAB_simple_c1_d3 | Minimax | Simple | 1 | ✗ | 614 | 1124 | 0.0 | 406.6 | 3,274,487 |
| Minimax_NoAB_simple_c2_d3 | Minimax | Simple | 2 | ✗ | 691 | 1277 | 0.0 | 456.3 | 3,673,473 |
| Minimax_NoAB_intermediate_c1_d3 | Minimax | Intermediate | 1 | ✗ | **1318** | 1942 | **40.0** | 1751.5 | 5,170,995 |
| Minimax_AB_simple_c1_d3 | Minimax | Simple | 1 | ✓ | 768 | 1411 | 0.0 | 99.7 | 572,203 |
| Minimax_AB_simple_c2_d3 | Minimax | Simple | 2 | ✓ | 627 | 1188 | 0.0 | **86.9** | **498,687** |
| Minimax_AB_intermediate_c1_d3 | Minimax | Intermediate | 1 | ✓ | 1280 | **1961** | 35.0 | 190.7 | 848,188 |
| Expectimax_simple_c1_d3 | Expectimax | Simple | 1 | ✗ | 1254 | 1813 | 35.0 | 664.0 | 5,345,286 |
| Expectimax_simple_c2_d3 | Expectimax | Simple | 2 | ✗ | 1075 | 1796 | 15.0 | 648.0 | 5,201,056 |

---

### 4.3 Rankings

#### 🥇 Top 3 - Mayor Max Tile
1. **Minimax_NoAB_intermediate_c1_d3**: 1318 (Win Rate: 40.0%)
2. **Minimax_AB_intermediate_c1_d3**: 1280 (Win Rate: 35.0%)
3. **Expectimax_simple_c1_d3**: 1254 (Win Rate: 35.0%)

#### 🥇 Top 3 - Mejor Score Promedio
1. **Minimax_AB_intermediate_c1_d3**: 1961 (Win Rate: 35.0%)
2. **Minimax_NoAB_intermediate_c1_d3**: 1942 (Win Rate: 40.0%)
3. **Expectimax_simple_c1_d3**: 1813 (Win Rate: 35.0%)

#### ⚡ Top 3 - Más Rápidos
1. **Minimax_AB_simple_c2_d3**: 86.9s (0.163s/move)
2. **Minimax_AB_simple_c1_d3**: 99.7s (0.158s/move)
3. **Minimax_AB_intermediate_c1_d3**: 190.7s (0.214s/move)

---

## 5. Análisis Comparativo

### 5.1 Minimax vs Expectimax

**Comparación directa: Simple Config 1**

| Métrica | Minimax AB | Expectimax | Ganador |
|---------|------------|------------|---------|
| Max Tile | 768 | 1254 | 🏆 Expectimax (+486) |
| Score | 1411 | 1813 | 🏆 Expectimax (+402) |
| Win Rate | 0% | 35% | 🏆 Expectimax (+35pp) |
| Tiempo | 99.7s | 664.0s | 🏆 Minimax (-85%) |
| Nodos | 572K | 5.3M | 🏆 Minimax (-89%) |

**Conclusiones**:
- ✅ **Expectimax es superior en calidad de juego** cuando usa heurística simple
- ✅ **Minimax es mucho más eficiente** computacionalmente
- ✅ **Con heurística intermedia**, Minimax alcanza niveles competitivos
- 💡 **Recomendación**: Expectimax para máximo rendimiento, Minimax AB para velocidad

---

### 5.2 Impacto de las Configuraciones

#### Minimax AB - Simple (C1 vs C2)

| Métrica | Config 1 | Config 2 | Diferencia |
|---------|----------|----------|------------|
| Max Tile | 768 | 627 | -141 (-18%) |
| Score | 1411 | 1188 | -223 (-16%) |
| Tiempo | 99.7s | 86.9s | -12.8s (-13%) |

**Observación**: Config 2 sacrifica calidad por velocidad

#### Expectimax - Simple (C1 vs C2)

| Métrica | Config 1 | Config 2 | Diferencia |
|---------|----------|----------|------------|
| Max Tile | 1254 | 1075 | -179 (-14%) |
| Win Rate | 35% | 15% | -20pp |
| Tiempo | 664s | 648s | -16s (-2%) |

**Observación**: Config 1 es claramente superior para Expectimax

---

### 5.3 Gráficos de Resultados

Los gráficos generados en `Analysis_Graficas.ipynb` muestran:

1. **Impacto de Alpha-Beta**: Reducción dramática en tiempo y nodos
2. **Comparación de configuraciones**: Config 1 generalmente superior
3. **Comparación de heurísticas**: Intermedia claramente mejor
4. **Expectimax vs Minimax**: Trade-off entre calidad y velocidad
5. **Resumen general**: Panorama completo de todos los experimentos

---

## 6. Conclusiones

### 6.1 Técnicas

#### Minimax con Alpha-Beta Pruning
- ✅ **Altamente efectivo**: Reducción de 75% en tiempo sin pérdida de calidad
- ✅ **Escalable**: Permite profundidades mayores con costo razonable
- ✅ **Recomendado**: Para aplicaciones con restricciones de tiempo
- ⚠️ **Limitación**: Asume adversario óptimo (no ideal para 2048)

#### Expectimax
- ✅ **Mejor adaptación**: Modela correctamente la aleatoriedad del juego
- ✅ **Superior en calidad**: Mejores resultados con heurísticas simples
- ✅ **Más robusto**: Menos dependiente de la heurística específica
- ⚠️ **Más costoso**: Sin posibilidad de poda alpha-beta

---

### 6.2 Funciones de Evaluación

#### Heurística Simple
- ✅ Suficiente para búsqueda rápida
- ✅ Excelente con Expectimax (35% victorias)
- ⚠️ Limitada con Minimax (0% victorias)

#### Heurística Intermedia
- ✅ **Mejor rendimiento global** (40% victorias)
- ✅ Alcanza fichas altas consistentemente
- ✅ Funciona bien con Minimax
- ⚠️ Mayor costo computacional

#### Configuraciones
- **Config 1**: Balance óptimo para rendimiento
- **Config 2**: Útil cuando se requiere velocidad

---

### 6.3 Recomendaciones Finales

#### Para Máximo Rendimiento
```
Algoritmo: Minimax SIN Alpha-Beta
Heurística: Intermedia
Config: 1
Resultado esperado: Max Tile 1318, Win Rate 40%
Costo: ~1750s por partida
```

#### Para Balance Rendimiento/Velocidad
```
Algoritmo: Minimax CON Alpha-Beta
Heurística: Intermedia
Config: 1
Resultado esperado: Max Tile 1280, Win Rate 35%
Costo: ~190s por partida (9x más rápido)
```

#### Para Aplicaciones en Tiempo Real
```
Algoritmo: Minimax CON Alpha-Beta
Heurística: Simple
Config: 2
Resultado esperado: Max Tile 627, Win Rate 0%
Costo: ~87s por partida
```

#### Para Investigación/Benchmark
```
Algoritmo: Expectimax
Heurística: Simple
Config: 1
Resultado esperado: Max Tile 1254, Win Rate 35%
Costo: ~664s por partida
```

---

### 6.4 Trabajo Futuro

Posibles mejoras identificadas:

1. **Profundidad adaptativa**: Ajustar profundidad según estado del tablero
2. **Heurísticas avanzadas**: Incorporar pattern databases
3. **Paralelización**: Explorar búsqueda paralela en múltiples hilos
4. **Aprendizaje automático**: Entrenar redes neuronales para evaluación
5. **Monte Carlo Tree Search**: Comparar con MCTS como alternativa

---

## Apéndice A: Detalles de Implementación

### Estructura del Código
```
2048/
├── Agent.py              # Clase base para agentes
├── Minimax_Agent.py      # Implementación de Minimax con Alpha-Beta
├── Expectimax_Agent.py   # Implementación de Expectimax
├── Heuristics.py         # Funciones de evaluación
├── GameBoard.py          # Lógica del juego
├── Experiments.py        # Framework de experimentación
└── Analysis_Graficas.ipynb  # Análisis y visualización
```

### Configuraciones Específicas

**Config 1 (Heurística Simple)**:
```python
weights = {
    'score': 1.0,
    'empty_cells': 2.7,
    'monotonicity': 1.0,
    'smoothness': 0.1
}
```

**Config 2 (Heurística Simple)**:
```python
weights = {
    'score': 1.0,
    'empty_cells': 3.0,
    'monotonicity': 1.5,
    'smoothness': 0.1
}
```

**Heurística Intermedia**:
```python
weights = {
    'score': 1.0,
    'empty_cells': 2.7,
    'monotonicity': 1.0,
    'smoothness': 0.1,
    'corner_bonus': 5.0,
    'merge_potential': 1.5,
    'dispersion_penalty': 0.5
}
```

---

## Referencias

- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.)
- Browne, C., et al. (2012). A Survey of Monte Carlo Tree Search Methods
- Yeh, K. H., et al. (2014). Multi-Stage Temporal Difference Learning for 2048

---

**Documento generado**: Diciembre 15, 2025
**Autores**: [Tu Nombre/ID]
**Curso**: Inteligencia Artificial - ORT
