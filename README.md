# ?? Bot Discord IA Conversationnel - Version Groq

Un bot Discord intelligent et conversationnel avec **8 personnalit?s diff?rentes**, aliment? par l'IA Groq ultra-rapide et 100% gratuite. Parfait pour des serveurs adultes avec des conversations immersives et r?alistes.

## ? Fonctionnalit?s

- ?? **8 Personnalit?s Pr?d?finies** : Amical, S?ducteur, Coquin, Romantique, Dominant, Soumis, Joueur, Intellectuel
- ?? **Conversations naturelles et immersives** : Le bot discute comme un vrai membre du serveur
- ?? **M?moire contextuelle** : Se souvient des 20 derniers messages par canal
- ?? **Multi-utilisateurs** : Peut g?rer plusieurs conversations simultan?ment
- ?? **Contr?le Admin** : Seuls les administrateurs peuvent activer/d?sactiver et configurer le bot
- ? **Ultra-rapide** : Utilise Groq, l'API d'IA la plus rapide (r?ponses en ~1 seconde)
- ?? **100% Gratuit** : Groq offre une API gratuite et g?n?reuse
- ?? **24/7 Ready** : Peut tourner en continu sur un VPS ou Raspberry Pi

## ?? Pr?requis

- Python 3.8 ou sup?rieur
- Un compte Discord et un bot cr?? sur le [Portail D?veloppeur Discord](https://discord.com/developers/applications)
- Un compte Groq gratuit pour obtenir une cl? API : [console.groq.com](https://console.groq.com)

## ?? Installation Rapide

### 1. Installer les d?pendances

```bash
pip install -r requirements.txt
```

Ou avec un environnement virtuel (recommand?):

```bash
python -m venv venv

# Activer l'environnement
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installer les d?pendances
pip install -r requirements.txt
```

### 2. Cr?er votre Bot Discord

1. Allez sur https://discord.com/developers/applications
2. Cliquez sur **"New Application"**
3. Donnez un nom ? votre bot
4. Allez dans **"Bot"** ? **"Add Bot"**
5. **IMPORTANT**: Activez ces intents:
   - ? Message Content Intent
   - ? Server Members Intent
6. Copiez le **Token**

### 3. Inviter le bot sur votre serveur

1. Allez dans **"OAuth2"** ? **"URL Generator"**
2. S?lectionnez:
   - **Scopes**: `bot`
   - **Bot Permissions**: 
     - Read Messages/View Channels
     - Send Messages
     - Send Messages in Threads
     - Read Message History
     - Embed Links
3. Copiez l'URL g?n?r?e et ouvrez-la pour inviter le bot

### 4. Obtenir une cl? API Groq (GRATUIT)

1. Allez sur https://console.groq.com
2. Cr?ez un compte gratuit
3. Allez dans **"API Keys"**
4. Cr?ez une nouvelle cl?
5. Copiez-la

### 5. Configuration

```bash
# Copier le fichier de configuration
cp .env.example .env
```

?ditez `.env` et ajoutez vos cl?s:

```env
DISCORD_TOKEN=votre_token_discord_ici
GROQ_API_KEY=votre_cle_groq_ici
AI_MODEL=llama-3.1-70b-versatile
```

### 6. D?marrer le bot

```bash
python bot.py
```

? **Le bot est en ligne!**

## ?? Utilisation

### Activation du bot (Admin uniquement)

Le bot ne r?pond PAS automatiquement. Un administrateur doit l'activer dans chaque canal:

```
/start
```

Le bot est maintenant actif dans ce canal!

### Interagir avec le bot

Une fois activ?, vous pouvez:

1. **Mentionner le bot** : `@BotIA Salut, comment vas-tu?`
2. **R?pondre ? ses messages** : Utilisez la fonction "R?pondre" de Discord
3. **Message priv?** : Envoyez-lui un DM directement

### ?? Commandes Administrateur

Toutes ces commandes n?cessitent les permissions d'administrateur:

```
/start                     ? Active le bot dans le canal actuel
/stop                      ? D?sactive le bot dans le canal actuel
/personality               ? Affiche toutes les personnalit?s disponibles
/personality <nom>         ? Change la personnalit? du bot
/reset                     ? R?initialise l'historique de conversation
/status                    ? Affiche le statut du bot dans ce canal
```

### ?? Commandes G?n?rales

```
/help                  ? Affiche l'aide compl?te
```

## ?? Personnalit?s Disponibles

Le bot dispose de **8 personnalit?s** pr?d?finies, adapt?es aux serveurs adultes:

| Nom | Code | Description |
|-----|------|-------------|
| ?? Amical | `amical` | Sympathique et ouvert d'esprit (par d?faut) |
| ?? S?ducteur | `seducteur` | Charmant, flirteur et confiant |
| ?? Coquin | `coquin` | Os?, direct et provocateur |
| ?? Romantique | `romantique` | Doux, passionn? et ?motionnel |
| ?? Dominant | `dominant` | Confiant, assertif et autoritaire |
| ?? Soumis | `soumis` | Respectueux, ob?issant et d?vou? |
| ?? Joueur | `joueur` | Fun, d?contract? et gamer |
| ?? Intellectuel | `intellectuel` | Cultiv?, sophistiqu? et profond |

### Changer de personnalit?

```
/personality seducteur
```

Le bot adopte imm?diatement la nouvelle personnalit?! L'historique est automatiquement r?initialis?.

### Exemple d'utilisation

```
Admin: /start
Bot: ? Bot Activ? avec la personnalit? Amical ??

Admin: /personality coquin
Bot: ? Personnalit? chang?e! Nouvelle personnalit?: Coquin ??

User: @Bot Salut toi! ??
Bot: Hey... *te regarde avec un sourire en coin* Je vois que quelqu'un est d'humeur coquine ce soir ??
```

## ? Pourquoi Groq?

Groq est une plateforme d'IA ultra-rapide:

- ? **Vitesse**: R?ponses en ~1 seconde (vs 5-15s pour les autres)
- ?? **Gratuit**: API g?n?reuse et gratuite
- ?? **Puissant**: Utilise Llama 3.1, Mixtral, Gemma
- ?? **Moins censur?**: Meilleur pour les conversations adultes

### Mod?les disponibles

Le bot supporte tous les mod?les Groq. Les meilleurs:

- **llama-3.1-70b-versatile** (par d?faut) - Le meilleur ?quilibre
- **mixtral-8x7b-32768** - Excellent avec contexte ?tendu
- **llama-3.1-8b-instant** - Ultra rapide pour conversations simples
- **llama-3.2-90b-text-preview** - Le plus puissant

Changez dans `.env`:
```env
AI_MODEL=mixtral-8x7b-32768
```

## ?? H?bergement 24/7

Pour garder votre bot en ligne en permanence, consultez le guide complet:

?? **[HEBERGEMENT_24_7.md](HEBERGEMENT_24_7.md)**

### Options recommand?es

1. **?? VPS Oracle Cloud** - GRATUIT pour toujours!
2. **?? Raspberry Pi** - ~60? une fois, 3?/an d'?lectricit?
3. **?? Contabo VPS** - 5?/mois, tr?s fiable

Le guide inclut des instructions ?tape par ?tape pour chaque option.

## ?? Configuration Avanc?e

### Personnaliser les param?tres

?ditez `bot.py` pour modifier:

```python
MAX_HISTORY = 20              # Messages gard?s en m?moire
RATE_LIMIT_SECONDS = 2        # D?lai entre r?ponses
```

### Cr?er vos propres personnalit?s

?ditez le dictionnaire `PERSONALITIES` dans `bot.py`:

```python
PERSONALITIES = {
    "votre_perso": {
        "name": "Votre Nom ??",
        "prompt": """Votre description de personnalit? ici..."""
    },
    # ... autres personnalit?s
}
```

## ?? Exemple de conversation

```
User1: @Bot Hey! Tu es l??
Bot: Bien s?r! Je suis toujours l? pour discuter avec vous ??

User2: @Bot Tu joues ? quoi en ce moment?
Bot: J'adore observer vos conversations! Vous jouez ? quoi vous autres?

User1: On joue ? Valorant!
Bot: Ah Valorant! Vous ?tes plut?t agressifs ou plut?t strat?ges?

User2: On rush ? fond! ??
Bot: Haha j'imagine le chaos! Vous gagnez au moins? ??
```

## ?? S?curit? et Confidentialit?

### Ce que le bot stocke

- ? Les 20 derniers messages par canal (en RAM, pas sur disque)
- ? Aucune donn?e n'est sauvegard?e apr?s red?marrage
- ? Pas de logs des conversations

### Donn?es envoy?es ? Groq

- Les 10 derniers messages de la conversation
- Le prompt de personnalit?
- **Aucune donn?e personnelle** (IDs, emails, etc.)

### Recommandations

1. Ne partagez JAMAIS votre `DISCORD_TOKEN` ou `GROQ_API_KEY`
2. Utilisez le bot uniquement sur des serveurs priv?s/adultes autoris?s
3. Respectez les conditions d'utilisation de Discord et Groq
4. Le bot n'a pas de filtre de contenu - ? utiliser de mani?re responsable

## ? FAQ

### Le bot ne r?pond pas

- ? V?rifiez que vous avez fait `/start` dans le canal (admin uniquement)
- ? V?rifiez que "Message Content Intent" est activ? sur Discord
- ? V?rifiez que votre cl? Groq est valide
- ? Mentionnez le bot ou r?pondez ? ses messages

### Le bot est trop lent

- Essayez `llama-3.1-8b-instant` dans `.env` pour plus de vitesse
- V?rifiez votre connexion internet
- Groq peut avoir des limites de d?bit si vous faites beaucoup de requ?tes

### Le bot se d?connecte

- Normal si vous ?teignez votre PC
- Pour du 24/7, consultez [HEBERGEMENT_24_7.md](HEBERGEMENT_24_7.md)

### Comment changer de serveur Discord?

Le bot fonctionne sur tous les serveurs o? il est invit?. Chaque canal peut avoir:
- Sa propre activation (on/off)
- Sa propre personnalit?
- Son propre historique

### Le bot dit des choses inappropri?es

- Changez de personnalit? avec `/personality amical`
- R?initialisez avec `/reset`
- Les mod?les IA peuvent parfois g?n?rer du contenu inattendu

### Limites de l'API Groq gratuite

- ~30 requ?tes/minute
- ~14,400 requ?tes/jour
- Largement suffisant pour un serveur Discord normal

## ??? D?pannage

### Erreur: "DISCORD_TOKEN non trouv?"

Assurez-vous d'avoir cr?? le fichier `.env` avec votre token.

### Erreur: "GROQ_API_KEY non trouv?"

Cr?ez un compte sur https://console.groq.com et obtenez une cl? API gratuite.

### Le bot r?pond ? tout le monde

Normal! Une fois activ? avec `/start`, le bot r?pond quand on le mentionne ou qu'on r?pond ? ses messages.

### D?sactiver temporairement

```
/stop
```

Le bot arr?te de r?pondre dans ce canal jusqu'au prochain `/start`.

## ?? Structure du projet

```
discord-bot/
??? bot.py                    # Code principal du bot
??? .env                      # Configuration (? cr?er)
??? .env.example             # Template de configuration
??? requirements.txt         # D?pendances Python
??? README.md               # Ce fichier
??? GUIDE_RAPIDE.md        # Guide de d?marrage rapide
??? HEBERGEMENT_24_7.md    # Guide d'h?bergement 24/7
??? config.json            # Configurations suppl?mentaires
```

## ?? Mises ? jour futures possibles

- [ ] Commandes de mod?ration automatique
- [ ] Syst?me de points/XP pour les utilisateurs
- [ ] Support d'images avec des mod?les multimodaux
- [ ] Base de donn?es pour persistance
- [ ] Interface web de configuration
- [ ] Statistiques d'utilisation
- [ ] Personnalit?s personnalis?es par utilisateur

## ?? Changelog

### Version 2.0 (Actuelle)
- ? Migration vers Groq (ultra-rapide!)
- ? 8 personnalit?s pr?d?finies
- ? Syst?me d'activation par canal (admin)
- ? Guide d'h?bergement 24/7 complet
- ?? Am?lioration des performances

### Version 1.0
- ?? Version initiale avec Hugging Face

## ?? Licence

Ce projet est fourni "tel quel" pour un usage personnel et ?ducatif.

## ?? Avertissement

- Utilisez ce bot de mani?re responsable et l?gale
- Respectez les conditions d'utilisation de Discord et Groq
- Le cr?ateur n'est pas responsable de l'utilisation faite de ce bot
- Ce bot est con?u pour des serveurs adultes priv?s avec consentement de tous les membres
- Assurez-vous de respecter les lois de votre juridiction

## ?? Support

- ?? Consultez la documentation compl?te
- ?? Cr?ez une issue sur GitHub pour les bugs
- ?? Partagez vos suggestions d'am?lioration

---

**Fait avec ?? pour la communaut? Discord**

Bon chat! ??
