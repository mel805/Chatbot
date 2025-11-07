# Recherche d'APIs GRATUITES pour Contenu NSFW Explicite

## 🎯 Objectif
Trouver une API gratuite (ou quasi-gratuite) qui peut générer des images NSFW explicites sans censure pour remplacer Pollinations.ai.

## 🔍 Options Identifiées

### Option 1: Hugging Face Inference API (GRATUIT avec limites)

**Service:** https://huggingface.co/
**Coût:** GRATUIT (avec rate limits)

**Avantages:**
- ✅ Complètement gratuit
- ✅ Nombreux modèles disponibles
- ✅ Certains modèles NSFW non-censurés
- ✅ API simple à utiliser

**Inconvénients:**
- ⚠️ Rate limits (quelques images/minute)
- ⚠️ Peut être lent
- ⚠️ Certains modèles NSFW désactivés

**Modèles NSFW Potentiels:**
1. `stabilityai/stable-diffusion-xl-base-1.0` - Parfois autorise NSFW
2. `dreamlike-art/dreamlike-photoreal-2.0` - Photoréalisme, moins de filtres
3. `SG161222/Realistic_Vision_V5.1` - Très populaire pour NSFW
4. `prompthero/openjourney-v4` - Moins de censure

**Status:** À tester - Certains modèles peuvent fonctionner

---

### Option 2: Prodia.com (GRATUIT)

**Service:** https://app.prodia.com/
**Coût:** GRATUIT (avec rate limits)

**Avantages:**
- ✅ Gratuit
- ✅ API publique
- ✅ Plusieurs modèles NSFW
- ✅ Moins de censure que Pollinations

**API:**
```
https://api.prodia.com/generate
```

**Inconvénients:**
- ⚠️ Peut être instable
- ⚠️ Rate limits stricts
- ⚠️ Documentation limitée

**Status:** À tester - Prometteur pour NSFW

---

### Option 3: Dezgo.com (GRATUIT)

**Service:** https://dezgo.com/
**Coût:** GRATUIT (pas de compte requis)

**Avantages:**
- ✅ 100% gratuit
- ✅ Pas de compte nécessaire
- ✅ API publique simple
- ✅ Supporte NSFW (pas de filtres stricts)

**API Endpoint:**
```
https://api.dezgo.com/text2image
```

**Paramètres:**
- `prompt`: Le prompt
- `width`: Largeur (défaut: 512)
- `height`: Hauteur (défaut: 512)
- `model`: Modèle (ex: "realistic_vision_v51")

**Inconvénients:**
- ⚠️ Qualité variable
- ⚠️ Peut être lent

**Status:** TRÈS PROMETTEUR - API simple et permet NSFW

---

### Option 4: GetIMG.ai (Crédits gratuits)

**Service:** https://getimg.ai/
**Coût:** 100 crédits gratuits/mois (100 images)

**Avantages:**
- ✅ 100 images gratuites/mois
- ✅ Excellente qualité
- ✅ NSFW autorisé
- ✅ API bien documentée

**Inconvénients:**
- ⚠️ Limité à 100 images/mois gratuit
- ⚠️ Nécessite compte et clé API

**Status:** Bon compromis gratuit/qualité

---

### Option 5: Stable Horde (GRATUIT - Distribué)

**Service:** https://stablehorde.net/
**Coût:** 100% GRATUIT (P2P)

**Avantages:**
- ✅ Totalement gratuit
- ✅ Pas de rate limits
- ✅ NSFW explicitement autorisé
- ✅ Réseau distribué (P2P)
- ✅ API publique

**API:**
```
https://stablehorde.net/api/
```

**Comment ça marche:**
- Réseau P2P où des gens partagent leurs GPUs
- Vous soumettez une requête
- Un worker la traite
- Vous récupérez l'image

**Inconvénients:**
- ⚠️ Temps d'attente variable (file d'attente)
- ⚠️ Qualité variable selon le worker
- ⚠️ Peut prendre 30s-2min par image

**Status:** EXCELLENT - Gratuit, NSFW autorisé, mais peut être lent

---

### Option 6: Mage.space (Crédits gratuits)

**Service:** https://www.mage.space/
**Coût:** Crédits gratuits quotidiens

**Avantages:**
- ✅ Crédits gratuits chaque jour
- ✅ NSFW autorisé
- ✅ Interface simple
- ✅ Bonne qualité

**Inconvénients:**
- ⚠️ Crédits limités par jour
- ⚠️ Nécessite compte

**Status:** Bon pour usage modéré

---

## 🏆 RECOMMANDATIONS

### 1. MEILLEUR GRATUIT : **Stable Horde** ⭐⭐⭐⭐⭐

