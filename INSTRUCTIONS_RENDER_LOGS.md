# ?? COMMENT VOIR LES LOGS SUR RENDER

## ?? INSTRUCTIONS CRITIQUES

Si vous ne voyez AUCUN log, suivez ces ?tapes **EXACTEMENT**:

---

## ?? ?tape 1: V?rifier le Statut du Service

1. Allez sur **https://dashboard.render.com**
2. Cliquez sur votre service **"discord-bot-ia"**
3. V?rifiez le statut en haut:
   - ? **? Live** (vert) = Service actif
   - ?? **? Building** (orange) = En cours de d?ploiement (attendez!)
   - ? **? Failed** (rouge) = ?chec (lisez les logs de build)

---

## ?? ?tape 2: Acc?der aux Logs

### Sur la page du service:

1. **Dans le menu de gauche**, cliquez sur **"Logs"**
   - PAS "Events"
   - PAS "Settings"
   - PAS "Environment"
   - **"Logs"** uniquement!

2. **En haut ? droite**, assurez-vous que:
   - **"Live tail"** est ACTIV? (bouton vert)
   - **"All logs"** est s?lectionn? (pas seulement "Errors")

---

## ?? ?tape 3: Attendre le Red?ploiement

Apr?s chaque `git push`, Render red?ploie automatiquement:

### Dur?e du red?ploiement:
```
Build: ~1-2 minutes
Start: ~30 secondes
Total: ~2-3 minutes
```

### Pendant le build, vous verrez:
```
==> Building...
==> Downloading Python
==> Installing dependencies from requirements.txt
==> Successfully installed discord.py-2.3.2 aiohttp-3.9.1 ...
==> Build successful
```

### Puis au d?marrage:
```
==> Starting service with 'python3 -u bot.py'
======================================================================
DEBUT DU SCRIPT bot.py
Python version: 3.11.x
======================================================================
DISCORD_TOKEN present: True
GROQ_API_KEY present: True
AI_MODEL: llama-3.1-70b-versatile
Demarrage du bot Discord IA avec Groq...
```

**Si vous ne voyez PAS ces logs, continuez...**

---

## ?? ?tape 4: V?rifier les Variables d'Environnement

1. Dans le menu de gauche, cliquez sur **"Environment"**
2. V?rifiez que ces variables existent:

```
DISCORD_TOKEN = [valeur cach?e] ?
GROQ_API_KEY = [valeur cach?e] ?
AI_MODEL = llama-3.1-70b-versatile ?
```

### Si DISCORD_TOKEN ou GROQ_API_KEY manquent:

1. Cliquez **"Add Environment Variable"**
2. Ajoutez:
   - **Key**: `DISCORD_TOKEN`
   - **Value**: Votre token Discord
3. Cliquez **"Save Changes"**
4. **Le service va red?marrer automatiquement**

---

## ?? ?tape 5: Forcer un Red?ploiement Manuel

Si aucun log n'appara?t apr?s 3 minutes:

1. En haut ? droite, cliquez **"Manual Deploy"**
2. S?lectionnez **"Clear build cache & deploy"**
3. Cliquez **"Deploy"**
4. **Attendez 2-3 minutes**
5. Rafra?chissez la page des logs

---

## ?? Logs Attendus au D?marrage

### Logs Normaux (succ?s):
```
======================================================================
DEBUT DU SCRIPT bot.py
Python version: 3.11.x
======================================================================
DISCORD_TOKEN present: True
GROQ_API_KEY present: True
AI_MODEL: llama-3.1-70b-versatile
Demarrage du bot Discord IA avec Groq...
Modele: llama-3.1-70b-versatile
======================================================================
============================================================
BOT READY - Version avec logs debug complets
Bot user: YourBotName#1234
Guilds: 1
AI_MODEL: llama-3.1-70b-versatile
GROQ_API_KEY defined: True
GROQ_API_KEY length: 107
Personalities: 8
============================================================
[SUCCESS] X slash commands synced
Serveur web demarre sur le port 10000
Health check disponible sur /health
```

### Logs d'Erreur (probl?me):
```
ERREUR CRITIQUE: DISCORD_TOKEN non trouve!
Sur Render: Verifiez Environment Variables dans Dashboard
```

**Si vous voyez cette erreur ? Allez ? l'?tape 4**

