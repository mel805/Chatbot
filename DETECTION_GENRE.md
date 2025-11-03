# ?? D?tection Automatique du Genre - Guide Complet

## ?? Nouvelle Fonctionnalit?

Le bot d?tecte maintenant **automatiquement le genre des membres Discord** et adapte ses r?ponses en cons?quence pour des conversations plus immersives et personnalis?es!

---

## ?? Comment ?a Marche?

### 1?? **D?tection via R?les Discord** (M?thode Principale)

Le bot scanne les r?les Discord de chaque membre et d?tecte automatiquement leur genre.

#### Mots-cl?s d?tect?s dans les r?les:

| Genre | Mots-cl?s d?tect?s |
|-------|-------------------|
| **Homme** | homme, men, male, mec, gar?on, boy, man |
| **Femme** | femme, women, female, fille, girl, woman |
| **Non-binaire** | non-binaire, nonbinary, enby, nb, non binaire |
| **Trans** | trans, transgender |

#### Exemples de r?les qui seront d?tect?s:

? R?le "Homme" ? D?tect? comme homme  
? R?le "Femme" ? D?tect? comme femme  
? R?le "?? Men" ? D?tect? comme homme  
? R?le "?? Women" ? D?tect? comme femme  
? R?le "Mec du serveur" ? D?tect? comme homme  
? R?le "Non-binaire" ? D?tect? comme non-binaire

---

### 2?? **Syst?me de Cache Intelligent**

Une fois le genre d?tect?, il est **automatiquement enregistr? en cache** pour ?viter de le scanner ? chaque message.

**Avantages:**
- ? Performances optimales
- ?? Coh?rence dans les r?ponses
- ?? Persistance durant toute la session

---

### 3?? **Adaptation Automatique des R?ponses**

Le bot adapte son langage selon le genre d?tect?:

#### Avec un Homme:
```
User (Homme): salut Luna
Luna: salut beau gosse ??
```

#### Avec une Femme:
```
User (Femme): salut Damien
Damien: salut beaut? ??
```

#### Genre Inconnu:
```
User: salut Jordan
Jordan: salut! ??
[Langage neutre]
```

---

## ?? Adaptation Selon la Personnalit?

### Personnalit? F?minine + Utilisateur Homme:
```
Luna (Femme 25ans) parlant ? un homme:
- Langage plus s?ducteur
- R?f?rences masculines appropri?es
- Tutoiement adapt?
```

### Personnalit? Masculine + Utilisatrice Femme:
```
Damien (Homme 28ans) parlant ? une femme:
- Langage charmant
- R?f?rences f?minines appropri?es
- Compliments adapt?s
```

### M?me Genre:
```
Luna (Femme) + Utilisatrice (Femme):
- Complicit? f?minine
- R?f?rences entre femmes
- Ton adapt?
```

---

## ??? Configuration Discord (Pour Admins)

### Comment Cr?er les R?les de Genre?

**1. Aller dans Param?tres du Serveur ? R?les**

**2. Cr?er les r?les suivants (exemples):**

```
?? Homme
?? Femme
?? Non-binaire
?????? Trans
```

**3. Attribuer les r?les aux membres**

**4. Le bot d?tectera automatiquement!**

---

### Exemples de Noms de R?les qui Fonctionnent:

? **Pour Hommes:**
- Homme
- Men
- Mec
- Gar?on
- ?? Male
- ?? Boy

? **Pour Femmes:**
- Femme
- Women
- Fille
- ?? Female
- ?? Girl

? **Pour Non-binaires:**
- Non-binaire
- Non binaire
- Enby
- NB
- ?? Nonbinary

? **Pour Trans:**
- Trans
- Transgender
- ?????? Trans

---

## ?? Informations Transmises au Bot

Selon le genre d?tect?, le bot AI re?oit cette information dans son prompt:

### Si Homme:
```
"Tu parles actuellement avec un homme. 
Adapte ton langage et tes r?f?rences en cons?quence."
```

### Si Femme:
```
"Tu parles actuellement avec une femme. 
Adapte ton langage et tes r?f?rences en cons?quence."
```

### Si Non-binaire:
```
"Tu parles actuellement avec une personne non-binaire. 
Utilise un langage neutre et inclusif."
```

### Si Trans:
```
"Tu parles actuellement avec une personne trans. 
Sois respectueux et utilise un langage inclusif."
```

### Si Inconnu:
```
"Genre inconnu - utilise un langage neutre 
ou adapte-toi selon le contexte."
```

---

## ?? Exemples Concrets de Diff?rences

### Scenario 1: Luna (Femme 25ans) + Homme

**Sans d?tection:**
```
User: t'es seule?
Luna: ouais pourquoi? ??
```

**Avec d?tection (Homme):**
```
User: t'es seule?
Luna: ouais, t'as envie de me tenir compagnie? ??
```

---

### Scenario 2: Damien (Homme 28ans) + Femme

**Sans d?tection:**
```
User: tu fais quoi?
Damien: je tra?ne, pourquoi?
```

**Avec d?tection (Femme):**
```
User: tu fais quoi?
Damien: je tra?ne, t'as envie qu'on fasse quelque chose ensemble? ??
```

---

### Scenario 3: Jordan (Neutre) + Non-binaire

**Avec d?tection:**
```
User: salut
Jordan: salut! content de te voir ??
[Langage inclusif sans genre]
```

---

## ?? Logs et Debug

Dans les logs Render, vous verrez maintenant:

