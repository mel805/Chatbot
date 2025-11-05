# ?? Syst?me de G?n?ration d'Images NSFW

## ?? Fonctionnalit?s

Le bot peut maintenant **g?n?rer des images** pour chaque personnalit? en utilisant l'IA Stable Diffusion!

### ? Caract?ristiques

- ?? **Images personnalis?es** par personnalit? (Luna, Damien, Catherine, etc.)
- ?? **8 styles diff?rents** (Portrait, Casual, ?l?gant, Lingerie, Nu, etc.)
- ?? **Contenu NSFW** support? (uniquement dans channels NSFW)
- ? **G?n?ration en 30-60 secondes**
- ??? **Haute qualit?** (Stable Diffusion XL)

---

## ?? Installation

### 1?? D?pendances

Nouvelle d?pendance ajout?e ? `requirements.txt`:
```
replicate==0.25.1
```

**Render installera automatiquement au prochain d?ploiement.**

---

### 2?? API Key Requise (Replicate)

Pour g?n?rer des images, vous avez besoin d'une **cl? API Replicate**.

#### Obtenir une Cl? API Gratuite:

1. **Cr?ez un compte sur Replicate:**
   - Allez sur https://replicate.com
   - Cliquez "Sign Up"
   - Inscrivez-vous (gratuit)

2. **R?cup?rez votre API Key:**
   - Allez sur https://replicate.com/account/api-tokens
   - Copiez votre token API

3. **Ajoutez-la sur Render:**
   - Dashboard Render ? Votre Service ? **Environment**
   - Cliquez **"Add Environment Variable"**
   - Nom: `REPLICATE_API_KEY`
   - Valeur: `r8_...` (votre token)
   - Cliquez **"Save Changes"**

**Tier Gratuit Replicate:**
- ? Gratuit pour commencer
- ? Cr?dits gratuits inclus
- ? ~100-200 g?n?rations gratuites/mois
- ? Pas de carte de cr?dit requise

---

## ?? Commandes Discord

### `/generer_image`

G?n?re une image de la personnalit? actuelle.

**Syntaxe:**
```
/generer_image style:[style]
```

**Param?tres:**
- `style` - Style de l'image (obligatoire)

**Exemples:**
```
/generer_image style:portrait
/generer_image style:lingerie
/generer_image style:artistic_nude
```

---

### `/galerie`

Affiche tous les styles disponibles avec descriptions.

**Syntaxe:**
```
/galerie
```

Montre:
- ?? Styles standards (SFW)
- ?? Styles NSFW (si channel NSFW)
- ?? Exemples d'utilisation

---

## ?? Styles Disponibles

### ?? Styles Standards (Tous Channels)

| Style | Description | Usage |
|-------|-------------|-------|
| **Portrait** | Photo de portrait classique | `/generer_image style:portrait` |
| **Casual** | Tenue d?contract?e, pose naturelle | `/generer_image style:casual` |
| **Elegant** | Tenue ?l?gante, look sophistiqu? | `/generer_image style:elegant` |
| **Swimsuit** | Maillot de bain, ambiance plage | `/generer_image style:swimsuit` |

---

### ?? Styles NSFW (Channels NSFW Uniquement)

| Style | Description | Usage |
|-------|-------------|-------|
| **Lingerie** | Lingerie sensuelle, pose intime | `/generer_image style:lingerie` |
| **Suggestif** | Pose suggestive, artistique | `/generer_image style:suggestive` |
| **Artistique Nu** | Nu artistique tasteful | `/generer_image style:artistic_nude` |
| **Intime** | Sc?ne intime romantique | `/generer_image style:intimate` |

**?? Important:** Les styles NSFW ne fonctionnent que dans les channels Discord marqu?s NSFW!

---

## ?? Processus de G?n?ration

### ?tape par ?tape

