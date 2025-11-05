# ?? Solution: Erreur Cloudflare 5xx

## ?? Erreur Rencontr?e

```
Performance & security by Cloudflare
[Erreur 5xx]
```

Cette erreur appara?t quand vous utilisez `/generer_image`.

---

## ?? CAUSE

L'erreur Cloudflare 5xx signifie que l'API Replicate n'est **pas accessible** ou **pas configur?e**.

**3 causes possibles:**

1. ? **API key REPLICATE_API_KEY non configur?e**
2. ? **API key invalide**
3. ?? **Replicate temporairement indisponible**

---

## ? SOLUTION 1: Configurer l'API Key (Recommand?)

### ?tape 1: Cr?er un Compte Replicate (GRATUIT)

1. Allez sur: **https://replicate.com**
2. Cliquez "**Sign Up**"
3. Inscrivez-vous avec votre email
4. Confirmez votre email

**?? Temps: 2 minutes**

---

### ?tape 2: R?cup?rer Votre API Key

1. Connectez-vous sur Replicate
2. Allez sur: **https://replicate.com/account/api-tokens**
3. Cliquez "**Create token**" si besoin
4. **Copiez** le token (commence par `r8_`)

**Exemple:** `r8_AbCdEfGh1234567890XyZ...`

---

### ?tape 3: Ajouter l'API Key sur Render

1. Allez sur votre **Dashboard Render**
2. Cliquez sur votre service bot
3. Allez dans l'onglet **"Environment"**
4. Cliquez **"Add Environment Variable"**
5. Remplissez:
   - **Key**: `REPLICATE_API_KEY`
   - **Value**: `r8_xxxxx` (votre token complet)
6. Cliquez **"Save Changes"**

**Le service va red?marrer automatiquement (2-3 min)**

---

### ?tape 4: Tester

Apr?s le red?marrage:

```
/start
[S?lectionnez une personnalit?]

/generer_image style:portrait
```

**Devrait fonctionner! ?**

---

## ?? Co?ts Replicate

**Tier Gratuit:**
- ? **~$5 de cr?dits gratuits** au d?but
- ? **~100-200 g?n?rations** gratuites/mois
- ? **Pas de carte bancaire** requise
- ? Renouvellement mensuel possible

**Prix apr?s gratuit:**
- SDXL: **$0.02-0.03 par image**
- Tr?s abordable!

---

## ?? SOLUTION 2: V?rifier l'API Key Existante

**Si vous avez d?j? ajout? l'API key:**

### V?rifiez sur Render:

1. Dashboard ? Votre service ? **Environment**
2. Cherchez `REPLICATE_API_KEY`
3. V?rifiez que:
   - ? Elle existe
   - ? Elle commence par `r8_`
   - ? Elle est compl?te (pas tronqu?e)

### Si l'API key est incorrecte:

1. Supprimez-la
2. Cr?ez-en une nouvelle sur Replicate
3. Ajoutez la nouvelle sur Render
4. Sauvegardez (red?marre le service)

---

## ?? SOLUTION 3: Replicate Indisponible

**Si l'API key est correcte mais erreur persiste:**

Replicate peut ?tre temporairement indisponible.

**V?rifiez:**
- https://www.replicate.com (le site est accessible?)
- https://status.replicate.com (statut du service)

**Si indisponible:**
- ? Attendez 10-30 minutes
- ?? R?essayez

---

## ?? SOLUTION 4: V?rifier les Logs

**Pour voir l'erreur exacte:**

1. Dashboard Render ? Votre service
2. Onglet **"Logs"**
3. Cherchez:
   ```
   [IMAGE] Generating image...
   [ERROR] Replicate generation error: ...
   ```

**Erreurs courantes:**

| Erreur | Cause | Solution |
|--------|-------|----------|
| `Invalid API token` | Token invalide | Cr?ez un nouveau token |
| `Rate limit exceeded` | Trop de requ?tes | Attendez 5-10 min |
| `Model not found` | Mod?le indisponible | Contactez-moi |
| `Timeout` | Requ?te trop longue | R?essayez |

---

## ?? ALTERNATIVE: Hugging Face API

**Si vous pr?f?rez une alternative ? Replicate:**

### Hugging Face Inference API (Gratuit)

1. Cr?ez un compte: https://huggingface.co
2. R?cup?rez votre token: https://huggingface.co/settings/tokens
3. Ajoutez sur Render:
   - Key: `HUGGINGFACE_API_KEY`
   - Value: `hf_xxxxx`

**Le bot essaiera automatiquement Hugging Face si Replicate ?choue!**

---

## ?? R?sum? Rapide

**Pour activer la g?n?ration d'images:**

```
1. Compte Replicate (gratuit): replicate.com
2. API Key: replicate.com/account/api-tokens
3. Render Environment: REPLICATE_API_KEY = r8_xxxxx
4. Attendez red?marrage (2-3 min)
5. Testez: /generer_image style:portrait
```

---

## ? FAQ

### Q: Dois-je payer?

**R:** Non! Le tier gratuit offre 100-200 g?n?rations/mois. Largement suffisant pour un usage personnel.

---

### Q: Pourquoi Cloudflare?

**R:** Replicate utilise Cloudflare pour prot?ger son API. L'erreur 5xx signifie que l'API ne peut pas ?tre contact?e (souvent car l'API key manque).

---

### Q: Combien de temps pour la g?n?ration?

**R:** 30-60 secondes par image.

---

### Q: Puis-je g?n?rer des images NSFW?

**R:** Oui, avec les styles NSFW (lingerie, intimate, etc.) dans les channels Discord NSFW.

---

### Q: L'erreur persiste apr?s configuration?

**R:** 
1. V?rifiez que le service a bien red?marr?
2. V?rifiez l'API key (correcte et compl?te)
3. Attendez 5 min (rate limit possible)
4. V?rifiez les logs Render pour l'erreur exacte

---

## ? Checklist de D?pannage

- [ ] Compte Replicate cr??
- [ ] API token copi? (commence par `r8_`)
- [ ] `REPLICATE_API_KEY` ajout? sur Render Environment
- [ ] Service red?marr? (2-3 min)
- [ ] Bot actif dans le channel (`/start`)
- [ ] Personnalit? s?lectionn?e
- [ ] Command `/generer_image` test?e

**Si tout est coch? et ?a ne marche pas:**
? V?rifiez les logs Render et contactez-moi avec l'erreur exacte!

---

**La g?n?ration d'images est OPTIONNELLE. Le bot fonctionne parfaitement sans!** ??

Mais avec les images, c'est encore plus immersif! ???
