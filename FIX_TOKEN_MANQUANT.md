# 🔧 FIX - Token Discord Manquant

## ❌ Erreur

```
[OK] HTTP server sur port 10000
[X] Token manquant !
```

**Cause :** La variable d'environnement `DISCORD_BOT_TOKEN` n'est pas définie dans Render.

---

## ✅ Solution - Ajouter le Token dans Render

### Étape 1 : Récupérer Votre Token Discord

Si vous ne l'avez plus :

1. Allez sur https://discord.com/developers/applications
2. Cliquez sur votre application (bot)
3. Menu gauche → **"Bot"**
4. Scrollez jusqu'à **"Token"**
5. Cliquez sur **"Reset Token"** (si besoin) ou **"Copy"**
6. **COPIEZ** le token (format: une longue chaîne de caractères)

⚠️ **IMPORTANT :** Ne partagez JAMAIS ce token publiquement !

---

### Étape 2 : Ajouter le Token dans Render

#### Option A : Via le Dashboard (Recommandé)

1. **Connectez-vous** à https://render.com
2. **Cliquez** sur votre service Discord Bot
3. Menu gauche → **"Environment"**
4. **Cliquez** sur **"Add Environment Variable"**
5. **Remplissez** :
   - Key:   `DISCORD_BOT_TOKEN`
   - Value: votre_token_discord_copié
6. **Cliquez** sur **"Save Changes"**
7. Le service va **redéployer automatiquement**

#### Option B : Via render.yaml (Alternative)

Si vous préférez, vous pouvez aussi définir la variable dans `render.yaml` :

```yaml
services:
  - type: web
    name: discord-bot-nsfw
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python discord_bot_main.py
    envVars:
      - key: DISCORD_BOT_TOKEN
        sync: false  # Ne pas syncer (pour sécurité)
```

Puis dans le Dashboard, définissez la valeur du token.

---

### Étape 3 : Vérifier les Logs

Après le redéploiement (2-3 minutes), vérifiez les logs :

**✅ Succès :**
```
[OK] HTTP server sur port 10000
[OK] Demarrage bot avec boutons persistants...
[OK] Bot connecte : VotreBot#1234
[OK] Serveurs : X
[OK] Bot pret !
```

**❌ Toujours l'erreur :**
```
[X] Token manquant !
```
→ Le token n'est pas bien défini, recommencez l'Étape 2.

---

## 🔍 Vérification Rapide

### Dans Render Dashboard

1. Votre service → **Environment**
2. Vérifiez que vous voyez :
   ```
   DISCORD_BOT_TOKEN: •••••••••••••••••••
   ```
   (Les points indiquent que le token est caché pour sécurité)

### Variables Actuelles Nécessaires

```env
# OBLIGATOIRE
DISCORD_BOT_TOKEN=votre_token_discord

# OPTIONNEL (pour optimiser)
TOGETHER_API_KEY=votre_clé_gratuite
OPENROUTER_API_KEY=votre_clé_gratuite
```

---

## 📸 Capture d'Écran du Processus

```
Render Dashboard
    ↓
Votre Service (discord-bot-nsfw)
    ↓
Environment (menu gauche)
    ↓
Add Environment Variable (bouton bleu)
    ↓
    Key:   DISCORD_BOT_TOKEN
    Value: [votre_token_copié]
    ↓
Save Changes
    ↓
Redéploiement automatique (2-3 min)
```

---

## 🆘 Si Vous N'Avez Plus le Token

### Option 1 : Réinitialiser le Token (Sûr)

1. Discord Developer Portal → Votre application
2. Bot → Reset Token
3. Copiez le nouveau token
4. Ajoutez-le dans Render
5. Le bot redemarre avec le nouveau token

### Option 2 : Copier le Token Existant (Si disponible)

1. Si vous avez un fichier `.env` local avec le token
2. Copiez la valeur
3. Ajoutez-la dans Render

---

## ⚠️ Sécurité

### À FAIRE ✅

- ✅ Ajouter le token dans Render Environment Variables
- ✅ Garder le token privé
- ✅ Ne JAMAIS commiter le token dans git

### À NE PAS FAIRE ❌

- ❌ Partager le token publiquement
- ❌ Mettre le token dans le code source
- ❌ Commiter le fichier `.env` avec le token

---

## 🚀 Après le Fix

Une fois le token ajouté :

1. **Render redéploie** (2-3 minutes)
2. **Bot démarre** avec succès
3. **Bot en ligne** sur Discord
4. **Testez** avec `/start` dans un canal NSFW

---

## 📋 Checklist Rapide

- [ ] Récupérer token sur Discord Developer Portal
- [ ] Aller sur Render Dashboard
- [ ] Environment → Add Environment Variable
- [ ] Key: `DISCORD_BOT_TOKEN`
- [ ] Value: `votre_token_copié`
- [ ] Save Changes
- [ ] Attendre redéploiement (2-3 min)
- [ ] Vérifier logs : `[OK] Bot connecte`
- [ ] Tester sur Discord

---

## 💡 Note

C'est la **seule variable OBLIGATOIRE** pour que le bot fonctionne.

Les autres clés (Together.ai, OpenRouter) sont **optionnelles** - le bot fonctionne sans, mais peut être légèrement plus rapide avec.

---

**Une fois le token ajouté, le bot démarrera normalement ! 🚀**