```
1. Utilisateur: /generer_image style:lingerie
2. Bot: "G?n?ration en cours... ?"
   ? Analyse la personnalit? active (ex: Luna)
   ? Construit le prompt Stable Diffusion
   ? Envoie ? l'API Replicate
3. Replicate: G?n?re l'image (30-60s)
4. Bot: Affiche l'image g?n?r?e ?
```

---

## ??? Exemples de Prompts G?n?r?s

### Pour Luna (Femme 25 ans, Coquine):

**Style Portrait:**
```
high quality portrait, beautiful woman, female, feminine, 
25 years old, seductive, alluring, playful, realistic, 
detailed face, professional photography, cinematic lighting, 8k uhd
```

**Style Lingerie:**
```
high quality portrait, beautiful woman, female, feminine, 
25 years old, seductive, alluring, playful, realistic, 
lingerie, sensual pose, bedroom setting, intimate lighting
```

**Style Artistique Nu:**
```
high quality portrait, beautiful woman, female, feminine, 
25 years old, seductive, alluring, playful, realistic, 
artistic nude, tasteful, professional photography, soft lighting, nsfw
```

---

### Pour Damien (Homme 28 ans, S?ducteur):

**Style Portrait:**
```
high quality portrait, handsome man, male, masculine, 
28 years old, seductive, alluring, confident, realistic, 
detailed face, professional photography, cinematic lighting, 8k uhd
```

---

### Pour Catherine (Femme 40 ans, Cougar):

**Style Elegant:**
```
high quality portrait, beautiful woman, female, feminine, 
40 years old, mature, experienced, confident, realistic, 
elegant dress, formal attire, sophisticated
```

---

## ?? Personnalisation par Personnalit?

Le syst?me adapte automatiquement les prompts selon:

- **Genre** (Femme/Homme/Trans/Non-binaire)
- **?ge** (25, 35, 40, 45 ans, etc.)
- **Traits** (Confiant, s?duisant, mature, coquin, etc.)
- **Description** de la personnalit?

**Chaque personnalit? g?n?re des images uniques!**

---

## ?? Qualit? et Param?tres

### Mod?le Utilis?

**Stable Diffusion XL** (SDXL)
- Mod?le de pointe d'image AI
- Haute r?solution
- Excellents d?tails
- Support NSFW

### Param?tres de G?n?ration

```python
width: 768px
height: 1024px (portrait)
guidance_scale: 7.5 (suit bien le prompt)
steps: 30 (bon ?quilibre qualit?/vitesse)
```

### Temps de G?n?ration

- ?? **30-60 secondes** en moyenne
- D?pend de la charge serveur Replicate
- Le bot affiche un message de patience

---

## ?? S?curit? et Restrictions

### 1. Channels NSFW Uniquement

Les styles NSFW ne fonctionnent que dans les channels Discord marqu?s **NSFW**.

**V?rification automatique:**
```python
if style in nsfw_styles:
    if not channel.is_nsfw():
        ? "?? Images NSFW disponibles uniquement dans channels NSFW"
```

---

### 2. Bot Actif Requis

Il faut avoir activ? le bot avec `/start` avant de g?n?rer des images.

---

### 3. Personnalit? Active

Une personnalit? doit ?tre s?lectionn?e (via `/start`).

---

## ?? Co?ts et Limites

### Replicate (API Recommand?e)

**Tier Gratuit:**
- ? ~$5 de cr?dits gratuits
- ? ~100-200 g?n?rations gratuites
- ? Renouvellement mensuel possible

**Prix apr?s gratuit:**
- SDXL: ~$0.02-0.03 par image
- Tr?s abordable pour usage personnel

**Aucune carte de cr?dit requise pour commencer!**

---

### Alternatives (Si Besoin)

Si vous d?passez les limites Replicate:

1. **Hugging Face Inference API** (Gratuit mais plus lent)
2. **Pollinations.ai** (Gratuit mais qualit? variable)
3. **Stability.ai API** (Payant, haute qualit?)
4. **Local avec Ollama + Stable Diffusion** (Gratuit mais n?cessite GPU)

