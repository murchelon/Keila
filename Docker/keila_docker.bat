@echo off
echo Escolha uma opção:
echo 1. Build da imagem Docker
echo 2. Rodar container com Docker
echo 3. Subir com docker-compose
echo 4. Parar docker-compose
set /p choice=Digite o número da opção:

if "%choice%"=="1" docker build -t keila .
if "%choice%"=="2" docker run --rm --privileged -p 5000:5000 keila
if "%choice%"=="3" docker-compose -f docker-compose-fastapi.yml up --build
if "%choice%"=="4" docker-compose -f docker-compose-fastapi.yml down