```
[INFO] Genre d?tect? via r?le 'Homme': homme
[INFO] Genre enregistr? pour user 123456789: homme
[INFO] Genre d?tect? pour JohnDoe: homme
[INFO] Calling ai_client.generate_response...
```

Cela vous permet de v?rifier que la d?tection fonctionne!

---

## ?? Personnalisation

### Ajouter d'Autres Mots-Cl?s

Si vous voulez ajouter d'autres mots-cl?s de d?tection, modifiez dans `bot.py`:

```python
ROLE_KEYWORDS = {
    "homme": ["homme", "men", "male", "mec", "garcon", "boy", "man", 
              "masculin"],  # ? Ajoutez ici
    "femme": ["femme", "women", "female", "fille", "girl", "woman",
              "feminin"],  # ? Ajoutez ici
    "non-binaire": ["non-binaire", "nonbinary", "enby", "nb", 
                     "non binaire", "they"],  # ? Ajoutez ici
    "trans": ["trans", "transgender", "ftm", "mtf"]  # ? Ajoutez ici
}
```

---

## ?? Avantages

### Pour les Utilisateurs:
? **Conversations plus naturelles** et personnalis?es  
? **Immersion accrue** (le bot s'adapte ? vous)  
? **Respect de l'identit?** de genre  
? **Langage appropri?** selon votre genre

### Pour le Serveur:
? **Inclusivit?** (support de tous les genres)  
? **Exp?rience am?lior?e** pour tous  
? **Configuration simple** (juste cr?er des r?les)  
? **D?tection automatique** (pas d'intervention manuelle)

---

## ?? Impact sur les R?ponses

| Situation | Sans D?tection | Avec D?tection |
|-----------|----------------|----------------|
| Compliment | "t'es sympa" | "t'es canon" (homme) / "t'es magnifique" (femme) |
| S?duction | G?n?rique | Adapt?e au genre |
| Tutoiement | Neutre | Genr? si appropri? |
| R?f?rences | Neutres | Personnalis?es |

---

## ?? FAQ

### Q: Que se passe-t-il si je n'ai pas de r?le de genre?

**R:** Le bot utilisera un **langage neutre** et s'adaptera au contexte de la conversation. Aucun probl?me!

---

### Q: Est-ce que je peux changer mon r?le en cours de conversation?

**R:** Oui! Changez votre r?le Discord et le bot d?tectera le changement au prochain message. Le cache sera mis ? jour automatiquement.

---

### Q: Le bot respecte-t-il mon genre?

**R:** Absolument! Le bot adapte son langage **respectueusement** selon votre genre d?tect?. Il utilise un langage inclusif pour les personnes non-binaires et trans.

---

### Q: Faut-il obligatoirement avoir un r?le de genre?

**R:** Non, c'est **optionnel**. Si aucun r?le n'est d?tect?, le bot fonctionne normalement avec un langage neutre.

---

### Q: Est-ce que mes informations de genre sont stock?es quelque part?

**R:** Le genre est stock? **temporairement en m?moire** pendant que le bot est actif, uniquement pour optimiser les performances. Rien n'est enregistr? dans des fichiers ou bases de donn?es.

---

### Q: Le bot peut-il d?tecter plusieurs genres?

**R:** Le bot d?tecte le **premier genre trouv?** dans vos r?les (dans l'ordre: homme, femme, non-binaire, trans). Si vous avez plusieurs r?les, le premier correspondant sera utilis?.

---

## ?? Conseils pour les Admins

### 1. Cr?ez des R?les Clairs
```
? BON: "Homme", "Femme", "Non-binaire"
? ?VITER: "Membre", "Actif", "VIP" (trop vagues)
```

### 2. Ajoutez des Emojis pour Visibilit?
```
?? Homme
?? Femme
?? Non-binaire
?????? Trans
```

### 3. Rendez-les Optionnels
Les membres doivent pouvoir **choisir** s'ils veulent afficher leur genre.

### 4. Communication
Informez vos membres que le bot adapte ses r?ponses selon ces r?les!

---

## ?? Cas d'Usage

### 1. Serveur NSFW Roleplay
Le bot adapte ses r?ponses sexuelles selon le genre de l'interlocuteur pour plus de r?alisme.

### 2. Serveur de Rencontre
Le bot peut faciliter les conversations en adaptant son langage (homme parlant ? femme, etc.)

### 3. Communaut? Inclusive
Support total des identit?s non-binaires et trans avec langage respectueux.

---

## ? R?sum?

| Fonctionnalit? | Status |
|----------------|--------|
| **D?tection automatique via r?les** | ? Actif |
| **Cache intelligent** | ? Actif |
| **Adaptation des r?ponses** | ? Actif |
| **Support homme/femme** | ? Actif |
| **Support non-binaire/trans** | ? Actif |
| **Langage inclusif** | ? Actif |
| **Logs de debug** | ? Actif |

---

## ?? D?ploiement

? **Code d?j? pouss? sur GitHub**  
? **Render red?ploie automatiquement (2-3 min)**

---

**Le bot adapte maintenant ses r?ponses selon votre genre pour des conversations ultra-immersives!** ??

**Configuration recommand?e:**
1. Cr?ez les r?les "Homme", "Femme", "Non-binaire" sur votre serveur Discord
2. Attribuez-les aux membres (optionnel)
3. Le bot d?tecte et adapte automatiquement!

---

**Testez dans 2-3 minutes apr?s le red?marrage Render!** ??
