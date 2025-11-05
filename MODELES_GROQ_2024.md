# ?? Mod?les Groq Actifs (Novembre 2024)

## ?? MOD?LES ABANDONN?S (NE PLUS UTILISER)

Ces mod?les ont ?t? retir?s par Groq:
- ? `llama-3.1-70b-versatile` (abandonn?)
- ? `llama-3.1-8b-instant` (abandonn?)

**Erreur si utilis?:**
```
"model_decommissioned" - Le mod?le a ?t? abandonn?
```

---

## ? MOD?LES ACTIFS (2024)

### ?? #1 - llama-3.3-70b-versatile (RECOMMAND?)
**Nom du mod?le**: `llama-3.3-70b-versatile`

**Le MEILLEUR pour contenu adulte/NSFW:**
- ? Remplacement direct de llama-3.1-70b
- ? Plus performant que 3.1
- ? Moins censur?
- ? Excellent pour role-play adulte
- ? Cr?atif et d?taill?
- ? Rapide (1-2 secondes)
- ?? Gratuit

**Qualit? NSFW**: ?????
**Vitesse**: ????
**Cr?ativit?**: ??????????

**Configur? par d?faut maintenant!**

---

### ?? #2 - mixtral-8x7b-32768
**Nom du mod?le**: `mixtral-8x7b-32768`

**Excellent alternatif:**
- ? Tr?s bon pour NSFW
- ? M?moire ?tendue (32k tokens = conversations longues)
- ? Cr?atif
- ? Rapide

**Qualit? NSFW**: ?????
**Vitesse**: ????
**M?moire**: ?????????? (32k tokens!)

---

### ?? #3 - llama-3.1-8b-instant (si toujours disponible)
**Nom du mod?le**: `llama-3.1-8b-instant`

**Compromis vitesse/qualit?:**
- ? Ultra rapide
- ? Acceptable pour NSFW
- ? Tr?s stable

**Qualit? NSFW**: ????
**Vitesse**: ?????

**Note**: Ce mod?le pourrait aussi ?tre abandonn? bient?t.

---

### Autres mod?les disponibles:
- `gemma2-9b-it` - Plus censur?, moins bon pour NSFW
- `llama-3.2-1b-preview` - Trop petit, pas recommand?
- `llama-3.2-3b-preview` - Trop petit, pas recommand?
- `llama-3.2-90b-vision-preview` - Pour images, lent

---

## ?? Comparaison des Meilleurs

| Mod?le | NSFW | Vitesse | Cr?ativit? | Statut |
|--------|------|---------|------------|--------|
| **llama-3.3-70b-versatile** | ????? | ???? | ?????????? | ? Actif |
| **mixtral-8x7b-32768** | ????? | ???? | ???????? | ? Actif |
| llama-3.1-8b-instant | ???? | ????? | ?????? | ?? ? v?rifier |
| llama-3.1-70b-versatile | N/A | N/A | N/A | ? Abandonn? |

---

## ?? Configuration sur Render

Le bot utilise maintenant **llama-3.3-70b-versatile** par d?faut.

### Pour changer de mod?le:

1. **Sur Render Dashboard** ? Environment
2. Modifiez `AI_MODEL`:
   - `llama-3.3-70b-versatile` (d?faut, meilleur)
   - `mixtral-8x7b-32768` (alternatif)
3. **Save Changes**
4. Le bot red?marre automatiquement

---

## ? Limites Groq (Tous mod?les)

### Tier Gratuit:
- ~30 requ?tes/minute
- ~14,400 requ?tes/jour
- Largement suffisant pour un serveur Discord

### Si rate limit:
```
[ERROR] Groq API error 429: Rate limit exceeded
```
**Solution**: Attendez 1 minute ou cr?ez un autre compte Groq

---

## ?? Pour Votre Bot

**Mod?le configur?**: `llama-3.3-70b-versatile`

**Avantages pour contenu adulte:**
- ?? Moins de censure que les autres
- ?? Comprend les nuances du contexte adulte
- ?? S'adapte parfaitement aux 8 personnalit?s
- ?? Excellent pour role-play et conversations os?es
- ? Assez rapide pour Discord
- ?? Gratuit

---

## ?? Ressources

- **Console Groq**: https://console.groq.com/docs/models
- **D?pr?cations**: https://console.groq.com/docs/deprecations
- **Cl? API gratuite**: https://console.groq.com/keys

---

? **Le bot est maintenant configur? avec llama-3.3-70b-versatile!**

Plus d'erreur "model_decommissioned"! ??
