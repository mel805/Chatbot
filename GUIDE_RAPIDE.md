# ?? Guide de D?marrage Rapide

## Installation en 5 minutes

### 1?? Installer Python
Assurez-vous d'avoir Python 3.8+ install?:
```bash
python --version
```

### 2?? Installer les d?pendances
```bash
pip install -r requirements.txt
```

### 3?? Cr?er votre bot Discord

1. Allez sur https://discord.com/developers/applications
2. Cliquez **"New Application"**
3. Donnez un nom ? votre bot
4. Allez dans **"Bot"** ? **"Add Bot"**
5. **IMPORTANT**: Activez "Message Content Intent" et "Server Members Intent"
6. Copiez le **Token**

### 4?? Obtenir une cl? API Groq (GRATUIT!)

1. Allez sur https://console.groq.com
2. Cr?ez un compte gratuit
3. Allez dans **"API Keys"**
4. Cliquez **"Create API Key"**
5. Copiez la cl?

### 5?? Inviter le bot

1. Allez dans **"OAuth2"** ? **"URL Generator"**
2. Cochez **"bot"** dans Scopes
3. Cochez ces permissions:
   - Read Messages/View Channels
   - Send Messages
   - Send Messages in Threads
   - Read Message History
   - Embed Links
4. Copiez l'URL et ouvrez-la pour inviter le bot

### 6?? Configuration

```bash
# Copier le fichier de configuration
cp .env.example .env

# ?diter avec votre ?diteur pr?f?r?
nano .env
# ou
notepad .env
```

Ajoutez vos cl?s:
```env
DISCORD_TOKEN=votre_token_discord_ici
GROQ_API_KEY=votre_cle_groq_ici
AI_MODEL=llama-3.1-70b-versatile
```

### 7?? D?marrer le bot

```bash
python bot.py
```

? **C'est pr?t!**

---

## ?? Comment l'utiliser?

### ?? Important: Activer le bot d'abord!

Le bot ne r?pond PAS automatiquement. Un **admin** doit l'activer:

```
/start
```

### Ensuite, interagissez:

**Mentionner le bot**
```
@BotIA Salut! Comment ?a va?
```

**R?pondre ? ses messages**
Utilisez la fonction "R?pondre" de Discord sur un message du bot

**En priv?**
Envoyez-lui un message priv? directement

---

## ?? Personnalit?s

Le bot a **8 personnalit?s** diff?rentes:

| Code | Description |
|------|-------------|
| `amical` | Sympathique et cool (d?faut) |
| `seducteur` | Charmant et flirteur ?? |
| `coquin` | Os? et provocateur ?? |
| `romantique` | Doux et passionn? ?? |
| `dominant` | Confiant et autoritaire ?? |
| `soumis` | Respectueux et d?vou? ?? |
| `joueur` | Fun et gamer ?? |
| `intellectuel` | Cultiv? et profond ?? |

### Changer de personnalit? (admin)

```
/personality coquin
```

---

## ?? Commandes Admin

```
/start                    ? Active le bot dans ce canal
/stop                     ? D?sactive le bot
/personality              ? Liste les personnalit?s
/personality <nom>        ? Change de personnalit?
/reset                    ? R?initialise l'historique
/status                   ? Affiche le statut
/help                 ? Aide compl?te
```

---

## ?? H?bergement 24/7

Pour garder le bot en ligne 24/7, vous avez plusieurs options:

### Option 1: VPS Oracle (GRATUIT!) ??

Oracle offre un VPS **gratuit ? vie**!

1. Cr?ez un compte sur https://www.oracle.com/cloud/free/
2. Cr?ez une instance Ubuntu
3. Suivez le guide complet: **[HEBERGEMENT_24_7.md](HEBERGEMENT_24_7.md)**

### Option 2: Raspberry Pi

~60? une fois, consommation ?lectrique ~3?/an

### Option 3: VPS payant

Contabo: 5?/mois, DigitalOcean: 5$/mois

?? **Guide complet dans [HEBERGEMENT_24_7.md](HEBERGEMENT_24_7.md)**

---

## ?? Conseils

### Pourquoi Groq?

- ? **Ultra rapide**: R?ponses en ~1 seconde (vs 5-15s)
- ?? **100% Gratuit**: API g?n?reuse
- ?? **Puissant**: Llama 3.1, Mixtral, Gemma
- ?? **Moins censur?**: Meilleur pour conversations adultes

### Mod?les recommand?s

- `llama-3.1-70b-versatile` (d?faut) - Meilleur ?quilibre
- `mixtral-8x7b-32768` - Excellent, contexte ?tendu
- `llama-3.1-8b-instant` - Ultra rapide

Changez dans `.env`:
```env
AI_MODEL=mixtral-8x7b-32768
```

---

## ?? Probl?mes courants

**Le bot ne r?pond pas?**
1. Avez-vous fait `/start`? (admin uniquement)
2. V?rifiez que "Message Content Intent" est activ?
3. Mentionnez le bot ou r?pondez ? ses messages

**"GROQ_API_KEY non trouv?"?**
- Cr?ez un compte sur https://console.groq.com
- Obtenez une cl? API gratuite
- Ajoutez-la dans le fichier `.env`

**"DISCORD_TOKEN invalide"?**
- V?rifiez que vous avez copi? le bon token
- Le token commence g?n?ralement par `MTk...`

**Le bot parle ? tout le monde?**
- Normal! Une fois activ?, il r?pond quand on le mentionne
- Utilisez `/stop` pour le d?sactiver dans un canal

---

## ?? Documentation compl?te

Pour plus de d?tails:

- **README.md** - Documentation compl?te
- **HEBERGEMENT_24_7.md** - Guide h?bergement 24/7
- **config.json** - Configurations suppl?mentaires

---

## ?? Exemple rapide

```
Admin: /start
Bot: ? Bot Activ? avec la personnalit? Amical ??

User: @Bot Hey!
Bot: Salut! Ravi de pouvoir discuter avec vous! ??

Admin: /personality seducteur
Bot: ? Personnalit? chang?e! Nouvelle personnalit?: S?ducteur ??

User: @Bot Toujours l??
Bot: Bien s?r... *te regarde avec un sourire charmeur* Comment pourrais-je partir alors que la conversation devient int?ressante? ??

Admin: /stop
Bot: ?? Bot d?sactiv? dans ce canal.
```

---

## ?? S?curit?

- ? Ne partagez jamais vos tokens
- ? Utilisez uniquement sur des serveurs priv?s
- ? Le bot ne sauvegarde aucune conversation
- ? Tout est stock? en RAM (effac? au red?marrage)

---

## ? Avantages de cette version

? **Groq** au lieu de Hugging Face (10x plus rapide)
? **8 personnalit?s** pr?d?finies
? **Contr?le admin** pour activation/d?sactivation
? **24/7 ready** avec guide complet
? **100% Gratuit** pour toujours
? **Conversations immersives** et r?alistes

---

## ?? Vous ?tes pr?t!

Votre bot IA est maintenant op?rationnel! Amusez-vous bien!

**Besoin d'aide?** Consultez le **README.md** complet!
