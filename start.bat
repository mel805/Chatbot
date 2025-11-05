@echo off
REM Script de d?marrage du Bot Discord IA pour Windows

echo ================================
echo Bot Discord IA avec Groq
echo ================================
echo.

REM V?rifier si Python est install?
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe!
    echo Installez Python 3.8 ou superieur: https://www.python.org/
    pause
    exit /b 1
)

REM V?rifier si le fichier .env existe
if not exist .env (
    echo [ATTENTION] Fichier .env non trouve!
    echo Creation a partir de .env.example...
    copy .env.example .env
    echo.
    echo [OK] Fichier .env cree!
    echo Veuillez editer le fichier .env avec vos tokens:
    echo   - DISCORD_TOKEN
    echo   - GROQ_API_KEY
    echo.
    echo Puis relancez ce script.
    pause
    exit /b 1
)

REM V?rifier si l'environnement virtuel existe
if not exist venv (
    echo [INFO] Creation de l'environnement virtuel...
    python -m venv venv
    echo [OK] Environnement virtuel cree!
)

REM Activer l'environnement virtuel
echo [INFO] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer/mettre ? jour les d?pendances
echo [INFO] Installation des dependances...
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo.
echo [OK] Tout est pret!
echo [INFO] Lancement du bot...
echo.
echo ================================
echo.

REM Lancer le bot
python bot.py

pause
