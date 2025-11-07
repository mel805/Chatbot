# 🚀 GUIDE DÉPLOIEMENT RENDER

## ⚠️ PROBLÈME IDENTIFIÉ

Vous utilisez **Render** pour héberger le bot. Les modifications locales ne suffisent pas, il faut :

1. ✅ Pousser vers GitHub (déjà fait)
2. ⚠️ **Redéployer sur Render** (À FAIRE)

---

## 🔄 ÉTAPES POUR REDÉPLOYER SUR RENDER

### Méthode 1 : Déploiement manuel (RECOMMANDÉ)

1. **Aller sur Render Dashboard**
   - https://dashboard.render.com/

2. **Trouver votre service bot**
   - Dans la liste, cliquez sur votre service Discord bot

3. **Forcer un redéploiement**
   - Cliquez sur **"Manual Deploy"** (bouton en haut à droite)
   - Sélectionnez **"Deploy latest commit"**
   - Ou cliquez sur **"Clear build cache & deploy"** si problème

4. **Attendre le déploiement**
   - Render va :
     - Cloner le repo GitHub
     - Installer les dépendances
     - Démarrer le bot
   - Temps : 2-5 minutes

5. **Vérifier les logs**
   - Dans Render, onglet **"Logs"**
   - Vous devriez voir :
     ```
     Logged in as YourBot#1234
     Bot ready!
     ```

---

### Méthode 2 : Auto-déploiement (si configuré)

Si vous avez activé l'auto-déploiement :
- Render détecte automatiquement les nouveaux commits
- Attendre 2-5 minutes après le push

**Vérifier :**
- Dashboard Render → Votre service → "Events"
- Vous devriez voir "Deploy started" récemment

---

## 🔍 VÉRIFIER LES LOGS RENDER

### Comment accéder aux logs :

1. Dashboard Render → Votre service
2. Onglet **"Logs"** (en haut)
3. Regarder les derniers logs

### Logs attendus (SUCCÈS) :

```
==> Cloning from https://github.com/mel805/Chatbot...
==> Running build command: pip install -r requirements.txt
==> Installing dependencies...
==> Starting service with: python bot.py
[INFO] Logged in as YourBot#1234
[INFO] Bot ready!
```

### Logs d'erreur possibles :

#### Erreur 1 : Module manquant
```
ModuleNotFoundError: No module named 'aiohttp'
```
**Solution :** Vérifier `requirements.txt`

#### Erreur 2 : Token invalide
```
discord.errors.LoginFailure: Improper token has been passed.
```
**Solution :** Vérifier variable d'environnement `DISCORD_TOKEN` sur Render

#### Erreur 3 : Import error
```
ImportError: cannot import name 'ImageGenerator'
```
**Solution :** Problème dans le code, vérifier les imports

---

## 🔧 VÉRIFIER LES VARIABLES D'ENVIRONNEMENT RENDER

**CRITIQUE :** Render doit avoir les variables d'environnement configurées !

### Comment vérifier :

1. Dashboard Render → Votre service
2. Onglet **"Environment"**
3. Vérifier que ces variables existent :

```
DISCORD_TOKEN=votre_token_discord
GROQ_API_KEY=votre_cle_groq
STABLE_HORDE_API_KEY=0000000000
```

### Variables optionnelles :

```
REPLICATE_API_KEY=r8_xxx  (pour 100% fiabilité)
HUGGINGFACE_API_KEY=hf_xxx  (optionnel)
```

### Ajouter une variable :

1. Onglet "Environment"
2. Bouton **"Add Environment Variable"**
3. Key: `STABLE_HORDE_API_KEY`
4. Value: `0000000000`
5. **SAVE**
6. **Redéployer le service** (bouton "Manual Deploy")

---

## 🐛 DEBUGGING - Aucun log visible

Si vous ne voyez AUCUN log dans Render :

### Cause 1 : Le service n'a pas redémarré
- Vérifier l'onglet "Events" dans Render
- Dernier déploiement : doit être récent (< 10 min)

### Cause 2 : Le bot crash au démarrage
- Erreur Python avant même le log
- Chercher "Failed" ou "Error" dans les logs

### Cause 3 : Build command incorrect
- Vérifier la configuration Render :
  - **Build Command** : `pip install -r requirements.txt`
  - **Start Command** : `python bot.py`

---

## 📊 APRÈS REDÉPLOIEMENT - TEST

### 1. Vérifier que le bot est en ligne sur Discord

- Le bot doit avoir un statut **vert** (en ligne)

### 2. Tester la génération d'image

```
/generer_image style:explicit_blowjob
```

### 3. Vérifier les logs Render en temps réel

Pendant le test, regardez les logs Render. Vous devriez voir :

```
[IMAGE] Using Stable Horde FREE P2P Network (NSFW allowed)
[IMAGE] Using Stable Horde anonymous API key (limited)
[IMAGE] Submitting to Stable Horde...
[IMAGE] Stable Horde request submitted: <uuid>
```

**Si vous ne voyez RIEN dans les logs Render :**
- Le bot n'est pas redéployé
- Ou le bot utilise l'ancienne version

---

## ❌ SI ÇA NE FONCTIONNE TOUJOURS PAS

### Checklist complète :

- [ ] Commit poussé vers GitHub (✅ Fait)
- [ ] Render a redéployé (vérifier "Events")
- [ ] Variables d'environnement configurées
- [ ] Bot en ligne sur Discord
- [ ] Logs Render montrent le démarrage
- [ ] Test `/generer_image` effectué
- [ ] Logs Render montrent les nouvelles lignes

### Si checklist OK mais échec :

**Copier-coller les logs Render ici !**

Les logs contiennent l'erreur exacte.

---

## 🔄 PROCÉDURE COMPLÈTE RÉSUMÉE

1. ✅ Code modifié (fait)
2. ✅ Commit créé (fait)
3. ✅ Push vers GitHub (fait)
4. ⚠️ **Aller sur Render Dashboard**
5. ⚠️ **Cliquer sur votre service bot**
6. ⚠️ **Manual Deploy → Deploy latest commit**
7. ⏳ **Attendre 2-5 minutes**
8. 👀 **Vérifier les logs Render**
9. ✅ **Tester `/generer_image`**
10. 📋 **Copier les logs si échec**

---

## 💡 ASTUCE : Logs en temps réel

Pour voir les logs en direct pendant le test :

1. Ouvrir Render Dashboard dans un onglet
2. Logs → activer "Auto-scroll" (si disponible)
3. Dans Discord, lancer `/generer_image`
4. Observer les logs Render en temps réel

Vous verrez immédiatement ce qui se passe !

---

## 📞 BESOIN D'AIDE

Si après redéploiement ça ne fonctionne toujours pas :

**Envoyez-moi :**
1. Screenshot des logs Render (dernier déploiement)
2. Screenshot des variables d'environnement Render
3. Message d'erreur Discord exact

Je pourrai diagnostiquer précisément !

---

**Status :** Commit `1ed116b` prêt, redéploiement Render requis
