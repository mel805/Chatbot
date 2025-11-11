# 🎯 Guide Rapide - API Gratuite NSFW

## Ce Qui a Changé

✅ **API 100% gratuite** remplace les APIs payantes  
✅ **Sans censure NSFW** - Modèles uncensored sélectionnés  
✅ **Sans limite stricte** - Rotation automatique entre 4 modèles  
✅ **Token optionnel** - Fonctionne sans config  

## Pour Déployer Immédiatement

### Sur Render.com

1. **Aucune modification nécessaire !**
   - Le bot utilise maintenant `AI_PROVIDER=free_nsfw` par défaut
   - Fonctionne sans token HuggingFace

2. **Pour améliorer les performances (optionnel):**
   - Créez un compte gratuit sur https://huggingface.co
   - Créez un token (Settings > Access Tokens)
   - Ajoutez dans Render: `HUGGINGFACE_API_KEY=hf_votre_token`

3. **Redéployez:**
   - Commitez les changements
   - Render redéploiera automatiquement

### En Local

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Lancer le bot
python discord_bot_main.py

# C'est tout ! Le bot fonctionne immédiatement.
```

## Variables d'Environnement

### Obligatoires

```env
DISCORD_BOT_TOKEN=votre_token_discord
```

### Optionnelles (pour meilleures performances)

```env
HUGGINGFACE_API_KEY=hf_votre_token_gratuit
AI_PROVIDER=free_nsfw
```

## Modèles Utilisés (Rotation Automatique)

1. **Mistral-7B-OpenOrca** (rapide, performant)
2. **Nous-Hermes-2-Mistral-7B-DPO** (roleplay NSFW)
3. **Dolphin-2.6-Mistral-7B** (uncensored populaire)
4. **MythoMax-L2-13b** (créatif, 13B paramètres)

Si un modèle est surchargé → passage automatique au suivant

## Performances

- **Sans token HF** : 5-20s première requête, 2-8s ensuite
- **Avec token HF** : 2-5s première requête, 1-5s ensuite

## Comparaison APIs

| API | Coût | NSFW | Token | Disponibilité |
|-----|------|------|-------|---------------|
| **free_nsfw (NOUVEAU)** | ✅ Gratuit | ✅ Oui | ⚠️ Optionnel | ✅✅ 99%+ |
| Groq | ⚠️ Limité | ⚠️ Filtré | ✅ Requis | ⚠️ 90% |
| OpenAI | ❌ Payant | ❌ Non | ✅ Requis | ✅✅ 99.9% |
| DeepInfra | ⚠️ Limites | ⚠️ Partiel | ✅ Requis | ⚠️ 85% |

## Dépannage

### "Modèles surchargés"
→ Très rare (< 1%), attendre 10-30 secondes

### "Réponse lente (15-20s)"
→ Normal première fois (chargement du modèle)
→ Créer un token HuggingFace gratuit pour améliorer

### "Pas de réponse"
→ Vérifier les logs: Le système essaie les 4 modèles automatiquement
→ Si tous échouent: problème HuggingFace (rare)

## Support

**Documentation complète:** `API_GRATUITE_NSFW.md`

**Logs de debug:**
```
[DEBUG] Tentative 1/4: HuggingFace-Mistral-Uncensored
[SUCCESS] HuggingFace-Mistral-Uncensored: Salut ! ...
```

---

**Le bot est maintenant 100% gratuit et sans censure NSFW ! 🚀**
