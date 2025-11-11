# 📋 Comment Voir les Logs Render - Guide Complet

## 🎯 Où Trouver les Logs

### **Méthode 1 : Via l'Interface Render (Recommandé)**

1. **Connectez-vous** à https://render.com
2. **Cliquez** sur votre service (le bot Discord)
3. Dans le menu en haut, vous verrez plusieurs onglets :
   - Overview
   - Events
   - **Logs** ← CLIQUEZ ICI
   - Shell
   - Metrics
   - Settings
4. Cliquez sur **"Logs"**
5. Les logs s'affichent en temps réel

### **Méthode 2 : Vérifier le Déploiement**

Avant de regarder les logs, vérifiez que le service a bien redéployé :

1. Dans votre service, regardez en haut
2. Vous devriez voir :
   ```
   ● Live    (vert si tout va bien)
   ou
   ● Deploying...    (orange pendant le déploiement)
   ou  
   ● Deploy failed    (rouge si échec)
   ```

---

## ⏰ Si Vous Voyez "Deploying..."

**C'est normal !** Le déploiement prend 2-3 minutes.

**Attendez** que ça passe à :
- ✅ **"Live"** (vert) → Le bot est démarré
- ❌ **"Deploy failed"** (rouge) → Erreur de build

---

## 🔍 Que Chercher dans les Logs

Une fois dans **Logs**, scrollez jusqu'en bas et cherchez :

```
[OK] HTTP server sur port 10000
[DEBUG] ========================================
[DEBUG] Vérification des variables d'environnement...
```

**Si vous voyez ça**, copiez TOUT depuis `[DEBUG]` jusqu'à `[X] Token manquant !`

**Si vous ne voyez pas ça**, le nouveau code n'est pas encore déployé.

---

## 🚀 Forcer le Redéploiement

Si après 5 minutes vous ne voyez toujours pas les nouveaux logs avec `[DEBUG]` :

### **Étape 1 : Vérifier le Dernier Déploiement**

1. Dans votre service → **Events**
2. Regardez le dernier événement
3. Vous devriez voir quelque chose comme :
   ```
   Deploy live
   Nov 11, 11:XX AM
   deploy bb92649
   ```

### **Étape 2 : Forcer un Nouveau Déploiement**

1. En haut à droite → **"Manual Deploy"**
2. Cliquez sur **"Deploy latest commit"**
3. Attendez 2-3 minutes
4. Retournez dans **Logs**

---

## 📸 À Quoi Ressemblent les Logs

### **Anciens Logs (Avant mon Fix)**

```
[OK] HTTP server sur port 10000
[X] Token manquant !
```

### **Nouveaux Logs (Après mon Fix)**

```
[OK] HTTP server sur port 10000
[DEBUG] ========================================
[DEBUG] Vérification des variables d'environnement...
[DEBUG] Nombre total de variables: 25
[DEBUG] ========================================
[DEBUG] Variables contenant 'TOKEN' ou 'DISCORD':
[DEBUG]   ✓ DISCORD_BOT_TOKEN: MTxxxxxxxxx...
[DEBUG] ========================================
[DEBUG] Toutes les variables d'environnement disponibles:
[DEBUG]   - PATH: /usr/local/bin...
[DEBUG]   - PORT: 10000
[DEBUG]   - DISCORD_BOT_TOKEN: [MASQUÉ - 59 caractères]
[DEBUG]   - ... (plus de variables)
[DEBUG] ========================================
[DEBUG] Tentatives de récupération du token:
[DEBUG] 1. os.getenv('DISCORD_BOT_TOKEN'): ✓ TROUVÉ
[DEBUG] ========================================
[OK] Token Discord trouvé (59 caractères)
[OK] Demarrage bot avec boutons persistants...
```

---

## 🆘 Problèmes Courants

### **"Je ne vois que les anciens logs"**

→ Render n'a pas encore redéployé
→ Solution : Manual Deploy → Deploy latest commit

### **"Les logs ne défilent pas"**

→ Cliquez sur le bouton **"Follow"** ou **"Auto-scroll"** en haut des logs
→ Ou scrollez manuellement jusqu'en bas

### **"Je vois 'Deploy failed'"**

→ Il y a une erreur de build
→ Regardez les logs de build pour voir l'erreur
→ Copiez-moi l'erreur complète

### **"Je ne trouve pas l'onglet Logs"**

→ Assurez-vous d'être sur la page de VOTRE service
→ Le menu devrait être : Overview | Events | **Logs** | Shell | Metrics | Settings

---

## 🎯 Checklist

- [ ] Connecté à Render.com
- [ ] Sur la page de mon service Discord Bot
- [ ] Onglet **"Logs"** sélectionné
- [ ] Service en état **"Live"** (vert)
- [ ] Scrollé jusqu'en bas des logs
- [ ] Cherché `[DEBUG] ========`

Si tout est ✅ et que vous voyez les nouveaux logs → Copiez-moi tout le bloc

Si vous voyez toujours les anciens logs → Faites **Manual Deploy**

---

## 📞 Alternative : Logs via API

Si vraiment l'interface ne marche pas, vous pouvez aussi :

1. Aller dans **Events**
2. Cliquer sur le dernier événement "Deploy live"
3. Cela ouvrira les logs de ce déploiement spécifique

---

**Une fois que vous voyez les logs avec [DEBUG], copiez-moi TOUT le bloc ! 📋**
