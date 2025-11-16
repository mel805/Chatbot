# 🚀 Déploiement des Nouvelles Commandes

## ⚠️ IMPORTANT : Les commandes sont dans le code mais pas encore synchronisées !

Les commandes `/rank` et `/leaderboard` sont bien ajoutées au bot, mais Discord ne les voit pas encore.

## 📋 Solution : Redémarrer le bot

### Option 1 : Sur Render.com (Hébergement)

1. **Allez sur votre Dashboard Render**
   - https://dashboard.render.com

2. **Sélectionnez votre service**
   - Cliquez sur votre bot Discord

3. **Redémarrez manuellement**
   - Cliquez sur **"Manual Deploy"** → **"Deploy latest commit"**
   - OU cliquez sur **"Restart"** dans les paramètres

4. **Attendez 2-3 minutes**
   - Le bot va redémarrer
   - Les commandes seront synchronisées automatiquement

### Option 2 : En local (Test)

Si vous testez en local :

```bash
# Arrêter le bot (Ctrl+C)
# Puis relancer :
python discord_bot_main.py
```

## ✅ Vérifier que ça marche

Une fois le bot redémarré, dans Discord :

1. Tapez `/` dans un canal
2. Vous devriez voir :
   - `/rank` - Voir ta carte de level unique
   - `/leaderboard` - Voir le classement des niveaux
   - `/start` (existant)
   - `/stop` (existant)
   - `/generate_image` (existant)

## 🔍 Si les commandes n'apparaissent toujours pas

### Vérifier les logs Render

Dans Render Dashboard → Logs, cherchez :
```
[OK] 5 commandes synchronisees
```

Cela confirme que les 5 commandes sont enregistrées.

### Forcer la synchronisation

Si besoin, vous pouvez ajouter cette ligne temporaire dans le code :

```python
# Dans on_ready()
await bot.tree.sync(guild=discord.Object(id=VOTRE_SERVER_ID))
```

Cela force la synchro pour un serveur spécifique (plus rapide).

## 🎮 Commandes disponibles après redémarrage

```
/start              → Menu principal (existant)
/stop               → Terminer conversation (existant)
/generate_image     → Générer image NSFW (existant)
/rank [membre]      → 🆕 Voir carte de level unique
/leaderboard [top]  → 🆕 Voir le classement
```

## 💡 Pourquoi ce problème ?

Discord met en cache les commandes slash. Quand vous ajoutez de nouvelles commandes :
1. Le bot doit redémarrer
2. Au démarrage, il appelle `bot.tree.sync()`
3. Discord enregistre les nouvelles commandes
4. Elles deviennent visibles (peut prendre 1-2 minutes)

## 🔧 Code de synchronisation actuel

Dans `discord_bot_main.py` ligne 494-498 :

```python
try:
    synced = await bot.tree.sync()
    print(f"[OK] {len(synced)} commandes synchronisees")
except Exception as e:
    print(f"[ERREUR] Sync commandes : {e}")
```

Cela devrait afficher `[OK] 5 commandes synchronisees` dans les logs.

## ✨ Après redémarrage

Les cartes de level fonctionneront :
- `/rank` génère une carte unique à chaque fois
- `/leaderboard` affiche le classement
- XP automatique à chaque message
- Notifications de level up

**Redémarrez simplement le bot sur Render et les commandes apparaîtront ! 🚀**
