# 🎨 Système de Génération d'Images UNIQUE

## ✨ Nouveautés : Personnalisation Complète !

Maintenant, chaque image générée est **vraiment unique** en utilisant :
- 🏠 **Nom du serveur Discord**
- 👤 **Pseudo du membre**
- 🎭 **Type NSFW choisi**
- ⏰ **Timestamp de génération**

## 🎯 Catégories NSFW Disponibles

### 1. **Softcore** (Sensuel, Élégant)
Styles : `sensual`, `elegant`, `artistic nude`, `glamour photography`, `boudoir`

### 2. **Romantic** (Romantique, Intime)
Styles : `intimate moment`, `passionate embrace`, `romantic atmosphere`, `candlelit`

### 3. **Intense** (Explicite, Provocant)
Styles : `explicit scene`, `provocative pose`, `seductive`, `erotic art`

### 4. **Fantasy** (Fantaisie, Magique)
Styles : `magical setting`, `fantasy character`, `mythical creature`, `dreamlike`

### 5. **Artistic** (Art, Classique)
Styles : `fine art photography`, `classical painting style`, `renaissance art`, `artistic nude`

## 🌈 Éléments de Variation Aléatoire

### Styles Visuels (15 variantes)
- Cinematic lighting
- Studio photography
- Natural light
- Dramatic shadows
- Soft focus
- Bokeh background
- High contrast
- Vintage film
- Digital art
- Oil painting style
- Watercolor art
- Anime style
- Realistic 3D render
- Hyperrealistic
- Photorealistic

### Ambiances (12 variantes)
- Sensual
- Mysterious
- Playful
- Elegant
- Passionate
- Dreamy
- Intense
- Romantic
- Seductive
- Artistic
- Glamorous
- Intimate

### Lieux/Settings (12 variantes)
- Luxury bedroom
- Modern apartment
- Beach sunset
- Forest clearing
- Cozy cabin
- Elegant hotel room
- Private pool
- Rooftop terrace
- Art studio
- Japanese onsen
- Tropical paradise
- Penthouse suite

## 🎮 Commandes Disponibles

### `/generate_image [prompt]`
Génération automatique avec détection du type selon le chatbot actif
```
/generate_image prompt:beautiful woman in nature
```

### `/generate_unique [prompt] [style]`
🆕 Génération avec choix manuel du style NSFW
```
/generate_unique prompt:elegant portrait style:romantic
/generate_unique prompt:fantasy scene style:fantasy
/generate_unique prompt:artistic nude style:artistic
```

**Paramètres :**
- `prompt` : Description de l'image (requis)
- `style` : Type NSFW - `softcore`, `romantic`, `intense`, `fantasy`, `artistic` (optionnel, défaut: artistic)

### Bouton "Générer Image" (Menu Principal)
Génération contextuelle basée sur le chatbot actif

## 🔮 Comment ça Fonctionne ?

### 1. Création du Seed Unique
```python
seed = hash(server_name + username + timestamp)
```
→ Chaque génération a un seed différent = résultat unique !

### 2. Sélection des Éléments
Basé sur le seed, le système choisit :
- 1 style visuel parmi 15
- 1 ambiance parmi 12
- 1 lieu parmi 12
- 1 style NSFW selon la catégorie

### 3. Construction du Prompt
```
[Prompt de base] + [Description personnage] + [Style NSFW] + 
[Ambiance] + [Lieu] + [Style visuel] + [Qualité] + 
[Thème du serveur]
```

### Exemple de Prompt Généré
**Input :**
- Prompt: "beautiful woman"
- Serveur: "Mon Serveur Discord"
- User: "Player123"
- Style: "romantic"

**Output (prompt interne) :**
```
beautiful woman, intimate moment, passionate, 
in elegant hotel room, cinematic lighting, 
masterpiece, best quality, highly detailed, 8k, 
professional photography, themed after Mon Serveur Discord
```

## 📊 Statistiques de Variation

### Combinaisons Possibles
- **5 catégories NSFW** × **5 styles par catégorie** = 25 styles de base
- **15 styles visuels** × **12 ambiances** × **12 lieux** = 2,160 variations
- **Total : 54,000+ combinaisons uniques !**

Et avec le seed basé sur timestamp, c'est **infini** !

