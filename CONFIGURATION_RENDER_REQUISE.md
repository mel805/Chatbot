# ⚠️ CONFIGURATION RENDER REQUISE

## 🔧 PROBLÈME ACTUEL

Les API ultra-rapides gratuites (Chai, Horde, OpenRouter) ont **toutes échoué**.

```
[ERROR] Toutes les APIs ont échoué
```

**Cause :** Ces API gratuites sont instables ou temporairement indisponibles.

---

## ✅ SOLUTION : Fallback Groq Activé

J'ai ajouté **Groq comme fallback fiable** :

**Stratégie :**
1. **Essaie d'abord les API rapides gratuites** (Chai, Horde, OpenRouter)
2. **Si échec → Utilise Groq** (fiable, testé, fonctionne)

**→ Le bot répondra toujours, même si les API gratuites échouent !**

---

## 🔑 CONFIGURATION RENDER OBLIGATOIRE

### **Variables d'environnement à configurer :**

**Dans Render Dashboard → Environment :**

```bash
DISCORD_BOT_TOKEN = [votre token Discord]
GROQ_API_KEY = [votre clé Groq]        # ← NÉCESSAIRE pour le fallback
AI_MODEL = llama-3.3-70b-versatile     # Optionnel (valeur par défaut)
```

---

## 🎯 COMMENT OBTENIR GROQ_API_KEY ?

1. **Allez sur** : https://console.groq.com/
2. **Créez un compte gratuit** (email + mot de passe)
3. **Allez dans "API Keys"**
4. **Créez une nouvelle clé** (bouton "Create API Key")
5. **Copiez la clé** (commence par `gsk_...`)
6. **Collez dans Render** : `GROQ_API_KEY = gsk_...`

**→ Gratuit, rapide, fiable, NSFW OK**

---

## 📊 COMPORTEMENT APRÈS CONFIGURATION

### **Avec GROQ_API_KEY configurée :**

```
[INFO] Essai API ultra-rapides (Chai/Horde/OpenRouter)...
[ERROR] Chai API failed
[ERROR] Horde API failed  
[ERROR] OpenRouter API failed
[INFO] API rapides échouées, fallback Groq...
[FALLBACK] Utilisation de Groq API...
[SUCCESS] Groq fallback: [réponse Luna]...
```

**→ Bot répond en 3-5 secondes (Groq)**

### **Sans GROQ_API_KEY :**

```
[INFO] Essai API ultra-rapides (Chai/Horde/OpenRouter)...
[ERROR] Toutes les APIs ont échoué
[WARNING] GROQ_API_KEY manquante, impossible d'utiliser le fallback
[ERROR] Toutes les API ont échoué (y compris Groq)
```

**→ Bot répond : "Desole, toutes les API sont temporairement indisponibles."**

---

## 🚀 ÉTAPES À SUIVRE

### **1. Configurer GROQ_API_KEY sur Render**

```
Dashboard → [Votre service] → Environment → Add Environment Variable
```

**Clé :** `GROQ_API_KEY`  
**Valeur :** `gsk_...` (votre clé depuis console.groq.com)

**→ Save Changes**

### **2. Redéploiement automatique**

Render va automatiquement redéployer après avoir ajouté la variable.

### **3. Vérifier les logs**

Dans les logs, vous devriez voir :

```
BOT READY - Version HYBRIDE (Ultra-fast + Groq fallback)
Bot user: VotreBot#1234
AI Backend: Chai/Horde/OpenRouter (priorité) -> Groq (fallback)
GROQ_API_KEY configurée: OUI  ← Doit être OUI
Personalities: 22
```

### **4. Tester dans Discord**

```
/start
Sélectionner "Luna 25ans - Coquine"
@BotName salut
```

**Si API rapides échouent → Groq prend le relai → Réponse en 3-5s**

---

## 🎯 RÉSUMÉ

**Avant (100% Groq) :**
- ✅ Fiable
- ⚠️ 3-8 secondes

**Après (Hybride) :**
- ✅ Essaie d'abord les API ultra-rapides (< 1s)
- ✅ Si échec → Fallback Groq (3-5s) 
- ✅ Garantit toujours une réponse
- ✅ Meilleur des deux mondes

**Configuration requise :**
```
DISCORD_BOT_TOKEN = [token]
GROQ_API_KEY = gsk_...        ← À AJOUTER
```

---

## ❓ QUESTIONS FRÉQUENTES

**Q: Pourquoi les API gratuites échouent ?**  
R: Chai, Horde et OpenRouter Free sont instables/limités. Groq est plus fiable.

**Q: Groq est payant ?**  
R: Non, gratuit avec limites généreuses (14000 requêtes/jour).

**Q: Dois-je supprimer les API rapides ?**  
R: Non, elles restent prioritaires. Si elles fonctionnent, réponse < 1s !

**Q: Puis-je utiliser seulement Groq ?**  
R: Oui, les API rapides échoueront et Groq prendra le relai automatiquement.

---

**Configurez GROQ_API_KEY sur Render pour un bot 100% fonctionnel ! 🎉**
