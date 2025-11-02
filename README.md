# ?? Bot Discord IA Conversationnel

Un bot Discord intelligent et conversationnel aliment? par l'IA, capable de participer naturellement aux discussions comme un vrai membre du serveur.

## ? Fonctionnalit?s

- ?? **Conversations naturelles** : Le bot r?pond de mani?re contextuelle et humaine
- ?? **M?moire contextuelle** : Se souvient des messages pr?c?dents dans chaque canal
- ?? **Multi-utilisateurs** : Peut interagir avec plusieurs personnes simultan?ment
- ?? **100% Gratuit** : Utilise des mod?les d'IA gratuits via Hugging Face
- ?? **Personnalisable** : Changez la personnalit? et le mod?le d'IA ? tout moment
- ?? **Priv?** : Fonctionne sur votre machine, pas de donn?es envoy?es ailleurs qu'? l'API d'IA

## ?? Pr?requis

- Python 3.8 ou sup?rieur
- Un compte Discord et un bot cr?? sur le [Portail D?veloppeur Discord](https://discord.com/developers/applications)
- (Optionnel) Un compte [Hugging Face](https://huggingface.co/) pour un token API gratuit

## ?? Installation

### 1. Cloner ou t?l?charger ce projet

```bash
git clone <votre-repo>
cd <dossier-du-projet>
```

### 2. Installer les d?pendances

```bash
pip install -r requirements.txt
```

Ou avec un environnement virtuel (recommand?):

```bash
# Cr?er l'environnement virtuel
python -m venv venv

# L'activer
# Sur Windows:
venv\Scripts\activate
# Sur Linux/Mac:
source venv/bin/activate

# Installer les d?pendances
pip install -r requirements.txt
```

### 3. Cr?er votre Bot Discord

1. Allez sur https://discord.com/developers/applications
2. Cliquez sur "New Application"
3. Donnez un nom ? votre application
4. Allez dans l'onglet "Bot"
5. Cliquez sur "Add Bot"
6. **Important** : Activez ces intents dans l'onglet Bot:
   - ? Message Content Intent
   - ? Server Members Intent
   - ? Presence Intent (optionnel)
7. Copiez le Token (vous en aurez besoin plus tard)

### 4. Inviter le bot sur votre serveur

1. Allez dans l'onglet "OAuth2" > "URL Generator"
2. S?lectionnez:
   - **Scopes**: `bot`
   - **Bot Permissions**: 
     - Read Messages/View Channels
     - Send Messages
     - Send Messages in Threads
     - Embed Links
     - Attach Files
     - Read Message History
     - Add Reactions
3. Copiez l'URL g?n?r?e et ouvrez-la dans votre navigateur
4. S?lectionnez votre serveur et autorisez le bot

### 5. Configuration

1. Copiez le fichier `.env.example` en `.env`:
```bash
cp .env.example .env
```

2. ?ditez le fichier `.env` et ajoutez votre token Discord:
```env
DISCORD_TOKEN=votre_token_discord_ici
```

3. (Optionnel) Ajoutez un token Hugging Face pour de meilleures performances:
   - Cr?ez un compte gratuit sur https://huggingface.co/
   - Allez sur https://huggingface.co/settings/tokens
   - Cr?ez un nouveau token (Read)
   - Ajoutez-le dans `.env`:
```env
HUGGINGFACE_TOKEN=votre_token_huggingface_ici
```

## ?? Utilisation

### D?marrer le bot

```bash
python bot.py
```

Vous devriez voir:
```
?? D?marrage du bot Discord IA...
?? Mod?le IA: mistralai/Mistral-7B-Instruct-v0.2
BotName est connect? et pr?t!
```

### Interagir avec le bot

Il y a plusieurs fa?ons d'interagir avec le bot:

1. **Mentionner le bot** : `@BotName Bonjour, comment vas-tu?`
2. **R?pondre ? un message du bot** : Utilisez la fonction "R?pondre" de Discord
3. **Message priv?** : Envoyez un DM au bot

### Commandes disponibles

- `!help_bot` - Affiche l'aide et les commandes disponibles
- `!reset` - R?initialise l'historique de conversation du canal
- `!personality [texte]` - Change la personnalit? du bot (admin uniquement)
- `!model [nom]` - Change le mod?le d'IA (admin uniquement)

### Exemples d'utilisation

```
Utilisateur: @BotIA Salut! Comment tu t'appelles?
Bot: Salut! Je suis le bot IA du serveur! Ravi de te rencontrer ??

Utilisateur: @BotIA Qu'est-ce que tu penses du temps aujourd'hui?
Bot: Je ne peux pas voir par la fen?tre, mais j'esp?re qu'il fait beau chez toi! Tu fais quelque chose de sp?cial aujourd'hui?
```

## ?? Configuration avanc?e

### Changer la personnalit? du bot

Utilisez la commande `!personality` (admin uniquement):

```
!personality Tu es un pirate sympathique qui parle toujours comme un vrai pirate. Tu es dr?le et utilises des expressions de pirate.
```

### Changer le mod?le d'IA

Mod?les gratuits recommand?s:

- `mistralai/Mistral-7B-Instruct-v0.2` (Par d?faut - Bon ?quilibre)
- `meta-llama/Llama-2-7b-chat-hf` (Bonne qualit? g?n?rale)
- `HuggingFaceH4/zephyr-7b-beta` (Tr?s conversationnel)
- `tiiuae/falcon-7b-instruct` (Rapide)
- `google/flan-t5-large` (L?ger et rapide)

Changez le mod?le avec:
```
!model mistralai/Mistral-7B-Instruct-v0.2
```

Ou modifiez directement dans le fichier `.env`:
```env
AI_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

### Personnalisation dans le code

?ditez `bot.py` pour modifier:

- `SYSTEM_PROMPT` : La personnalit? de base du bot
- `MAX_HISTORY` : Nombre de messages gard?s en m?moire (d?faut: 20)
- `RATE_LIMIT_SECONDS` : D?lai minimum entre r?ponses (d?faut: 2s)
- `max_new_tokens` : Longueur maximale des r?ponses (d?faut: 500)
- `temperature` : Cr?ativit? des r?ponses (0.0 = pr?visible, 1.0 = cr?atif)

## ?? D?pannage

### Le bot ne r?pond pas

1. V?rifiez que les Message Content Intents sont activ?s dans le portail d?veloppeur
2. Assurez-vous que le bot a les permissions de lire et envoyer des messages
3. V?rifiez que le token Discord est correct dans le fichier `.env`

### Erreur "Model is loading"

Les mod?les Hugging Face gratuits peuvent prendre 20-30 secondes ? se charger la premi?re fois. R?essayez apr?s quelques secondes.

### R?ponses lentes

- Ajoutez un token Hugging Face dans `.env` pour acc?l?rer les requ?tes
- Essayez un mod?le plus petit comme `google/flan-t5-large`
- Les mod?les gratuits peuvent avoir des temps de r?ponse variables selon la charge

### Le bot utilise trop de RAM

- R?duisez `MAX_HISTORY` dans le code (ligne ~26)
- Utilisez la commande `!reset` r?guli?rement pour vider l'historique

## ?? Notes importantes

- **Respectez les conditions d'utilisation** de Discord et Hugging Face
- Le bot est pr?vu pour des serveurs priv?s. Pour un bot public, ajoutez plus de mod?ration
- Les mod?les IA gratuits peuvent avoir des limitations de d?bit
- Ne partagez jamais votre token Discord publiquement
- Ce bot utilise l'API d'inf?rence gratuite de Hugging Face

## ?? Am?liorations futures possibles

- [ ] Support de plusieurs langues
- [ ] Commandes de mod?ration automatique
- [ ] Syst?me de niveaux et XP
- [ ] Int?gration avec d'autres services (m?t?o, news, etc.)
- [ ] Support d'images avec des mod?les multimodaux
- [ ] Base de donn?es pour persistance de l'historique
- [ ] Interface web de configuration

## ?? Licence

Ce projet est fourni "tel quel" pour un usage personnel et ?ducatif.

## ?? Contribution

Les contributions, suggestions et rapports de bugs sont les bienvenus!

## ?? Avertissement

- Utilisez ce bot de mani?re responsable
- Le cr?ateur n'est pas responsable de l'utilisation faite de ce bot
- Assurez-vous de respecter les lois locales et les conditions d'utilisation des plateformes
- Le bot n'a pas de filtres de contenu int?gr?s par d?faut

---

**Bon bot! ??**

Pour toute question ou probl?me, n'h?sitez pas ? cr?er une issue sur le d?p?t GitHub.
