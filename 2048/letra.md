## Contexto del problema

Han sido seleccionados para formar parte del desarrollo de robots humanoides de propósito general,
Pésimusk, de la aclamada empresa tecnológica Tosla. En su rol, estarán encargados de resolver dos
problemas críticos para el avance de nuestro ambicioso proyecto.

## Objetivos

En Tosla, esperamos que demuestren su expertise en aplicar técnicas de Q-Learning y
Minimax/Expectimax para resolver los problemas que se presentan a continuación:

### Módulo de Balance Dinámico (MBD)

Nuestros prototipos Pésimusk, aunque estéticamente impecables, a veces muestran una tendencia
alarmante a perder el equilibrio. Pero no hay problema, porque para eso están ustedes. Como primer
paso para resolver esta problemática, deben programar una IA que aprenda a mantener un poste
vertical sobre una plataforma móvil el mayor tiempo posible.

### Módulo de Estrategia Cognitiva (MEC)

Una vez que nuestros Pésimusks caminen con estabilidad, deben demostrar su capacidad para la
toma de decisiones complejas. Para ello, los pondremos a prueba en el juego 2048. Este entorno nos
permitirá evaluar su capacidad para anticipar movimientos, planificar a largo plazo y optimizar resul-
tados. Su tarea es crear un algoritmo que no solo resuelva el juego, sino que lo domine, demostrando
que nuestros robots son mucho más que un simple cuerpo de metal.

## Tareas a desarrollar

### MBD

La primera tarea está basada en el ambiente CartPole-v1. Concretamente, se pide:

1. **Discretizar las observaciones y acciones:** Dado que las observaciones y acciones son con-
   tinuas, deben discretizarse. Se espera al menos 2 pruebas diferentes, justificando su elección
   e impacto en el agente.

2. **Técnica:** La técnica elegida para resolver el problema es Q-Learning.

3. **Exploración de hiperparámetros** para encontrar el algoritmo que obtenga mejores resultados.
   Se espera que se experimenten múltiples combinaciones de hiperparámetros, justificando su
   forma de evaluar el rendimiento del agente, y la elección final de los mismos.

4. **Lectura de artículo:** leer el artículo *Stochastic Q-learning for Large Discrete Action Spaces* e
   implementar Stochastic Q-learning. Se espera que apliquen un análisis y experimentación
   similares a su trabajo con Q-Learning.

### MEC

La segunda tarea está basada en el juego 2048. Concretamente, se les pide:

1. **Técnicas:** implementar tanto Minimax como Expectimax para decidir cuál es la mejor técnica
   para este caso. En el caso de Minimax, deben implementarlo utilizando Alpha-Beta Pruning y
   analizar su impacto.

2. **Funciones de evaluación:** implementar funciones de evaluación que permitan analizar un es-
   tado dado. Se espera que experimenten con las funciones, intentando con distintas combina-
   ciones de las mismas, y ponderadas de distintas formas.

3. **Experimentación:** Definir pruebas para evaluar los agentes y hacer un registro completo de
   los resultados obtenidos.

## Auditoría

Para evaluar el desempeño de los agentes entrenados, deben entregar todo el código en Python (.py
y .ipynb), los modelos computados (.pkl o formatos similares) y un informe de no más de 20 páginas
más anexos, en formato .pdf. Todo el contenido debe ser entregado en un archivo .zip.

Es obligatorio entregar al menos un modelo computado para el primer ejercicio. Caso contrario, el
ejercicio será considerado como no hecho. El informe debe incluir:

- Resumen de cómo abordó cada tarea. Incluyendo información relevante. (Ej: Bitácora con: in-
  teracción con el simulador, parámetros utilizados, tiempo de ejecución y resultados obtenidos).

- Apoyo visual (gráficos) y comentarios que permitan entender el desempeño de sus soluciones.

- Cualquier nota de advertencia que desee comunicar. Por ejemplo, en caso de haber encontrado
  dificultades, elaborar en cuáles fueron y por qué no se pudieron solucionar.

La evaluación se basará en la documentación entregada. Es fundamental que su informe sea claro,
legible y contenga toda la información necesaria para comprender a fondo el enfoque, los resultados
y las conclusiones de su trabajo.

## Ambiente

Se utilizará Poetry para ambos ejercicios en entornos separados. Se les entregará código de ambos
ambientes listo para ejecutar el simulador.

## Recomendación

Les recomendamos que comiencen el trabajo con antelación, ya que las ejecuciones pueden tomar
tiempo.
