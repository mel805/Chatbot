# ? D?ploiement Render - Guide Ultra-Rapide

## ?? D?ploiement en 5 minutes

### 1?? Pr?requis (2 min)

**Obtenez vos tokens:**
- ?? Token Discord: https://discord.com/developers/applications
- ?? Cl? Groq (gratuit): https://console.groq.com

**Assurez-vous que:**
- ? Votre code est sur GitHub
- ? Le fichier `.env` n'est PAS committ?

### 2?? D?ployer sur Render (3 min)

1. **Allez sur https://render.com**
   - Sign up avec GitHub

2. **New + ? Blueprint**
   - Connectez votre d?p?t GitHub
   - S?lectionnez le repo du bot

3. **Render d?tecte automatiquement `render.yaml`**
   - V?rifiez les param?tres

4. **Configurez les variables d'environnement:**
   
   ```
   DISCORD_TOKEN = votre_token_discord
   GROQ_API_KEY = votre_cle_groq_ici
   ```

5. **Cliquez sur "Apply"**
   - Render d?ploie automatiquement!

### 3?? V?rifier (30 sec)

- Voir les logs dans Render Dashboard
- Le bot appara?t en ligne sur Discord
- Taper `/start` sur Discord (admin)

## ? C'est fait!

---

## ?? Limitations Plan Gratuit

- ?? **750h/mois** (environ 31 jours)
- ?? **Se met en veille apr?s 15 min d'inactivit?**
- ?? **Red?marrage mensuel**

**? Pour un bot 24/7 fiable: Upgrade ? 7$/mois ou utilisez Oracle Cloud (gratuit, VPS)**

---

## ?? Commandes Git Rapides

Si votre code n'est pas encore sur GitHub:

```bash
# Initialiser
git init
git add .
git commit -m "Discord bot initial commit"

# Cr?er un repo sur github.com puis:
git remote add origin https://github.com/votre-username/votre-repo.git
git branch -M main
git push -u origin main
```

---

## ?? Apr?s le d?ploiement

### Voir les logs
Dashboard ? Votre service ? Logs

### Red?ployer
Dashboard ? Manual Deploy

### Changer les variables
Dashboard ? Environment ? Edit

---

## ? Probl?mes courants

**Le bot ne d?marre pas?**
? V?rifiez les logs pour voir l'erreur

**"DISCORD_TOKEN non trouv?"?**
? Ajoutez-le dans Environment variables

**Bot se d?connecte?**
? Plan gratuit = veille apr?s 15 min. Upgrade ? 7$/mois ou utilisez Oracle Cloud

**Bot lent?**
? Normal avec plan gratuit partag?

---

## ?? Alternative Gratuite 24/7

**Oracle Cloud (Recommand?)**
- Gratuit ? vie
- VPS complet
- Pas de veille
- Pas de limitations

? Voir **HEBERGEMENT_24_7.md** pour le guide complet

---

## ?? Documentation Compl?te

Pour plus de d?tails:
- **DEPLOIEMENT_RENDER.md** - Guide complet Render
- **HEBERGEMENT_24_7.md** - Autres options (VPS, Raspberry Pi)
- **README.md** - Documentation du bot

---

## ?? Structure des fichiers pour Render

Fichiers n?cessaires (? d?j? inclus):

```
??? bot.py                    ? Code du bot
??? requirements.txt          ? D?pendances
??? render.yaml              ? Config Render
??? runtime.txt              ? Version Python
??? .gitignore               ? Ne pas commit .env
```

**IMPORTANT**: Le `.env` ne doit PAS ?tre sur GitHub!

---

## ?? Profitez de votre bot!

Une fois d?ploy?, sur Discord:

```
/start        ? Active le bot (admin)
/personality  ? Change la personnalit?  
/help         ? Voir l'aide
```

**8 personnalit?s disponibles:**
?? Amical | ?? S?ducteur | ?? Coquin | ?? Romantique | ?? Dominant | ?? Soumis | ?? Joueur | ?? Intellectuel

---

Besoin d'aide? ? **DEPLOIEMENT_RENDER.md** (guide complet)
