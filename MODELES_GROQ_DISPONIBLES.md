# ?? Mod?les Groq Disponibles

## ? Mod?le Actuel: llama-3.1-8b-instant

Le bot utilise maintenant **llama-3.1-8b-instant** pour:
- ? **Plus de rapidit?** (2-3x plus rapide)
- ?? **Plus de stabilit?** (moins d'erreurs)
- ? **Meilleure fiabilit?** pour les conversations
- ?? **Toujours gratuit**

---

## ?? Tous les mod?les Groq disponibles

### Recommand? ?

#### llama-3.1-8b-instant (ACTUEL)
- **Vitesse**: ????? Ultra rapide
- **Qualit?**: ???? Tr?s bon
- **Usage**: Conversations, r?ponses rapides
- **Id?al pour**: Bot Discord 24/7
- **Nom**: `llama-3.1-8b-instant`

---

### Alternatives

#### llama-3.1-70b-versatile
- **Vitesse**: ??? Rapide
- **Qualit?**: ????? Excellent
- **Usage**: Conversations complexes
- **Note**: Plus lent mais plus intelligent
- **Nom**: `llama-3.1-70b-versatile`

#### mixtral-8x7b-32768
- **Vitesse**: ??? Rapide
- **Qualit?**: ????? Excellent
- **Usage**: Contexte long (32k tokens)
- **Id?al pour**: Conversations longues
- **Nom**: `mixtral-8x7b-32768`

#### gemma2-9b-it
- **Vitesse**: ???? Tr?s rapide
- **Qualit?**: ???? Tr?s bon
- **Usage**: Conversations g?n?rales
- **Id?al pour**: L?ger et rapide
- **Nom**: `gemma2-9b-it`

#### llama-3.2-90b-text-preview
- **Vitesse**: ?? Moyen
- **Qualit?**: ????? Exceptionnel
- **Usage**: T?ches complexes
- **Note**: Le plus puissant mais plus lent
- **Nom**: `llama-3.2-90b-text-preview`

---

## ?? Comment changer de mod?le

### M?thode 1: Variable d'environnement Render (Recommand?)

1. **Dashboard Render** ? Votre service
2. **Settings** ? **Environment**
3. Trouvez `AI_MODEL` (ou ajoutez-la)
4. Changez la valeur:
   ```
   llama-3.1-8b-instant          (Rapide et stable)
   llama-3.1-70b-versatile       (Plus intelligent)
   mixtral-8x7b-32768            (Contexte long)
   gemma2-9b-it                  (L?ger)
   llama-3.2-90b-text-preview    (Le plus puissant)
   ```
5. **Save Changes**
6. **Manual Deploy**

### M?thode 2: Fichier .env (Local)

Dans votre fichier `.env`:
```env
AI_MODEL=llama-3.1-8b-instant
```

### M?thode 3: render.yaml

Dans `render.yaml`:
```yaml
envVars:
  - key: AI_MODEL
    value: llama-3.1-8b-instant
```

---

## ?? Comparaison

| Mod?le | Vitesse | Qualit? | RAM | Usage Discord |
|--------|---------|---------|-----|---------------|
| **llama-3.1-8b-instant** ? | ????? | ???? | Faible | ? Parfait |
| llama-3.1-70b-versatile | ??? | ????? | Moyen | ? Excellent |
| mixtral-8x7b-32768 | ??? | ????? | Moyen | ? Excellent |
| gemma2-9b-it | ???? | ???? | Faible | ? Tr?s bon |
| llama-3.2-90b-text-preview | ?? | ????? | ?lev? | ?? Lent |

---

## ?? Recommandations

### Pour un bot Discord 24/7:
? **llama-3.1-8b-instant** (d?faut actuel)
- Rapide et stable
- Parfait pour conversations en temps r?el
- Moins de timeout

### Pour des conversations complexes:
? **llama-3.1-70b-versatile**
- Plus intelligent
- Meilleure compr?hension
- Peut ?tre plus lent

### Pour des discussions tr?s longues:
? **mixtral-8x7b-32768**
- Contexte de 32k tokens
- Se souvient de beaucoup plus
- Excellent pour role-play

### Pour un serveur avec beaucoup d'activit?:
? **gemma2-9b-it** ou **llama-3.1-8b-instant**
- Tr?s rapide
- G?re bien la charge
- Stable

---

## ? Pourquoi llama-3.1-8b-instant maintenant?

Le bot a ?t? chang? pour ce mod?le car:

1. **Plus stable** - Moins d'erreurs techniques
2. **Plus rapide** - R?ponses quasi-instantan?es
3. **Meilleure fiabilit?** - Parfait pour Render Free
4. **Toujours intelligent** - Qualit? de conversation excellente
5. **Moins de timeout** - Important avec les limitations de Render

---

## ?? Tester diff?rents mod?les

Vous pouvez tester:

1. Changez `AI_MODEL` sur Render
2. Red?ployez
3. Testez avec `/start`
4. Discutez avec le bot
5. Comparez les r?ponses

---

## ?? Note sur les limitations

### Plan Gratuit Groq:
- ~30 requ?tes/minute
- ~14,400 requ?tes/jour
- Tous les mod?les disponibles
- Pas de limitation de tokens par mod?le

### Tous les mod?les sont gratuits! ??

---

## ?? R?sum?

**Mod?le actuel**: `llama-3.1-8b-instant`

**Pourquoi**: Plus rapide et plus stable pour un bot Discord

**Changer**: Mettez ? jour `AI_MODEL` dans Render Environment

**R?sultat**: Bot plus r?actif et moins d'erreurs!

---

? **Le bot utilise maintenant le mod?le le plus adapt? pour Discord!**
