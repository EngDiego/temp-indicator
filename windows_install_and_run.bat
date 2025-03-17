@echo off

:: Passo 0 - Verificar se o Python está instalado
echo Verificando versão do Python...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo Python não está instalado. Por favor, instale o Python primeiro.
    exit /b
)

:: Passo 1 - Verificar se o ambiente virtual já existe
if not exist .venv (
    echo Ambiente virtual não encontrado. Criando o ambiente virtual...
    python -m venv .venv
) else (
    echo Ambiente virtual já existe.
)

:: Passo 2 - Ativar o ambiente virtual
echo Ativando o ambiente virtual...
Set-ExecutionPolicy Unrestricted -Scope Process
call .venv\Scripts\Activate

:: Passo 3 - Verificar e instalar as dependências
echo Verificando dependências...
pip show -q -f -l -e . >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Instalando dependências...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo Dependências já instaladas.
)

:: Passo 4 - Rodar o main.py
echo Rodando o main.py...
python main.py

:: Passo 5 - Desativar o ambiente virtual
deactivate
