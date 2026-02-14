@echo off
cd /d "%~dp0"
echo Iniciando app Streamlit...
streamlit run src/app.py
pause
@echo off
echo.
echo ==========================================
echo  Sistema de Retencion - Banco Horizonte
echo ==========================================
echo.
echo Iniciando aplicacion Streamlit...
echo.

cd /d "%~dp0"
streamlit run src/app.py

pause
