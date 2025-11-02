# ?? FIX: "DISCORD_TOKEN non trouv? dans le fichier .env"

## ?? Le Probl?me

Vous voyez cette erreur sur Render:
```
? ERREUR: DISCORD_TOKEN non trouv? dans le fichier .env
Veuillez cr?er un fichier .env avec votre token Discord
```

**MAIS** vous avez bien configur? `DISCORD_TOKEN` dans les variables d'environnement Render!

---

## ?? Pourquoi cette erreur?

Sur Render, il n'y a **pas de fichier `.env`** - les variables d'environnement sont configur?es via le Dashboard.

Le bot a ?t? mis ? jour pour fonctionner avec les deux m?thodes:
- ? **En local**: Fichier `.env`
- ? **Sur Render**: Variables d'environnement du Dashboard

---

## ? Solutions

### Solution 1: V?rifier que les variables sont bien configur?es

1. **Dashboard Render** ? Votre service
2. **Settings** ? **Environment**
3. V?rifiez que vous avez:

```
DISCORD_TOKEN = MTk... (ou ODc...)
GROQ_API_KEY = gsk_...
```

**?? IMPORTANT**: 
- Pas d'espaces avant ou apr?s le token!
- Le token doit ?tre complet
- Pas de guillemets autour

### Solution 2: Red?ployer apr?s avoir configur? les variables

1. **Ajoutez/V?rifiez les variables** dans Settings ? Environment
2. **Save Changes**
3. **Manual Deploy** ? Deploy latest commit
4. **V?rifiez les logs**

### Solution 3: Pousser le code mis ? jour

J'ai corrig? le message d'erreur dans `bot.py`. Poussez la mise ? jour:

```bash
git add bot.py
git commit -m "Fix: Support Render environment variables"
git push
```

Render red?ploiera automatiquement.

---

## ?? V?rification des Variables

### Comment v?rifier que Render a bien les variables?

Dans les **logs de d?ploiement**, vous devriez voir:

```
? Building...
? Installing dependencies...
? Starting service...
?? D?marrage du bot Discord IA avec Groq...
```

Si vous voyez l'erreur "DISCORD_TOKEN non trouv?", c'est que la variable n'est pas configur?e correctement.

---

## ?? Configuration Correcte des Variables

### Sur Render Dashboard:

1. **Votre service** ? **Environment**
2. **Add Environment Variable**

**Variable 1:**
```
Key: DISCORD_TOKEN
Value: [Collez votre token sans espaces]
```

**Exemple de token valide:**
```
[Votre token commence g?n?ralement par MTk... ou ODc... suivi d'une longue cha?ne]
```

**Variable 2:**
```
Key: GROQ_API_KEY
Value: [Collez votre cl? Groq]
```

**Exemple de cl? valide:**
```
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
```

### ?? Erreurs Communes

? **Mauvais:**
```
DISCORD_TOKEN =  MTk... (espace apr?s =)
DISCORD_TOKEN="MTk..." (guillemets)
DISCORD_TOKEN=MTk...  (espace ? la fin)
```

