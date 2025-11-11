# 🚀 Configuration Render.com - Fix Déploiement

## ❌ Problème Résolu

**Erreur:** `can't open file 'bot.py': No such file or directory`

**Cause:** L'ancien fichier `bot.py` n'existe plus. Le nouveau fichier est `discord_bot_main.py`.

## ✅ Solution

Trois fichiers de configuration ont été créés :

### 1. `Procfile`
```
web: python discord_bot_main.py
```

### 2. `render.yaml`
Configuration complète pour Render

### 3. `start.sh`
Script de démarrage alternatif

## 📋 Configuration Render Dashboard

### Option 1 : Automatique (Recommandé)

Render détectera automatiquement `render.yaml` et l'utilisera.

**Aucune action nécessaire après le push !**

### Option 2 : Configuration Manuelle

Si Render ne détecte pas automatiquement :

1. Allez dans votre service Render
2. Cliquez sur **Settings**
3. Trouvez **Build & Deploy** → **Start Command**
4. Changez de :
   ```
   python bot.py
   ```
   vers :
   ```
   python discord_bot_main.py
   ```
5. Sauvegardez

## 🔧 Variables d'Environnement

Vérifiez que ces variables sont bien définies dans Render :

### Obligatoire

```
DISCORD_BOT_TOKEN = votre_token_discord
```

### Optionnel (pour meilleures performances)

```
HUGGINGFACE_API_KEY = hf_votre_token_gratuit
AI_PROVIDER = free_nsfw
```

### Automatique (géré par Render)

```
PORT = (attribué automatiquement par Render)
```

## 🚀 Déploiement

### Étape 1 : Commit et Push

```bash
git add -A
git commit -m "fix: Update start command to discord_bot_main.py + API gratuite NSFW"
git push origin cursor/update-discord-bot-chat-api-3e13
```

### Étape 2 : Redéploiement Render

Render redéploiera automatiquement après le push.

### Étape 3 : Vérifier les Logs

Dans Render Dashboard → Logs, vous devriez voir :

```
🚀 Démarrage du bot Discord NSFW avec API gratuite...
📋 Provider: free_nsfw
[OK] Bot connecté : VotreBot#1234
[OK] Serveurs : X
[OK] Vues configurees
[OK] Bot pret !
[OK] HTTP server sur port 10000
```

## 🐛 Dépannage

### Erreur "bot.py not found" persiste

→ Vérifiez que la **Start Command** dans Render est bien :
```
python discord_bot_main.py
```

### Erreur "Module not found"

→ Vérifiez que `requirements.txt` est bien présent et contient :
```
discord.py>=2.3.2
aiohttp>=3.9.0
python-dotenv>=1.0.0
asyncio>=3.4.3
```

### Bot ne se connecte pas

→ Vérifiez que `DISCORD_BOT_TOKEN` est bien défini dans les variables d'environnement Render

### "API non configurée"

→ C'est normal ! Le bot utilise maintenant `AI_PROVIDER=free_nsfw` qui ne nécessite PAS de token obligatoire
→ Pour optimiser, ajoutez un token HuggingFace gratuit

## 📊 Vérification du Déploiement

Après le déploiement, vérifiez :

1. **Logs Render** : Aucune erreur, bot démarré
2. **Discord** : Bot apparaît en ligne
3. **Test** : `/start` dans un canal NSFW
4. **Conversation** : Tester avec un chatbot

## 🎉 Résultat Attendu

Après le fix, vous devriez voir dans les logs Render :

```
[OK] Bot connecté : VotreBot#1234
[DEBUG] Tentative 1/4: HuggingFace-Mistral-Uncensored
[SUCCESS] HuggingFace-Mistral-Uncensored: ...
[OK] HTTP server sur port 10000
```

---

## 📞 Support Rapide

| Problème | Solution |
|----------|----------|
| "bot.py not found" | Changer Start Command vers `discord_bot_main.py` |
| "Module not found" | Vérifier `requirements.txt` |
| Bot offline | Vérifier `DISCORD_BOT_TOKEN` |
| API errors | Normal avec `free_nsfw`, aucun token requis |

---

**Le bot devrait maintenant démarrer correctement avec l'API gratuite ! 🚀**
