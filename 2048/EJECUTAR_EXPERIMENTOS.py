"""
SCRIPT DE INICIO - EXPERIMENTOS FINALES
========================================

Este script ejecuta los 36 experimentos completos del obligatorio:
- 2 profundidades (3, 4)
- 3 heurísticas (simple, intermediate, complex)
- 2 configuraciones de pesos por heurística
- 3 algoritmos (Minimax sin AB, Minimax con AB, Expectimax)

Ejecutar con:
    python EJECUTAR_EXPERIMENTOS.py

Para test rápido (5 partidas):
    python EJECUTAR_EXPERIMENTOS.py --quick

Para modo standard (20 partidas):
    python EJECUTAR_EXPERIMENTOS.py --standard
"""

import subprocess
import sys
import os

def main():
    print("\n" + "=" * 80)
    print("EXPERIMENTOS 2048 - OBLIGATORIO MEC".center(80))
    print("=" * 80)
    print("\n")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("run_experiments.py"):
        print("❌ ERROR: No se encuentra run_experiments.py")
        print("   Asegúrate de estar en el directorio correcto.")
        sys.exit(1)
    
    # Verificar que los archivos necesarios existen
    required_files = [
        "Heuristics.py",
        "Minimax_Agent.py", 
        "Expectimax_Agent.py",
        "Experiments.py",
        "GameBoard.py"
    ]
    
    missing = [f for f in required_files if not os.path.exists(f)]
    if missing:
        print(f"❌ ERROR: Faltan archivos: {', '.join(missing)}")
        sys.exit(1)
    
    print("✅ Todos los archivos necesarios están presentes\n")
    
    # Mostrar información
    print("📋 CONFIGURACIÓN DE EXPERIMENTOS:")
    print("   • Total de experimentos: 36")
    print("   • Profundidades: 3, 4")
    print("   • Heurísticas: simple (c1, c2), intermediate (c1, c2), complex (c1, c2)")
    print("   • Algoritmos por config: Minimax (sin AB), Minimax (con AB), Expectimax")
    print()
    print("⏱️  TIEMPO ESTIMADO:")
    print("   • Quick Test (5 partidas):  1-2 horas")
    print("   • Standard (20 partidas):   6-12 horas")
    print()
    print("📁 RESULTADOS:")
    print("   • Carpeta: results/")
    print("   • Archivos CSV individuales por experimento")
    print("   • Archivo combinado: all_experiments_FECHA_HORA.csv")
    print()
    
    # Determinar modo
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            mode = "1"
        elif sys.argv[1] == "--standard":
            mode = "2"
        else:
            print(f"❌ Opción desconocida: {sys.argv[1]}")
            print("   Usa: --quick o --standard")
            sys.exit(1)
    else:
        # Modo interactivo
        print("SELECCIONA EL MODO:")
        print("1. Quick Test (5 partidas/experimento)")
        print("2. Standard (20 partidas/experimento)")
        print("3. Salir")
        print()
        mode = input("Opción (1-3): ").strip()
    
    if mode == "3":
        print("\n👋 Saliendo...")
        sys.exit(0)
    
    if mode not in ["1", "2"]:
        print(f"\n❌ Opción inválida: {mode}")
        sys.exit(1)
    
    # Confirmación
    mode_name = "QUICK TEST" if mode == "1" else "STANDARD"
    time_est = "1-2 horas" if mode == "1" else "6-12 horas"
    
    print("\n" + "⚠️ " * 20)
    print(f"\nMODO SELECCIONADO: {mode_name}")
    print(f"TIEMPO ESTIMADO: {time_est}")
    print("\nASEGÚRATE DE QUE:")
    print("  ✓ El ordenador NO se suspenda automáticamente")
    print("  ✓ Tengas al menos 1 GB de espacio libre")
    print("  ✓ Otros programas pesados estén cerrados")
    print("\n" + "⚠️ " * 20 + "\n")
    
    confirm = input("¿Iniciar experimentos? (S/N): ").strip().upper()
    
    if confirm != "S":
        print("\n❌ Experimentos cancelados")
        sys.exit(0)
    
    print("\n🚀 INICIANDO EXPERIMENTOS...\n")
    print("=" * 80)
    
    # Ejecutar run_experiments.py
    try:
        # Simular entrada del usuario para run_experiments.py
        cmd = [sys.executable, "run_experiments.py"]
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
        
        # Enviar la opción seleccionada
        process.communicate(input=f"{mode}\nS\n")
        
        if process.returncode == 0:
            print("\n\n" + "=" * 80)
            print("✅ EXPERIMENTOS COMPLETADOS CON ÉXITO".center(80))
            print("=" * 80)
            print("\n📊 Próximos pasos:")
            print("   1. Revisa los archivos CSV en results/")
            print("   2. Abre Analysis.ipynb para visualizar resultados")
            print("   3. Genera gráficos para el informe")
            print()
        else:
            print("\n\n❌ Los experimentos terminaron con errores")
            print("   Revisa los resultados parciales en results/")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n❌ Experimentos interrumpidos por el usuario")
        print("   Los resultados parciales se han guardado en results/")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error al ejecutar experimentos: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