---

## ?? Logs Attendus Quand Vous Utilisez le Bot

### Apr?s `/start`:
```
[MESSAGE] From VotreNom in channel 123456789
[MESSAGE] Content: /start
```

### Apr?s avoir mentionn? le bot (`@BotName salut`):
```
[MESSAGE] From VotreNom in channel 123456789
[MESSAGE] Content: @BotName salut
[INFO] Checking if bot active in channel 123456789
[INFO] bot_active_channels: {123456789: True}
[INFO] Bot IS active in channel 123456789
[INFO] bot_mentioned=True, is_dm=False, is_reply_to_bot=False
[INFO] Bot WILL respond to this message
[INFO] Using personality: coquin
[INFO] Calling ai_client.generate_response...
[DEBUG] generate_response - Personality: coquin
[DEBUG] Messages count: 1
[DEBUG] AI_MODEL: llama-3.1-70b-versatile
[DEBUG] Calling Groq API...
[DEBUG] Groq response status: 200
[DEBUG] Response received
[DEBUG] Content length: 150
[INFO] Response received: Hey... *te regarde avec un sourire en coin* ...
```

---

## ? Probl?mes Courants

### Probl?me 1: "No logs available"
**Cause**: Le service n'a pas encore d?marr?
**Solution**: Attendez 2-3 minutes apr?s le build

### Probl?me 2: Logs fig?s (ne bougent plus)
**Cause**: Live tail d?sactiv?
**Solution**: Cliquez sur "Live tail" pour le r?activer

### Probl?me 3: Seulement les logs de build, pas de logs d'ex?cution
**Cause**: Le bot crash au d?marrage silencieusement
**Solution**: 
1. V?rifiez Environment Variables (DISCORD_TOKEN, GROQ_API_KEY)
2. Regardez s'il y a une erreur juste apr?s "Starting service..."

### Probl?me 4: "Port scan timeout"
**Cause**: Normal pour un bot Discord, mais on a ajout? un serveur web
**Solution**: Ignorez ce message s'il appara?t, le bot devrait quand m?me fonctionner

---

## ?? Checklist de V?rification

Avant de dire "pas de logs", v?rifiez:

- [ ] Je suis bien sur la page **"Logs"** (pas Events/Settings)
- [ ] Le service est **? Live** (vert), pas Building
- [ ] **"Live tail"** est activ? (bouton vert)
- [ ] J'ai attendu **au moins 3 minutes** apr?s le dernier push
- [ ] Les variables **DISCORD_TOKEN** et **GROQ_API_KEY** sont d?finies
- [ ] J'ai rafra?chi la page des logs (F5)

---

## ?? Si Vraiment Aucun Log

Si apr?s TOUT ?a vous ne voyez toujours rien:

1. **Capturez une screenshot** de:
   - La page "Logs" compl?te
   - La page "Environment" montrant les variables
   - Le statut du service (? Live/Building/Failed)

2. **V?rifiez le dernier commit sur GitHub**:
   - Le commit est-il bien pouss??
   - Render a-t-il d?tect? le push?

3. **Essayez de vous connecter via SSH** (si disponible):
   ```bash
   render shell [votre-service]
   python3 -u bot.py
   ```

---

## ? Ce Qu'on Doit Voir Absolument

**MINIMUM**: Ces 3 lignes DOIVENT appara?tre:
```
DEBUT DU SCRIPT bot.py
DISCORD_TOKEN present: True
GROQ_API_KEY present: True
```

**Si vous ne voyez m?me pas ?a**, le probl?me est:
- Render n'ex?cute pas `python3 -u bot.py`
- Les variables d'environnement ne sont pas charg?es
- Le build a ?chou?

**Solution**: Manual Deploy + Clear cache

---

## ?? Informations ? Me Donner

Si vous avez besoin d'aide, donnez-moi:

1. **Screenshot de la page Logs**
2. **Screenshot de la page Environment** (masquez les valeurs sensibles!)
3. **Statut du service** (Live/Building/Failed)
4. **Derni?re ligne visible** dans les logs
5. **Depuis combien de temps** le service est "Live"

Sans ces infos, je ne peux pas diagnostiquer!

---

? **Avec `python3 -u` et `flush=True`, les logs DOIVENT s'afficher en temps r?el!**
