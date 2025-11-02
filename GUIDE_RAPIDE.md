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

### 4?? Inviter le bot

1. Allez dans **"OAuth2"** ? **"URL Generator"**
2. Cochez **"bot"** dans Scopes
3. Cochez ces permissions:
   - Read Messages/View Channels
   - Send Messages
   - Send Messages in Threads
   - Read Message History
4. Copiez l'URL et ouvrez-la pour inviter le bot

### 5?? Configuration

```bash
# Copier le fichier de configuration
cp .env.example .env

# ?diter avec votre ?diteur pr?f?r?
nano .env
# ou
notepad .env
```

Ajoutez votre token:
```
DISCORD_TOKEN=votre_token_ici
```

### 6?? D?marrer le bot

```bash
python bot.py
```

? **C'est pr?t!**

## ?? Comment l'utiliser?

### Mentionner le bot
```
@BotIA Salut! Comment ?a va?
```

### R?pondre ? ses messages
Utilisez la fonction "R?pondre" de Discord sur un message du bot

### En priv?
Envoyez-lui un message priv? directement

## ?? Commandes utiles

```
!help_bot          ? Affiche l'aide
!reset             ? Efface l'historique de conversation
!personality ...   ? Change la personnalit? (admin)
!model ...         ? Change le mod?le IA (admin)
```

## ?? Personnalisation rapide

### Changer la personnalit?
```
!personality Tu es un pirate sympathique qui parle comme un vrai pirate des Cara?bes!
```

### Utiliser un mod?le plus rapide
Dans le fichier `.env`:
```
AI_MODEL=google/flan-t5-large
```

## ?? Conseils

- **Token Hugging Face** (optionnel): Cr?ez un compte gratuit sur https://huggingface.co/ pour des r?ponses plus rapides
- **Premi?re utilisation**: Le mod?le peut prendre 20-30 secondes ? se charger la premi?re fois
- **Conversation fluide**: Le bot se souvient des 20 derniers messages de chaque canal

## ?? Probl?mes courants

**Le bot ne r?pond pas?**
- V?rifiez que "Message Content Intent" est activ? dans le portail Discord
- Assurez-vous que le token est correct dans `.env`

**"Model is loading"?**
- C'est normal la premi?re fois, attendez 30 secondes et r?essayez

**Trop lent?**
- Ajoutez un token Hugging Face dans `.env`
- Essayez un mod?le plus petit comme `google/flan-t5-large`

## ?? Vous ?tes pr?t!

Votre bot IA est maintenant op?rationnel! Amusez-vous bien!

Pour plus de d?tails, consultez le **README.md** complet.
