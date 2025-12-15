#!/bin/bash
# Script para ejecutar los experimentos completos del obligatorio 2048

echo "========================================"
echo "EXPERIMENTOS 2048 - OBLIGATORIO MEC"
echo "========================================"
echo ""
echo "Este script ejecutará los experimentos completos."
echo ""
echo "IMPORTANTE:"
echo "- Desactiva la suspensión automática del equipo"
echo "- Cierra programas pesados"
echo "- Tiempo estimado: 6-12 horas"
echo ""
read -p "Presiona ENTER para continuar..."

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Ejecutar experimentos
python run_experiments.py

echo ""
echo "Experimentos finalizados. Revisa la carpeta results/"
