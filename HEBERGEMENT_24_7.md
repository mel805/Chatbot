# ?? Guide d'H?bergement 24/7

Ce guide vous explique comment garder votre bot Discord en ligne 24h/24 et 7j/7.

## ?? Table des mati?res

1. [Solutions d'h?bergement](#solutions-dh?bergement)
2. [Option 1: VPS Linux (Recommand?)](#option-1-vps-linux-recommand?)
3. [Option 2: Raspberry Pi](#option-2-raspberry-pi)
4. [Option 3: H?bergement cloud gratuit](#option-3-h?bergement-cloud-gratuit)
5. [Option 4: Votre PC personnel](#option-4-votre-pc-personnel)

---

## Solutions d'h?bergement

### Comparaison rapide

| Solution | Co?t | Difficult? | Fiabilit? | Recommand? |
|----------|------|-----------|-----------|------------|
| VPS (Oracle, Contabo) | Gratuit - 5?/mois | Moyenne | ????? | ? Oui |
| Raspberry Pi | 40-100? (une fois) | Facile | ???? | ? Oui |
| Cloud gratuit (Render, Railway) | Gratuit | Facile | ??? | ?? Limit? |
| PC personnel | Gratuit | Tr?s facile | ?? | ? Non |

---

## Option 1: VPS Linux (Recommand?) ??

Un VPS (Virtual Private Server) est la meilleure solution pour un bot 24/7.

### Fournisseurs recommand?s

#### 1. Oracle Cloud (GRATUIT ? vie!) ?
- **Prix**: GRATUIT pour toujours
- **Specs**: 1-4 CPU, 1-24 GB RAM, 50 GB stockage
- **Site**: https://www.oracle.com/cloud/free/

#### 2. Contabo
- **Prix**: ~5?/mois
- **Specs**: 4 CPU, 8 GB RAM, 200 GB SSD
- **Site**: https://contabo.com/

#### 3. DigitalOcean
- **Prix**: 5$/mois (200$ de cr?dit gratuit)
- **Site**: https://www.digitalocean.com/

### Installation sur VPS Ubuntu/Debian

#### ?tape 1: Se connecter au VPS

```bash
ssh root@votre_ip_vps
```

#### ?tape 2: Installer Python et les d?pendances

```bash
# Mettre ? jour le syst?me
sudo apt update && sudo apt upgrade -y

# Installer Python et pip
sudo apt install python3 python3-pip python3-venv git -y

# V?rifier l'installation
python3 --version
pip3 --version
```

#### ?tape 3: Cloner votre bot

```bash
# Cr?er un dossier pour le bot
cd /home
mkdir discord-bot
cd discord-bot

# Si vous utilisez git
git clone <votre-repo> .

# Ou transf?rer les fichiers avec scp depuis votre PC:
# scp -r /chemin/local/* root@votre_ip:/home/discord-bot/
```

#### ?tape 4: Installer les d?pendances Python

```bash
# Cr?er un environnement virtuel
python3 -m venv venv

# L'activer
source venv/bin/activate

# Installer les d?pendances
pip install -r requirements.txt
```

#### ?tape 5: Configurer le bot

```bash
# Cr?er le fichier .env
nano .env

# Ajoutez:
# DISCORD_TOKEN=votre_token
# GROQ_API_KEY=votre_cle_groq
# AI_MODEL=llama-3.1-70b-versatile

# Sauvegarder: CTRL+X, puis Y, puis Entr?e
```

#### ?tape 6: Tester le bot

```bash
python3 bot.py
```

Si ?a fonctionne, passez ? l'?tape suivante!

#### ?tape 7: Cr?er un service systemd (d?marrage automatique)

```bash
# Cr?er le fichier de service
sudo nano /etc/systemd/system/discord-bot.service
```

Collez ce contenu:

```ini
[Unit]
Description=Discord Bot IA
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/discord-bot
Environment="PATH=/home/discord-bot/venv/bin"
ExecStart=/home/discord-bot/venv/bin/python3 /home/discord-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Sauvegarder et activer:

```bash
# Recharger systemd
sudo systemctl daemon-reload

# Activer le service au d?marrage
sudo systemctl enable discord-bot

# D?marrer le service
sudo systemctl start discord-bot

# V?rifier le statut
sudo systemctl status discord-bot
```

#### ?tape 8: Commandes utiles

```bash
# Voir les logs en temps r?el
sudo journalctl -u discord-bot -f

# Arr?ter le bot
sudo systemctl stop discord-bot

# Red?marrer le bot
sudo systemctl restart discord-bot

# Voir le statut
sudo systemctl status discord-bot
```

? **Votre bot est maintenant en ligne 24/7!**

---

## Option 2: Raspberry Pi

Un Raspberry Pi est parfait pour h?berger un bot Discord.

### Mat?riel n?cessaire

- Raspberry Pi 4 (2GB RAM minimum, 4GB recommand?) - ~60?
- Carte SD (16GB minimum) - ~10?
- Alimentation officielle - ~10?
- Bo?tier (optionnel) - ~10?

### Installation

1. **Installer Raspberry Pi OS**
   - T?l?chargez Raspberry Pi Imager
   - Installez Raspberry Pi OS Lite (64-bit)

2. **Configuration initiale**
   ```bash
   sudo raspi-config
   # Configurez le WiFi, changez le mot de passe, etc.
   ```

3. **Suivez les m?mes ?tapes que le VPS** (ci-dessus) ? partir de l'?tape 2

### Avantages
- ? Co?t unique, pas d'abonnement
- ? Faible consommation ?lectrique (~3?/an)
- ? Contr?le total

### Inconv?nients
- ? D?pend de votre connexion internet
- ? Pas de backup automatique

---

## Option 3: H?bergement Cloud Gratuit

### Render.com (Gratuit avec limitations)

**Limitations**: Le bot se met en veille apr?s 15 min d'inactivit?.

#### Installation

1. Cr?ez un compte sur https://render.com
2. Cr?ez un nouveau "Web Service"
3. Connectez votre d?p?t GitHub
4. Configuration:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
5. Ajoutez vos variables d'environnement:
   - `DISCORD_TOKEN`
   - `GROQ_API_KEY`

?? **Note**: Le plan gratuit a des limitations. Pour ?viter la mise en veille, vous devrez upgrader.

### Railway.app

Similaire ? Render, avec 5$ de cr?dit gratuit par mois.

### Replit

- Gratuit avec limitations
- Le bot peut se d?connecter r?guli?rement
- Pas id?al pour du 24/7

---

## Option 4: Votre PC Personnel

?? **Non recommand?** pour du 24/7, mais fonctionne pour des tests.

### Windows

#### Option A: Terminal toujours ouvert (simple mais pas fiable)

```bash
python bot.py
```

Gardez le terminal ouvert. ? Se ferme si vous ?teignez votre PC.

#### Option B: T?che planifi?e Windows

1. Cr?ez un fichier `start_bot.bat`:
```batch
@echo off
cd C:\chemin\vers\votre\bot
python bot.py
```

2. Cr?ez une t?che planifi?e:
   - Ouvrez "Planificateur de t?ches"
   - Cr?ez une t?che de base
   - D?clencheur: "Au d?marrage"
   - Action: D?marrer le fichier `.bat`

### Linux/Mac

Ajoutez au crontab:

```bash
crontab -e
```

Ajoutez:
```
@reboot cd /chemin/vers/bot && python3 bot.py
```

---

## ?? Mise ? jour du bot

### Sur VPS/Raspberry Pi

```bash
# Se connecter
ssh user@votre_ip

# Aller dans le dossier
cd /home/discord-bot

# Arr?ter le bot
sudo systemctl stop discord-bot

# Mettre ? jour le code
git pull
# Ou transf?rer les nouveaux fichiers

# Mettre ? jour les d?pendances si n?cessaire
source venv/bin/activate
pip install -r requirements.txt

# Red?marrer
sudo systemctl start discord-bot
```

---

## ??? S?curit?

### Bonnes pratiques

1. **Ne jamais exposer votre .env**
   ```bash
   chmod 600 .env  # Permissions limit?es
   ```

2. **Utiliser un utilisateur non-root** (recommand?)
   ```bash
   # Cr?er un utilisateur
   sudo adduser botuser
   
   # D?placer le bot
   sudo mv /home/discord-bot /home/botuser/
   sudo chown -R botuser:botuser /home/botuser/discord-bot
   
   # Modifier le service systemd pour utiliser User=botuser
   ```

3. **Configurer un firewall**
   ```bash
   sudo apt install ufw
   sudo ufw allow ssh
   sudo ufw enable
   ```

4. **Sauvegardes r?guli?res**
   ```bash
   # Sauvegarder le dossier
   tar -czf bot-backup-$(date +%Y%m%d).tar.gz /home/discord-bot
   ```

---

## ?? Monitoring

### Voir les logs

```bash
# Logs en temps r?el
sudo journalctl -u discord-bot -f

# Derni?res 100 lignes
sudo journalctl -u discord-bot -n 100

# Logs depuis aujourd'hui
sudo journalctl -u discord-bot --since today
```

### V?rifier l'utilisation des ressources

```bash
# CPU et RAM
htop

# Espace disque
df -h

# Trafic r?seau
vnstat
```

---

## ? FAQ

**Q: Mon bot se d?connecte r?guli?rement**
- V?rifiez les logs: `sudo journalctl -u discord-bot -n 100`
- Assurez-vous que le service est configur? avec `Restart=always`

**Q: Comment savoir si mon bot est en ligne?**
- Regardez son statut sur Discord
- Ou: `sudo systemctl status discord-bot`

**Q: Le bot utilise beaucoup de RAM**
- Normal si beaucoup de conversations
- Utilisez `!reset` pour vider l'historique
- R?duisez `MAX_HISTORY` dans le code

**Q: Combien co?te l'?lectricit??**
- Raspberry Pi: ~3?/an
- PC: ~50-100?/an
- VPS: inclus dans le prix

---

## ?? Conclusion

Pour un bot 24/7 professionnel, nous recommandons:

1. **?? VPS Oracle Cloud** (gratuit!) ou Contabo (5?/mois)
2. **?? Raspberry Pi** (si vous avez une bonne connexion)
3. **?? Render/Railway** (pour d?buter avec limitations)

Besoin d'aide? Consultez le README.md principal!
