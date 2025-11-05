# ?? Guide Complet : D?ployer 2 Bots (NSFW + SFW)

## ?? Ce Que Vous Allez Avoir

**2 bots Discord s?par?s** qui tournent en m?me temps :

1. ?? **Bot NSFW** - Pour channels adultes (NSFW)
   - 22 personnalit?s explicites
   - Fonctionne UNIQUEMENT dans les channels NSFW

2. ? **Bot SFW** - Pour channels normaux  
   - 6 personnalit?s respectueuses
   - Fonctionne UNIQUEMENT dans les channels non-NSFW

---

## ?? ?TAPE 1 : Cr?er la 2?me Application Discord (Bot SFW)

### 1.1 Aller sur Discord Developer Portal

?? https://discord.com/developers/applications

### 1.2 Cr?er Nouvelle Application

1. Cliquez **"New Application"** (en haut ? droite)
2. Nom : `Bot SFW - [Nom de votre serveur]`
3. Acceptez les Terms
4. Cliquez **"Create"**

### 1.3 Configurer le Bot

1. Menu gauche ? **"Bot"**
2. Cliquez **"Add Bot"** ? Confirmer **"Yes, do it!"**
3. **Bot Username** : `Bot SFW` (ou votre choix)
4. **Icon** : Uploadez une image (diff?rente du bot NSFW)

### 1.4 R?cup?rer le Token

1. Section **"TOKEN"**
2. Cliquez **"Reset Token"** ? Confirmer
3. Cliquez **"Copy"** pour copier le token
4. **?? GARDEZ CE TOKEN SECRET!**
5. **Notez-le quelque part en s?curit?** (vous en aurez besoin dans 5 minutes)

Format du token : `LONG_STRING_WITH_DOTS.AND_NUMBERS`

### 1.5 Activer les Intents

Scrollez en bas, section **"Privileged Gateway Intents"** :

? **Presence Intent** ? ON
? **Server Members Intent** ? ON  
? **Message Content Intent** ? ON

Cliquez **"Save Changes"**

### 1.6 Configurer OAuth2

1. Menu gauche ? **"OAuth2"** ? **"URL Generator"**
2. **SCOPES** : Cochez
   - ? `bot`
   - ? `applications.commands`

3. **BOT PERMISSIONS** : Cochez
   - ? Read Messages/View Channels
   - ? Send Messages
   - ? Send Messages in Threads
   - ? Embed Links
   - ? Attach Files
   - ? Read Message History
   - ? Add Reactions
   - ? Use Slash Commands
   - ? Change Nickname

4. **Copiez l'URL g?n?r?e** en bas de page

### 1.7 Inviter le Bot SFW sur votre serveur

