# ?? D?ploiement sur Render.com (24/7 Gratuit avec Limitations)

Ce guide vous explique comment d?ployer votre bot Discord sur Render.com pour qu'il tourne 24/7.

## ?? Table des mati?res

1. [Pr?sentation de Render](#pr?sentation-de-render)
2. [Pr?requis](#pr?requis)
3. [?tape 1: Pr?parer votre code](#?tape-1-pr?parer-votre-code)
4. [?tape 2: Cr?er un compte Render](#?tape-2-cr?er-un-compte-render)
5. [?tape 3: D?ployer le bot](#?tape-3-d?ployer-le-bot)
6. [?tape 4: Configuration](#?tape-4-configuration)
7. [Limitations du plan gratuit](#limitations-du-plan-gratuit)
8. [Surveillance et logs](#surveillance-et-logs)
9. [D?pannage](#d?pannage)

---

## ?? Pr?sentation de Render

### Avantages
- ? **Gratuit** (avec limitations)
- ? **24/7** (avec le plan payant - 7$/mois)
- ? **D?ploiement facile** depuis GitHub
- ? **Auto-d?ploiement** sur chaque commit
- ? **Logs en temps r?el**

### Inconv?nients
- ?? **Plan gratuit limit?**: 750 heures/mois (?31 jours mais partag? entre tous vos services)
- ?? **Inactivit?**: Le service gratuit peut se mettre en veille (probl?matique pour un bot Discord)
- ?? **Red?marrage mensuel**: Le plan gratuit red?marre automatiquement chaque mois

### Alternatives recommand?es
- **Oracle Cloud** (VPS gratuit ? vie) - Voir HEBERGEMENT_24_7.md
- **Raspberry Pi** (60? une fois, contr?le total)
- **Contabo** (5?/mois, tr?s fiable)

---

## ?? Pr?requis

Avant de commencer:

1. ? **Compte GitHub**
   - Cr?ez un compte sur https://github.com si vous n'en avez pas
   
2. ? **Token Discord**
   - Obtenez votre token sur https://discord.com/developers/applications
   
3. ? **Cl? API Groq**
   - Obtenez votre cl? gratuite sur https://console.groq.com
   
4. ? **Code sur GitHub**
   - Votre bot doit ?tre dans un d?p?t GitHub (public ou priv?)

---

## ?? ?tape 1: Pr?parer votre code

### Option A: Utiliser votre propre d?p?t GitHub

Si vous avez d?j? clon?/fork? ce projet:

```bash
# 1. Initialisez git si ce n'est pas fait
git init

# 2. Ajoutez vos fichiers
git add .

# 3. Commitez
git commit -m "Initial commit - Discord bot IA"

# 4. Cr?ez un repo sur GitHub et suivez les instructions pour push
git remote add origin https://github.com/votre-username/votre-repo.git
git branch -M main
git push -u origin main
```

### Option B: Forker le projet original

Si vous avez acc?s au projet original:
1. Allez sur la page GitHub du projet
2. Cliquez sur "Fork" en haut ? droite
3. Le code sera copi? dans votre compte

### Fichiers n?cessaires (d?j? inclus)

? `render.yaml` - Configuration pour Render
? `runtime.txt` - Version Python
? `requirements.txt` - D?pendances
? `bot.py` - Code du bot
? `.gitignore` - Fichiers ? ignorer (inclut `.env`)

**?? IMPORTANT**: Ne commitez JAMAIS votre fichier `.env` avec vos tokens!

---

## ?? ?tape 2: Cr?er un compte Render

1. Allez sur https://render.com
2. Cliquez sur **"Get Started"** ou **"Sign Up"**
3. Inscrivez-vous avec:
   - GitHub (recommand?)
   - GitLab
   - Email

4. Confirmez votre email

---

## ?? ?tape 3: D?ployer le bot

### M?thode 1: Avec le fichier render.yaml (Recommand?)

1. **Connecter GitHub**
   - Dans Render Dashboard, allez dans "New +"
   - S?lectionnez "Blueprint"
   - Connectez votre compte GitHub si demand?
   - Autorisez Render ? acc?der ? vos d?p?ts

2. **S?lectionner le d?p?t**
   - Trouvez votre d?p?t du bot Discord
   - Cliquez sur "Connect"

3. **Configuration automatique**
   - Render d?tecte automatiquement le fichier `render.yaml`
   - V?rifiez les param?tres:
     - **Name**: discord-bot-ia
     - **Type**: Worker (important!)
     - **Region**: Choisissez le plus proche
     - **Plan**: Free

4. **Variables d'environnement** (tr?s important!)
   - Render va vous demander de configurer:
   
   ```
   DISCORD_TOKEN = votre_token_discord_ici
   GROQ_API_KEY = votre_cle_groq_ici
   AI_MODEL = llama-3.1-70b-versatile (d?j? configur?)
   ```

5. **D?ployer**
   - Cliquez sur "Apply"
   - Render va:
     - Cloner votre code
     - Installer les d?pendances
     - Lancer le bot

### M?thode 2: Manuelle

Si vous pr?f?rez configurer manuellement:

1. **New Worker**
   - Dashboard ? "New +" ? "Background Worker"

2. **Connecter le d?p?t**
   - S?lectionnez votre d?p?t GitHub
   - Branch: `main` (ou votre branche principale)

3. **Configuration**
   - **Name**: `discord-bot-ia`
   - **Region**: Choisissez selon votre localisation
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`

4. **Environment**
   - Cliquez sur "Advanced" ou "Environment"
   - Ajoutez les variables:
   
   | Key | Value |
   |-----|-------|
   | `DISCORD_TOKEN` | Votre token Discord |
   | `GROQ_API_KEY` | Votre cl? Groq |
   | `AI_MODEL` | `llama-3.1-70b-versatile` |
   | `PYTHON_VERSION` | `3.11.0` |

5. **Plan**
   - S?lectionnez "Free"

6. **Create Worker**
   - Cliquez pour lancer le d?ploiement

---

## ?? ?tape 4: Configuration

### V?rifier le d?ploiement

1. **Logs en temps r?el**
   - Dans le Dashboard Render
   - S?lectionnez votre service
   - Onglet "Logs"
   
   Vous devriez voir:
   ```
   ?? D?marrage du bot Discord IA avec Groq...
   ?? Mod?le: llama-3.1-70b-versatile
   ?? Personnalit?s: 8
   ? Commandes Slash activ?es!
   ?? [VotreBotName] est connect? et pr?t!
   ?? Connect? ? X serveur(s)
   ? 6 commandes slash synchronis?es!
   ```

2. **V?rifier sur Discord**
   - Le bot devrait appara?tre en ligne
   - Tapez `/start` dans un canal (en tant qu'admin)
   - Testez avec `/help`

### Configuration avanc?e

#### Auto-d?ploiement

Par d?faut, Render red?ploie automatiquement quand vous poussez sur GitHub:

```bash
# Faire une modification
nano bot.py

# Committer et pusher
git add .
git commit -m "Mise ? jour du bot"
git push

# Render red?ploie automatiquement!
```

Pour d?sactiver:
- Dashboard ? Votre service ? Settings
- D?cochez "Auto-Deploy"

#### Notifications

Configurez les notifications pour ?tre alert? en cas de probl?me:
- Settings ? Notifications
- Ajoutez votre email ou webhook Discord

---

## ?? Limitations du plan gratuit

### Plan Free de Render

| Caract?ristique | Plan Free | Plan Starter (7$/mois) |
|-----------------|-----------|------------------------|
| Heures/mois | 750h | Illimit? |
| Inactivit? | Se met en veille apr?s 15 min d'inactivit? | ? Pas de veille |
| Red?marrage | Mensuel | Pas de red?marrage forc? |
| RAM | 512 MB | 512 MB |
| CPU | Partag? | Partag? |

### ?? Probl?me majeur: Veille automatique

**Le plan gratuit met les services en veille apr?s 15 minutes d'inactivit?!**

Pour un bot Discord, c'est probl?matique car:
- Le bot se d?connecte
- Il ne r?pond plus aux commandes
- Il faut une activit? pour le r?veiller

### Solutions:

#### Solution 1: Upgrade au plan Starter (7$/mois)
- Pas de veille
- Bot actif 24/7
- Recommand? si vous voulez un service fiable

#### Solution 2: Utiliser un service de "keep-alive" (hack, non recommand?)
Ajouter un endpoint web que vous pingez r?guli?rement (compliqu? pour un bot Discord)

#### Solution 3: Utiliser une alternative gratuite
- **Oracle Cloud** - VPS gratuit ? vie (recommand?)
- **Raspberry Pi** - 60? une fois, contr?le total
- Voir **HEBERGEMENT_24_7.md**

---

## ?? Surveillance et logs

### Voir les logs

1. **Dashboard Render**
   - S?lectionnez votre service
   - Onglet "Logs"
   - Logs en temps r?el

2. **Filtrer les logs**
   ```
   # Chercher des erreurs
   Ctrl+F "erreur" ou "error"
   
   # Voir les connexions
   Chercher "connect?"
   ```

3. **T?l?charger les logs**
   - Bouton "Download" dans l'interface

### Statistiques

- Dashboard ? Votre service ? Metrics
- Voir:
  - Uptime
  - Utilisation CPU
  - Utilisation RAM
  - Red?marrages

### Alertes

Configurez des alertes pour:
- Service down
- Erreurs r?p?t?es
- Utilisation excessive de ressources

Settings ? Notifications

---

## ?? D?pannage

### Le bot ne se lance pas

1. **V?rifier les logs**
   ```
   Dashboard ? Logs
   ```

2. **Erreurs communes**:

   **"DISCORD_TOKEN non trouv?"**
   - Allez dans Settings ? Environment
   - V?rifiez que `DISCORD_TOKEN` est bien configur?
   - Le token doit commencer par `MTk...` ou `ODc...`

   **"GROQ_API_KEY non trouv?"**
   - V?rifiez que `GROQ_API_KEY` est configur?
   - Testez votre cl? sur https://console.groq.com

   **"Module discord not found"**
   - V?rifiez le Build Command: `pip install -r requirements.txt`
   - Red?ployez manuellement

### Le bot se d?connecte

1. **Plan gratuit?**
   - V?rifiez si c'est d? ? l'inactivit? (15 min)
   - Passez au plan Starter (7$/mois)

2. **Erreur dans le code?**
   - Regardez les logs pour voir le message d'erreur
   - Le bot crashe peut-?tre

3. **Limites API Groq?**
   - V?rifiez votre utilisation sur console.groq.com
   - Peut-?tre trop de requ?tes

### Le bot est lent

1. **Latence Groq**
   - Normal, Groq peut ?tre lent parfois
   - Essayez un mod?le plus rapide: `llama-3.1-8b-instant`

2. **R?gion Render**
   - Choisissez une r?gion proche de vous
   - Settings ? Change region (red?ploie)

### Red?ploiement manuel

Si besoin de red?marrer:

1. **Dashboard ? Votre service**
2. **Bouton "Manual Deploy"** en haut ? droite
3. **Deploy latest commit**

---

## ?? Co?ts

### Plan Free
- **0?/mois**
- 750 heures partag?es entre tous vos services
- Veille apr?s 15 min d'inactivit?
- Red?marrage mensuel

### Plan Starter (recommand? pour bot Discord)
- **7$/mois** (environ 6,50?)
- Pas de veille
- Pas de limitation d'heures
- Pas de red?marrage forc?
- Bot actif 24/7

### Comparaison avec alternatives

| Service | Co?t | Fiabilit? | Difficult? |
|---------|------|-----------|------------|
| Render Free | 0? | ?? | Facile |
| Render Starter | 7$/mois | ???? | Facile |
| Oracle Cloud VPS | **0?** | ????? | Moyenne |
| Raspberry Pi | 60? (une fois) | ???? | Facile |
| Contabo VPS | 5?/mois | ????? | Moyenne |

---

## ?? Checklist de d?ploiement

Avant de d?ployer, v?rifiez:

- [ ] Code sur GitHub
- [ ] Fichier `.env` NOT dans le repo (dans .gitignore)
- [ ] `render.yaml` pr?sent
- [ ] `requirements.txt` pr?sent
- [ ] `runtime.txt` pr?sent
- [ ] Compte Render cr??
- [ ] Token Discord obtenu
- [ ] Cl? API Groq obtenue
- [ ] Bot invit? sur Discord avec `applications.commands`
- [ ] Variables d'environnement configur?es sur Render

---

## ?? Ressources

- **Site Render**: https://render.com
- **Documentation Render**: https://render.com/docs
- **Status Render**: https://status.render.com
- **Support Render**: https://community.render.com

- **Discord Developers**: https://discord.com/developers
- **Groq Console**: https://console.groq.com

- **Documentation du bot**: README.md
- **Autres options d'h?bergement**: HEBERGEMENT_24_7.md

---

## ? R?sum? rapide

```bash
# 1. Code sur GitHub
git init
git add .
git commit -m "Bot Discord IA"
git push origin main

# 2. Render.com
- New + ? Blueprint (ou Background Worker)
- Connecter GitHub
- S?lectionner le repo
- Configurer les variables d'environnement:
  DISCORD_TOKEN
  GROQ_API_KEY
  AI_MODEL
- Deploy!

# 3. V?rifier
- Voir les logs
- Bot en ligne sur Discord
- /start pour activer
```

---

## ?? C'est parti!

Votre bot Discord est maintenant d?ploy? sur Render! ??

**Note**: Pour un bot 24/7 vraiment fiable et gratuit, consid?rez **Oracle Cloud** (voir HEBERGEMENT_24_7.md) ou le plan Starter de Render ? 7$/mois.

Besoin d'aide? Consultez la documentation compl?te dans README.md!