? **Bon:**
```
DISCORD_TOKEN=MTk7NjIzODQyNzE2ODc0ODU0NA.GxYz8a.K5nP_3aQ7R...
```
(pas d'espaces, pas de guillemets)

---

## ?? Debug: Tester si les variables sont charg?es

### M?thode 1: Ajouter un print temporaire

Dans `bot.py`, apr?s les variables d'environnement, ajoutez:

```python
# DEBUG - ? supprimer apr?s v?rification
print(f"DEBUG: DISCORD_TOKEN pr?sent: {bool(DISCORD_TOKEN)}")
print(f"DEBUG: GROQ_API_KEY pr?sent: {bool(GROQ_API_KEY)}")
if DISCORD_TOKEN:
    print(f"DEBUG: Token commence par: {DISCORD_TOKEN[:5]}...")
```

Puis v?rifiez les logs Render.

### M?thode 2: V?rifier depuis le Shell Render

1. Dashboard ? Votre service ? **Shell**
2. Tapez:
```bash
echo $DISCORD_TOKEN
echo $GROQ_API_KEY
```

Si rien ne s'affiche, les variables ne sont pas configur?es.

---

## ?? Proc?dure Compl?te de Fix

```bash
# 1. Localement, mettez ? jour le code (d?j? fait)
git pull  # Si vous travaillez en ?quipe

# 2. Le code a ?t? mis ? jour pour supporter Render
# V?rifiez que vous avez la derni?re version

# 3. Poussez sur GitHub
git add .
git commit -m "Fix: Environment variables support for Render"
git push

# 4. Sur Render Dashboard:
# ? Settings ? Environment
# ? V?rifiez DISCORD_TOKEN et GROQ_API_KEY
# ? Save Changes
# ? Manual Deploy ? Deploy latest commit

# 5. V?rifiez les logs
# ? Dashboard ? Logs
# ? Devrait afficher: "?? D?marrage du bot..."
```

---

## ?? Si ?a ne marche toujours pas

### V?rification 1: Le token Discord est valide

1. Allez sur https://discord.com/developers/applications
2. S?lectionnez votre application
3. **Bot** ? **Reset Token**
4. Copiez le **nouveau token**
5. Mettez-le dans Render Environment Variables
6. Red?ployez

### V?rification 2: Les Intents sont activ?s

Sur Discord Developer Portal:
- ? **Privileged Gateway Intents** ? Message Content Intent
- ? **Privileged Gateway Intents** ? Server Members Intent

### V?rification 3: Cr?er le service manuellement

Si le probl?me persiste:

1. **Supprimez le service** sur Render
2. **Recr?ez-le manuellement**:
   - New + ? Background Worker
   - Connectez le repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python3 bot.py`
   - **Avant de cr?er**, ajoutez les variables d'environnement
   - Create Worker

---

## ?? Diff?rences Local vs Render

### En Local (sur votre PC):
```
? Vous avez un fichier .env
? load_dotenv() charge ce fichier
? Les variables sont accessibles via os.getenv()
```

### Sur Render:
```
? PAS de fichier .env
? Variables configur?es dans le Dashboard
? Render les injecte automatiquement dans l'environnement
? os.getenv() les lit directement
? load_dotenv() ne fait rien (normal, pas de .env)
```

---

## ? Confirmation que ?a fonctionne

Logs Render corrects:
```
==> Starting service with command: python3 bot.py
?? D?marrage du bot Discord IA avec Groq...
?? Mod?le: llama-3.1-70b-versatile
?? Personnalit?s: 8
? Commandes Slash activ?es!
?? [VotreBotName] est connect? et pr?t!
?? Connect? ? X serveur(s)
? 6 commandes slash synchronis?es!
```

Sur Discord:
```
? Bot en ligne (pastille verte)
? /start fonctionne
? Le bot r?pond aux mentions
```

---

## ?? S?curit?

**Important:**
- ?? Ne JAMAIS commiter le fichier `.env` sur GitHub
- ? `.env` est d?j? dans `.gitignore`
- ? Sur Render, les variables sont s?curis?es et chiffr?es

---

## ?? R?sum? Ultra-Rapide

```
1. Dashboard Render ? Settings ? Environment
2. V?rifier DISCORD_TOKEN (sans espaces, sans guillemets)
3. V?rifier GROQ_API_KEY
4. Save Changes
5. Manual Deploy
6. V?rifier les logs
```

**Si l'erreur persiste**: Copiez les logs complets et v?rifiez que le token commence bien par `MTk` ou `ODc`.

---

## ?? Alternative: Oracle Cloud (Gratuit ? vie)

Si vous rencontrez trop de probl?mes avec Render:
- **Oracle Cloud** offre un VPS gratuit ? vie
- Pas de limitations, contr?le total
- Voir le guide complet dans **`HEBERGEMENT_24_7.md`**

---

? **Avec ces corrections, votre bot devrait d?marrer correctement sur Render!**
