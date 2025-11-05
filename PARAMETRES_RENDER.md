# ?? Param?tres Build et D?ploiement Render

## ?? Configuration Compl?te pour Render.com

### ?? Section: Service Details

```
Service Type: Background Worker
Name: discord-bot-ia (ou votre choix)
Region: Frankfurt (ou Oregon, Singapore selon votre localisation)
Branch: main (ou votre branche principale)
```

---

## ??? Section: Build & Deploy

### Build Command
```bash
pip install -r requirements.txt
```

**Alternative si probl?mes:**
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

### Start Command
```bash
python3 bot.py
```

**Alternative:**
```bash
python bot.py
```

### Root Directory
```
.
```
(laisser vide ou mettre un point = racine du repo)

---

## ?? Section: Environment Variables

### Variables OBLIGATOIRES

| Key | Value | Description |
|-----|-------|-------------|
| `DISCORD_TOKEN` | `votre_token_discord` | Token de votre bot Discord |
| `GROQ_API_KEY` | `votre_cle_groq` | Cl? API Groq (gratuite) |

### Variables OPTIONNELLES

| Key | Value | Description |
|-----|-------|-------------|
| `AI_MODEL` | `llama-3.1-70b-versatile` | Mod?le Groq ? utiliser |
| `PYTHON_VERSION` | `3.11.0` | Version Python (g?n?ralement auto-d?tect?e) |

---

## ?? Section: Plan

```
Plan: Free (Starter: 7$/mois pour 24/7 sans veille)
```

---

## ?? Section: Auto-Deploy

```
Auto-Deploy: Yes (recommand?)
```

Cela red?ploie automatiquement quand vous faites un `git push`.

---

## ?? Configuration Compl?te (Copier-Coller)

### Pour la cr?ation manuelle du service:

**Service Type:**
```
Background Worker
```

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python3 bot.py
```

**Environment Variables:**
```
DISCORD_TOKEN = [Coller votre token Discord ici]
GROQ_API_KEY = [Coller votre cl? Groq ici]
AI_MODEL = llama-3.1-70b-versatile
```

---

## ?? Guide ?tape par ?tape

### 1. Cr?er le Service

1. **Dashboard Render** ? **New +**
2. S?lectionnez **"Background Worker"** (pas Web Service!)

### 2. Connecter GitHub

1. **Connect a repository**
2. Connectez votre compte GitHub si pas d?j? fait
3. S?lectionnez votre d?p?t

### 3. Configurer le Service

**Name:**
```
discord-bot-ia
```

**Region:**
```
Frankfurt (EU)
```
Ou choisissez le plus proche de vous:
- `Oregon` (US West)
- `Ohio` (US East)
- `Frankfurt` (Europe)
- `Singapore` (Asia)

**Branch:**
```
main
```

**Root Directory:**
```
.
```
(laisser vide)

### 4. Build Settings

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python3 bot.py
```

### 5. Environment Variables

Cliquez sur **"Add Environment Variable"** pour chaque:

**Variable 1:**
- Key: `DISCORD_TOKEN`
- Value: `MTk...` (votre token Discord complet)

**Variable 2:**
- Key: `GROQ_API_KEY`
- Value: `gsk_...` (votre cl? Groq)

**Variable 3 (optionnelle):**
- Key: `AI_MODEL`
- Value: `llama-3.1-70b-versatile`

### 6. Advanced Settings

**Instance Type:**
```
Free
```

**Auto-Deploy:**
```
Yes ?
```

### 7. Create Worker

Cliquez sur **"Create Background Worker"**

---

## ?? Fichiers Requis dans votre Repo

Assurez-vous d'avoir ces fichiers:

### `requirements.txt`
```txt
discord.py>=2.3.2
python-dotenv>=1.0.0
aiohttp>=3.9.0
```

### `runtime.txt`
```txt
python-3.11.0
```

### `render.yaml` (optionnel mais recommand?)
```yaml
services:
  - type: worker
    name: discord-bot-ia
    env: python
    region: frankfurt
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python3 bot.py
    envVars:
      - key: DISCORD_TOKEN
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: AI_MODEL
        value: llama-3.1-70b-versatile
      - key: PYTHON_VERSION
        value: 3.11.0
    autoDeploy: true
```

### `.gitignore`
```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## ?? V?rification Post-D?ploiement

### 1. V?rifier les Logs

Dashboard ? Votre service ? **Logs**

**Vous devriez voir:**
```
==> Cloning from https://github.com/...
==> Checking out commit ...
==> Running build command: pip install -r requirements.txt
    Collecting discord.py>=2.3.2
    Collecting python-dotenv>=1.0.0
    Collecting aiohttp>=3.9.0
    Successfully installed ...

