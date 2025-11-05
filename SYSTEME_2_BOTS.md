# ?? Syst?me ? 2 Bots : NSFW + SFW

## ?? Vue d'Ensemble

Vous avez maintenant **2 bots s?par?s** :

### ?? Bot NSFW (`bot.py`)
- **Fonction**: Contenu adulte/explicite
- **O?**: UNIQUEMENT dans les channels Discord marqu?s NSFW
- **Personnalit?s**: 22 personnalit?s adultes (Luna, Catherine, Richard, etc.)
- **Comportement**: Direct, explicite, os?

### ? Bot SFW (`bot_sfw.py`)  
- **Fonction**: Conversations normales
- **O?**: UNIQUEMENT dans les channels Discord normaux (non-NSFW)
- **Personnalit?s**: 6 personnalit?s SFW (Jordan, Alex, Morgan, etc.)
- **Comportement**: Respectueux, fun, tous publics

---

## ?? S?curit? et S?paration

### Bot NSFW - Restrictions:
```python
# V?rifie automatiquement si le channel est NSFW
if not channel.is_nsfw():
    return  # N'activera PAS
```

**Le bot NSFW refuse de d?marrer** si le channel n'est pas marqu? NSFW sur Discord!

### Bot SFW - Restrictions:
```python
# V?rifie automatiquement si le channel est NON-NSFW
if channel.is_nsfw():
    return  # N'activera PAS
```

**Le bot SFW refuse de d?marrer** dans un channel NSFW!

---

## ?? Personnalit?s Disponibles

### Bot NSFW (22 personnalit?s):
**Femmes:**
- Luna (25) - Coquine
- Am?lie (27) - Romantique
- Victoria (30) - Dominatrice
- Sophie (23) - Soumise
- Isabelle (35) - Femme Fatale ??
- Catherine (40) - Cougar ????
- Nathalie (45) - Experte ??????

**Hommes:**
- Damien (28) - S?ducteur
- Alexandre (32) - Dominant
- Julien (26) - Tendre
- Lucas (24) - Soumis
- Marc (35) - Exp?riment? ??
- Philippe (40) - Dominant exp ????
- Richard (45) - Libertin ??????

**Trans/NB:**
- Alex (26) - Trans
- Sam (25) - Non-binaire
- Lexa (35) - Trans exp ??
- Nova (40) - Trans libertine ????
- Ash (35) - NB exp?riment? ??
- River (40) - NB libertin ????

**Neutres:**
- Jordan, Morgan

### Bot SFW (6 personnalit?s):
- **Jordan** - Amical et ouvert
- **Alex** - Gamer passionn?
- **Morgan** - Motivateur positif
- **Sam** - Intellectuel cultiv?
- **Charlie** - Blagueur dr?le
- **Jade** - Zen et calme

---

## ?? D?ploiement sur Render

### Option 1: Un seul service avec le bot NSFW (Actuel)
**Fichier actif**: `bot.py` (NSFW uniquement)
**Fonctionnement**: Automatique dans channels NSFW

### Option 2: Deux services s?par?s (Recommand?)

#### Service 1 - Bot NSFW:
```yaml
# render.yaml
services:
  - type: web
    name: discord-bot-nsfw
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python3 -u bot.py
    envVars:
      - key: DISCORD_TOKEN
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: AI_MODEL
        value: llama-3.3-70b-versatile
```

#### Service 2 - Bot SFW:
```yaml
  - type: web
    name: discord-bot-sfw
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python3 -u bot_sfw.py
    envVars:
      - key: DISCORD_TOKEN_SFW  # TOKEN DIFFERENT !
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: AI_MODEL
        value: llama-3.3-70b-versatile
      - key: PORT_SFW
        value: 10001
```

---

## ?? Configuration Discord

### 1. Cr?er 2 Applications Discord

#### Bot NSFW:
1. **Discord Developer Portal** ? New Application
2. Nom: "Bot NSFW - [VotreServeur]"
3. Bot ? Add Bot
4. **Token**: Copiez pour `DISCORD_TOKEN`
5. Permissions: Same as before
6. Invitez sur votre serveur

#### Bot SFW:
1. **Discord Developer Portal** ? New Application  
2. Nom: "Bot SFW - [VotreServeur]"
3. Bot ? Add Bot
4. **Token**: Copiez pour `DISCORD_TOKEN_SFW`
5. Permissions: Same as before
6. Invitez sur votre serveur

### 2. Marquer vos Channels

#### Channels NSFW:
```
Param?tres du Channel ? Overview ? Age-Restricted Channel (NSFW) ? ? ON
```

