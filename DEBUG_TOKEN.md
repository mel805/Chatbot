# 🔍 DEBUG - Token Discord Manquant

## 🎯 Situation Actuelle

Vous avez ajouté `DISCORD_BOT_TOKEN` dans Render mais le bot affiche toujours :
```
[X] Token manquant !
```

## 🔧 Nouveau Debug Ajouté

J'ai ajouté des logs de debug dans le code. Après le prochain déploiement, vous verrez dans les logs Render :

```
[DEBUG] Vérification des variables d'environnement...
[DEBUG] Variables disponibles contenant 'TOKEN' ou 'DISCORD':
[DEBUG]   - VARIABLE_NAME: valeur...
```

Cela nous dira **exactement** quelles variables Render voit.

---

## ✅ Actions Immédiates

### 1. Vérifier le Nom EXACT dans Render

**Problème possible :** Faute de frappe dans le nom de la variable.

Allez dans **Render Dashboard** → Votre service → **Environment**

Vérifiez que vous avez **EXACTEMENT** :
```
DISCORD_BOT_TOKEN
```

**PAS :**
- `DISCORD_TOKEN` ❌
- `BOT_TOKEN` ❌
- `Discord_Bot_Token` ❌ (majuscules importantes)
- `DISCORD_BOT_TOKEN ` ❌ (pas d'espace à la fin)

### 2. Vérifier qu'il N'y a Pas d'Espaces

Dans la **Value** du token :
- ❌ ` MTxxx...` (espace au début)
- ❌ `MTxxx... ` (espace à la fin)
- ✅ `MTxxx...` (pas d'espaces)

### 3. Vérifier que le Service a Bien Redémarré

Après avoir ajouté la variable :
1. Render doit afficher "Deploying..."
2. Attendre 2-3 minutes
3. Le service doit passer à "Live"

Si ce n'est pas le cas, **cliquez manuellement** sur :
- **Manual Deploy** → **Deploy latest commit**

---

## 🔍 Que Faire Maintenant

### Étape 1 : Attendre le Redéploiement (2-3 min)

Le code avec le debug vient d'être pushé. Render va redéployer.

### Étape 2 : Regarder les Nouveaux Logs

Vous verrez maintenant :
```
[DEBUG] Vérification des variables d'environnement...
[DEBUG] Variables disponibles contenant 'TOKEN' ou 'DISCORD':
```

**Si vous voyez :** `[DEBUG]   - DISCORD_BOT_TOKEN: MTxxx...`
→ ✅ Le token est là, mais il y a un autre problème

**Si vous NE voyez RIEN après "Variables disponibles":**
→ ❌ Le token n'est pas défini dans Render

### Étape 3 : Selon le Résultat

#### Cas A : Le token apparaît dans les logs debug

→ Il y a un problème avec `os.getenv()` ou `load_dotenv()`
→ Je corrigerai le code

#### Cas B : Le token n'apparaît PAS dans les logs

→ Le token n'est vraiment pas défini dans Render
→ Voici la checklist complète :

---

## 📋 Checklist Complète Render

### Dans Render Dashboard

1. ✅ Connecté à https://render.com
2. ✅ Service correct sélectionné (votre bot Discord)
3. ✅ Menu gauche → **Environment**
4. ✅ Cliquez sur **"Add Environment Variable"** (ou Edit si existe)
5. ✅ Dans **Key** : Tapez **exactement** `DISCORD_BOT_TOKEN`
6. ✅ Dans **Value** : Collez votre token (sans espaces)
7. ✅ Cliquez **"Save Changes"**
8. ✅ Vérifiez que la variable apparaît dans la liste :
   ```
   DISCORD_BOT_TOKEN: ••••••••••••••••••
   ```
9. ✅ Attendez "Deploying..." → "Live" (2-3 min)

### Si la Variable Est Là Mais Masquée

Render masque les valeurs par défaut (••••••).

**Pour vérifier qu'elle est bien là :**
- Cliquez sur l'icône "œil" 👁️ à côté de la variable
- Ou cliquez "Edit" pour voir la valeur

---

## 🆘 Solution Alternative - Script de Test

Si vraiment ça ne marche pas, on peut aussi tester avec un script :

1. Dans Render, allez dans **Shell** (si disponible)
2. Tapez :
   ```bash
   python3 debug_env.py
   ```
3. Cela affichera toutes les variables

---

## 📞 Prochaines Étapes

1. **Attendez** le redéploiement (2-3 min)
2. **Regardez** les nouveaux logs avec `[DEBUG]`
3. **Copiez-moi** la section des logs qui commence par :
   ```
   [DEBUG] Vérification des variables...
   ```
   jusqu'à :
   ```
   [X] Token manquant !
   ```

Avec ces logs, je pourrai voir **exactement** ce qui se passe.

---

## 💡 Causes Possibles

1. **Nom de variable incorrect** (faute de frappe)
2. **Variable non sauvegardée** dans Render
3. **Service pas redémarré** après ajout de la variable
4. **Espace** dans le token ou le nom de variable
5. **Cache** de Render (rare, mais possible)

---

**Envoyez-moi les nouveaux logs avec [DEBUG] dès que le déploiement est terminé ! 🔍**
