# ?? Configuration Web Service pour Render

## ? Bot converti en Web Service

Le bot a ?t? modifi? pour fonctionner en **Web Service** avec un serveur HTTP.

### Ce qui a ?t? ajout?:

1. **Serveur HTTP** (port 10000 par d?faut)
2. **Endpoint de sant?**: `/health`
3. **Page d'accueil**: `/`
4. **Bot Discord** tourne en parall?le

---

## ?? D?ploiement

### Sur Render:

1. **Type de service**: Web Service ?
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `python3 bot.py`

### Variables d'environnement:

```
DISCORD_TOKEN = [Votre token Discord]
GROQ_API_KEY = [Votre cl? Groq]
AI_MODEL = llama-3.1-70b-versatile (optionnel)
```

---

## ?? Endpoints disponibles

### `/` - Page d'accueil
```
https://votre-service.onrender.com/
```
Affiche une page HTML avec le statut du bot.

### `/health` - Health check
```
https://votre-service.onrender.com/health
```
Retourne un JSON avec les infos du bot:
```json
{
  "status": "online",
  "bot": "NomDuBot#1234",
  "guilds": 2,
  "active_channels": 3,
  "personalities": 8,
  "model": "llama-3.1-70b-versatile"
}
```

---

## ?? Configuration

### Port

Le bot utilise automatiquement:
- **Port 10000** (d?faut)
- Ou le port d?fini par la variable `PORT` (Render d?finit cela automatiquement)

### Render d?tecte automatiquement le port

Render scanne et d?tecte que le port 10000 est ouvert ? Plus d'erreur "No open ports"!

---

## ? Avantages du Web Service

1. **URL publique** pour v?rifier le statut
2. **Health check** pour monitoring
3. **Compatible** avec les Web Services Render
4. **Bot Discord** fonctionne en parall?le

---

## ?? Logs attendus

```
==> Building...
==> Installing dependencies...
Successfully installed discord.py aiohttp python-dotenv

==> Starting service with command: python3 bot.py
?? D?marrage du bot Discord IA avec Groq...
?? Mod?le: llama-3.1-70b-versatile
?? Personnalit?s: 8
? Commandes Slash activ?es!
?? Serveur web d?marr? sur le port 10000
?? Health check disponible sur /health
?? [BotName] est connect? et pr?t!
?? Connect? ? X serveur(s)
? 6 commandes slash synchronis?es!

==> Port 10000 detected ?
==> Service is live!
```

---

## ?? V?rifications

### 1. Bot Discord

Sur Discord:
- ? Bot en ligne (pastille verte)
- ? `/start` fonctionne
- ? Bot r?pond aux mentions

### 2. Web Service

Dans le navigateur:
- ? `https://votre-service.onrender.com/` affiche la page
- ? `https://votre-service.onrender.com/health` retourne le JSON

---

## ?? Apr?s le d?ploiement

1. Render d?tecte automatiquement le port
2. Assigne une URL publique
3. Le bot Discord fonctionne normalement
4. Vous pouvez v?rifier le statut via l'URL

---

## ?? Utilisation

Le bot fonctionne exactement comme avant:

```
/start          ? Active le bot (admin)
/personality    ? Change la personnalit?
/help           ? Affiche l'aide
```

**Bonus**: Vous avez maintenant une URL pour v?rifier que tout fonctionne!

---

## ?? Note

Le plan **Free** met le service en veille apr?s 15 min d'inactivit?.

Pour garder le bot actif 24/7:
- **Upgrade ? Starter** (7$/mois)
- **Ou utilisez Oracle Cloud** (gratuit) - Voir HEBERGEMENT_24_7.md

---

? **Le bot est maintenant compatible avec les Web Services Render!**
