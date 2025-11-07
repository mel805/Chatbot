# 🔄 REDÉMARRAGE DU BOT - OBLIGATOIRE

## ⚠️ IMPORTANT

Les modifications ont été faites dans le code, mais le bot utilise **l'ancienne version en mémoire**.

**Vous DEVEZ redémarrer le bot pour appliquer les changements !**

---

## 🔄 MÉTHODE 1 : Redémarrage simple (RECOMMANDÉ)

### Si le bot tourne en arrière-plan :

1. **Trouver le processus :**
   ```bash
   ps aux | grep bot.py
   ```

2. **Arrêter le bot :**
   ```bash
   kill <PID_du_processus>
   ```
   Ou utiliser `Ctrl+C` si dans le terminal

3. **Redémarrer le bot :**
   ```bash
   cd /workspace
   python3 bot.py
   ```

---

## 🔄 MÉTHODE 2 : Avec screen/tmux

### Si vous utilisez screen :

```bash
screen -r bot    # Se reconnecter à la session
Ctrl+C           # Arrêter le bot
python3 bot.py   # Redémarrer
Ctrl+A puis D    # Détacher
```

### Si vous utilisez tmux :

```bash
tmux attach -t bot    # Se reconnecter
Ctrl+C                # Arrêter
python3 bot.py        # Redémarrer
Ctrl+B puis D         # Détacher
```

---

## 🔄 MÉTHODE 3 : Systemd (si configuré)

```bash
sudo systemctl restart discord-bot
```

---

## ✅ VÉRIFICATION APRÈS REDÉMARRAGE

Une fois le bot redémarré, testez immédiatement :

```
/generer_image style:explicit_blowjob
```

**Vous DEVEZ voir dans les logs :**

```
[IMAGE] Using Stable Horde FREE P2P Network (NSFW allowed)
[IMAGE] models: ["Deliberate", "Realistic Vision V5.1", "DreamShaper"]
```

**Si Stable Horde échoue, vous verrez :**

```
[IMAGE] Stable Horde failed, trying Hugging Face (FREE, NSFW allowed)...
[IMAGE] Using Hugging Face Inference API (FREE, NSFW allowed)
```

---

## ❌ SI VOUS VOYEZ TOUJOURS L'ANCIENNE ERREUR

Si vous voyez encore :
```
Pollinations.ai peut être temporairement indisponible
```

**C'est que le bot n'a PAS été redémarré !**

Vérifiez que :
1. L'ancien processus est bien arrêté
2. Vous avez lancé le nouveau bot depuis `/workspace`
3. Le bot charge bien les fichiers modifiés

---

## 🔍 DIAGNOSTIC

Pour vérifier que les modifications sont chargées :

```bash
# Vérifier la date de modification des fichiers
ls -lh /workspace/image_generator.py
ls -lh /workspace/bot.py

# Vérifier le contenu (devrait montrer les nouveaux modèles)
grep -A 3 "models.*\[" /workspace/image_generator.py
```

Vous devriez voir :
```python
"models": [
    "Deliberate",
    "Realistic Vision V5.1",
    "DreamShaper"
]
```

---

## 📝 RÉSUMÉ

1. ✅ **Modifications faites** dans le code
2. ⚠️ **Bot non redémarré** → utilise ancienne version
3. 🔄 **REDÉMARRER LE BOT** pour appliquer
4. ✅ **Tester** avec `/generer_image`
5. 👀 **Vérifier logs** pour nouveaux services

---

**BRANCHE :** `cursor/debug-image-generation-for-conversational-accuracy-30a6`  
**FICHIERS MODIFIÉS :** `image_generator.py` (791 lignes), `bot.py` (1509 lignes)  
**STATUS :** ✅ Code modifié, ⚠️ Redémarrage requis
