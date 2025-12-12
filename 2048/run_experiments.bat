@echo off
REM Script para ejecutar experimentos de 2048 en Windows
REM Doble clic en este archivo para ejecutar

echo.
echo ================================================================================
echo     EXPERIMENTOS 2048 - EJERCICIO MEC
echo ================================================================================
echo.
echo Este script te ayudara a ejecutar los experimentos automaticamente.
echo.
echo Opciones disponibles:
echo   1) Prueba rapida (15 minutos) - Verificar que todo funciona
echo   2) Experimentos completos (2-4 horas) - Recomendado
echo   3) Analisis exhaustivo (8-12 horas) - Para dejar durante la noche
echo   4) Verificar instalacion
echo   5) Salir
echo.

:menu
set /p choice="Elige una opcion (1-5): "

if "%choice%"=="1" goto quick
if "%choice%"=="2" goto standard
if "%choice%"=="3" goto extensive
if "%choice%"=="4" goto verify
if "%choice%"=="5" goto end

echo Opcion invalida. Intenta de nuevo.
goto menu

:quick
echo.
echo ================================================================================
echo EJECUTANDO: Prueba Rapida
echo ================================================================================
echo.
python run_experiments.py quick
goto finish

:standard
echo.
echo ================================================================================
echo EJECUTANDO: Experimentos Completos
echo ================================================================================
echo.
echo IMPORTANTE: Esto tomara 2-4 horas.
echo Asegurate de que:
echo   - El ordenador NO se suspenda automaticamente
echo   - Tengas al menos 1 GB de espacio libre
echo   - Otros programas pesados esten cerrados
echo.
set /p confirm="Continuar? (S/N): "
if /i "%confirm%" NEQ "S" goto menu

python run_experiments.py standard
goto finish

:extensive
echo.
echo ================================================================================
echo EJECUTANDO: Analisis Exhaustivo (NOCTURNO)
echo ================================================================================
echo.
echo ADVERTENCIA: Esto tomara 8-12 horas.
echo.
echo CHECKLIST ANTES DE COMENZAR:
echo   [ ] Ordenador conectado a corriente (si es portatil)
echo   [ ] Suspension automatica DESACTIVADA
echo   [ ] Al menos 1 GB de espacio libre
echo   [ ] Otros programas cerrados
echo   [ ] Nadie va a apagar el ordenador
echo.
set /p confirm="Estas seguro que quieres continuar? (S/N): "
if /i "%confirm%" NEQ "S" goto menu

echo.
echo Iniciando experimentos...
echo Los resultados se guardaran en la carpeta 'results/'
echo.
python run_experiments.py extensive
goto finish

:verify
echo.
echo ================================================================================
echo VERIFICANDO INSTALACION
echo ================================================================================
echo.
python quick_start_guide.py
echo.
pause
goto menu

:finish
echo.
echo ================================================================================
echo EXPERIMENTOS COMPLETADOS
echo ================================================================================
echo.
echo Proximos pasos:
echo   1. Abre Analysis.ipynb en VS Code o Jupyter
echo   2. Ejecuta todas las celdas (Run All)
echo   3. Revisa los graficos en results/plots/
echo   4. Usa las estadisticas para tu informe
echo.
echo Archivos generados:
echo   - results/*.csv : Resultados detallados
echo   - results/plots/*.png : Graficos
echo   - models/ : Mejores configuraciones
echo.
goto end

:end
echo.
pause