**Dans ces channels**, utilisez le **Bot NSFW**:
```
/start
[S?lectionnez Luna, Catherine, Richard, etc.]
```

#### Channels Normaux:
```
Param?tres du Channel ? Age-Restricted Channel (NSFW) ? ? OFF
```

**Dans ces channels**, utilisez le **Bot SFW**:
```
/start
[S?lectionnez Jordan, Alex, Morgan, etc.]
```

---

## ?? Utilisation

### Exemple Serveur Discord:

```
Votre Serveur
??? #general (non-NSFW)
?   ??? Bot SFW actif (Jordan, Alex, etc.)
??? #gaming (non-NSFW)
?   ??? Bot SFW actif (Alex - Gamer)
??? #aide (non-NSFW)
?   ??? Bot SFW actif (Morgan - Motivateur)
?
??? #nsfw-discussions (NSFW ?)
?   ??? Bot NSFW actif (Luna, Catherine, etc.)
??? #nsfw-roleplay (NSFW ?)
?   ??? Bot NSFW actif (Richard, Nathalie, etc.)
??? #nsfw-rencontres (NSFW ?)
    ??? Bot NSFW actif (Toutes personnalit?s NSFW)
```

---

## ?? Variables d'Environnement

### Sur Render (ou local .env):

```env
# Bot NSFW
DISCORD_TOKEN=NzQ5MDU4ODU...  # Token du bot NSFW
GROQ_API_KEY=gsk_...
AI_MODEL=llama-3.3-70b-versatile
PORT=10000

# Bot SFW (si vous d?ployez les 2)
DISCORD_TOKEN_SFW=ODE2NDg0MzY...  # Token DIFFERENT du bot SFW
PORT_SFW=10001
```

---

## ?? Avantages de ce Syst?me

### ? S?curit?:
- S?paration stricte contenu adulte / normal
- Impossible de d?marrer le mauvais bot dans le mauvais type de channel
- Conforme aux r?gles Discord

### ? Flexibilit?:
- Personnalit?s adapt?es au contexte
- Bot NSFW = 22 personnalit?s explicites
- Bot SFW = 6 personnalit?s respectueuses

### ? Clart?:
- Les utilisateurs savent quel bot utiliser o?
- Messages d'erreur clairs si mauvais channel

---

## ?? Commandes

### Bot NSFW (dans channels NSFW uniquement):
```
/start - Active avec 22 personnalit?s adultes
/stop - D?sactive le bot
/personality - Change de personnalit?
/reset - R?initialise l'historique
/status - Statut du bot
```

### Bot SFW (dans channels normaux uniquement):
```
/start - Active avec 6 personnalit?s SFW
/stop - D?sactive le bot
```

---

## ?? Messages d'Erreur

### Si vous essayez le bot NSFW dans un channel normal:
```
? Ce bot est reserv? aux channels NSFW. 
Activez le bot SFW dans les channels normaux.
```

### Si vous essayez le bot SFW dans un channel NSFW:
```
? Ce bot SFW est reserve aux channels normaux. 
Utilisez le bot NSFW dans les channels NSFW.
```

---

## ?? Fichiers Backup

Un backup complet a ?t? cr??:
- `backup_bot_YYYYMMDD_HHMMSS.tar.gz` (archive)
- Git commit avec tag "Backup: Complete backup before NSFW/SFW split"

Pour restaurer:
```bash
tar -xzf backup_bot_YYYYMMDD_HHMMSS.tar.gz
```

---

## ?? Prochaines ?tapes

### Si vous voulez UN SEUL bot (actuel):
? Gardez `bot.py` uniquement (NSFW)
? Il ne fonctionne QUE dans les channels NSFW
? D?j? configur? et d?ploy?

### Si vous voulez DEUX bots s?par?s:
1. Cr?ez une 2?me application Discord
2. Obtenez le 2?me token (`DISCORD_TOKEN_SFW`)
3. D?ployez `bot_sfw.py` sur un 2?me service Render
4. Invitez les 2 bots sur votre serveur
5. Utilisez chacun dans le bon type de channel

---

## ? R?sum?

- ?? **Bot NSFW** = `bot.py` = Channels NSFW seulement
- ? **Bot SFW** = `bot_sfw.py` = Channels normaux seulement
- ?? S?paration automatique et s?curis?e
- ?? Backup complet effectu?
- ?? Pr?t ? d?ployer

**Le bot NSFW actuel ne fonctionne maintenant QUE dans les channels marqu?s NSFW sur Discord!**
