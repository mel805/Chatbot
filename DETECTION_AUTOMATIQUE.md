# ?? D?tection Automatique des Messages - Guide Complet

## ?? Nouveau Syst?me de R?ponse Intelligent

Le bot d?tecte maintenant automatiquement les messages qui lui sont destin?s, m?me **sans mention directe**.

---

## ?? Taux de R?ponse par Type

| Type de Message | Probabilit? | Exemple |
|----------------|-------------|---------|
| **@Bot mention** | 100% ? | `@Luna salut` |
| **R?ponse ? son message** | 100% ? | [Clic sur Reply du bot] |
| **Nom de personnalit?** | 100% ? | `Luna tu fais quoi?` |
| **Salutations** | 90% ?? | `bonjour`, `hello`, `salut` |
| **Questions** | 60% ?? | `qui est l??`, `comment ?a va?` |
| **Messages normaux** | 20% ?? | Messages al?atoires |

---

## ?? 1. D?tection du Nom de Personnalit?

Le bot r?pond **automatiquement ? 100%** si son nom est mentionn? dans le message.

### Exemples:

```
User: Luna t'es l??
Bot: ouais je suis l? ??

User: hey Luna, ?a va?
Bot: ?a va et toi?

User: Damien viens par ici
Bot: j'arrive
```

**Fonctionne avec tous les noms:**
- Luna, Damien, Catherine, Victoria, Alex, Jade, etc.
- **Pas besoin de @mention!**

---

## ?? 2. Salutations (90% de r?ponse)

Le bot d?tecte ces mots et r?pond **90% du temps**:

### Mots d?tect?s:
- `bonjour`
- `hello`
- `salut`
- `hey`
- `coucou`
- `cc`
- `yo`
- `bonsoir`
- `hi`
- `bjr`
- `slt`

### Exemples:

```
User: bonjour tout le monde
Bot: salut! ??

User: hey
Bot: yo

User: cc les gens
Bot: cc! ?a va?
```

**Le bot participe naturellement aux salutations du channel!**

---

## ? 3. Questions (60% de r?ponse)

Le bot d?tecte les questions et r?pond **60% du temps**, m?me sans mention.

