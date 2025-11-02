# ?? Guide d'Installation Complet

## ?? Erreur courante: "Aucun fichier requirements.txt"

Cette erreur signifie que vous n'?tes **pas dans le bon r?pertoire** dans votre terminal.

## ?? Installation Pas ? Pas

### ?tape 1: T?l?charger/Cloner le projet

Si vous avez clon? depuis Git:
```bash
git clone <url-du-repo>
cd <nom-du-dossier>
```

Si vous avez t?l?charg? les fichiers:
```bash
# Naviguez vers le dossier o? se trouvent les fichiers
cd /chemin/vers/le/dossier/du/bot
```

### ?tape 2: V?rifier que vous ?tes au bon endroit

```bash
# Listez les fichiers
ls

# Vous devriez voir:
# bot.py
# requirements.txt
# .env.example
# README.md
# etc.
```

**Important**: Vous DEVEZ ?tre dans le dossier contenant tous ces fichiers!

### ?tape 3: Cr?er l'environnement virtuel (RECOMMAND?)

#### Sur Linux/Mac:
```bash
# Cr?er l'environnement virtuel
python3 -m venv venv

# L'activer
source venv/bin/activate

# Votre prompt devrait maintenant afficher (venv)
```

#### Sur Windows:
```cmd
# Cr?er l'environnement virtuel
python -m venv venv

# L'activer
venv\Scripts\activate.bat

# Votre prompt devrait maintenant afficher (venv)
```

### ?tape 4: Installer les d?pendances

```bash
# S'assurer que pip est ? jour
pip install --upgrade pip

# Installer les d?pendances
pip install -r requirements.txt
```

Vous devriez voir:
```
Collecting discord.py>=2.3.2
Collecting python-dotenv>=1.0.0
Collecting aiohttp>=3.9.0
Installing collected packages: ...
Successfully installed discord.py-2.3.2 python-dotenv-1.0.0 aiohttp-3.9.1 ...
```

### ?tape 5: Configurer le bot

```bash
# Copier le fichier de configuration
cp .env.example .env

# Sur Windows, utilisez:
# copy .env.example .env
```

Puis ?ditez `.env` avec vos tokens:

#### Sur Linux/Mac:
```bash
nano .env
# ou
vim .env
# ou
code .env  # Si vous avez VSCode
```

#### Sur Windows:
```cmd
notepad .env
```

Ajoutez:
```env
DISCORD_TOKEN=votre_token_discord_ici
GROQ_API_KEY=votre_cle_groq_ici
AI_MODEL=llama-3.1-70b-versatile
```

### ?tape 6: Lancer le bot

```bash
python bot.py
```

Ou utilisez les scripts fournis:

#### Linux/Mac:
```bash
./start.sh
```

#### Windows:
```cmd
start.bat
```
Ou double-cliquez sur `start.bat`

## ? V?rification de l'installation

### V?rifier que Python est install?:
```bash
python --version
# ou
python3 --version

# Devrait afficher: Python 3.8.x ou sup?rieur
```

### V?rifier que pip fonctionne:
```bash
pip --version
# ou
pip3 --version
```

### V?rifier la structure des fichiers:
```bash
ls -la

# Vous devriez voir:
# bot.py
# requirements.txt
# .env.example
# README.md
# GUIDE_RAPIDE.md
# etc.
```

### V?rifier les d?pendances install?es:
```bash
pip list

# Devrait inclure:
# discord.py
# aiohttp
# python-dotenv
```

## ?? R?solution des probl?mes courants

### "Aucun fichier requirements.txt"

**Cause**: Vous n'?tes pas dans le bon r?pertoire

**Solution**:
```bash
# Trouvez o? sont les fichiers
find ~ -name "bot.py" -type f 2>/dev/null

# Allez dans ce dossier
cd /chemin/trouv?/

# V?rifiez
ls
```

### "Python n'est pas reconnu"

**Cause**: Python n'est pas install? ou pas dans le PATH

**Solution**:
- **Windows**: T?l?chargez depuis https://www.python.org/ 
  - ?? Cochez "Add Python to PATH" pendant l'installation!
