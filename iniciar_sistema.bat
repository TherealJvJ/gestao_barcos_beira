@echo off
echo =======================================================
echo    INICIANDO SISTEMA COMPLETO (DJANGO + FLUTTER)
echo =======================================================
echo.

echo 1. Criando a "ponte" USB (adb reverse) para o telemovel...
adb reverse tcp:8000 tcp:8000

echo.
echo 2. Iniciando Servidor Django em segundo plano...
start cmd /k "call .venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8000"

echo.
echo 3. Configurando variaveis de ambiente para o drive E (Evita falta de espaco em C)...
set TEMP=E:\.temp
set TMP=E:\.temp
set PUB_CACHE=E:\.pub-cache
set GRADLE_USER_HOME=E:\.gradle
set PATH=%PATH%;E:\src\flutter\bin

echo.
echo 4. Iniciando Aplicacao Mobile no Telemovel...
cd mobile_app
flutter run
pause
