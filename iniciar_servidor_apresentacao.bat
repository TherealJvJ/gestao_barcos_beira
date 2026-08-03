@echo off
echo =======================================================
echo    INICIANDO SERVIDOR PARA APRESENTACAO (USB E WIFI)
echo =======================================================
echo.
echo 1. Criando a "ponte" USB (adb reverse) para o telemovel...
adb reverse tcp:8000 tcp:8000
echo.
echo 2. Iniciando Servidor Django...
call .venv\Scripts\activate.bat
python manage.py runserver 0.0.0.0:8000
pause
