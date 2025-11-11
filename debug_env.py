"""
Script de debug pour vérifier les variables d'environnement
"""
import os
from dotenv import load_dotenv

print("=" * 60)
print("DEBUG - Variables d'environnement")
print("=" * 60)

# Charger .env si existe
load_dotenv()
print(f"\n[1] load_dotenv() exécuté")

# Vérifier DISCORD_BOT_TOKEN
token = os.getenv('DISCORD_BOT_TOKEN')
print(f"\n[2] DISCORD_BOT_TOKEN trouvé: {bool(token)}")
if token:
    print(f"    Longueur: {len(token)} caractères")
    print(f"    Début: {token[:10]}...")
else:
    print("    ❌ TOKEN NON TROUVÉ")

# Lister toutes les variables qui contiennent "TOKEN" ou "DISCORD"
print(f"\n[3] Variables contenant 'TOKEN' ou 'DISCORD':")
for key in os.environ.keys():
    if 'TOKEN' in key.upper() or 'DISCORD' in key.upper():
        value = os.environ[key]
        print(f"    - {key}: {value[:20] if value else 'vide'}...")

# Vérifier PORT
port = os.getenv('PORT', '10000')
print(f"\n[4] PORT: {port}")

# Autres variables importantes
print(f"\n[5] Autres variables:")
for key in ['TOGETHER_API_KEY', 'OPENROUTER_API_KEY', 'HUGGINGFACE_API_KEY']:
    val = os.getenv(key)
    print(f"    - {key}: {'✓ défini' if val else '✗ non défini'}")

print("\n" + "=" * 60)
print("Fin du debug")
print("=" * 60)