### D?tection:
- `?` (point d'interrogation)
- `qui`, `quoi`, `comment`, `pourquoi`, `o?`, `quand`

### Exemples:

```
User: quelqu'un sait o? est le fichier?
Bot: non d?sol? je sais pas

User: qui veut jouer?
Bot: moi je veux bien

User: comment vous allez?
Bot: bien et toi?
```

**Le bot participe aux conversations avec questions!**

---

## ?? 4. Messages Normaux (20% de r?ponse)

Pour tous les autres messages, le bot a **20% de chance** de r?pondre spontan?ment.

```
User: j'ai eu une journ?e de fou
Bot: ah ouais? raconte
[20% de chance]

User: je vais manger
Bot: bon app?tit!
[20% de chance]
```

**Cela rend le bot plus naturel et immersif!**

---

## ?? Priorit? de D?tection

Le bot v?rifie dans cet ordre:

```
1. @Mention directe          ? 100% TOUJOURS
2. R?ponse ? son message     ? 100% TOUJOURS
3. Nom de personnalit?       ? 100% TOUJOURS
4. Salutation d?tect?e       ? 90% TR?S PROBABLE
5. Question d?tect?e         ? 60% PROBABLE
6. Message normal            ? 20% RARE
```

---

## ?? Exemples de Conversations Naturelles

### Scenario 1: Arriv?e d'un Membre

```
User1: bonjour
Luna: salut! ?? [90%]

User2: hey tout le monde
Luna: hey! [90%]

User1: ?a va les gens?
Luna: ouais ?a va et toi? [60% - question]
```

### Scenario 2: Conversation Normale

```
User1: qui veut regarder un film?
Luna: ?a d?pend quel film [60% - question]

User2: un film d'horreur
Luna: ah non moi j'aime pas trop ?a [20% spontan?]

User1: Luna t'aimes quoi comme films?
Luna: j'aime bien les com?dies perso [100% - nom]
```

### Scenario 3: Channel NSFW

```
User: hey
Catherine: salut ?? [90%]

User: t'es seule?
Catherine: ouais pourquoi? [60% - question]

User: Catherine viens en dm
Catherine: j'arrive ?? [100% - nom]
```

---

## ?? Configuration Technique

### Dans `bot.py`:

```python
# D?tection des salutations
greetings = ['bonjour', 'hello', 'salut', 'hey', 'coucou', 
             'cc', 'yo', 'bonsoir', 'hi', 'bjr', 'slt']
is_greeting = any(greeting in message_lower.split() for greeting in greetings)

# Salutations -> 90% de r?ponse
if is_greeting:
    if random.random() < 0.9:  # 90%
        should_respond_naturally = True
```

---

## ?? Comparaison Avant/Apr?s

| Situation | Avant | Maintenant |
|-----------|-------|------------|
| User: `bonjour` | 30% | **90%** ?? |
| User: `Luna ?a va?` | 30% | **100%** ? |
| User: `qui est l??` | 30% | **60%** ?? |
| User: `@Bot salut` | 100% | **100%** ? |
| Message normal | 30% | **20%** |

**Le bot est maintenant beaucoup plus r?actif aux interactions sociales!**

---

## ?? Personnalisation

Vous pouvez ajuster les pourcentages dans `bot.py`:

```python
# Lignes ? modifier pour changer les taux

# Salutations (actuellement 90%)
elif is_greeting:
    if random.random() < 0.9:  # Changez 0.9 (90%) ici
        should_respond_naturally = True

# Questions (actuellement 60%)
elif is_question:
    if random.random() < 0.6:  # Changez 0.6 (60%) ici
        should_respond_naturally = True

# Messages normaux (actuellement 20%)
elif random.random() < 0.2:  # Changez 0.2 (20%) ici
    should_respond_naturally = True
```

---

## ?? Ajout de Nouveaux Mots de Salutation

Pour ajouter d'autres salutations d?tect?es, modifiez dans `bot.py`:

```python
greetings = [
    'bonjour', 'hello', 'salut', 'hey', 'coucou',
    'cc', 'yo', 'bonsoir', 'hi', 'bjr', 'slt',
    # Ajoutez les v?tres ici:
    'wesh', 'kikou', 'hola', 'ciao'
]
```

---

## ?? R?sultat

Le bot se comporte maintenant comme un **vrai membre actif** du serveur:

? **R?pond aux salutations** (naturel et social)  
? **Participe aux questions** (engageant)  
? **R?agit ? son nom** (attentif)  
? **Intervient spontan?ment** (vivant)

**Plus besoin de toujours mentionner le bot!**

---

## ?? Debug/Logs

Dans les logs Render, vous verrez maintenant:

```
[INFO] Salutation detectee - reponse naturelle (90% chance)
[INFO] Question detectee - reponse naturelle (60% chance)
[INFO] Nom de la personnalite detecte: luna
[INFO] Reponse naturelle spontanee (20% chance)
```

Cela vous aide ? comprendre pourquoi le bot r?pond.

---

## ?? Conseils d'Utilisation

### Pour Plus d'Interactions:

1. **Utilisez le nom du bot**: `Luna tu fais quoi?` ? 100%
2. **Dites bonjour en arrivant**: Le bot r?pondra presque toujours
3. **Posez des questions ouvertes**: 60% de chance qu'il participe
4. **R?pondez ? ses messages**: 100% qu'il continue la conversation

### Pour Moins d'Interactions:

1. **Messages g?n?raux**: Le bot n'intervient que 20% du temps
2. **Pas de salutation ni question**: Moins de r?ponses spontan?es

---

**Le bot est maintenant BEAUCOUP plus interactif et naturel!** ??