- **Linux**: `sudo apt install python3 python3-pip python3-venv`
- **Mac**: `brew install python3`

### "pip n'est pas reconnu"

**Solution**:
```bash
# Linux/Mac
sudo apt install python3-pip
# ou
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Windows
python -m ensurepip --upgrade
```

### "Permission denied" sur Linux/Mac

**Solution**:
```bash
# Rendre le script ex?cutable
chmod +x start.sh

# Puis le lancer
./start.sh
```

### "Module discord not found"

**Cause**: Les d?pendances ne sont pas install?es

**Solution**:
```bash
# V?rifiez que vous ?tes dans le bon dossier
ls requirements.txt

# R?installez
pip install -r requirements.txt
```

### Erreur lors de l'installation de discord.py

**Solution**:
```bash
# Installer les d?pendances syst?me (Linux)
sudo apt-get install python3-dev libffi-dev

# Puis r?essayer
pip install -r requirements.txt
```

## ?? Structure du projet attendue

```
votre-dossier-bot/
??? bot.py                    ? Fichier principal
??? requirements.txt          ? D?pendances
??? .env.example             ? Template configuration
??? .env                     ? Votre configuration (? cr?er)
??? README.md                ? Documentation
??? GUIDE_RAPIDE.md         
??? DEMARRAGE.md
??? HEBERGEMENT_24_7.md
??? SLASH_COMMANDS.md
??? NOUVEAUTES.md
??? INSTALLATION.md          ? Ce fichier
??? config.json
??? start.sh                 ? Script Linux/Mac
??? start.bat                ? Script Windows
??? .gitignore
??? venv/                    ? Environnement virtuel (cr?? par vous)
```

## ?? Commandes essentielles r?capitulatives

### Installation compl?te (Linux/Mac):
```bash
# 1. Aller dans le dossier
cd /chemin/vers/bot

# 2. Cr?er environnement virtuel
python3 -m venv venv

# 3. Activer
source venv/bin/activate

# 4. Installer d?pendances
pip install -r requirements.txt

# 5. Configurer
cp .env.example .env
nano .env  # Ajoutez vos tokens

# 6. Lancer
python bot.py
```

### Installation compl?te (Windows):
```cmd
REM 1. Aller dans le dossier
cd C:\chemin\vers\bot

REM 2. Cr?er environnement virtuel
python -m venv venv

REM 3. Activer
venv\Scripts\activate.bat

REM 4. Installer d?pendances
pip install -r requirements.txt

REM 5. Configurer
copy .env.example .env
notepad .env

REM 6. Lancer
python bot.py
```

## ?? Besoin d'aide?

Si vous avez toujours des probl?mes:

1. **V?rifiez votre emplacement**:
   ```bash
   pwd    # Linux/Mac
   cd     # Windows
   ```

2. **Listez les fichiers**:
   ```bash
   ls -la  # Linux/Mac
   dir     # Windows
   ```

3. **V?rifiez Python**:
   ```bash
   python --version
   which python  # Linux/Mac
   where python  # Windows
   ```

4. **Consultez les logs** si le bot se lance mais plante:
   - Regardez les messages d'erreur dans le terminal
   - V?rifiez que vos tokens sont corrects dans `.env`

## ?? Documentation compl?mentaire

- **README.md** - Documentation principale
- **GUIDE_RAPIDE.md** - Installation en 5 minutes
- **DEMARRAGE.md** - Premier d?marrage
- **SLASH_COMMANDS.md** - Guide des commandes
- **HEBERGEMENT_24_7.md** - H?bergement permanent

## ? Checklist avant de lancer

- [ ] Python 3.8+ install?
- [ ] Vous ?tes dans le bon dossier (vous voyez bot.py)
- [ ] Environnement virtuel cr?? et activ? (optionnel mais recommand?)
- [ ] D?pendances install?es (`pip install -r requirements.txt`)
- [ ] Fichier `.env` cr?? avec vos tokens
- [ ] Token Discord valide
- [ ] Cl? API Groq valide
- [ ] Bot invit? sur votre serveur avec `applications.commands`

**Si tout est coch?, lancez simplement**: `python bot.py` ??
