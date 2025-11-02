# ?? Votre Bot Discord IA est Pr?t!

## ?? D?marrage Ultra-Rapide

### Windows
Double-cliquez sur **`start.bat`**

### Linux/Mac
```bash
./start.sh
```

Ou manuellement:
```bash
python bot.py
```

---

## ? Configuration Minimale Requise

Avant de d?marrer, assurez-vous d'avoir:

### 1. Token Discord ?
- Allez sur https://discord.com/developers/applications
- Cr?ez une application et un bot
- Copiez le token
- Activez "Message Content Intent"

### 2. Cl? API Groq (GRATUIT) ?
- Allez sur https://console.groq.com
- Cr?ez un compte gratuit
- Cr?ez une cl? API
- Copiez-la

### 3. Fichier .env ?
Cr?ez un fichier `.env` avec:
```env
DISCORD_TOKEN=votre_token_discord
GROQ_API_KEY=votre_cle_groq
AI_MODEL=llama-3.1-70b-versatile
```

---

## ?? Premi?re Utilisation

### 1. Inviter le bot
Utilisez l'URL OAuth2 depuis le portail Discord Developer

### 2. Activer le bot (ADMIN UNIQUEMENT)
Sur Discord, dans un canal:
```
/start
```

### 3. Tester
```
@VotreBot Salut!
```

### 4. Changer de personnalit?
```
/personality seducteur
```

---

## ?? 8 Personnalit?s Disponibles

| Commande | Personnalit? |
|----------|--------------|
| `/personality amical` | ?? Sympathique (d?faut) |
| `/personality seducteur` | ?? Charmant et flirteur |
| `/personality coquin` | ?? Os? et provocateur |
| `/personality romantique` | ?? Doux et passionn? |
| `/personality dominant` | ?? Confiant et autoritaire |
| `/personality soumis` | ?? Respectueux et d?vou? |
| `/personality joueur` | ?? Fun et gamer |
| `/personality intellectuel` | ?? Cultiv? et profond |

---

## ?? Commandes Essentielles

### Admin uniquement
```
/start              ? Active le bot dans ce canal
/stop               ? D?sactive le bot
/personality        ? Liste les personnalit?s
/personality <nom>  ? Change de personnalit?
/reset              ? R?initialise l'historique
/status             ? Affiche le statut
```

### Tout le monde
```
/help           ? Affiche l'aide
```

---

## ?? Documentation Compl?te

- **README.md** - Documentation compl?te du projet
- **GUIDE_RAPIDE.md** - Installation en 5 minutes
- **HEBERGEMENT_24_7.md** - Guide pour h?bergement 24/7
- **config.json** - Configurations et personnalisations

---

## ?? H?bergement 24/7

Pour garder votre bot en ligne en permanence:

### Option Gratuite ??
**Oracle Cloud** - VPS gratuit ? vie
- Cr?ez un compte sur https://www.oracle.com/cloud/free/
- Suivez le guide dans **HEBERGEMENT_24_7.md**

### Option Budget ??
**Contabo** - 5?/mois, tr?s fiable
- https://contabo.com/

### Option DIY ??
**Raspberry Pi** - ~60? une fois
- 3?/an d'?lectricit?
- Guide complet dans **HEBERGEMENT_24_7.md**

---

## ? Pourquoi Groq?

- **10x Plus Rapide** que Hugging Face ou OpenAI
- **100% Gratuit** avec limites g?n?reuses
- **Moins Censur?** pour conversations adultes
- **Mod?les Puissants** : Llama 3.1, Mixtral, Gemma

---

## ?? S?curit? & Confidentialit?

? Aucune conversation sauvegard?e sur disque
? Tout en RAM (effac? au red?marrage)
? Uniquement les 20 derniers messages gard?s en m?moire
? Contr?le admin pour activation/d?sactivation

---

## ?? Astuces

### D?sactiver temporairement
```
/stop
```

### Effacer l'historique
```
/reset
```

### V?rifier le statut
```
/status
```

### Mod?le plus rapide
Dans `.env`, changez:
```env
AI_MODEL=llama-3.1-8b-instant
```

### Mod?le plus puissant
```env
AI_MODEL=llama-3.2-90b-text-preview
```

---

## ? Probl?mes Courants

### "Le bot ne r?pond pas"
1. Avez-vous fait `/start`? (admin uniquement)
2. L'avez-vous mentionn?? `@Bot`
3. Message Content Intent activ? sur Discord?

### "GROQ_API_KEY non trouv?"
- Cr?ez le fichier `.env`
- Ajoutez votre cl? Groq

### "Le bot se d?connecte"
- Normal si vous ?teignez votre PC
- Pour du 24/7 ? **HEBERGEMENT_24_7.md**

---

## ?? Fonctionnalit?s Principales

? 8 personnalit?s pr?d?finies et personnalisables
? Contr?le admin pour activation par canal
? M?moire contextuelle des conversations
? Support multi-utilisateurs simultan?s
? R?ponses ultra-rapides (Groq)
? 100% gratuit
? Pr?t pour h?bergement 24/7
? Conversations immersives et r?alistes

---

## ?? Bon Chat!

Votre bot est maintenant pr?t ? discuter comme un vrai membre de votre serveur Discord!

**Besoin d'aide?** Consultez les autres fichiers de documentation.

**Amusez-vous bien! ??**
