# 🎯 PROCÉDURE SIMPLE RENDER

## ⚠️ POURQUOI ÇA ÉCHOUE

**Problème :** Render utilise encore l'ancienne version du code

**"Aucun log" = Render n'a pas redéployé le bot**

---

## ✅ SOLUTION EN 5 ÉTAPES

### ÉTAPE 1 : Ouvrir Render Dashboard

🔗 **Aller sur :** https://dashboard.render.com/

---

### ÉTAPE 2 : Trouver votre service bot

Dans la liste des services, **cliquer sur celui qui héberge le bot Discord**

Nom probable : `chatbot`, `discord-bot`, `bot`, etc.

---

### ÉTAPE 3 : Ajouter/Vérifier la variable d'environnement

1. **Cliquer sur l'onglet "Environment"** (à gauche)

2. **Chercher** : `STABLE_HORDE_API_KEY`

3. **Si elle n'existe PAS :**
   - Cliquer **"Add Environment Variable"**
   - **Key** : `STABLE_HORDE_API_KEY`
   - **Value** : `0000000000`
   - Cliquer **"Save Changes"**

4. **Si elle existe déjà :**
   - Vérifier que la valeur est `0000000000`
   - Si différente, modifier et sauvegarder

---

### ÉTAPE 4 : Redéployer manuellement

1. **En haut à droite**, cliquer sur **"Manual Deploy"**

2. Dans le menu déroulant :
   - Sélectionner **"Deploy latest commit"**
   - OU **"Clear build cache & deploy"** (si problème)

3. **Attendre** : Render va reconstruire et redémarrer (2-5 min)

**Vous verrez :**
```
Deploying...
Building...
Starting...
Live ✅
```

---

### ÉTAPE 5 : Vérifier les logs

1. **Cliquer sur l'onglet "Logs"** (à gauche)

2. **Scroller jusqu'au bas** (logs les plus récents)

3. **Vous DEVEZ voir** (si redéploiement réussi) :

```
==> Starting service with: python bot.py
discord.ext.commands.bot INFO Logging in using static token
discord.client INFO Successfully logged in as VotreBot#1234
[INFO] Bot ready!
```

**Si vous ne voyez PAS ces lignes = le bot n'a pas redémarré**

---

## 🧪 TESTER APRÈS REDÉPLOIEMENT

### 1. Vérifier le bot sur Discord

Le bot doit être **EN LIGNE** (cercle vert)

---

### 2. Tester la génération d'image

Dans Discord :
```
/generer_image style:explicit_blowjob
```

---

### 3. REGARDER LES LOGS RENDER EN TEMPS RÉEL

**Pendant que vous testez dans Discord :**

- Rester sur l'onglet "Logs" de Render
- Les logs doivent défiler en temps réel
- **Vous DEVEZ voir** :

```
[IMAGE] Using Stable Horde FREE P2P Network (NSFW allowed)
[IMAGE] Using Stable Horde anonymous API key (limited)
[IMAGE] Submitting to Stable Horde with prompt length: XXX
[IMAGE] Stable Horde request submitted: abc-123-xyz
[IMAGE] Stable Horde waiting... Queue: 5
[IMAGE] Stable Horde SUCCESS after 45s
```

**Si vous ne voyez RIEN de nouveau dans les logs Render :**
= Le bot n'est pas redéployé ou utilise l'ancienne version

---

## ❌ SI "AUCUN LOG" PERSISTE

### Vérifications :

1. **Onglet "Events"** dans Render
   - Dernier événement = "Deploy succeeded" (récent < 10 min)
   - Si pas récent → Refaire "Manual Deploy"

2. **Le bot répond dans Discord ?**
   - Essayer `/ping` ou autre commande
   - Si pas de réponse = bot down

3. **Chercher "Error" dans les logs**
   - Logs Render → Ctrl+F → "Error"
   - Si erreur trouvée → me la copier

---

## 📋 CHECKLIST COMPLÈTE

Après avoir suivi les 5 étapes :

- [ ] Variable `STABLE_HORDE_API_KEY=0000000000` ajoutée
- [ ] "Manual Deploy" cliqué
- [ ] Status = "Live" avec checkmark vert
- [ ] Logs montrent "Bot ready!"
- [ ] Bot en ligne sur Discord
- [ ] Commande `/generer_image` testée
- [ ] Logs Render montrent les NOUVELLES lignes Stable Horde

**Si TOUTE la checklist est OK mais génération échoue :**
→ Copier-coller les logs Render complets

---

## 🆘 BESOIN D'AIDE

**Si ça ne fonctionne toujours pas, envoyez-moi :**

### 1. Screenshot Render - Onglet "Logs" (dernières 50 lignes)

### 2. Screenshot Render - Onglet "Environment" 

Montrer les variables :
- `DISCORD_TOKEN`
- `GROQ_API_KEY`
- `STABLE_HORDE_API_KEY`
- (masquer les valeurs sensibles si besoin)

### 3. Message d'erreur Discord

Le message exact affiché quand `/generer_image` échoue

---

## 💡 ASTUCE

**Pour voir les logs défiler en direct :**

1. Ouvrir 2 fenêtres côte à côte :
   - Gauche : Discord
   - Droite : Render Logs

2. Lancer `/generer_image` dans Discord

3. Observer immédiatement les logs Render
   - Si rien n'apparaît = problème
   - Si logs défilent = bot fonctionne

---

**Code validé ✅ | Commit 1ed116b prêt ✅ | Action : Redéployer Render**
