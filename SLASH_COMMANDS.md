# ? Guide des Slash Commands

## ?? Nouveau: Commandes Slash (/)

Le bot utilise maintenant les **Slash Commands** modernes de Discord au lieu des commandes pr?fix?es (`!`).

## ? Avantages des Slash Commands

- ? **Auto-compl?tion** - Discord sugg?re automatiquement les commandes disponibles
- ? **Menu d?roulant** - Pour `/personality`, un menu interactif avec toutes les options
- ? **Descriptions** - Chaque commande affiche sa description directement
- ? **Plus propre** - Pas de spam dans le chat avec des commandes invalides
- ? **Plus moderne** - Interface utilisateur Discord native

## ?? Configuration dans Discord Developer Portal

### IMPORTANT: Activer les Slash Commands

Lors de l'invitation du bot, assurez-vous de:

1. Allez dans **OAuth2** ? **URL Generator**
2. Cochez:
   - ? **bot**
   - ? **applications.commands** (NOUVEAU - n?cessaire pour les slash commands)
3. Dans Bot Permissions, cochez:
   - Read Messages/View Channels
   - Send Messages
   - Send Messages in Threads
   - Read Message History
   - Embed Links
4. Utilisez la nouvelle URL g?n?r?e pour inviter/r?inviter le bot

### Si le bot est d?j? invit?

Si vous aviez d?j? invit? le bot AVANT ce changement:

**Option 1: R?inviter avec la nouvelle URL**
- G?n?rez une nouvelle URL avec `applications.commands` coch?
- Utilisez cette URL (le bot ne sera pas dupliqu?)

**Option 2: Donner manuellement la permission**
- Dans les param?tres du serveur ? Int?grations
- Trouvez votre bot
- Activez les permissions n?cessaires

## ?? Liste des Commandes Slash

### Commandes Admin (?? Administrateur requis)

#### `/start`
**Description**: Active le bot dans le canal actuel  
**Usage**: Tapez `/start` et appuyez sur Entr?e  
**R?sultat**: Le bot commence ? r?pondre quand il est mentionn?

```
/start
```

---

#### `/stop`
**Description**: D?sactive le bot dans le canal actuel  
**Usage**: Tapez `/stop` et appuyez sur Entr?e  
**R?sultat**: Le bot arr?te de r?pondre dans ce canal

```
/stop
```

---

#### `/personality`
**Description**: Change la personnalit? du bot  
**Usage**: Tapez `/personality` et **s?lectionnez dans le menu d?roulant**  
**Options disponibles**:
- ?? Amical - Sympathique et ouvert
- ?? S?ducteur - Charmant et flirteur
- ?? Coquin - Os? et provocateur
- ?? Romantique - Doux et passionn?
- ?? Dominant - Confiant et autoritaire
- ?? Soumis - Respectueux et d?vou?
- ?? Joueur - Fun et gamer
- ?? Intellectuel - Cultiv? et profond

```
/personality
[S?lectionner dans le menu qui appara?t]
```

**Note**: L'historique de conversation est automatiquement r?initialis? quand vous changez de personnalit?.

---

#### `/reset`
**Description**: R?initialise l'historique de conversation du canal  
**Usage**: Tapez `/reset` et appuyez sur Entr?e  
**R?sultat**: Le bot oublie tous les messages pr?c?dents de ce canal

```
/reset
```

---

### Commandes Publiques (?? Tout le monde)

#### `/status`
**Description**: Affiche le statut actuel du bot dans ce canal  
**Usage**: Tapez `/status` et appuyez sur Entr?e  
**Affiche**:
- ?tat (actif/inactif)
- Personnalit? actuelle
- Nombre de messages en m?moire
- Mod?le IA utilis?

```
/status
```

---

#### `/help`
**Description**: Affiche l'aide compl?te du bot  
**Usage**: Tapez `/help` et appuyez sur Entr?e  
**Affiche**: Guide complet des commandes et fonctionnalit?s

```
/help
```

---

## ?? Comment utiliser les Slash Commands

### M?thode 1: Auto-compl?tion

1. Tapez `/` dans Discord
2. Une liste de toutes les commandes disponibles appara?t
3. Cliquez sur la commande voulue ou utilisez les fl?ches ??
4. Appuyez sur Entr?e

### M?thode 2: Directement

1. Tapez `/start` (ou autre commande)
2. La commande s'affiche avec sa description
3. Appuyez sur Entr?e pour ex?cuter

### M?thode 3: Menu d?roulant (pour /personality)

1. Tapez `/personality`
2. Un champ avec un menu d?roulant appara?t
3. Cliquez dessus pour voir toutes les options
4. S?lectionnez une personnalit?
5. Appuyez sur Entr?e

## ?? Exemples d'utilisation

### Exemple 1: Premier d?marrage

```
Administrateur tape: /start
[Appuie sur Entr?e]

Bot r?pond:
? Bot Activ?!
Je suis maintenant actif dans ce canal avec la personnalit? Amical ??

?? Comment interagir?
? Mentionnez-moi (@bot)
? R?pondez ? mes messages
? En message priv?
```

### Exemple 2: Changer de personnalit?

```
Administrateur tape: /personality
[Un menu d?roulant appara?t]
[S?lectionne "?? Coquin - Os? et provocateur"]
[Appuie sur Entr?e]

Bot r?pond:
? Personnalit? Chang?e!
Nouvelle personnalit?: Coquin ??

[Description de la personnalit? s'affiche]
```

### Exemple 3: V?rifier le statut

```
Utilisateur tape: /status
[Appuie sur Entr?e]

Bot r?pond:
?? Statut du Bot

?tat: ?? Actif
Personnalit?: Coquin ??
Messages en m?moire: 12
Mod?le IA: llama-3.1-70b-versatile
```

### Exemple 4: Conversation normale

```
Utilisateur: @Bot Salut!
Bot: Hey! Comment tu vas? ??

Utilisateur r?pond au message du bot: ?a va bien, et toi?
Bot: Super! Content de discuter avec toi! ??
```

## ?? Migration depuis les anciennes commandes

| Ancienne commande | Nouvelle commande | Changement |
|-------------------|-------------------|------------|
| `!start` | `/start` | M?me fonction |
| `!stop` | `/stop` | M?me fonction |
| `!personality` | `/personality` | Maintenant avec menu d?roulant |
| `!personality coquin` | `/personality` ? s?lectionner | Plus interactif |
| `!reset` | `/reset` | M?me fonction |
| `!status` | `/status` | M?me fonction |
| `!help_bot` | `/help` | Nom simplifi? |

## ? FAQ

### Les slash commands n'apparaissent pas?

1. **Red?marrez le bot** - Les commandes se synchronisent au d?marrage
2. **V?rifiez les permissions** - Le bot doit avoir `applications.commands`
3. **R?invitez le bot** - Avec la nouvelle URL OAuth2
4. **Attendez quelques minutes** - La synchronisation peut prendre du temps

### Je pr?f?re les anciennes commandes `!`

Les slash commands sont maintenant le standard Discord et offrent une bien meilleure exp?rience utilisateur. Les anciennes commandes pr?fix?es ne sont plus support?es.

### Le menu d?roulant ne s'affiche pas?

Assurez-vous d'utiliser une version r?cente de Discord (web, desktop, ou mobile).

### Les commandes admin ne fonctionnent pas?

V?rifiez que vous avez bien les **permissions d'administrateur** sur le serveur.

## ?? Profitez des Slash Commands!

Les slash commands rendent l'utilisation du bot beaucoup plus intuitive et agr?able! 

**Tapez simplement `/` et laissez-vous guider!** ?
