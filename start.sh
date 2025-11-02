#!/bin/bash
# Script de d?marrage du Bot Discord IA

echo "?? D?marrage du Bot Discord IA avec Groq..."
echo ""

# V?rifier si Python est install?
if ! command -v python3 &> /dev/null; then
    echo "? Python 3 n'est pas install?!"
    echo "Installez Python 3.8 ou sup?rieur: https://www.python.org/"
    exit 1
fi

# V?rifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "??  Fichier .env non trouv?!"
    echo "Cr?ation ? partir de .env.example..."
    cp .env.example .env
    echo ""
    echo "? Fichier .env cr??!"
    echo "?? Veuillez ?diter le fichier .env avec vos tokens:"
    echo "   - DISCORD_TOKEN"
    echo "   - GROQ_API_KEY"
    echo ""
    echo "Puis relancez ce script."
    exit 1
fi

# V?rifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "?? Cr?ation de l'environnement virtuel..."
    python3 -m venv venv
    echo "? Environnement virtuel cr??!"
fi

# Activer l'environnement virtuel
echo "?? Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer/mettre ? jour les d?pendances
echo "?? Installation des d?pendances..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "? Tout est pr?t!"
echo "?? Lancement du bot..."
echo ""
echo "????????????????????????????????????????"
echo ""

# Lancer le bot
python3 bot.py
