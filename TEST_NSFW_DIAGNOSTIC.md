# 🔍 DIAGNOSTIC : Test Services NSFW Gratuits

## ✅ CE QUI A ÉTÉ FAIT

Pollinations a été **DÉSACTIVÉ** dans le code pour vos tests.

Maintenant le bot essaie UNIQUEMENT :
1. **Stable Horde** (gratuit, NSFW OK)
2. **Dezgo** (gratuit, NSFW OK)
3. **Replicate** (payant si clé configurée)

Si tous échouent → **Aucune image** (c'est normal pour les tests)

---

## 🚀 COMMENT TESTER MAINTENANT

### 1. Redémarrer le bot

```bash
# Arrêter le bot (Ctrl+C si il tourne)
python3 bot.py
```

### 2. Sur Discord, demander une image explicite

Exemples :
- "Montre-moi toi en train de me sucer"
- "Envoie-moi une photo de toi nue"
- "Je veux te voir te masturber"

### 3. Observer les LOGS dans le terminal

Vous devriez voir :

```
[IMAGE] Trying Stable Horde (FREE P2P, NSFW allowed)...
[IMAGE] Stable Horde request submitted: abc123
[IMAGE] Stable Horde waiting... Queue: 10
[IMAGE] Stable Horde waiting... Queue: 5
...
```

---

## 📊 RÉSULTATS POSSIBLES

### ✅ SUCCÈS - Stable Horde fonctionne

**Logs:**
```
[IMAGE] Stable Horde SUCCESS after 45s
[IMAGE] SUCCESS with Stable Horde (FREE)!
```

**Résultat:** Image explicite GRATUITE générée ! 🎉

---

### ✅ SUCCÈS - Dezgo fonctionne

**Logs:**
```
[IMAGE] Stable Horde timeout after 120s
[IMAGE] Stable Horde failed, trying Dezgo (FREE, NSFW allowed)...
[IMAGE] Dezgo SUCCESS
[IMAGE] SUCCESS with Dezgo (FREE)!
```

**Résultat:** Image explicite GRATUITE générée ! 🎉

---

### ⚠️ ÉCHEC - Services gratuits ne fonctionnent pas

**Logs:**
```
[ERROR] Stable Horde submit failed: 400
[ERROR] Dezgo failed: 401
[IMAGE] Pollinations DISABLED - Testing NSFW services only
[IMAGE] All attempts failed
```

**Résultat:** Aucune image générée (normal, Pollinations désactivé)

**Diagnostic:** Les services gratuits NSFW sont inaccessibles actuellement

---

## 🔍 POURQUOI LES SERVICES GRATUITS PEUVENT ÉCHOUER

### Stable Horde (Erreur 400)

**Raisons possibles:**
1. ❌ **Prompt trop explicite** → API refuse les mots trop crus
2. ❌ **Format payload incorrect** → API rejette la requête
3. ❌ **Service en maintenance** → Temporairement indisponible
4. ❌ **Rate limit** → Trop de requêtes

**Solution:**
- Vérifier les logs exacts de l'erreur
- Simplifier le prompt (moins de mots explicites)
- Attendre quelques minutes et réessayer

---

### Dezgo (Erreur 401)

**Raisons possibles:**
1. ❌ **Clé API requise** → Service a changé et nécessite maintenant une clé
2. ❌ **Rate limit** → Trop de requêtes depuis votre IP
3. ❌ **Service payant** → N'est plus gratuit

**Solution:**
- Vérifier si Dezgo nécessite maintenant une inscription
- Essayer depuis une autre IP (VPN)
- Passer à un service payant (Replicate)

---

## 🎯 DIAGNOSTIC RAPIDE

### Test 1: Vérifier si Stable Horde est accessible

```bash
curl -X POST https://stablehorde.net/api/v2/generate/async \
  -H "Content-Type: application/json" \
  -d '{"prompt": "beautiful woman", "nsfw": true, "censor_nsfw": false}'
```

**Résultat attendu:** Code 202 + ID de requête

**Si erreur 400:** Le service a peut-être bloqué le NSFW

---

### Test 2: Vérifier si Dezgo est accessible

```bash
curl -X POST https://api.dezgo.com/text2image \
  -F "prompt=beautiful woman" \
  -F "model=realistic_vision_v51"
```

**Résultat attendu:** Données d'image

**Si erreur 401:** Le service nécessite maintenant une clé API

---

## 💡 SOLUTIONS SI SERVICES GRATUITS ÉCHOUENT

### Option 1: Utiliser Replicate (Recommandé)

**Avantages:**
- ✅ Fonctionne à 100%
- ✅ NSFW autorisé
- ✅ Rapide et fiable
- ✅ Très peu cher ($0.0025/image)

**Configuration:**

1. Créer un compte : https://replicate.com/
2. Obtenir une clé API
3. L'ajouter à votre environnement :
   ```bash
   export REPLICATE_API_KEY="r8_votre_cle_ici"
   ```
4. Redémarrer le bot

**Coût:** $0.25 pour 100 images (25 centimes)

---

### Option 2: Réactiver Pollinations (Images censurées)

Si vous voulez au moins avoir des images (même censurées) :

```bash
# Décommenter les lignes dans image_generator.py
# Lignes 81-87 et 632-637
```

**Résultat:** Images générées mais parties intimes censurées/floues

---

### Option 3: Services NSFW alternatifs

**GetIMG.ai** (100 images gratuites/mois)
- Créer compte : https://getimg.ai/
- Obtenir clé API gratuite
- Limite : 100 images/mois

**Prodia.com** (gratuit avec rate limits)
- API publique
- Peut fonctionner pour NSFW
- Moins stable

---

## 📝 RÉSUMÉ DES LOGS À VÉRIFIER

Quand vous testez, cherchez ces lignes dans les logs :

### ✅ Si ça marche

```
[IMAGE] Trying Stable Horde (FREE P2P, NSFW allowed)...
[IMAGE] Stable Horde SUCCESS after 45s
[IMAGE] SUCCESS with Stable Horde (FREE)!
```

OU

```
[IMAGE] Trying Dezgo (FREE, NSFW allowed)...
[IMAGE] Dezgo SUCCESS
[IMAGE] SUCCESS with Dezgo (FREE)!
```

### ❌ Si ça ne marche pas

```
[ERROR] Stable Horde submit failed: 400
[ERROR] Dezgo failed: 401
[IMAGE] Pollinations DISABLED - Testing NSFW services only
```

---

## 🎯 RECOMMANDATION FINALE

Après vos tests :

### Si Stable Horde/Dezgo fonctionnent
→ **Parfait !** Gardez la config actuelle (gratuit)

### Si Stable Horde/Dezgo échouent
→ **Configurez Replicate** (payant mais fiable)

**Pourquoi Replicate est recommandé:**
- ✅ 100% de fiabilité (garanti)
- ✅ NSFW explicite autorisé
- ✅ Rapide (5-10s par image)
- ✅ Coût dérisoire ($0.0025 = 0.25 centime par image)
- ✅ Support professionnel

**Exemple de coût:**
- 10 images/jour = $0.025/jour = $0.75/mois (75 centimes)
- 50 images/jour = $0.125/jour = $3.75/mois
- 100 images/jour = $0.25/jour = $7.50/mois

---

## 🆘 SI PROBLÈME

Envoyez-moi les logs exacts que vous voyez :

```
[IMAGE] Trying Stable Horde...
[ERROR] Stable Horde submit failed: XXX  ← Ce message
[ERROR] Dezgo failed: XXX  ← Ce message
```

Je pourrai diagnostiquer précisément pourquoi ça ne marche pas.

---

## ✅ CHECKLIST DE TEST

- [ ] Bot redémarré après modification
- [ ] Conversation explicite sur Discord
- [ ] Observation des logs dans le terminal
- [ ] Vérification des codes d'erreur (400, 401, etc.)
- [ ] Note du service qui échoue (Stable Horde, Dezgo, ou les deux)
- [ ] Décision : Rester gratuit ou passer à Replicate

---

**IMPORTANT:** Les services gratuits NSFW sont **communautaires** et **non garantis**. Ils peuvent :
- Être indisponibles
- Avoir changé leurs politiques
- Bloquer le NSFW
- Nécessiter maintenant une clé API

**Replicate est la seule solution 100% fiable pour du NSFW explicite.**
