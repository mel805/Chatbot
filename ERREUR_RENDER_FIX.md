# ?? ERREUR RENDER: "discord_bot_main.py non trouv?"

## ?? Le Probl?me

Vous voyez cette erreur:
```
impossible d'ouvrir le fichier ? /opt/render/project/src/discord_bot_main.py ?
[Errno 2] Aucun fichier ou r?pertoire de ce type
```

**Cause**: Render cherche un fichier qui n'existe pas ou la commande de d?marrage est incorrecte.

---

## ? Solutions

### Solution 1: V?rifier la Start Command dans Render Dashboard

1. **Allez dans Render Dashboard**
   - S?lectionnez votre service

2. **Settings ? Build & Deploy**
   - Trouvez **"Start Command"**
   
3. **La commande DOIT ?tre:**
   ```
   python3 bot.py
   ```
   OU
   ```
   python bot.py
   ```

4. **Si c'est diff?rent**, modifiez-la!

5. **Save Changes** et **red?ployez manuellement**

### Solution 2: V?rifier votre d?p?t GitHub

1. **V?rifiez que `bot.py` existe ? la racine**
   ```bash
   # Dans votre d?p?t local
   ls -la
   
   # Vous DEVEZ voir:
   bot.py              ? IMPORTANT!
   render.yaml
   requirements.txt
   runtime.txt
   ```

2. **Si `bot.py` est dans un sous-dossier**, d?placez-le ? la racine:
   ```bash
   # Exemple si dans src/
   mv src/bot.py .
   git add .
   git commit -m "Move bot.py to root"
   git push
   ```

### Solution 3: V?rifier render.yaml

1. **Ouvrez `render.yaml`**

2. **V?rifiez la section startCommand:**
   ```yaml
   services:
     - type: worker
       name: discord-bot-ia
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: python3 bot.py    # ? DOIT pointer vers bot.py
   ```

3. **Si incorrect, corrigez et push:**
   ```bash
   git add render.yaml
   git commit -m "Fix start command"
   git push
   ```

### Solution 4: M?thode Manuelle (Sans render.yaml)

Si le render.yaml pose probl?me, configurez manuellement:

1. **Dashboard Render ? Votre service ? Settings**

2. **Build & Deploy section:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python3 bot.py`

3. **Environment section** (si pas d?j? fait):
   - `DISCORD_TOKEN` = votre token
   - `GROQ_API_KEY` = votre cl?
   - `AI_MODEL` = llama-3.1-70b-versatile

4. **Save Changes**

5. **Manual Deploy** ? Deploy latest commit

---

## ?? V?rification de la Structure

Votre structure de fichiers sur GitHub DOIT ressembler ?:

```
votre-repo/
??? bot.py                 ? ? LA RACINE!
??? render.yaml
??? requirements.txt
??? runtime.txt
??? .env.example
??? .gitignore
??? README.md
```

**? PAS comme ?a:**
```
votre-repo/
??? src/
    ??? bot.py            ? Mauvais emplacement!
```

---

## ?? Debug: V?rifier ce que Render voit

1. **Render Dashboard ? Logs**

2. **Cherchez la section "Build":**
   ```
   Cloning repository...
   Checking out commit...
   ```

3. **V?rifiez la liste des fichiers:**
   Si vous ne voyez pas `bot.py` list?, c'est qu'il n'est pas ? la racine du repo!

---

## ?? Checklist de V?rification

- [ ] `bot.py` existe ? la **racine** du d?p?t
- [ ] `bot.py` est bien **committ?** sur GitHub
- [ ] La **Start Command** dans Render = `python3 bot.py` ou `python bot.py`
- [ ] Le `render.yaml` pointe vers `bot.py`
- [ ] Les **variables d'environnement** sont configur?es
- [ ] Vous avez **red?ploy?** apr?s les changements

---

## ?? Proc?dure Compl?te de Fix

```bash
# 1. V?rifier la structure locale
cd votre-projet
ls -la

# Vous DEVEZ voir bot.py ici

# 2. Si bot.py n'est pas ? la racine
# D?placez-le (exemple si dans src/)
mv src/bot.py .

# 3. V?rifier render.yaml
cat render.yaml | grep startCommand
# Doit afficher: startCommand: python3 bot.py

# 4. Si besoin de corriger render.yaml
nano render.yaml
# Changez startCommand pour: python3 bot.py

# 5. Commiter et pusher
git add .
git commit -m "Fix: bot.py at root with correct start command"
git push origin main

# 6. Sur Render Dashboard
# ? Manual Deploy ? Deploy latest commit
```

---

## ?? Configuration Render Correcte

### Dans render.yaml:
```yaml
services:
  - type: worker
    name: discord-bot-ia
    env: python
    region: frankfurt
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python3 bot.py        # ? Correct!
    envVars:
      - key: DISCORD_TOKEN
        sync: false
      - key: GROQ_API_KEY
        sync: false
      - key: AI_MODEL
        value: llama-3.1-70b-versatile
```

### OU dans Dashboard Render (Settings):
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python3 bot.py`

---

## ?? Pourquoi cette erreur?

Render cherche `discord_bot_main.py` probablement parce que:

1. ? Vous avez une **Start Command incorrecte**
2. ? Le fichier `bot.py` n'est **pas ? la racine** du repo
3. ? Le fichier n'a **pas ?t? committ?** sur GitHub
4. ? Mauvaise configuration dans `render.yaml`

---

## ? Apr?s le Fix

Une fois corrig?, vous devriez voir dans les logs:

```
Building...
Installing dependencies...
Successfully installed discord.py-2.3.2 aiohttp-3.9.1 python-dotenv-1.0.0

Starting...
?? D?marrage du bot Discord IA avec Groq...
?? Mod?le: llama-3.1-70b-versatile
?? Personnalit?s: 8
? Commandes Slash activ?es!
?? BotName est connect? et pr?t!
? 6 commandes slash synchronis?es!
```

---

## ?? ?a ne marche toujours pas?

### Essayez cette approche alternative:

1. **Supprimez le service sur Render**
   - Dashboard ? Votre service ? Settings ? Delete Service

2. **Recr?ez MANUELLEMENT (pas avec Blueprint)**
   - New + ? **Background Worker** (pas Blueprint!)
   - Connectez le repo GitHub
   - Configuration manuelle:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python3 bot.py`
   - Ajoutez les variables d'environnement
   - Create Worker

3. **V?rifiez les logs**

---

## ?? Besoin d'Aide Suppl?mentaire?

Si le probl?me persiste:

1. **V?rifiez les logs complets** dans Render
2. **Copiez l'erreur exacte**
3. **V?rifiez votre structure** GitHub (partagez `ls -la`)

**Alternative**: Utilisez **Oracle Cloud (gratuit)** ou **Raspberry Pi** pour un contr?le total
? Voir `HEBERGEMENT_24_7.md`

---

## ?? R?sum? Ultra-Rapide

```bash
# 1. bot.py ? la racine
ls bot.py  # Doit exister

# 2. V?rifier render.yaml
grep "startCommand" render.yaml
# ? startCommand: python3 bot.py

# 3. Commiter
git add .
git commit -m "Fix structure"
git push

# 4. Render Dashboard
# Settings ? Start Command ? python3 bot.py
# Manual Deploy
```

**C'est r?gl?!** ??
