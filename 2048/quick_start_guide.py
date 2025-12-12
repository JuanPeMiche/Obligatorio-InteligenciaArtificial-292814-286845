"""
GUÍA RÁPIDA - EJECUCIÓN NOCTURNA
=================================

Este archivo contiene instrucciones paso a paso para dejar corriendo
los experimentos durante la noche.
"""

# ============================================================================
# PASO 1: VERIFICAR QUE TODO FUNCIONA
# ============================================================================

print("PASO 1: Verificar instalación")
print("-" * 60)

try:
    from GameBoard import GameBoard
    from Expectimax_Agent import ExpectimaxAgentOptimized
    from Minimax_Agent import MinimaxAgentOptimized
    from Experiments import ExperimentSuite
    print("✓ Todos los módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("\nSolución: Ejecuta 'poetry install' en la terminal")
    exit(1)

# Test rápido
print("\nPASO 2: Test rápido (30 segundos)")
print("-" * 60)

try:
    agent = ExpectimaxAgentOptimized(depth=2, weights_config='balanced')
    board = GameBoard()
    
    for _ in range(10):
        action = agent.play(board)
        done = board.play(action)
        if done:
            break
    
    print(f"✓ Test completado. Max tile alcanzado: {board.get_max_tile()}")
except Exception as e:
    print(f"❌ Error durante el test: {e}")
    exit(1)

# ============================================================================
# PASO 3: INSTRUCCIONES PARA EJECUCIÓN NOCTURNA
# ============================================================================

print("\n" + "=" * 80)
print("PASO 3: LISTO PARA EJECUCIÓN NOCTURNA")
print("=" * 80)

print("""
TODO ESTÁ CONFIGURADO CORRECTAMENTE ✓

Para iniciar los experimentos nocturnos, ejecuta UNO de estos comandos:

┌─────────────────────────────────────────────────────────────────────────┐
│                     OPCIÓN 1: MODO EXTENSIVO                            │
│  (Recomendado para ejecución nocturna - 8-12 horas)                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  python run_experiments.py extensive                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                     OPCIÓN 2: MODO ESTÁNDAR                             │
│  (Si no quieres esperar tanto - 2-4 horas)                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  python run_experiments.py standard                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                     OPCIÓN 3: MODO RÁPIDO                               │
│  (Solo para verificar que funciona - 10-15 minutos)                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  python run_experiments.py quick                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


IMPORTANTE - ANTES DE INICIAR:
═══════════════════════════════

1. ⚡ Desactiva suspensión automática del ordenador:
   Windows: Panel de Control > Opciones de energía > "Nunca" suspender
   
2. 💾 Asegúrate de tener al menos 1 GB libre en disco

3. 🔋 Si es portátil, conéctalo a la corriente

4. ❌ Cierra programas pesados (navegadores, juegos, etc.)

5. 📊 Los resultados se guardarán automáticamente en la carpeta 'results/'


DESPUÉS DE LA EJECUCIÓN:
════════════════════════

1. Abre Analysis.ipynb
2. Ejecuta todas las celdas (Run All)
3. Revisa los gráficos en results/plots/
4. Usa las estadísticas para tu informe


MONITOREAR PROGRESO:
═══════════════════

Durante la ejecución verás:
- Barra de progreso para cada experimento
- Estadísticas después de cada conjunto
- Los resultados se guardan automáticamente

Si necesitas cancelar: Presiona Ctrl+C
Los resultados parciales se habrán guardado.


¿LISTO PARA COMENZAR?
════════════════════

Ejecuta el comando elegido en una nueva terminal:

  cd "{}"
  python run_experiments.py extensive

¡Buena suerte! 🚀
""".format(__file__.replace('quick_start_guide.py', '')))

print("=" * 80)
print()
