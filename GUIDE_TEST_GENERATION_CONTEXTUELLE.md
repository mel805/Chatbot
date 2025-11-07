# 🧪 GUIDE TEST - Génération Contextuelle Améliorée

## 🎯 OBJECTIF

Tester que le bouton "🎨 Générer image contextuelle" **capture bien** :
- ✅ Les tenues/vêtements
- ✅ Les positions
- ✅ Les actions/situations

---

## 🚀 PRÉREQUIS

1. ✅ Redéployer Render (commit `b56736e`)
2. ✅ Bot en ligne sur Discord
3. ✅ Logs Render ouverts (pour voir les détections)

---

## 🧪 TEST 1 : Vêtements + Position

### Étapes :

1. **Dans Discord, canal NSFW, tapez `/start`**
2. **Choisir une personnalité** (ex: Amelie)
3. **Dans la conversation, tapez :**
   ```
   Mets ta robe courte et écarte les jambes
   ```
4. **Le bot répond** (n'importe quoi)
5. **Cliquez sur le bouton "🎨 Générer image contextuelle"**

### Logs attendus dans Render :

```
[IMAGE CONTEXT] Analyzing 2 messages...
[IMAGE CONTEXT] ✅ DETECTED: Clothing detected: ...robe courte...
[IMAGE CONTEXT] PRIORITY: Clothing context added: ...robe courte...
[IMAGE CONTEXT] ✅ DETECTED: Position 'jambes écartées' → legs spread wide
[IMAGE CONTEXT] ✅ 2 context elements detected
[IMAGE CONTEXT] Keywords: wearing ...robe courte..., legs spread wide...
```

### Résultat attendu :

✅ **Image générée** montrant le bot :
- En robe courte
- Jambes écartées

---

## 🧪 TEST 2 : Position explicite

### Étapes :

1. **Conversation existante ou nouvelle**
2. **Dans la conversation :**
   ```
   Mets-toi à 4 pattes
   ```
3. **Le bot répond**
4. **Cliquez sur le bouton contextuel**

### Logs attendus :

```
[IMAGE CONTEXT] ✅ DETECTED: Position '4 pattes' → on all fours position, doggystyle pose
```

### Résultat :

✅ Image du bot à 4 pattes / doggystyle

---

## 🧪 TEST 3 : Action explicite (NSFW)

### Étapes :

1. **Dans la conversation :**
   ```
   Je pénètre ma queue dans ton cul
   ```
2. **Le bot répond**
3. **Cliquez sur le bouton contextuel**

### Logs attendus :

```
[IMAGE CONTEXT] ✅ DETECTED: ULTRA EXPLICIT Penetration / Sex
[IMAGE CONTEXT] Penetration keywords found in conversation
[IMAGE CONTEXT] Keywords: NSFW explicit hardcore sex scene, dick penetrating pussy...
```

### Résultat :

✅ Image explicite de pénétration

---

## 🧪 TEST 4 : Combinaison complexe

### Étapes :

1. **Conversation longue avec plusieurs détails :**
   ```
   User: Relève ta jupe
   Bot: [répond]
   User: Mets-toi à genoux
   Bot: [répond]
   User: Je vais te prendre dans ma bouche
   Bot: [répond]
   ```
2. **Cliquez sur le bouton contextuel**

### Logs attendus :

```
[IMAGE CONTEXT] Analyzing 6 messages...
[IMAGE CONTEXT] ✅ DETECTED: Clothing detected: ...jupe...
[IMAGE CONTEXT] ✅ DETECTED: Position 'à genoux' → on knees position
[IMAGE CONTEXT] ✅ DETECTED: ULTRA EXPLICIT Oral sex / Fellation
[IMAGE CONTEXT] ✅ 3 context elements detected
```

### Résultat :

✅ Image combinant : jupe relevée + à genoux + fellation

---

## ❌ SI ÇA NE FONCTIONNE PAS

### Scénario 1 : Aucune détection

**Logs :**
```
[IMAGE CONTEXT] ⚠️ NO specific context detected
```

**Cause :** Les mots utilisés ne correspondent pas aux mots-clés

**Solution :**
1. Vérifier dans les logs le texte analysé : `[IMAGE CONTEXT] Last 200 chars: ...`
2. Utiliser les mots-clés listés dans le guide
3. M'envoyer les logs pour que j'ajoute + de variations

---

### Scénario 2 : Détection partielle

**Logs :**
```
[IMAGE CONTEXT] ✅ DETECTED: Position 'à genoux'
[IMAGE CONTEXT] ⚠️ Clothing not detected
```

**Cause :** Certains mots-clés détectés, d'autres non

**Solution :**
- L'image sera générée avec ce qui a été détecté
- Pour améliorer, utiliser les mots-clés exacts

---

### Scénario 3 : Image générée mais pas explicite

**Cause :** Stable Horde peut toujours censurer selon le prompt

**Solution :**
1. Réessayer (parfois ça marche au 2e essai)
2. Configurer Replicate pour 100% fiabilité :
   ```bash
   REPLICATE_API_KEY=r8_xxx
   ```

---

## 📋 CHECKLIST DE TEST

Après redéploiement Render :

- [ ] Test 1 : Vêtements + Position
- [ ] Test 2 : Position explicite
- [ ] Test 3 : Action explicite
- [ ] Test 4 : Combinaison complexe
- [ ] Vérifier logs Render pour chaque test
- [ ] Confirmer images correspondent au contexte

---

## 🆘 RAPPORT DE BUG

**Si un test échoue, envoyez-moi :**

1. **Ce que vous avez tapé** dans la conversation
2. **Screenshot des logs Render** (section IMAGE CONTEXT)
3. **Screenshot de l'image générée** (ou "aucune image")

Exemple de rapport :

```
TEST : Vêtements + Position
CONVERSATION : "Mets ta robe courte et écarte les jambes"

LOGS RENDER :
[IMAGE CONTEXT] Analyzing 2 messages...
[IMAGE CONTEXT] ⚠️ NO specific context detected

RÉSULTAT : Image générique (pas de robe, pas jambes écartées)

ATTENDU : Détection de "robe courte" et "jambes écartées"
```

---

## 📊 MOTS-CLÉS COMPLETS

### Positions détectées :

- quatre pattes, 4 pattes, à quatre pattes
- genoux, à genoux
- jambes écartées, jambe écartée, jambes ouvertes, écarte les jambes
- allongée, couchée, sur le dos
- assise sur, monte sur
- debout contre, contre le mur
- penchée, courbée

### Vêtements détectés :

- robe (courte/longue/légère)
- jupe (courte/longue/mini-jupe)
- lingerie, string, dentelle, soutien-gorge, culotte
- nuisette, déshabillé
- chemise, chemisier
- pantalon, jean, legging
- short, mini short
- haut, top, crop top, tee-shirt
- talons, talons hauts, escarpins
- toute nue, complètement nue, sans rien

### Actions détectées :

**Oral :**
- bouche, dans ma bouche, prend dans ma bouche
- lèche, lécher, suce, sucer
- pipe, fellation, blowjob
- vais te prendre

**Pénétration :**
- pénètre, pénétrer, entre dans
- dans ton cul, dans ta chatte
- enfonce, rentre en
- te baise, baise, fuck

**Masturbation :**
- masturbe, caresse, touche
- doigt, doigter, frotte

**Exhibition :**
- montre, regarde, expose
- sein, seins, fesse, chatte, pussy

---

**Commit :** `b56736e`  
**Status :** ✅ Prêt à tester après redéploiement Render
