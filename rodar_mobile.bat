@echo off
echo.
echo =======================================================
echo    INICIANDO A APLICACAO MOBILE (FLUTTER) NO CHROME    
echo =======================================================
echo.
rem Carrega temporariamente o Flutter no PATH local caso o Windows ainda nao tenha recarregado o ambiente
set PATH=%PATH%;E:\src\flutter\bin
cd mobile_app
flutter run -d chrome
