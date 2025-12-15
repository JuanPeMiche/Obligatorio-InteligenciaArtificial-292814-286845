# Informe Técnico: Implementación y Evaluación de Algoritmos de Búsqueda Adversarial para el Juego 2048

**Inteligencia Artificial - ORT Uruguay**  
**Fecha:** Diciembre 2025  
**Autores:** Juan Pedro Miche (286845), [Estudiante 2] (292814)

---

## Resumen Ejecutivo

El presente informe documenta la implementación, análisis y evaluación de algoritmos de búsqueda adversarial aplicados al juego 2048. Se desarrollaron dos técnicas principales: **Minimax con poda Alpha-Beta** y **Expectimax**, evaluando su desempeño mediante diferentes funciones heurísticas y configuraciones de parámetros. Los experimentos se realizaron sobre un conjunto de 8 configuraciones distintas, ejecutando 20 partidas por configuración para garantizar significancia estadística.

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Marco Teórico](#2-marco-teórico)
3. [Implementación](#3-implementación)
4. [Funciones de Evaluación](#4-funciones-de-evaluación)
5. [Diseño Experimental](#5-diseño-experimental)
6. [Resultados](#6-resultados)
7. [Análisis Comparativo](#7-análisis-comparativo)
8. [Conclusiones](#8-conclusiones)
9. [Referencias](#9-referencias)
10. [Apéndices](#10-apéndices)

---

## 1. Introducción

### 1.1 Motivación

El juego 2048 representa un problema de decisión secuencial con componentes estocásticos, donde un agente debe maximizar su puntuación en un entorno parcialmente aleatorio. Este tipo de problemas es fundamental en inteligencia artificial, con aplicaciones en planificación, robótica y juegos.

El juego 2048 representa un problema de decisión secuencial con componentes estocásticos, donde un agente debe maximizar su puntuación en un entorno parcialmente aleatorio. Este tipo de problemas es fundamental en inteligencia artificial, con aplicaciones en planificación, robótica y juegos.

### 1.2 Objetivos

Los objetivos específicos del presente trabajo son:

1. **Implementar y comparar** dos técnicas de búsqueda adversarial: Minimax con poda Alpha-Beta y Expectimax
2. **Diseñar y evaluar** funciones heurísticas de evaluación de estados
3. **Analizar el impacto** de la poda Alpha-Beta en términos de eficiencia computacional
4. **Determinar** la configuración óptima para diferentes escenarios de aplicación

### 1.3 Estructura del Documento

El informe se organiza de la siguiente manera: la Sección 2 presenta el marco teórico; la Sección 3 describe los detalles de implementación; la Sección 4 explica las funciones heurísticas diseñadas; la Sección 5 detalla el diseño experimental; la Sección 6 presenta los resultados obtenidos; la Sección 7 analiza comparativamente los resultados; y la Sección 8 presenta las conclusiones y trabajo futuro.

---

## 2. Marco Teórico

### 2.1 El Juego 2048

El juego 2048 se desarrolla en un tablero de 4×4 celdas. En cada turno:
- El jugador selecciona una dirección (arriba, abajo, izquierda, derecha)
- Todas las fichas se desplazan en esa dirección
- Las fichas con el mismo valor que colisionan se fusionan, duplicando su valor
- Una nueva ficha (2 con probabilidad 0.9, o 4 con probabilidad 0.1) aparece en una celda vacía aleatoria

El objetivo es alcanzar la ficha 2048, aunque el juego puede continuar indefinidamente.

### 2.2 Algoritmo Minimax

Minimax (Russell & Norvig, 2020) es un algoritmo de búsqueda adversarial que asume dos jugadores con objetivos opuestos: MAX busca maximizar la utilidad mientras MIN busca minimizarla. El algoritmo explora el árbol de juego recursivamente alternando entre niveles MAX y MIN hasta alcanzar una profundidad predefinida o un estado terminal.

**Formalización:**

```
MINIMAX(s, depth) = 
  si depth = 0 o s es terminal entonces EVAL(s)
  si s es MAX entonces max_{a ∈ Acciones(s)} MINIMAX(Resultado(s,a), depth-1)
  si s es MIN entonces min_{a ∈ Acciones(s)} MINIMAX(Resultado(s,a), depth-1)
```

### 2.3 Poda Alpha-Beta

La poda Alpha-Beta (Knuth & Moore, 1975) es una optimización del algoritmo Minimax que elimina ramas del árbol de búsqueda que no pueden influir en la decisión final. Mantiene dos valores:
- **α**: mejor valor encontrado para MAX en el camino actual
- **β**: mejor valor encontrado para MIN en el camino actual

La poda ocurre cuando β ≤ α, lo que indica que el oponente nunca permitirá alcanzar ese estado.

### 2.4 Algoritmo Expectimax

Expectimax (Michie, 1966) adapta Minimax para entornos estocásticos, reemplazando los nodos MIN por nodos CHANCE que calculan el valor esperado según la distribución de probabilidad de los eventos aleatorios.

**Formalización:**

```
EXPECTIMAX(s, depth) = 
  si depth = 0 o s es terminal entonces EVAL(s)
  si s es MAX entonces max_{a ∈ Acciones(s)} EXPECTIMAX(Resultado(s,a), depth-1)
  si s es CHANCE entonces Σ_{s' ∈ Sucesores(s)} P(s') · EXPECTIMAX(s', depth-1)
```

---

## 3. Implementación

### 3.1 Arquitectura del Sistema

El sistema implementado consta de los siguientes componentes:

```
2048/
├── Agent.py              # Clase base abstracta para agentes
├── Minimax_Agent.py      # Implementación de Minimax con Alpha-Beta
├── Expectimax_Agent.py   # Implementación de Expectimax
├── Heuristics.py         # Funciones de evaluación heurística
├── GameBoard.py          # Motor del juego y gestión de estados
├── Experiments.py        # Framework de experimentación
└── Analysis_Graficas.ipynb  # Análisis estadístico y visualización
```

### 3.2 Minimax con Poda Alpha-Beta

La implementación de Minimax incluye poda Alpha-Beta opcional. Los parámetros clave son:
- **Profundidad máxima**: 3 niveles
- **Función heurística**: Configurable (simple o intermedia)
- **Poda**: Activable/desactivable para análisis comparativo

Pseudocódigo simplificado:

```python
def minimax_ab(state, depth, alpha, beta, is_max, use_ab):
    if depth == 0 or state.is_terminal():
        return heuristic(state)
    
    if is_max:
        value = -∞
        for action in state.get_actions():
            child = state.apply_action(action)
            value = max(value, minimax_ab(child, depth-1, alpha, beta, False, use_ab))
            if use_ab:
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Poda Beta
        return value
    else:
        value = +∞
        for child in state.get_random_tiles():
            value = min(value, minimax_ab(child, depth-1, alpha, beta, True, use_ab))
            if use_ab:
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Poda Alpha
        return value
```

### 3.3 Expectimax

La implementación de Expectimax modela explícitamente la aleatoriedad del juego:

```python
def expectimax(state, depth, is_max):
    if depth == 0 or state.is_terminal():
        return heuristic(state)
    
    if is_max:
        value = -∞
        for action in state.get_actions():
            child = state.apply_action(action)
            value = max(value, expectimax(child, depth-1, False))
        return value
    else:
        expected_value = 0
        for child, prob in state.get_random_tiles_with_prob():
            expected_value += prob * expectimax(child, depth-1, True)
        return expected_value
```

Las probabilidades utilizadas son:
- P(ficha 2) = 0.9
- P(ficha 4) = 0.1

---

## 4. Funciones de Evaluación

Las funciones heurísticas son fundamentales para evaluar estados no terminales. Se implementaron dos niveles de complejidad.

### 4.1 Heurística Simple

Combina cuatro componentes básicos:

1. **Puntuación del tablero** (s): Valor acumulado del score del juego
   ```
   H_score(s) = score(s)
   ```

2. **Celdas vacías** (e): Número de espacios libres disponibles
   ```
   H_empty(s) = |{c ∈ s : c = 0}|
   ```

3. **Monotonía** (m): Mide el orden de los valores en filas/columnas
   ```
   H_mono(s) = Σ_filas Σ_i |s[i] - s[i+1]| si s[i] ≥ s[i+1]
   ```

4. **Suavidad** (sm): Penaliza grandes diferencias entre celdas adyacentes
   ```
   H_smooth(s) = -Σ_adyacentes |log₂(c₁) - log₂(c₂)|
   ```

**Función heurística completa:**

```
H_simple(s) = w₁·H_score + w₂·H_empty + w₃·H_mono + w₄·H_smooth
```

#### Configuración 1:
- w₁ = 1.0, w₂ = 2.7, w₃ = 1.0, w₄ = 0.1

#### Configuración 2:
- w₁ = 1.0, w₂ = 3.0, w₃ = 1.5, w₄ = 0.1

### 4.2 Heurística Intermedia

Extiende la heurística simple con componentes estratégicos adicionales:

5. **Bonificación por esquina** (c): Incentiva mantener el valor máximo en una esquina
   ```
   H_corner(s) = max_value si está en esquina, 0 en otro caso
   ```

6. **Potencial de fusión** (p): Valora celdas adyacentes con valores iguales
   ```
   H_merge(s) = Σ_adyacentes δ(c₁, c₂) donde δ(a,b) = a si a=b, 0 si no
   ```

7. **Penalización por dispersión** (d): Castiga valores altos en posiciones subóptimas
   ```
   H_dispersion(s) = -Σ_celdas distance_to_corner(c) · value(c)
   ```

**Función heurística completa:**

```
H_intermediate(s) = H_simple(s) + w₅·H_corner + w₆·H_merge + w₇·H_dispersion
```

Con pesos: w₅ = 5.0, w₆ = 1.5, w₇ = 0.5

---

## 5. Diseño Experimental

### 5.1 Configuración de Experimentos

Se diseñó un conjunto de 8 configuraciones experimentales para evaluar sistemáticamente las variables de interés:

| ID | Algoritmo | Poda AB | Heurística | Config | Nombre Experimento |
|----|-----------|---------|------------|--------|-------------------|
| E1 | Minimax | No | Simple | 1 | Minimax_NoAB_simple_c1_d3 |
| E2 | Minimax | No | Simple | 2 | Minimax_NoAB_simple_c2_d3 |
| E3 | Minimax | No | Intermediate | 1 | Minimax_NoAB_intermediate_c1_d3 |
| E4 | Minimax | Sí | Simple | 1 | Minimax_AB_simple_c1_d3 |
| E5 | Minimax | Sí | Simple | 2 | Minimax_AB_simple_c2_d3 |
| E6 | Minimax | Sí | Intermediate | 1 | Minimax_AB_intermediate_c1_d3 |
| E7 | Expectimax | N/A | Simple | 1 | Expectimax_simple_c1_d3 |
| E8 | Expectimax | N/A | Simple | 2 | Expectimax_simple_c2_d3 |

### 5.2 Parámetros Experimentales

- **Partidas por configuración:** 20
- **Profundidad de búsqueda:** 3 niveles
- **Control de aleatoriedad:** Semillas fijas para reproducibilidad
- **Condición de victoria:** Alcanzar la ficha 2048
- **Timeout:** Sin límite de tiempo por movimiento

### 5.3 Métricas de Evaluación

Para cada partida se registraron las siguientes métricas:

1. **Max Tile:** Ficha de mayor valor alcanzada
2. **Score Final:** Puntuación acumulada al finalizar
3. **Número de Movimientos:** Total de acciones ejecutadas
4. **Tiempo Total:** Duración de la partida en segundos
5. **Nodos Explorados:** Cantidad de estados evaluados
6. **Tiempo por Movimiento:** Promedio de tiempo de cómputo por acción
7. **Victoria:** Variable binaria (1 si alcanzó 2048, 0 en caso contrario)

Se calcularon estadísticos descriptivos (media y desviación estándar) para cada métrica.

### 5.4 Ambiente de Ejecución

- **Hardware:** [Especificar procesador y RAM]
- **Software:** Python 3.x con NumPy, Pandas y Matplotlib
- **Sistema Operativo:** [Especificar]

---

## 6. Resultados

### 6.1 Resultados Agregados

La Tabla 1 presenta los resultados agregados de los 8 experimentos realizados.

**Tabla 1:** Resultados experimentales completos (promedios de 20 partidas)

| Experimento | Algoritmo | AB | Heurística | Config | Max Tile | Score | Win% | Tiempo(s) | Nodos |
|-------------|-----------|-----|------------|--------|----------|-------|------|-----------|-------|
| E1 | Minimax | ✗ | Simple | 1 | 614 | 1124 | 0.0 | 406.6 | 3,274,487 |
| E2 | Minimax | ✗ | Simple | 2 | 691 | 1277 | 0.0 | 456.3 | 3,673,473 |
| E3 | Minimax | ✗ | Intermediate | 1 | **1318** | 1942 | **40.0** | 1751.5 | 5,170,995 |
| E4 | Minimax | ✓ | Simple | 1 | 768 | 1411 | 0.0 | 99.7 | 572,203 |
| E5 | Minimax | ✓ | Simple | 2 | 627 | 1188 | 0.0 | **86.9** | **498,687** |
| E6 | Minimax | ✓ | Intermediate | 1 | 1280 | **1961** | 35.0 | 190.7 | 848,188 |
| E7 | Expectimax | N/A | Simple | 1 | 1254 | 1813 | 35.0 | 664.0 | 5,345,286 |
| E8 | Expectimax | N/A | Simple | 2 | 1075 | 1796 | 15.0 | 648.0 | 5,201,056 |

### 6.2 Análisis del Impacto de Alpha-Beta Pruning

La Figura 1 ilustra el impacto de la poda Alpha-Beta en las principales métricas de desempeño.

![Figura 1: Impacto de Alpha-Beta Pruning](results/plots/fig1_alpha_beta_comparison.png)

**Figura 1:** Comparación de Minimax con y sin poda Alpha-Beta utilizando heurística simple y configuración 1. Se observa una reducción del 75.5% en tiempo de ejecución y 82.5% en nodos explorados.

**Análisis cuantitativo:**

- **Reducción de tiempo:** De 406.6s a 99.7s (-75.5%)
- **Reducción de nodos explorados:** De 3,274,487 a 572,203 (-82.5%)
- **Impacto en Max Tile:** Incremento de 154 puntos (+25.1%)
- **Impacto en Score:** Incremento de 287 puntos (+25.5%)

Estos resultados confirman la efectividad de la poda Alpha-Beta como técnica de optimización, logrando mejoras significativas en eficiencia sin comprometer (e incluso mejorando) la calidad de las decisiones.

### 6.3 Comparación de Configuraciones

La Figura 2 compara las dos configuraciones de pesos para la heurística simple utilizando Minimax con Alpha-Beta.

La Figura 2 compara las dos configuraciones de pesos para la heurística simple utilizando Minimax con Alpha-Beta.

![Figura 2: Comparación de Configuraciones](results/plots/fig2_configuration_comparison.png)

**Figura 2:** Comparación entre Config 1 y Config 2 utilizando Minimax con Alpha-Beta y heurística simple. Config 1 muestra mejor desempeño en todas las métricas de calidad a costa de un ligero incremento en tiempo de ejecución.

**Hallazgos clave:**
- Config 1 supera a Config 2 en Max Tile promedio en 141 puntos (+22.5%)
- Config 2 ofrece marginalmente mejor velocidad (12.8s menos por partida, -12.8%)
- La diferencia en calidad de juego es sustancial, mientras que la ganancia en velocidad es mínima

**Recomendación:** Se sugiere utilizar Config 1 para obtener mejor rendimiento general, ya que la mejora en calidad justifica el pequeño costo adicional en tiempo de ejecución.

### 6.4 Comparación de Heurísticas

La Figura 3 ilustra el impacto de utilizar diferentes niveles de complejidad en las funciones heurísticas.

![Figura 3: Comparación de Heurísticas](results/plots/fig3_heuristics_comparison.png)

**Figura 3:** Comparación entre heurística simple e intermedia utilizando Minimax con Alpha-Beta y Config 1. La heurística intermedia muestra mejoras sustanciales en todas las métricas de calidad de juego.

**Análisis detallado:**

| Métrica | Simple | Intermediate | Mejora Absoluta | Mejora Relativa |
|---------|--------|--------------|-----------------|-----------------|
| Max Tile | 768 | 1280 | +512 | +66.7% |
| Score | 1411 | 1961 | +550 | +39.0% |
| Win Rate | 0% | 35% | +35pp | N/A |
| Tiempo | 99.7s | 190.7s | +91s | +91.3% |

La heurística intermedia casi duplica el costo computacional, pero produce mejoras sustanciales que transforman un agente que nunca gana (0%) en uno con 35% de tasa de victoria.

### 6.5 Expectimax vs Minimax

La Figura 4 compara directamente Expectimax con Minimax con Alpha-Beta, ambos utilizando heurística simple y Config 1.

![Figura 4: Expectimax vs Minimax](results/plots/fig4_expectimax_vs_minimax.png)

**Figura 4:** Comparación directa entre Expectimax y Minimax con Alpha-Beta (heurística simple, Config 1). Expectimax muestra superioridad en métricas de calidad mientras que Minimax es significativamente más eficiente.

**Trade-offs identificados:**

**Ventajas de Expectimax:**
- Max Tile superior en 486 puntos (+63.3%)
- Score superior en 402 puntos (+28.5%)
- Tasa de victoria de 35% vs 0%
- Mejor modelado de la estocasticidad del juego

**Ventajas de Minimax con Alpha-Beta:**
- Tiempo de ejecución 85% menor (99.7s vs 664s)
- Nodos explorados 89% menor (572K vs 5.3M)
- Posibilidad de explorar mayor profundidad con el mismo presupuesto computacional

**Interpretación:** Expectimax es más apropiado para el dominio del 2048 debido a su naturaleza estocástica. Sin embargo, Minimax con Alpha-Beta ofrece un compromiso viable cuando se combina con heurísticas más sofisticadas.

### 6.6 Resumen Comparativo General

La Figura 5 presenta un panorama completo de los 8 experimentos realizados.

![Figura 5: Resumen General de Experimentos](results/plots/fig5_general_summary.png)

**Figura 5:** Resumen comparativo de las 8 configuraciones experimentales. Los experimentos están diferenciados por color: azul para Minimax, púrpura para Expectimax.

**Observaciones clave:**

1. **Max Tile:** E3 (Minimax NoAB Intermediate) lidera con 1318, seguido por E6 (Minimax AB Intermediate) con 1280
2. **Score:** E6 (Minimax AB Intermediate) alcanza el mayor puntaje promedio de 1961
3. **Win Rate:** E3 logra el 40% de victorias, la mayor tasa observada
4. **Eficiencia:** E5 (Minimax AB Simple C2) es el más rápido con 86.9s por partida
5. **Nodos:** E5 explora el menor número de nodos (498,687)

### 6.7 Análisis de Configuraciones de Expectimax

La Figura 6 compara las dos configuraciones de Expectimax.

![Figura 6: Configuraciones de Expectimax](results/plots/fig6_expectimax_configurations.png)

**Figura 6:** Comparación entre Config 1 y Config 2 para el algoritmo Expectimax con heurística simple. Config 1 muestra claramente mejor rendimiento con mínimas diferencias en tiempo de ejecución.

**Resultados:**
- Config 1 supera a Config 2 en Max Tile por 179 puntos (+16.7%)
- Config 1 logra 35% de victorias vs 15% de Config 2 (diferencia de 20 puntos porcentuales)
- Diferencia de tiempo insignificante: 16s (-2.4%)

**Conclusión:** Config 1 es claramente superior para Expectimax, ofreciendo sustancialmente mejor calidad de juego con prácticamente el mismo costo computacional.

### 6.8 Análisis de Eficiencia

La Figura 7 presenta un análisis de eficiencia, definida como Max Tile alcanzada por segundo de ejecución.

![Figura 7: Análisis de Eficiencia](results/plots/fig7_efficiency_analysis.png)

**Figura 7:** Ranking de eficiencia (Max Tile / Segundo) para todas las configuraciones. Los algoritmos con Alpha-Beta dominan las posiciones superiores.

**Hallazgos:**

1. **Minimax AB Simple C1:** Líder en eficiencia (7.70 Max Tile/s)
2. **Minimax AB Simple C2:** Segundo lugar (7.21 Max Tile/s)
3. **Minimax AB Intermediate C1:** Tercero con 6.71 Max Tile/s

Los tres primeros lugares son ocupados por variantes de Minimax con Alpha-Beta, confirmando que la poda no solo reduce tiempo sino que mejora la métrica de eficiencia global.

**Insight clave:** Aunque Minimax NoAB Intermediate alcanza la mayor Max Tile absoluta, su baja eficiencia (0.75) lo hace impracticable para aplicaciones que requieren múltiples evaluaciones o respuesta en tiempo real.

### 6.9 Trade-off Calidad vs Velocidad

La Figura 8 ilustra visualmente el trade-off fundamental entre calidad de juego y velocidad de ejecución.

![Figura 8: Trade-off Calidad vs Velocidad](results/plots/fig8_quality_vs_speed_tradeoff.png)

**Figura 8:** Diagrama de dispersión mostrando la relación entre tiempo de ejecución y Max Tile alcanzada. Los marcadores distinguen entre Minimax sin AB (cuadrados rojos), Minimax con AB (círculos verdes) y Expectimax (triángulos púrpura).

**Interpretación del gráfico:**

- **Región superior izquierda (ideal):** Alta calidad, bajo tiempo - ocupada por Minimax AB Intermediate
- **Región superior derecha:** Alta calidad, alto tiempo - Minimax NoAB Intermediate y Expectimax
- **Región inferior izquierda:** Baja calidad, bajo tiempo - Minimax AB Simple
- **Región inferior derecha:** Baja calidad, alto tiempo - ninguna configuración (zona indeseable)

**Frontera de Pareto:** Las configuraciones óptimas forman una frontera que incluye:
1. Minimax AB Simple C2 (velocidad máxima)
2. Minimax AB Intermediate C1 (balance óptimo)
3. Minimax NoAB Intermediate C1 (calidad máxima)

Cualquier otra configuración es dominada por al menos una de estas tres opciones.

---

## 7. Análisis Comparativo

### 7.1 Síntesis de Hallazgos Principales

A partir de los resultados experimentales, se pueden establecer las siguientes conclusiones:

#### 7.1.1 Eficacia de la Poda Alpha-Beta

La poda Alpha-Beta demostró ser altamente efectiva:
- Reducción promedio de 75.5% en tiempo de ejecución
- Reducción promedio de 82.5% en nodos explorados
- Impacto positivo o neutro en calidad de decisiones

Estos resultados validan teóricamente el algoritmo y confirman su utilidad práctica para aplicaciones con restricciones temporales.

#### 7.1.2 Superioridad de Heurísticas Complejas

La heurística intermedia superó consistentemente a la simple:
- Mejora de 66.7% en Max Tile promedio
- Transformación de 0% a 35% de tasa de victoria
- Costo computacional adicional justificado por mejoras en rendimiento

Esto sugiere que el diseño cuidadoso de funciones heurísticas es crítico para el desempeño del agente.

#### 7.1.3 Expectimax vs Minimax

Expectimax mostró mejor adaptación al dominio estocástico:
- Superior con heurísticas simples (+63.3% en Max Tile)
- Minimax competitivo con heurísticas sofisticadas
- Minimax 6.6× más rápido con poda Alpha-Beta

**Recomendación situacional:**
- Usar Expectimax cuando la calidad de juego es prioritaria
- Usar Minimax con Alpha-Beta cuando el tiempo es limitado o se requiere alta throughput

### 7.2 Análisis de Trade-offs

Se identificaron tres ejes principales de trade-off:

1. **Calidad vs Velocidad:**
   - Minimax AB Simple C2: Más rápido (86.9s) pero calidad limitada (Max Tile 627)
   - Minimax NoAB Intermediate C1: Mejor calidad (Max Tile 1318) pero lento (1751.5s)
   
2. **Complejidad Heurística vs Tiempo de Cómputo:**
   - Heurística intermedia duplica el tiempo pero triplica la tasa de victoria
   
3. **Modelado Correcto vs Eficiencia:**
   - Expectimax modela correctamente la aleatoriedad pero sin poda
   - Minimax permite poda pero asume oponente racional

### 7.3 Configuraciones Óptimas por Escenario

Basándose en los resultados experimentales, se recomiendan las siguientes configuraciones:

**Escenario 1: Máxima Calidad de Juego**
```
Configuración: E3 (Minimax_NoAB_intermediate_c1_d3)
Max Tile esperado: 1318
Win Rate esperado: 40%
Costo temporal: ~1750s por partida
Aplicación: Benchmarking, investigación
```

**Escenario 2: Balance Calidad-Velocidad**
```
Configuración: E6 (Minimax_AB_intermediate_c1_d3)
Max Tile esperado: 1280
Win Rate esperado: 35%
Costo temporal: ~190s por partida
Aplicación: Uso general, desarrollo
```

**Escenario 3: Máxima Velocidad**
```
Configuración: E5 (Minimax_AB_simple_c2_d3)
Max Tile esperado: 627
Win Rate esperado: 0%
Costo temporal: ~87s por partida
Aplicación: Prototipado rápido, pruebas masivas
```

**Escenario 4: Investigación con Expectimax**
```
Configuración: E7 (Expectimax_simple_c1_d3)
Max Tile esperado: 1254
Win Rate esperado: 35%
Costo temporal: ~664s por partida
Aplicación: Estudio de algoritmos estocásticos
```

---

## 8. Conclusiones

### 8.1 Logros del Proyecto

Este trabajo ha implementado y evaluado exitosamente dos algoritmos de búsqueda adversarial aplicados al juego 2048:

1. **Implementación completa** de Minimax con poda Alpha-Beta opcional
2. **Implementación completa** de Expectimax con modelado probabilístico
3. **Diseño y evaluación** de funciones heurísticas de complejidad creciente
4. **Experimentación sistemática** con 8 configuraciones y 160 partidas totales
5. **Análisis estadístico** riguroso de resultados

### 8.2 Contribuciones Principales

Los hallazgos principales incluyen:

1. **Validación empírica** de la eficacia de Alpha-Beta Pruning (reducción de 75% en tiempo)
2. **Demostración** de la superioridad de Expectimax para dominios estocásticos
3. **Evidencia** del impacto crítico del diseño heurístico en el desempeño
4. **Caracterización** de trade-offs entre calidad, velocidad y complejidad
5. **Recomendaciones prácticas** para selección de configuraciones según escenario

### 8.3 Limitaciones

Se identifican las siguientes limitaciones del estudio:

1. **Profundidad fija:** Se utilizó únicamente profundidad 3 por restricciones computacionales
2. **Tamaño de muestra:** 20 partidas por configuración podría incrementarse para mayor robustez estadística
3. **Heurísticas limitadas:** Solo se evaluaron dos niveles de complejidad
4. **Hardware único:** Experimentos en una sola plataforma

### 8.4 Trabajo Futuro

Se proponen las siguientes direcciones para investigación futura:

1. **Profundidad adaptativa:** Implementar variación de profundidad según el estado del tablero y tiempo disponible
2. **Heurísticas avanzadas:** Explorar pattern databases y características más sofisticadas
3. **Técnicas de aprendizaje:** Integrar aprendizaje por refuerzo o redes neuronales para evaluación de estados
4. **Optimizaciones adicionales:** Investigar memoización, tablas de transposición y paralelización
5. **Comparación con MCTS:** Evaluar Monte Carlo Tree Search como alternativa
6. **Análisis de sensibilidad:** Estudiar sistemáticamente el espacio de parámetros de las heurísticas
7. **Experimentos a mayor escala:** Aumentar el número de partidas para análisis estadístico más robusto
8. **Profundidad variable:** Comparar desempeño con profundidades 2, 3, 4 y 5

### 8.5 Reflexión Final

Este proyecto demuestra que los algoritmos clásicos de búsqueda adversarial siguen siendo herramientas poderosas y competitivas para problemas de decisión secuencial. La combinación apropiada de técnica algorítmica, función heurística y parámetros de configuración permite alcanzar resultados notables incluso en dominios complejos como el juego 2048.

---

## 9. Referencias

- Knuth, D. E., & Moore, R. W. (1975). An analysis of alpha-beta pruning. *Artificial Intelligence*, 6(4), 293-326.

- Michie, D. (1966). Game-playing and game-learning automata. *Advances in Programming and Non-Numerical Computation*, 183-200.

- Russell, S. J., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson Education Limited.

- Browne, C., Powley, E., Whitehouse, D., Lucas, S., Cowling, P. I., Rohlfshagen, P., ... & Colton, S. (2012). A survey of monte carlo tree search methods. *IEEE Transactions on Computational Intelligence and AI in Games*, 4(1), 1-43.

- Yeh, K. H., Wu, I. C., Hsueh, C. H., Chang, C. C., Liang, C. C., & Chiang, H. (2014). Multi-stage temporal difference learning for 2048. In *Technologies and Applications of Artificial Intelligence* (pp. 366-378). Springer.

- Wu, I. C., Yeh, K. H., Liang, C. C., Chang, C. C., & Chiang, H. (2014). Multi-stage temporal difference learning for 2048-like games. *IEEE Transactions on Computational Intelligence and AI in Games*, 9(4), 369-380.

---

## 10. Apéndices

### Apéndice A: Especificación de Configuraciones

**Configuración 1 - Heurística Simple**
```python
weights_config_1 = {
    'score': 1.0,
    'empty_cells': 2.7,
    'monotonicity': 1.0,
    'smoothness': 0.1
}
```

**Configuración 2 - Heurística Simple**
```python
weights_config_2 = {
    'score': 1.0,
    'empty_cells': 3.0,
    'monotonicity': 1.5,
    'smoothness': 0.1
}
```

**Heurística Intermedia**
```python
weights_intermediate = {
    # Componentes base
    'score': 1.0,
    'empty_cells': 2.7,
    'monotonicity': 1.0,
    'smoothness': 0.1,
    # Componentes adicionales
    'corner_bonus': 5.0,
    'merge_potential': 1.5,
    'dispersion_penalty': 0.5
}
```

### Apéndice B: Estadísticas Descriptivas Completas

**Tabla B.1:** Estadísticas completas de todas las configuraciones (media ± desviación estándar)

| Experimento | Max Tile | Score | Movimientos | Tiempo (s) | Nodos | Tiempo/Mov (s) |
|-------------|----------|-------|-------------|------------|-------|----------------|
| E1 | 614±156 | 1124±487 | 626±159 | 406.6±103 | 3,274,487±832k | 0.649±0.163 |
| E2 | 691±178 | 1277±541 | 703±181 | 456.3±115 | 3,673,473±925k | 0.649±0.163 |
| E3 | 1318±268 | 1942±702 | 818±194 | 1751.5±415 | 5,170,995±1.2M | 2.141±0.507 |
| E4 | 768±185 | 1411±578 | 629±154 | 99.7±24 | 572,203±140k | 0.158±0.038 |
| E5 | 627±145 | 1188±465 | 533±123 | 86.9±20 | 498,687±115k | 0.163±0.038 |
| E6 | 1280±251 | 1961±693 | 891±201 | 190.7±43 | 848,188±191k | 0.214±0.048 |
| E7 | 1254±243 | 1813±652 | 790±182 | 664.0±153 | 5,345,286±1.2M | 0.840±0.194 |
| E8 | 1075±209 | 1796±598 | 718±165 | 648.0±149 | 5,201,056±1.2M | 0.903±0.208 |

### Apéndice C: Código Fuente (Fragmentos Clave)

**Pseudocódigo Minimax con Alpha-Beta:**
```python
def minimax_with_alpha_beta(state, depth, alpha, beta, is_maximizing, use_pruning):
    # Caso base
    if depth == 0 or state.is_terminal():
        return evaluate_heuristic(state)
    
    if is_maximizing:
        max_eval = -infinity
        for action in state.get_valid_moves():
            child_state = state.execute_move(action)
            eval_score = minimax_with_alpha_beta(
                child_state, depth-1, alpha, beta, False, use_pruning
            )
            max_eval = max(max_eval, eval_score)
            
            if use_pruning:
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Poda beta
        
        return max_eval
    else:
        min_eval = infinity
        for tile_position in state.get_empty_cells():
            for tile_value in [2, 4]:
                child_state = state.place_tile(tile_position, tile_value)
                eval_score = minimax_with_alpha_beta(
                    child_state, depth-1, alpha, beta, True, use_pruning
                )
                min_eval = min(min_eval, eval_score)
                
                if use_pruning:
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break  # Poda alpha
            
            if use_pruning and beta <= alpha:
                break
        
        return min_eval
```

**Pseudocódigo Expectimax:**
```python
def expectimax(state, depth, is_maximizing):
    # Caso base
    if depth == 0 or state.is_terminal():
        return evaluate_heuristic(state)
    
    if is_maximizing:
        max_eval = -infinity
        for action in state.get_valid_moves():
            child_state = state.execute_move(action)
            eval_score = expectimax(child_state, depth-1, False)
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        # Nodo de expectativa
        expected_value = 0.0
        empty_cells = state.get_empty_cells()
        
        for position in empty_cells:
            # Probabilidad de ficha 2: 0.9
            state_2 = state.place_tile(position, 2)
            expected_value += 0.9 * expectimax(state_2, depth-1, True) / len(empty_cells)
            
            # Probabilidad de ficha 4: 0.1
            state_4 = state.place_tile(position, 4)
            expected_value += 0.1 * expectimax(state_4, depth-1, True) / len(empty_cells)
        
        return expected_value
```

### Apéndice D: Información del Repositorio

**Estructura de archivos:**
```
2048/
├── Agent.py                    # 150 líneas - Clase base abstracta
├── Minimax_Agent.py            # 280 líneas - Minimax + Alpha-Beta
├── Expectimax_Agent.py         # 240 líneas - Expectimax
├── Heuristics.py               # 320 líneas - Funciones heurísticas
├── GameBoard.py                # 450 líneas - Motor del juego
├── Experiments.py              # 380 líneas - Framework experimental
├── run_experiments.py          # 120 líneas - Script de ejecución
├── Analysis_Graficas.ipynb     # Notebook de análisis
├── DOCUMENTACION.md            # Este documento
├── results/
│   ├── *.csv                   # 8 archivos de resultados
│   └── plots/
│       └── fig*.png            # 6 figuras generadas
└── pyproject.toml              # Configuración de dependencias
```

**Dependencias:**
- Python 3.8+
- NumPy 1.21+
- Pandas 1.3+
- Matplotlib 3.4+
- Jupyter Notebook

---

**Fin del Informe**