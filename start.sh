#!/bin/bash
# Script de démarrage pour le bot Discord

echo "🚀 Démarrage du bot Discord NSFW avec API gratuite..."
echo "📋 Provider: ${AI_PROVIDER:-free_nsfw}"
echo "🔧 Python version: $(python --version)"

# Lancer le bot
python discord_bot_main.py