---

## ?? D?ploiement

### Automatique

Le code est pr?t! Il suffit d'ajouter la cl? API:

1. ? Code d?j? pouss? sur GitHub
2. ? Render red?marre automatiquement
3. ? Ajoutez `REPLICATE_API_KEY` dans Environment
4. ? Red?marrez le service (ou attendez auto-deploy)

---

## ?? Test

### Test 1: Commande Galerie

```
/galerie
```

Devrait afficher tous les styles disponibles.

---

### Test 2: G?n?ration Portrait (SFW)

```
/start
[S?lectionnez Luna]

/generer_image style:portrait
```

Devrait g?n?rer un portrait de Luna en 30-60s.

---

### Test 3: G?n?ration NSFW (Channel NSFW)

**Dans un channel NSFW:**
```
/generer_image style:lingerie
```

Devrait g?n?rer une image de la personnalit? en lingerie.

---

## ? D?pannage

### "? API key manquante ou invalide"

**Solution:**
1. V?rifiez que `REPLICATE_API_KEY` est dans Render Environment
2. V?rifiez que le token commence par `r8_`
3. Red?marrez le service Render

---

### "? G?n?ration ?choue apr?s 60s"

**Causes possibles:**
- Replicate surcharg? (r?essayez)
- Limite de taux d?pass?e (attendez 5 min)
- Cr?dits gratuits ?puis?s (v?rifiez compte Replicate)

---

### "?? Images NSFW non disponibles"

**Solution:**
Marquez le channel Discord comme NSFW:
1. Param?tres du channel
2. Cochez "NSFW Channel"
3. Sauvegardez

---

## ?? Utilisation Recommand?e

### Pour Roleplay Immersif

1. Activez une personnalit?: `/start`
2. G?n?rez son portrait: `/generer_image style:portrait`
3. Conversation avec la personnalit?
4. G?n?rez d'autres styles selon contexte:
   - Flirt ? `/generer_image style:elegant`
   - Intime ? `/generer_image style:lingerie`
   - NSFW ? `/generer_image style:intimate`

---

### Pour Collection de Personnalit?s

Cr?ez une galerie de toutes vos personnalit?s:

```
/start ? S?lectionnez Luna
/generer_image style:portrait

/start ? S?lectionnez Damien  
/generer_image style:portrait

/start ? S?lectionnez Catherine
/generer_image style:portrait

Etc...
```

---

## ?? Notes Techniques

### Int?gration Code

**Fichiers ajout?s:**
- `image_generator.py` - Classe de g?n?ration
- `bot_image_commands.py` - Commandes Discord

**Modifications:**
- `bot.py` - Import du g?n?rateur
- `requirements.txt` - Ajout de `replicate`

---

### API Endpoints

**Replicate:**
```
POST https://api.replicate.com/v1/predictions
GET https://api.replicate.com/v1/predictions/{id}
```

**Mod?le SDXL:**
```
stability-ai/sdxl
Version: 39ed52f2a78e...
```

---

## ? R?sum?

**Le bot peut maintenant:**

? G?n?rer des images personnalis?es pour chaque personnalit?  
? 8 styles diff?rents (SFW + NSFW)  
? Haute qualit? (Stable Diffusion XL)  
? G?n?ration en 30-60 secondes  
? S?curis? (NSFW uniquement dans channels NSFW)  
? Gratuit pour commencer (Replicate tier gratuit)  

---

## ?? Pour Activer

1. **Cr?ez un compte Replicate** (gratuit): https://replicate.com
2. **R?cup?rez votre API key**: https://replicate.com/account/api-tokens
3. **Ajoutez-la sur Render**: Environment ? `REPLICATE_API_KEY`
4. **Testez**: `/generer_image style:portrait`

---

**Profitez de vos personnalit?s avec des visuels!** ???