==> Starting service with command: python3 bot.py
?? D?marrage du bot Discord IA avec Groq...
?? Mod?le: llama-3.1-70b-versatile
?? Personnalit?s: 8
? Commandes Slash activ?es!
?? [VotreBotName] est connect? et pr?t!
?? Connect? ? X serveur(s)
? 6 commandes slash synchronis?es!
```

### 2. V?rifier sur Discord

- Le bot appara?t **en ligne** (pastille verte)
- Testez `/start` dans un canal (en tant qu'admin)
- Testez `/help`

---

## ?? Erreurs Courantes et Solutions

### Erreur: "No module named 'discord'"

**Probl?me:** D?pendances pas install?es

**Solution:**
- V?rifiez le **Build Command**: `pip install -r requirements.txt`
- V?rifiez que `requirements.txt` existe ? la racine

### Erreur: "discord_bot_main.py not found"

**Probl?me:** Fichier bot.py pas ? la racine ou mauvaise Start Command

**Solution:**
- **Start Command** doit ?tre: `python3 bot.py`
- `bot.py` doit ?tre ? la racine du repo (pas dans un sous-dossier)

### Erreur: "DISCORD_TOKEN non trouv?"

**Probl?me:** Variable d'environnement pas configur?e

**Solution:**
- Dashboard ? Settings ? Environment
- Ajoutez `DISCORD_TOKEN` avec votre token

### Erreur: "Login failed"

**Probl?me:** Token Discord invalide

**Solution:**
- V?rifiez que le token est correct
- Pas d'espaces avant/apr?s
- Regenerez le token si n?cessaire

---

## ?? Red?ploiement

### Automatique
```bash
# Faire une modification
git add .
git commit -m "Update"
git push

# Render red?ploie automatiquement!
```

### Manuel
1. Dashboard ? Votre service
2. **Manual Deploy** (bouton en haut ? droite)
3. **Deploy latest commit**

---

## ?? Monitoring

### Voir l'utilisation
Dashboard ? Metrics

**Affiche:**
- Uptime
- CPU usage
- Memory usage
- Red?marrages

### Logs en temps r?el
Dashboard ? Logs

**Filtrer:**
- Search box pour chercher des erreurs
- Scroll pour voir l'historique

---

## ?? Plans Render

### Plan Free
- **Prix:** 0?/mois
- **Limitations:**
  - 750 heures/mois
  - Se met en veille apr?s 15 min d'inactivit?
  - Red?marrage mensuel
- **Recommand? pour:** Tests, d?veloppement

### Plan Starter
- **Prix:** 7$/mois (~6,50?)
- **Avantages:**
  - Pas de veille
  - Pas de limite d'heures
  - Pas de red?marrage forc?
- **Recommand? pour:** Bot Discord 24/7 en production

---

## ?? Checklist Compl?te

Avant de cr?er le service:

- [ ] Code sur GitHub (branche main)
- [ ] `bot.py` ? la racine
- [ ] `requirements.txt` pr?sent
- [ ] `runtime.txt` pr?sent (optionnel)
- [ ] `.env` NOT dans le repo (v?rifi? par .gitignore)
- [ ] Token Discord obtenu
- [ ] Cl? Groq obtenue
- [ ] Bot invit? sur Discord avec permissions

Lors de la cr?ation:

- [ ] Service Type = Background Worker
- [ ] Build Command = `pip install -r requirements.txt`
- [ ] Start Command = `python3 bot.py`
- [ ] DISCORD_TOKEN configur?
- [ ] GROQ_API_KEY configur?
- [ ] AI_MODEL configur? (optionnel)
- [ ] Auto-Deploy activ?

Apr?s le d?ploiement:

- [ ] Logs montrent "connect? et pr?t"
- [ ] Bot en ligne sur Discord
- [ ] `/start` fonctionne
- [ ] `/help` fonctionne
- [ ] Bot r?pond aux mentions

---

## ?? Ressources

- **Dashboard Render:** https://dashboard.render.com
- **Documentation Render:** https://render.com/docs
- **Discord Developers:** https://discord.com/developers/applications
- **Groq Console:** https://console.groq.com

---

## ?? Astuce Pro

**Pour ?viter la veille du plan gratuit:**
1. Upgrade au plan Starter (7$/mois)
2. OU utilisez Oracle Cloud (VPS gratuit ? vie)
   ? Voir `HEBERGEMENT_24_7.md`

---

? **Avec ces param?tres, votre bot devrait se d?ployer correctement!**

Si probl?mes: consultez `ERREUR_RENDER_FIX.md`
