# ?? DEBUG: DISCORD_TOKEN non trouv? sur Render

## ?? ?tapes de V?rification D?taill?es

### ?tape 1: V?rifier la Configuration sur Render

1. **Allez sur** https://dashboard.render.com

2. **Cliquez sur votre service** (discord-bot-ia ou le nom que vous avez donn?)

3. **Dans le menu de gauche, cliquez sur "Environment"**

4. **V?rifiez EXACTEMENT ce qui suit:**

   Vous DEVEZ voir une ligne comme:
   ```
   DISCORD_TOKEN    [Secret]    [Edit] [Delete]
   ```

   Si vous NE voyez PAS cette ligne ? La variable n'est PAS configur?e!

### ?tape 2: Ajouter/Modifier la Variable

#### Si la variable n'existe PAS:

1. **Cliquez sur "Add Environment Variable"**

2. **Remplissez:**
   ```
   Key:   DISCORD_TOKEN
   Value: [Collez votre nouveau token Discord ici]
   ```

3. **ATTENTION:**
   - Pas d'espaces avant le token
   - Pas d'espaces apr?s le token
   - Pas de guillemets ""
   - Pas d'apostrophes ''
   - Juste le token brut

4. **Cliquez "Save Changes"**

#### Si la variable existe d?j?:

1. **Cliquez sur "Edit"** ? c?t? de DISCORD_TOKEN

2. **V?rifiez/Remplacez la valeur:**
   ```
   Value: [Votre nouveau token]
   ```

3. **Cliquez "Save"**

### ?tape 3: M?me chose pour GROQ_API_KEY

R?p?tez pour GROQ_API_KEY:
```
Key:   GROQ_API_KEY
Value: [Votre cl? Groq]
```

### ?tape 4: Sauvegarder et Red?ployer

1. **Apr?s avoir ajout?/modifi? les variables:**
   - Cliquez sur "Save Changes" en haut de la page

2. **Allez dans l'onglet "Manual Deploy"** (en haut)

3. **Cliquez sur "Deploy latest commit"**

4. **Attendez le d?ploiement** (1-2 minutes)

### ?tape 5: V?rifier les Logs

1. **Cliquez sur l'onglet "Logs"**

2. **Vous devriez voir:**
   ```
   ==> Cloning repository...
   ==> Running build command...
   ==> Starting service...
   ?? D?marrage du bot Discord IA avec Groq...
   ```

   **SI vous voyez toujours:**
   ```
   ? ERREUR: DISCORD_TOKEN non trouv?
   ```
   ? Les variables ne sont PAS correctement configur?es!

---

## ?? Debug Avanc?

### Option 1: V?rifier via le Shell Render

1. **Onglet "Shell"** sur Render

2. **Tapez:**
   ```bash
   echo $DISCORD_TOKEN
   ```

3. **Si rien ne s'affiche** ? La variable n'est pas configur?e!

4. **Si le token s'affiche** ? Le probl?me est ailleurs

### Option 2: V?rifier le Type de Service

Le service DOIT ?tre un **"Background Worker"**, PAS un "Web Service"!

1. V?rifiez dans les settings
2. Si c'est un Web Service, recr?ez-le en Background Worker

---

## ?? Erreurs Courantes

### Erreur 1: Espaces dans la valeur

? MAUVAIS:
```
DISCORD_TOKEN = MTk...    (espace apr?s =)
DISCORD_TOKEN= MTk...     (espace avant le token)
DISCORD_TOKEN=MTk...      (espace ? la fin)
```

? BON:
```
DISCORD_TOKEN=MTk7NjIzODQyNzE2ODc0ODU0NA.GxYz8a...
```

### Erreur 2: Guillemets

? MAUVAIS:
```
DISCORD_TOKEN="MTk..."
DISCORD_TOKEN='MTk...'
```

? BON:
```
DISCORD_TOKEN=MTk...
```

### Erreur 3: Variable dans le mauvais service

Si vous avez plusieurs services Render, assurez-vous d'?tre dans le BON service!

### Erreur 4: Pas de red?ploiement apr?s ajout

Apr?s avoir ajout?/modifi? des variables, vous DEVEZ red?ployer!

---

## ?? Checklist Compl?te

Cochez chaque ?tape:

- [ ] J'ai cr?? un NOUVEAU token Discord (l'ancien est compromis)
- [ ] Je suis sur dashboard.render.com
- [ ] J'ai s?lectionn? le BON service
- [ ] J'ai cliqu? sur "Environment" dans le menu
- [ ] J'ai ajout? DISCORD_TOKEN avec "Add Environment Variable"
- [ ] J'ai coll? le token SANS espaces ni guillemets
- [ ] J'ai ajout? GROQ_API_KEY de la m?me mani?re
- [ ] J'ai cliqu? "Save Changes"
- [ ] J'ai fait "Manual Deploy" ? "Deploy latest commit"
- [ ] J'ai attendu la fin du d?ploiement
- [ ] J'ai v?rifi? les logs

---

## ?? Si ?a ne marche TOUJOURS pas

### Solution Radicale: Recr?er le Service

1. **Supprimez le service actuel:**
   - Settings ? Delete Service

2. **Cr?ez un nouveau service:**
   - New + ? **Background Worker** (PAS Web Service!)
   - Connectez votre repo GitHub: mel805/Chatbot
   - Branch: cursor/cr-er-un-bot-discord-nsfw-immersif-9882

3. **AVANT de cliquer "Create Worker":**
   - Scrollez vers "Environment Variables"
   - Ajoutez DISCORD_TOKEN
   - Ajoutez GROQ_API_KEY

4. **Configuration:**
   ```
   Build Command:  pip install -r requirements.txt
   Start Command:  python3 bot.py
   ```

5. **Cliquez "Create Worker"**

---

## ?? Captures d'?cran de ce que vous devez voir

### Dans Environment:
```
Environment Variables

DISCORD_TOKEN    [Secret]    [Edit] [Delete]
GROQ_API_KEY     [Secret]    [Edit] [Delete]
AI_MODEL         llama-3.... [Edit] [Delete]

[+ Add Environment Variable]
```

### Dans les Logs (succ?s):
```
==> Starting service with command: python3 bot.py
?? D?marrage du bot Discord IA avec Groq...
?? Mod?le: llama-3.1-70b-versatile
?? Personnalit?s: 8
? Commandes Slash activ?es!
?? [NomDuBot] est connect? et pr?t!
```

---

## ?? Test Final

Pour ?tre S?R que les variables sont l?, faites ce test:

1. **Shell Render**
2. Tapez:
   ```bash
   printenv | grep DISCORD
   printenv | grep GROQ
   ```

3. Vous devriez voir:
   ```
   DISCORD_TOKEN=MTk...
   GROQ_API_KEY=gsk_...
   ```

Si vous ne voyez RIEN ? Les variables ne sont PAS configur?es!

---

? Suivez ces ?tapes une par une et confirmez ? chaque ?tape!