## 🎨 Exemples d'Utilisation

### Scénario 1 : Génération Automatique avec Chatbot
```
1. Utilisateur active le chatbot "Emma" (romantique)
2. Clique sur "Générer Image" dans le menu
3. Le système détecte le type "romantic" automatiquement
4. Génère une image romantique unique pour ce serveur+user
```

### Scénario 2 : Génération Manuelle avec Style
```
/generate_unique prompt:fantasy elf warrior style:fantasy
→ Génère une guerrière elfe avec style fantaisie
→ Éléments aléatoires basés sur serveur+user+timestamp
```

### Scénario 3 : Prompt Personnalisé
```
/generate_image prompt:woman with red hair on a beach at sunset
→ Détecte automatiquement le style selon contexte
→ Ajoute des variations uniques (ambiance, lieu, éclairage)
```

## 🔍 Détection Automatique du Type NSFW

Quand un chatbot est actif, le système détecte automatiquement :

| Personnalité Chatbot | Type NSFW Détecté |
|---------------------|-------------------|
| Romantique, Doux    | **Romantic**      |
| Intense, Dominant   | **Intense**       |
| Fantaisie, Magique  | **Fantasy**       |
| Sensuel, Élégant    | **Softcore**      |
| Autre               | **Artistic**      |

## 📋 Informations Affichées

Chaque image générée affiche :
- ✅ **Prompt utilisé**
- ✅ **Style NSFW choisi**
- ✅ **Nom du membre**
- ✅ **Nom du serveur**
- ✅ **Message de confirmation d'unicité**

### Exemple d'Embed
```
🎨 Image Unique Générée !

Prompt: beautiful woman in elegant dress

Cette image est 100% unique, générée spécialement 
pour Player123 sur le serveur Mon Serveur avec un 
style romantic !

🎭 Style NSFW: Romantic
👤 Créé pour: Player123
🏠 Serveur: Mon Serveur

✨ Chaque génération est vraiment unique | 
Seed basé sur Mon Serveur+Player123+timestamp
```

## 🛠️ Configuration Technique

### Fichier : `image_generator.py`

**Nouvelles fonctionnalités :**
- `_get_random_elements(seed)` : Génère éléments aléatoires
- `_enhance_prompt_nsfw()` : Amélioration avec contexte serveur+user
- Seed unique basé sur MD5 hash

**Paramètres de `generate()` :**
```python
await image_generator.generate(
    prompt="...",
    character_desc="...",
    server_name="Mon Serveur",      # 🆕 Nouveau
    username="Player123",            # 🆕 Nouveau
    nsfw_type="romantic",            # 🆕 Nouveau
    prefer_speed=True
)
```

## 🎊 Avantages du Nouveau Système

### ✅ Vraiment Unique
Chaque image est différente, même avec le même prompt !

### ✅ Personnalisé
Intègre le contexte du serveur et du membre

### ✅ Varié
Milliers de combinaisons possibles

### ✅ Contextuel
S'adapte au chatbot actif automatiquement

### ✅ Contrôlable
L'utilisateur peut choisir le style manuellement

### ✅ Traçable
Affiche clairement pour qui et où l'image a été créée

## 🚀 Pour Utiliser

### 1. Redémarrer le bot
Les modifications sont dans le code, redémarrez pour activer

### 2. Tester les nouvelles commandes
```
/generate_unique prompt:test style:romantic
```

### 3. Vérifier les variations
Générez plusieurs fois avec le même prompt → toujours différent !

## 📈 Logs de Debug

Dans la console, vous verrez :
```
[DEBUG] Génération image NSFW unique...
[DEBUG] Serveur: Mon Serveur | User: Player123 | Type: romantic
[DEBUG] Prompt unique généré - Seed: 12345678, Style: passionate embrace
[DEBUG] Éléments: intimate | elegant hotel room | cinematic lighting
```

## 🎯 Conclusion

Le système génère maintenant des images **100% uniques** en combinant :
- 🏠 Contexte du serveur
- 👤 Identité du membre
- 🎭 Style NSFW choisi
- 🌈 Variations aléatoires infinies
- ⏰ Timestamp unique

**Chaque image raconte une histoire unique pour chaque membre sur chaque serveur ! ✨**
