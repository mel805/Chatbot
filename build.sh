#!/bin/bash
set -e

echo "🔧 Nettoyage du cache Python..."
rm -rf .venv
rm -rf __pycache__
rm -rf *.pyc

echo "✅ Version Python actuelle:"
python3 --version

echo "📦 Installation des dépendances avec Python 3.11..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build terminé avec succès!"