**Pourquoi:**
- ✅ 100% gratuit sans limites
- ✅ NSFW explicitement autorisé
- ✅ API publique bien documentée
- ✅ Communauté active

**Inconvénient:** Peut être lent (file d'attente)

**Implémentation:** Facile - API REST simple

---

### 2. PLUS RAPIDE GRATUIT : **Dezgo** ⭐⭐⭐⭐

**Pourquoi:**
- ✅ Gratuit
- ✅ Pas de compte
- ✅ Rapide
- ✅ NSFW autorisé

**Inconvénient:** Qualité moyenne

---

### 3. MEILLEURE QUALITÉ GRATUITE : **GetIMG.ai** ⭐⭐⭐⭐

**Pourquoi:**
- ✅ 100 images/mois gratuites
- ✅ Excellente qualité
- ✅ NSFW autorisé

**Inconvénient:** Limité à 100/mois

---

## 💻 Implémentation Recommandée

### Solution Hybride (Recommandé)

```python
# 1. Essayer Stable Horde (gratuit illimité)
# 2. Si trop lent, fallback sur Dezgo (gratuit rapide)
# 3. Si échec, fallback sur Replicate (payant mais garanti)
```

**Avantages:**
- ✅ Gratuit dans 99% des cas
- ✅ Fallback payant pour garantie
- ✅ Meilleur des deux mondes

---

## 🔧 APIs à Implémenter

### Priority 1: Stable Horde
```python
async def _generate_stable_horde(self, prompt):
    """Gratuit illimité, NSFW OK, mais peut être lent"""
    api_url = "https://stablehorde.net/api/v2/generate/async"
    # Code à implémenter
```

### Priority 2: Dezgo
```python
async def _generate_dezgo(self, prompt):
    """Gratuit rapide, NSFW OK, qualité moyenne"""
    api_url = "https://api.dezgo.com/text2image"
    # Code à implémenter
```

### Priority 3: Hugging Face
```python
async def _generate_huggingface(self, prompt, model="SG161222/Realistic_Vision_V5.1"):
    """Gratuit avec limits, certains modèles NSFW OK"""
    # Code à implémenter
```

---

## 📊 Comparaison Finale

| Service | Coût | Vitesse | Qualité | NSFW | Limites | Score |
|---------|------|---------|---------|------|---------|-------|
| **Stable Horde** | Gratuit | Lent | Bonne | ✅ | Aucune | ⭐⭐⭐⭐⭐ |
| **Dezgo** | Gratuit | Rapide | Moyenne | ✅ | Raisonnables | ⭐⭐⭐⭐ |
| **GetIMG.ai** | 100/mois | Rapide | Excellente | ✅ | 100/mois | ⭐⭐⭐⭐ |
| **Prodia** | Gratuit | Moyenne | Bonne | ✅ | Strictes | ⭐⭐⭐ |
| **HuggingFace** | Gratuit | Lent | Variable | ⚠️ | Strictes | ⭐⭐⭐ |
| **Replicate** | $0.0025 | Rapide | Excellente | ✅ | Aucune | ⭐⭐⭐⭐⭐ |

---

## 🎯 Plan d'Action

### Étape 1: Implémenter Stable Horde
- API REST simple
- Gratuit illimité
- NSFW explicitement autorisé

### Étape 2: Implémenter Dezgo (Fallback)
- Pour les cas où Stable Horde est trop lent
- Gratuit et rapide

### Étape 3: Garder Replicate (Fallback final)
- Garantie de fonctionnement
- Payant mais abordable

### Architecture de Fallback

```
1. Stable Horde (gratuit illimité) → Essayer d'abord
   ↓ Si trop lent (>30s) ou échec
2. Dezgo (gratuit rapide) → Essayer ensuite
   ↓ Si échec
3. Replicate (payant $0.0025) → Garantie finale
```

**Résultat:** Gratuit dans la grande majorité des cas, avec garantie payante

---

## 📝 Prochaines Étapes

1. ✅ Implémenter fonction pour Stable Horde
2. ✅ Implémenter fonction pour Dezgo
3. ✅ Modifier le flow de génération pour utiliser les services gratuits d'abord
4. ✅ Tester avec des prompts NSFW explicites
5. ✅ Documenter les résultats

---

## ⚠️ Notes Légales

- Ces services autorisent le NSFW mais vérifiez leurs ToS
- Toujours respecter les lois locales
- Contenu 18+ uniquement
- Utilisation responsable

---

## 🔗 Liens Utiles

- Stable Horde: https://stablehorde.net/
- Dezgo: https://dezgo.com/
- GetIMG.ai: https://getimg.ai/
- HuggingFace: https://huggingface.co/models?other=stable-diffusion
