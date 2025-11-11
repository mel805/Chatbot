# 🤖 Bot Discord Chat NSFW - API Gratuite Sans Limite

Bot Discord utilisant l'API Hugging Face Inference (100% gratuite) pour des conversations IA sans censure, NSFW, et sans limite de messages.

## ✨ Caractéristiques

- ✅ **100% Gratuit** - Utilise l'API Hugging Face Inference
- 🔞 **Sans censure NSFW** - Aucun filtre de contenu
- ♾️ **Sans limite** - Pas de limite de messages ou de conversations
- 💾 **Mémoire de conversation** - L'IA se souvient du contexte
- 🔄 **Modèles multiples** - Plusieurs modèles IA disponibles
- ⚡ **Rapide et réactif** - Réponses en quelques secondes

## 📋 Modèles Disponibles

1. **Mistral-7B-Instruct-v0.2** (par défaut) - Rapide et performant
2. **Nous-Hermes-2-Mixtral-8x7B-DPO** - Plus créatif
3. **Llama-2-70b-chat** - Plus puissant

Tous ces modèles sont open source et sans filtre NSFW.

## 🚀 Installation

### 1. Prérequis

- Python 3.8 ou supérieur
- Un compte Discord
- (Optionnel) Un compte Hugging Face

### 2. Cloner le projet

```bash
git clone <votre-repo>
cd <votre-repo>
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration

1. Créez votre bot Discord:
   - Allez sur https://discord.com/developers/applications
   - Créez une nouvelle application
   - Allez dans "Bot" et créez un bot
   - Copiez le token du bot
   - Activez les "Privileged Gateway Intents" (Message Content Intent)

2. (Optionnel) Créez un token Hugging Face:
   - Créez un compte sur https://huggingface.co
   - Allez dans Settings > Access Tokens
   - Créez un nouveau token

3. Configurez le fichier `.env`:
   ```bash
   cp .env.example .env
   nano .env
   ```
   
   Remplissez vos tokens:
   ```env
   DISCORD_TOKEN=votre_token_discord_ici
   HF_TOKEN=votre_token_huggingface_ici  # Optionnel
   PREFIX=!
   ```

### 5. Inviter le bot sur votre serveur

1. Dans le Developer Portal, allez dans "OAuth2" > "URL Generator"
2. Sélectionnez les scopes: `bot` et `applications.commands`
3. Sélectionnez les permissions:
   - Send Messages
   - Read Messages/View Channels
   - Read Message History
   - Use Slash Commands
4. Copiez l'URL générée et ouvrez-la dans votre navigateur
5. Sélectionnez votre serveur et autorisez le bot

### 6. Lancer le bot

```bash
python bot.py
```

Vous devriez voir:
```
🚀 Démarrage du bot Discord...
✅ Bot connecté en tant que VotreBot#1234
```

## 📖 Commandes

### Commandes de Chat

| Commande | Alias | Description | Exemple |
|----------|-------|-------------|---------|
| `!chat <message>` | `!c` | Discute avec l'IA | `!chat Bonjour!` |
| `!clear` | `!reset` | Efface l'historique de conversation | `!clear` |

### Commandes de Gestion

| Commande | Alias | Description | Exemple |
|----------|-------|-------------|---------|
| `!models` | `!listmodels` | Liste les modèles disponibles | `!models` |
| `!switchmodel <index>` | `!sm` | Change le modèle utilisé | `!switchmodel 1` |
| `!info` | - | Informations sur le bot | `!info` |
| `!ping` | - | Vérifie la latence | `!ping` |
| `!help` | - | Affiche toutes les commandes | `!help` |

## 💡 Exemples d'Utilisation

### Conversation simple
```
Vous: !chat Salut, comment ça va?
Bot: Salut! Je vais bien, merci! Comment puis-je t'aider aujourd'hui?

Vous: !chat Parle-moi de l'astronomie
Bot: L'astronomie est la science qui étudie les objets célestes...
```

### Conversation NSFW
```
Vous: !chat [contenu NSFW]
Bot: [réponse sans censure]
```

### Gestion de l'historique
```
Vous: !chat Rappelle-toi que j'aime le chocolat
Bot: D'accord, je me souviens que tu aimes le chocolat!

Vous: !chat Qu'est-ce que j'aime?
Bot: Tu aimes le chocolat!

Vous: !clear
Bot: 🗑️ Votre historique de conversation a été effacé!
```

### Changer de modèle
```
Vous: !models
Bot: 📋 Modèles disponibles:
     ✅ 0. mistralai/Mistral-7B-Instruct-v0.2
        1. NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO
        2. meta-llama/Llama-2-70b-chat-hf

Vous: !switchmodel 1
Bot: ✅ Modèle changé pour: NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO
```

## 🔧 Configuration Avancée

### Modifier le préfixe
Dans le fichier `.env`, changez la valeur de `PREFIX`:
```env
PREFIX=$
```

### Ajouter d'autres modèles
Dans `chat_api.py`, ajoutez des modèles à la liste `self.models`:
```python
self.models = [
    "mistralai/Mistral-7B-Instruct-v0.2",
    "votre-nouveau-modele",
]
```

### Ajuster les paramètres de génération
Dans `chat_api.py`, modifiez les paramètres dans la fonction `get_response()`:
```python
"parameters": {
    "max_new_tokens": 500,      # Longueur maximale de la réponse
    "temperature": 0.7,         # Créativité (0.0-2.0)
    "top_p": 0.95,             # Diversité des réponses
    "do_sample": True,         # Échantillonnage aléatoire
}
```

## 🛠️ Dépannage

### Le bot ne répond pas
1. Vérifiez que le bot est en ligne (présence dans la liste des membres)
2. Vérifiez que les permissions sont correctes
3. Vérifiez que "Message Content Intent" est activé dans le Developer Portal

### Erreur "Model is loading"
L'API Hugging Face charge le modèle. Attendez quelques secondes et réessayez.

### Erreur "Rate limit"
Vous avez fait trop de requêtes. Attendez quelques secondes. Pour éviter cela, créez un token Hugging Face.

### Réponses lentes
1. Utilisez un token Hugging Face pour des performances optimales
2. Essayez un modèle plus petit (Mistral-7B est le plus rapide)
3. Les premiers messages sont plus lents (chargement du modèle)

## 🔐 Sécurité

- **Ne partagez jamais** votre token Discord ou Hugging Face
- Ajoutez `.env` à votre `.gitignore`
- N'hébergez pas le bot sur des services publics avec vos tokens exposés

## 📝 Notes Importantes

- L'API Hugging Face est gratuite mais peut avoir des limites de rate sans token
- Les modèles peuvent mettre quelques secondes à charger lors de la première utilisation
- L'historique de conversation est stocké en mémoire (perdu au redémarrage du bot)
- Le bot nécessite une connexion internet

## 🤝 Contribution

Les contributions sont les bienvenues! N'hésitez pas à:
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Ajouter de nouveaux modèles

## 📄 Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le distribuer.

## ⚠️ Avertissement

Ce bot permet des conversations NSFW sans censure. Utilisez-le de manière responsable et conformément aux règles de Discord et aux lois de votre juridiction. Les développeurs ne sont pas responsables de l'utilisation qui est faite de ce bot.

## 🌟 Support

Si vous rencontrez des problèmes ou avez des questions:
1. Consultez la section Dépannage
2. Vérifiez les logs du bot pour les erreurs
3. Créez une issue sur GitHub

---

**Bon chat! 🚀**