1. Collez l'URL dans votre navigateur
2. S?lectionnez **votre serveur**
3. Cliquez **"Autoriser"**
4. Le **Bot SFW** appara?t maintenant dans votre serveur (offline pour l'instant)

---

## ?? ?TAPE 2 : D?ployer sur Render

### Option A : Via Dashboard Render (Recommand?)

#### 2.1 Service Bot NSFW (d?j? actif)

Votre service actuel `discord-bot-ia` continue de fonctionner.

**? Rien ? faire pour ce service.**

#### 2.2 Cr?er Service Bot SFW

1. Allez sur **https://dashboard.render.com**
2. Cliquez **"New +"** ? **"Web Service"**
3. Connectez votre **repository GitHub** (m?me que le bot NSFW)
4. Configurez :

**Nom** : `discord-bot-sfw`
**Region** : Frankfurt (ou votre r?gion)
**Branch** : `cursor/cr-er-un-bot-discord-nsfw-immersif-9882` (votre branche actuelle)
**Runtime** : `Python 3`
**Build Command** : `pip install -r requirements.txt`
**Start Command** : `python3 -u bot_sfw.py`
**Plan** : `Free`

5. Cliquez **"Advanced"** pour ajouter les variables d'environnement

#### 2.3 Variables d'Environnement Bot SFW

Ajoutez ces variables (cliquez "Add Environment Variable") :

```
DISCORD_TOKEN_SFW = [Collez le token du Bot SFW que vous avez copi?]
GROQ_API_KEY = [M?me cl? que le bot NSFW]
AI_MODEL = llama-3.3-70b-versatile
PYTHON_VERSION = 3.11.0
PORT_SFW = 10001
```

**?? IMPORTANT** : `DISCORD_TOKEN_SFW` doit contenir le **TOKEN DU BOT SFW** (pas le m?me que le NSFW!)

6. Cliquez **"Create Web Service"**

#### 2.4 Attendre le D?ploiement

Render va :
- Cloner le code ?
- Installer les d?pendances ?
- D?marrer `bot_sfw.py` ?

**Dur?e** : 2-3 minutes

**Logs attendus** :
```
============================================================
BOT SFW READY
Bot user: Bot SFW#1234
Mode: SAFE FOR WORK (channels non-NSFW)
============================================================
[SUCCESS] 2 commands synced
Web server SFW started on port 10001
```

---

### Option B : Via render.yaml (Avanc?)

Si vous voulez tout g?rer via fichier :

1. **Remplacez** `render.yaml` par `render_dual_bots.yaml` :
```bash
mv render.yaml render.yaml.backup
mv render_dual_bots.yaml render.yaml
git add render.yaml
git commit -m "Deploy: Dual bots configuration"
git push
```

2. Render d?tectera automatiquement les 2 services
3. Ajoutez les variables d'environnement manuellement dans le Dashboard

---

## ?? ?TAPE 3 : Configuration des Channels Discord

### 3.1 Marquer les Channels NSFW

Pour les channels adultes (o? le **Bot NSFW** fonctionnera) :

1. Clic droit sur le channel
2. **Param?tres du channel**
3. **Overview**  
4. **Age-Restricted Channel (NSFW)** ? ? **ON**
5. **Enregistrer les modifications**

**R?p?tez pour tous vos channels adultes.**

### 3.2 Channels Normaux (d?j? configur?s)

Les channels normaux n'ont RIEN ? configurer.
Le **Bot SFW** y fonctionnera automatiquement.

---

## ?? ?TAPE 4 : Test des 2 Bots

### Test Bot NSFW (dans un channel NSFW ?)

```
/start
```

**R?sultat attendu** :
```
? Menu avec 22 personnalit?s :
- Luna, Catherine, Nathalie (femmes)
- Damien, Philippe, Richard (hommes)
- etc.
```

**Si dans un channel normal** :
```
? Ce bot est reserve aux channels NSFW
```

---

### Test Bot SFW (dans un channel normal)

```
/start
```

**R?sultat attendu** :
```
? Menu avec 6 personnalit?s SFW :
- Jordan (Amical)
- Alex (Gamer)
- Morgan (Motivateur)
- Sam (Intellectuel)
- Charlie (Blagueur)
- Jade (Zen)
```

**Si dans un channel NSFW** :
```
? Ce bot SFW est reserve aux channels normaux
```

---

## ?? ?TAPE 5 : Utilisation Quotidienne

### Exemple de Configuration Serveur

```
Votre Serveur Discord
?
??? ?? #annonces (normal)
?   ??? Bot SFW : Jordan (Amical)
?
??? ?? #gaming (normal)
?   ??? Bot SFW : Alex (Gamer)
?
??? ?? #general (normal)
?   ??? Bot SFW : Morgan (Motivateur)
?
??? ?? #nsfw-discussion (NSFW ?)
?   ??? Bot NSFW : Luna (Coquine)
?
??? ?? #nsfw-roleplay (NSFW ?)
?   ??? Bot NSFW : Catherine (Cougar)
?
??? ?? #nsfw-rencontres (NSFW ?)
    ??? Bot NSFW : Richard (Libertin)
```

### Dans les Channels Normaux :
```
User: /start
[Menu SFW appara?t]
User: [S?lectionne "Alex - Gamer"]

Alex: yo ??

User: t'as vu le dernier match?
Alex: ouais c'etait incroyable, t'as vu ce clutch?

User2: j'etais l? aussi
Alex: trop styl? ce match franchement
```

### Dans les Channels NSFW :
```
User: /start  
[Menu NSFW appara?t avec 22 personnalit?s]
User: [S?lectionne "Catherine 40ans - Cougar"]

Catherine: hey ??

User: @Catherine t'es libre?
Catherine: toujours pour toi ??

[Conversation explicite continue...]
```

---

## ? Checklist Finale

### Bot NSFW :
- ? Service Render actif
- ? `DISCORD_TOKEN` configur?
- ? Invit? sur le serveur
- ? Channels NSFW marqu?s ?
- ? Teste avec `/start` dans channel NSFW

### Bot SFW :
- ? 2?me application Discord cr??e
- ? Token `DISCORD_TOKEN_SFW` copi?
- ? Service Render cr??
- ? Variables d'environnement configur?es
- ? Invit? sur le serveur
- ? Teste avec `/start` dans channel normal

---

## ?? V?rifications Render Dashboard

### Service 1 : discord-bot-nsfw
```
Status: ? Live
Logs: "BOT READY - Version avec logs debug complets"
Environment: DISCORD_TOKEN, GROQ_API_KEY, AI_MODEL
```

### Service 2 : discord-bot-sfw
```
Status: ? Live  
Logs: "BOT SFW READY"
Environment: DISCORD_TOKEN_SFW, GROQ_API_KEY, AI_MODEL
```

---

## ?? Co?ts

**Plan Free Render** :
- ? 2 services gratuits possibles
- ? 750h/mois par service
- ? Largement suffisant pour 2 bots Discord

**Co?t total** : **0?** ??

---

## ?? D?pannage

### Bot SFW ne d?marre pas

**V?rifiez** :
1. `DISCORD_TOKEN_SFW` est bien d?fini (pas le m?me que DISCORD_TOKEN!)
2. Le token est correct (copiez-le ? nouveau)
3. Le bot est invit? sur le serveur
4. Start Command est bien `python3 -u bot_sfw.py`

### Bot refuse de d?marrer dans un channel

**C'est NORMAL** :
- Bot NSFW refuse les channels normaux ? OK ?
- Bot SFW refuse les channels NSFW ? OK ?

C'est la protection voulue!

### Les 2 bots ont le m?me nom

**Solution** :
1. Changez le **nickname** de l'un des deux
2. Ou changez le **username** dans Discord Developer Portal

---

## ?? R?sum? en 5 ?tapes

1. ? **Cr?er 2?me app Discord** ? Copier token SFW
2. ? **Cr?er 2?me service Render** ? Nommer "discord-bot-sfw"
3. ? **Configurer variables** ? `DISCORD_TOKEN_SFW` + autres
4. ? **Marquer channels NSFW** ? Sur Discord
5. ? **Tester les 2 bots** ? `/start` dans chaque type de channel

---

## ?? F?licitations !

Vous avez maintenant **2 bots fonctionnels** :

?? **Bot NSFW** ? 22 personnalit?s explicites ? Channels NSFW uniquement
? **Bot SFW** ? 6 personnalit?s respectueuses ? Channels normaux uniquement

**S?curit? maximale + Flexibilit? totale!** ???
