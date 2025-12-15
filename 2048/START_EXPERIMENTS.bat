@echo off
echo ========================================
echo EXPERIMENTOS 2048 - OBLIGATORIO MEC
echo ========================================
echo.
echo Este script ejecutara los experimentos completos.
echo.
echo IMPORTANTE:
echo - Desactiva la suspension automatica del equipo
echo - Cierra programas pesados
echo - Tiempo estimado: 6-12 horas
echo.
pause

cd /d "%~dp0"
python run_experiments.py

pause
