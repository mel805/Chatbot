# ?? NOUVEAUT?S - Slash Commands (/)

## ? Changement Important: Commandes Slash

Le bot utilise maintenant les **Slash Commands** modernes de Discord!

## ?? Qu'est-ce qui a chang??

### Avant (anciennes commandes avec `!`)
```
!start
!personality coquin
!reset
!help_bot
```

### Maintenant (nouvelles commandes avec `/`)
```
/start
/personality    ? Menu d?roulant interactif!
/reset
/help
```

## ? Pourquoi ce changement?

### Avantages des Slash Commands:

1. **?? Auto-compl?tion**
   - Tapez `/` et toutes les commandes s'affichent automatiquement
   - Discord vous guide avec des descriptions

2. **?? Menu d?roulant pour /personality**
   - Plus besoin de se souvenir des noms
   - S?lectionnez visuellement parmi les 8 personnalit?s
   - Descriptions visibles directement

3. **? Plus propre**
   - Pas de spam de commandes invalides dans le chat
   - Interface native Discord

4. **?? Plus moderne**
   - Standard Discord actuel
   - Meilleure exp?rience utilisateur

## ?? Comment utiliser?

### M?thode simple:
```
1. Tapez /
2. Choisissez votre commande dans la liste
3. Appuyez sur Entr?e
```

### Exemple avec /personality:
```
1. Tapez /personality
2. Un menu appara?t avec:
   ?? Amical
   ?? S?ducteur
   ?? Coquin
   ?? Romantique
   ?? Dominant
   ?? Soumis
   ?? Joueur
   ?? Intellectuel
3. Cliquez sur celui que vous voulez
4. Appuyez sur Entr?e
```

## ?? Configuration requise

### Important: Permissions Discord

Pour que les slash commands fonctionnent, le bot doit avoir la permission `applications.commands`.

#### Si vous invitez le bot pour la premi?re fois:

1. Allez dans Discord Developer Portal
2. OAuth2 ? URL Generator
3. Cochez:
   - ? `bot`
   - ? `applications.commands` ? **NOUVEAU!**
4. Dans Bot Permissions:
   - Read Messages/View Channels
   - Send Messages
   - Send Messages in Threads
   - Read Message History
   - Embed Links
5. Utilisez la nouvelle URL g?n?r?e

#### Si le bot est d?j? sur votre serveur:

**Option 1: R?inviter** (recommand?)
- G?n?rez la nouvelle URL avec `applications.commands`
- Ouvrez-la (le bot ne sera pas dupliqu?)
- Les permissions seront mises ? jour

**Option 2: Permissions manuelles**
- Param?tres serveur ? Int?grations
- Trouvez votre bot
- Activez les permissions n?cessaires

## ?? Liste compl?te des commandes

### Admin uniquement (??)

| Commande | Description | Changement |
|----------|-------------|------------|
| `/start` | Active le bot | M?me fonction |
| `/stop` | D?sactive le bot | M?me fonction |
| `/personality` | Change la personnalit? | **Maintenant avec menu!** |
| `/reset` | R?initialise l'historique | M?me fonction |

### Tout le monde (??)

| Commande | Description | Changement |
|----------|-------------|------------|
| `/status` | Affiche le statut | M?me fonction |
| `/help` | Affiche l'aide | Nouveau nom (avant: `!help_bot`) |

## ?? Exemple d'utilisation compl?te

```
=== PREMI?RE UTILISATION ===

Administrateur:
/start
[Appuie sur Entr?e]

Bot:
? Bot Activ?!
Je suis actif avec la personnalit? Amical ??

=== CHANGER DE PERSONNALIT? ===

Administrateur:
/personality
[Un menu s'affiche]
[S?lectionne "?? Coquin - Os? et provocateur"]
[Appuie sur Entr?e]

Bot:
? Personnalit? Chang?e!
Nouvelle personnalit?: Coquin ??

=== CONVERSATION ===

Utilisateur:
@Bot Salut! ??

Bot:
Hey... *te regarde avec un sourire en coin* 
Quelqu'un est d'humeur coquine ce soir? ??

=== V?RIFIER LE STATUT ===

Utilisateur:
/status

Bot:
?? Statut du Bot
?tat: ?? Actif
Personnalit?: Coquin ??
Messages en m?moire: 4
Mod?le IA: llama-3.1-70b-versatile
```

## ? Probl?mes courants

### Les slash commands n'apparaissent pas?

1. ? **Red?marrez le bot** - Elles se synchronisent au d?marrage
2. ? **V?rifiez les permissions** - `applications.commands` n?cessaire
3. ? **R?invitez le bot** - Avec la nouvelle URL
4. ? **Attendez 1-2 minutes** - La synchronisation peut prendre du temps
5. ? **V?rifiez le log** au d?marrage du bot:
   ```
   ? 6 commandes slash synchronis?es!
   ```

### Le menu d?roulant ne s'affiche pas?

- Mettez ? jour votre client Discord (web/desktop/mobile)
- Assurez-vous d'appuyer sur `/personality` puis d'attendre le menu

### "Cette interaction a ?chou?"?

- Le bot n'est peut-?tre pas en ligne
- V?rifiez que le bot a les bonnes permissions
- Red?marrez le bot

## ?? Documentation compl?te

Pour plus de d?tails, consultez:

- **SLASH_COMMANDS.md** - Guide complet des slash commands
- **README.md** - Documentation principale
- **GUIDE_RAPIDE.md** - Installation rapide
- **DEMARRAGE.md** - Guide de d?marrage

## ?? Profitez-en!

Les slash commands rendent le bot beaucoup plus facile ? utiliser!

**Tapez simplement `/` et laissez-vous guider!** ?

---

**Note**: Les anciennes commandes avec `!` ne fonctionnent plus. Utilisez uniquement les slash commands `/`.
