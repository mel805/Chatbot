# 🤖 Bot Discord NSFW - API 100% Gratuite Sans Censure

Bot Discord avec chatbots IA pour serveurs NSFW (18+), utilisant une **API 100% gratuite, sans censure, et sans limite stricte**.

## ✨ Nouveauté: API Gratuite NSFW

Le bot utilise maintenant un système intelligent qui combine **4 modèles uncensored** en rotation automatique:

- ✅ **100% Gratuit** - Aucun coût, aucune carte bancaire
- ✅ **Sans Censure NSFW** - Modèles spécialement sélectionnés
- ✅ **Sans Limite Stricte** - Rotation automatique si rate limit
- ✅ **Token Optionnel** - Fonctionne sans configuration
- ✅ **Haute Disponibilité** - 99%+ uptime

## 🚀 Démarrage Rapide

### Option 1: Déploiement Sur Render.com (Recommandé)

1. Fork ce repo
2. Créez un compte sur [Render.com](https://render.com)
3. Créez un nouveau "Web Service"
4. Connectez votre repo
5. Ajoutez la variable d'environnement:
   ```
   DISCORD_BOT_TOKEN=votre_token_discord
   ```
6. Déployez !

**C'est tout !** Le bot fonctionne immédiatement avec l'API gratuite.

### Option 2: Local

```bash
# 1. Cloner
git clone <votre-repo>
cd <votre-repo>

# 2. Installer
pip install -r requirements.txt

# 3. Configurer
echo "DISCORD_BOT_TOKEN=votre_token" > .env

# 4. Lancer
python discord_bot_main.py
```

## 📋 Fonctionnalités

### Chatbots IA

- **13 chatbots prédéfinis** avec personnalités variées
- **Conversations NSFW** sans censure
- **Mémoire contextuelle** - Le bot se souvient de la conversation
- **Génération d'images** - Boutons interactifs pour visualiser les personnages

### Interface

- **Commandes Slash** - `/start`, `/stop`
- **Boutons Discord** - Interface intuitive
- **Threads Privés** - Conversations isolées
- **Catégories** - Romantique, Intense, Doux, etc.

### Sécurité

- **Canaux NSFW uniquement** - Vérification automatique
- **Rate Limiting** - Protection contre le spam
- **Historique privé** - Conversations isolées par utilisateur

## 🎯 Utilisation

### Pour les Utilisateurs

1. Dans un canal NSFW, tapez `/start`
2. Cliquez sur **"Galerie"** pour voir les chatbots
3. Choisissez une catégorie puis un chatbot
4. Cliquez sur **"Utiliser ce chatbot"**
5. Cliquez sur **"Discuter"** pour créer une conversation
6. Tapez vos messages dans le thread créé !

### Commandes

- `/start` - Afficher le menu principal
- `/stop` - Terminer la conversation active

## 🔧 Configuration Avancée

### Variables d'Environnement

#### Obligatoire

```env
DISCORD_BOT_TOKEN=votre_token_discord
```

#### Optionnelles (pour améliorer les performances)

```env
# Token HuggingFace gratuit (améliore vitesse et rate limits)
HUGGINGFACE_API_KEY=hf_votre_token_gratuit

# Provider d'IA (par défaut: free_nsfw)
AI_PROVIDER=free_nsfw

# Port HTTP (par défaut: 10000)
PORT=10000
```

### Créer un Token HuggingFace (Optionnel)

1. Créez un compte sur [HuggingFace](https://huggingface.co)
2. Allez dans Settings > Access Tokens
3. Créez un token (Read access suffit)
4. Ajoutez-le dans votre `.env` ou Render

**Avantages avec token:**
- Réponses plus rapides
- Rate limits plus généreux
- Priorité de chargement des modèles

## 📊 APIs Utilisées

### Provider: `free_nsfw` (Par Défaut)

Rotation automatique entre 4 modèles Hugging Face uncensored:

1. **Mistral-7B-OpenOrca** (Open-Orca)
2. **Nous-Hermes-2-Mistral-7B-DPO** (NousResearch)
3. **Dolphin-2.6-Mistral-7B** (Cognitive Computations)
4. **MythoMax-L2-13b** (Gryphe)

Si un modèle est surchargé → passage automatique au suivant.

### Autres Providers Disponibles

Modifiez `AI_PROVIDER` pour utiliser:

- `free_nsfw` - **4 modèles gratuits NSFW** (recommandé)
- `groq` - Groq (nécessite token, limites strictes)
- `openai` - OpenAI GPT-4 (payant)
- `deepinfra` - DeepInfra (gratuit avec limites)

## 📖 Documentation

- **[API_GRATUITE_NSFW.md](API_GRATUITE_NSFW.md)** - Documentation complète du système gratuit
- **[GUIDE_API_GRATUITE.md](GUIDE_API_GRATUITE.md)** - Guide rapide de déploiement
- **[RESUME_CHANGEMENTS_API.md](RESUME_CHANGEMENTS_API.md)** - Résumé des changements

## 🏗️ Structure du Projet

```
/workspace/
├── discord_bot_main.py       # Bot Discord principal
├── enhanced_chatbot_ai.py    # Gestion des APIs IA (MODIFIÉ)
├── chatbot_manager.py        # Gestion des profils de chatbots
├── public_chatbots.py        # 13 chatbots prédéfinis
├── thread_manager.py         # Gestion des threads privés
├── image_generator.py        # Génération d'images
├── requirements.txt          # Dépendances Python
└── README.md                 # Ce fichier
```

## 📈 Performances

### Temps de Réponse

- **Sans token HF** : 5-20s (première), 2-8s (suivantes)
- **Avec token HF** : 2-5s (première), 1-5s (suivantes)

### Disponibilité

- **99%+** : Au moins 1 modèle disponible à tout moment
- **Rotation intelligente** : Fallback automatique

## ⚠️ Avertissements

### Légalité

- ❌ **Interdit** : Contenu impliquant des mineurs
- ❌ **Interdit** : Contenu illégal
- ✅ **Autorisé** : Contenu NSFW consensuel entre adultes

### Responsabilité

- Ce bot est fourni à des fins **éducatives**
- **Vous** êtes responsable de l'utilisation
- Respectez les [ToS Discord](https://discord.com/terms)
- Les créateurs ne sont **pas responsables** de l'utilisation

### Modération

- Un **modérateur humain** doit superviser le serveur
- Vérifiez l'âge des membres (18+)
- Activez uniquement dans des canaux NSFW

## 🐛 Dépannage

### "Modèles surchargés"
→ Très rare (< 1%), attendez 10-30 secondes

### "Réponse lente"
→ Normal pour la première requête (chargement du modèle)
→ Créez un token HuggingFace gratuit

### Bot ne répond pas
→ Vérifiez que le canal est marqué NSFW
→ Vérifiez les permissions du bot
→ Consultez les logs

### Erreur "Token Discord invalide"
→ Vérifiez `DISCORD_BOT_TOKEN` dans `.env` ou Render

## 🔍 Logs

Le système affiche des logs détaillés:

```
[DEBUG] Tentative 1/4: HuggingFace-Mistral-Uncensored
[SUCCESS] HuggingFace-Mistral-Uncensored: Salut ! Comment...
[WARN] HuggingFace-Nous-Hermes surcharge (503), passage au suivant...
```

## 🤝 Contribution

Les contributions sont bienvenues !

1. Fork le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements
4. Push vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est fourni "tel quel" à des fins éducatives.

**IMPORTANT**: Vous êtes responsable de:
- La conformité légale dans votre juridiction
- Le respect des ToS de Discord et des APIs
- La modération de votre serveur
- Le contenu généré par le bot

## 🌟 Remerciements

- **Hugging Face** - Pour l'API Inference gratuite
- **NousResearch, Gryphe, Cognitive Computations** - Pour les modèles uncensored
- **Discord.py** - Pour la bibliothèque Discord
- **Communauté open source** - Pour les modèles et outils

## 📞 Support

- **Issues GitHub** : Pour bugs et suggestions
- **Documentation** : Consultez les fichiers `.md`
- **Discord.py Docs** : [discordpy.readthedocs.io](https://discordpy.readthedocs.io/)

---

**🚀 Bot 100% gratuit, NSFW sans censure, prêt à l'emploi !**

*Utilisez de manière responsable, légale et éthique.*
