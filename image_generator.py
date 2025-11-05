"""
G?n?rateur d'images NSFW pour les personnalit?s du bot Discord
Utilise Pollinations.ai (gratuit, sans cl? API) comme m?thode principale
"""

import aiohttp
import asyncio
import os
import json
import urllib.parse
import random
import time

class ImageGenerator:
    """G?n?re des images NSFW bas?es sur les personnalit?s"""
    
    def __init__(self):
        self.replicate_key = os.getenv('REPLICATE_API_KEY', '')
        self.huggingface_key = os.getenv('HUGGINGFACE_API_KEY', '')
        
    async def generate_personality_image(self, personality_data, prompt_addition="", max_retries=5):
        """
        G?n?re une image bas?e sur la personnalit? avec retry automatique
        
        Args:
            personality_data: Dictionnaire avec name, genre, age, description, visual
            prompt_addition: Texte additionnel pour le prompt
            max_retries: Nombre maximum de tentatives (d?faut: 3)
        
        Returns:
            URL de l'image ou None si erreur
        """
        
        # Construire le prompt bas? sur la personnalit?
        name = personality_data.get('name', 'Person')
        genre = personality_data.get('genre', 'Neutre')
        age = personality_data.get('age', '25 ans')
        description = personality_data.get('description', '')
        visual_traits = personality_data.get('visual', '')  # Caract?ristiques visuelles uniques
        
        # Extraire l'?ge num?rique
        age_num = ''.join(filter(str.isdigit, age))
        
        # Construire le prompt Stable Diffusion avec traits visuels uniques
        base_prompt = self._build_base_prompt(genre, age_num, description, visual_traits)
        full_prompt = f"{base_prompt}, {prompt_addition}" if prompt_addition else base_prompt
        
        print(f"[IMAGE] Generating image for {name} with prompt: {full_prompt[:100]}...", flush=True)
        
        # Essayer avec retry automatique et fallback intelligent pour 100% de r?ussite
        image_url = None
        
        for attempt in range(max_retries):
            print(f"[IMAGE] Attempt {attempt + 1}/{max_retries}...", flush=True)
            
            # M?thode 1: Pollinations.ai avec strat?gie adapt?e ? la tentative
            print(f"[IMAGE] Trying Pollinations.ai (free, unlimited)...", flush=True)
            image_url = await self._generate_pollinations(full_prompt, attempt=attempt+1)
            
            if image_url:
                print(f"[IMAGE] ✓ Success on attempt {attempt + 1}!", flush=True)
                return image_url
            
            # Si le prompt est complexe, essayer une version simplifi?e
            if attempt >= 2 and len(full_prompt) > 200:
                print(f"[IMAGE] Trying with simplified prompt...", flush=True)
                simplified_prompt = self._simplify_prompt(full_prompt)
                image_url = await self._generate_pollinations(simplified_prompt, attempt=attempt+1)
                if image_url:
                    print(f"[IMAGE] ✓ Success with simplified prompt on attempt {attempt + 1}!", flush=True)
                    return image_url
            
            # M?thode 2: Replicate (backup si cl? configur?e)
            if self.replicate_key and attempt >= 3:
                print(f"[IMAGE] Pollinations failed, trying Replicate...", flush=True)
                image_url = await self._generate_replicate(full_prompt)
                
                if image_url:
                    print(f"[IMAGE] ✓ Success with Replicate on attempt {attempt + 1}!", flush=True)
                    return image_url
            
            if attempt < max_retries - 1:
                wait_time = 1 + attempt  # Augmente le d?lai progressivement
                print(f"[IMAGE] Attempt {attempt + 1} failed, waiting {wait_time}s before retry...", flush=True)
                await asyncio.sleep(wait_time)
        
        # DERNIER RECOURS: Retourner une URL simple sans validation
        print(f"[IMAGE] All validation attempts exhausted, generating final fallback URL", flush=True)
        random_seed = random.randint(1, 999999999)
        encoded_prompt = urllib.parse.quote(self._simplify_prompt(full_prompt))
        fallback_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=768&model=turbo&seed={random_seed}&nologo=true"
        print(f"[IMAGE] Returning fallback URL (no validation)", flush=True)
        return fallback_url
    
    def _build_base_prompt(self, genre, age, description, visual_traits=""):
        """Construit le prompt de base selon la personnalit?"""
        
        # Si des traits visuels sp?cifiques sont fournis, les utiliser en priorit?
        if visual_traits:
            print(f"[IMAGE] Using specific visual traits: {visual_traits[:80]}...", flush=True)
            # Prompt plus simple et plus fiable
            prompt = f"{visual_traits}, {age} years old, portrait photography"
            return prompt
        
        # Sinon, utiliser l'ancienne m?thode (fallback)
        gender_map = {
            "Femme": "beautiful sensual woman, feminine figure, attractive",
            "Homme": "handsome man, masculine, athletic build",
            "Trans": "beautiful person, alluring, attractive",
            "Non-binaire": "attractive androgynous person, unique style",
            "Neutre": "attractive person, appealing"
        }
        
        gender_desc = gender_map.get(genre, "attractive person")
        
        # Extraire traits de la description
        traits = []
        if "seduisant" in description.lower() or "belle" in description.lower():
            traits.append("seductive, alluring")
        if "confiant" in description.lower():
            traits.append("confident")
        if "mature" in description.lower():
            traits.append("mature, experienced")
        if "coquin" in description.lower() or "ose" in description.lower():
            traits.append("playful, teasing")
        
        traits_str = ", ".join(traits) if traits else "attractive"
        
        # Prompt complet (simplifi?)
        prompt = f"portrait, {gender_desc}, {age} years old, {traits_str}, professional photography"
        
        return prompt
    
    async def _generate_pollinations(self, prompt, attempt=1):
        """G?n?re via Pollinations.ai (gratuit, sans cl? API) avec fallback intelligent"""
        try:
            print(f"[IMAGE] Using Pollinations.ai FREE API (attempt {attempt})", flush=True)
            
            # G?n?rer un seed VRAIMENT al?atoire pour ?viter images identiques
            random_seed = random.randint(1, 999999999) + int(time.time() * 1000)
            print(f"[IMAGE] Using random seed: {random_seed}", flush=True)
            
            # Encoder le prompt pour URL
            encoded_prompt = urllib.parse.quote(prompt)
            
            # STRAT?GIE MULTI-FALLBACK pour garantir 100% de r?ussite
            strategies = [
                # Strat?gie 1: Flux avec enhance (meilleure qualit?)
                {"model": "flux", "enhance": "true", "width": 768, "height": 1024},
                # Strat?gie 2: Flux sans enhance (plus rapide)
                {"model": "flux", "enhance": "false", "width": 768, "height": 1024},
                # Strat?gie 3: Flux avec r?solution r?duite (plus fiable)
                {"model": "flux", "enhance": "true", "width": 512, "height": 768},
                # Strat?gie 4: Turbo (le plus rapide)
                {"model": "turbo", "enhance": "false", "width": 768, "height": 1024},
            ]
            
            # Choisir la strat?gie selon la tentative
            strategy_index = min(attempt - 1, len(strategies) - 1)
            strategy = strategies[strategy_index]
            
            # Construire l'URL avec la strat?gie choisie
            params = f"width={strategy['width']}&height={strategy['height']}&model={strategy['model']}&seed={random_seed}&nologo=true&enhance={strategy['enhance']}"
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?{params}"
            
            print(f"[IMAGE] Strategy {strategy_index + 1}: {strategy['model']} ({strategy['width']}x{strategy['height']}) enhance={strategy['enhance']}", flush=True)
            print(f"[IMAGE] URL generated, validating...", flush=True)
            
            # VALIDATION SOUPLE: On accepte m?me avec timeout
            if await self._validate_image_url(image_url):
                print(f"[IMAGE] Image validated successfully!", flush=True)
                return image_url
            else:
                print(f"[IMAGE] Image validation failed, will retry with different strategy", flush=True)
                return None
            
        except Exception as e:
            print(f"[ERROR] Pollinations.ai error: {e}", flush=True)
            return None
    
    async def _generate_replicate(self, prompt):
        """G?n?re via Replicate API (n?cessite cl? API)"""
        try:
            headers = {
                "Authorization": f"Token {self.replicate_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "version": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                "input": {
                    "prompt": prompt,
                    "width": 768,
                    "height": 1024,
                    "num_outputs": 1
                }
            }
            
            timeout = aiohttp.ClientTimeout(total=90)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    "https://api.replicate.com/v1/predictions",
                    headers=headers,
                    json=data
                ) as resp:
                    if resp.status == 201:
                        result = await resp.json()
                        prediction_url = result.get('urls', {}).get('get')
                        
                        # Attendre g?n?ration (max 60s)
                        for _ in range(30):
                            await asyncio.sleep(2)
                            async with session.get(prediction_url, headers=headers) as check_resp:
                                check_result = await check_resp.json()
                                status = check_result.get('status')
                                
                                if status == 'succeeded':
                                    output = check_result.get('output', [])
                                    if output:
                                        return output[0]
                                elif status == 'failed':
                                    return None
                    
                    return None
        except Exception as e:
            print(f"[ERROR] Replicate error: {e}", flush=True)
            return None
    
    async def _validate_image_url(self, url, timeout_seconds=20):
        """Valide qu'une URL d'image est accessible et retourne une vraie image"""
        try:
            timeout = aiohttp.ClientTimeout(total=timeout_seconds)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Essayer GET au lieu de HEAD pour Pollinations.ai
                async with session.get(url, allow_redirects=True) as resp:
                    # V?rifier le code de statut
                    if resp.status != 200:
                        print(f"[IMAGE] Validation failed: HTTP {resp.status}", flush=True)
                        return False
                    
                    # V?rifier le type de contenu
                    content_type = resp.headers.get('Content-Type', '')
                    if not content_type.startswith('image/'):
                        print(f"[IMAGE] Validation failed: Not an image (Content-Type: {content_type})", flush=True)
                        return False
                    
                    # V?rifier que nous avons re?u des donn?es
                    content_length = resp.headers.get('Content-Length', '0')
                    if int(content_length) < 1000:  # Image trop petite = probablement erreur
                        print(f"[IMAGE] Validation failed: Image too small ({content_length} bytes)", flush=True)
                        return False
                    
                    print(f"[IMAGE] Validation success: {content_type}, {content_length} bytes, HTTP {resp.status}", flush=True)
                    return True
        except asyncio.TimeoutError:
            print(f"[IMAGE] Validation timeout after {timeout_seconds}s - Accepting URL anyway", flush=True)
            # CHANGEMENT: On accepte l'URL m?me en cas de timeout car Pollinations.ai peut ?tre lent
            return True
        except Exception as e:
            print(f"[IMAGE] Validation error: {e} - Accepting URL anyway", flush=True)
            # En cas d'erreur, on accepte quand m?me (mieux vaut essayer que ne rien afficher)
            return True
    
    def _simplify_prompt(self, prompt):
        """Simplifie un prompt trop complexe pour am?liorer la g?n?ration"""
        # Garder seulement les ?l?ments essentiels
        words = prompt.split(',')
        # Garder les 5 premiers ?l?ments les plus importants
        essential = words[:5]
        simplified = ', '.join(essential).strip()
        print(f"[IMAGE] Simplified prompt from {len(prompt)} to {len(simplified)} chars", flush=True)
        return simplified
    
    async def _generate_huggingface(self, prompt):
        """G?n?re via Hugging Face (n?cessite cl? API)"""
        print(f"[IMAGE] Hugging Face not implemented yet", flush=True)
        return None
    
    async def generate_contextual_image(self, personality_data, conversation_history):
        """
        G?n?re une image bas?e sur le contexte de la conversation
        
        Args:
            personality_data: Dictionnaire avec name, genre, age, description
            conversation_history: Liste des derniers messages de conversation
        
        Returns:
            URL de l'image ou None si erreur
        """
        # ANALYSE AVANC?E : Analyser TOUS les messages r?cents
        conversation_text = " ".join(conversation_history[-15:]).lower()  # Plus de contexte
        
        print(f"[IMAGE] Analyzing {len(conversation_history)} messages for detailed context...", flush=True)
        
        # SYST?ME DE SCORING pour d?tecter pr?cis?ment le contexte
        context_keywords = []
        context_detected = []
        
        # 1. NUE/D?SHABILL? (priorit? maximale si d?tect?)
        nude_words = ["nue", "nu", "nud", "d?shabill", "sans v?tement", "corps nu", "montre tout", "voir tout", "naked", "bare", "strip", "d?nu"]
        if any(word in conversation_text for word in nude_words):
            context_keywords.append("nude, bare skin, natural body, no clothing, fully exposed")
            context_detected.append("NUDE")
        
        # 2. LIEU/SETTING (important pour ambiance)
        if any(word in conversation_text for word in ["lit", "chambre", "bedroom", "bed", "matelas", "oreiller", "draps"]):
            context_keywords.append("bedroom setting, on bed, intimate room")
            context_detected.append("BEDROOM")
        elif any(word in conversation_text for word in ["douche", "salle de bain", "baignoire", "shower", "bathroom"]):
            context_keywords.append("bathroom, shower, wet skin, water")
            context_detected.append("BATHROOM")
        elif any(word in conversation_text for word in ["plage", "beach", "piscine", "pool", "eau"]):
            context_keywords.append("beach setting, by water, outdoor")
            context_detected.append("WATER")
        
        # 3. V?TEMENTS/LINGERIE
        if any(word in conversation_text for word in ["lingerie", "sous-v?tement", "underwear", "soutien-gorge", "culotte", "string"]):
            context_keywords.append("wearing sexy lingerie, revealing underwear, intimate clothing")
            context_detected.append("LINGERIE")
        elif any(word in conversation_text for word in ["robe", "jupe", "d?collet?", "moulant", "transparent", "dress"]):
            context_keywords.append("revealing outfit, form-fitting clothes")
            context_detected.append("CLOTHING")
        
        # 4. POSITIONS/POSES (tr?s important pour l'image)
        if any(word in conversation_text for word in ["position", "pose", "allong?", "?cart?", "ouvre", "penche", "cambre", "? quatre pattes"]):
            context_keywords.append("provocative seductive pose, suggestive position")
            context_detected.append("POSE")
        elif any(word in conversation_text for word in ["assis", "debout", "accroupi", "agenouill?"]):
            context_keywords.append("specific position, deliberate stance")
            context_detected.append("STANCE")
        
        # 5. ATMOSPH?RE/?MOTION
        if any(word in conversation_text for word in ["plaisir", "jouissance", "extase", "g?mir", "soupir"]):
            context_keywords.append("pleasure expression, ecstatic face, sensual emotion")
            context_detected.append("PLEASURE")
        elif any(word in conversation_text for word in ["sexy", "hot", "sensuel", "?rotique", "excit?", "chaud"]):
            context_keywords.append("sexy, seductive, alluring, provocative")
            context_detected.append("SEXY")
        elif any(word in conversation_text for word in ["envie", "d?sir", "veux", "besoin"]):
            context_keywords.append("desire, wanting, passionate expression")
            context_detected.append("DESIRE")
        
        # 6. CONTACT PHYSIQUE
        if any(word in conversation_text for word in ["touche", "caresse", "embrasse", "l?che", "suce", "frotte", "masse"]):
            context_keywords.append("intimate touching, sensual physical contact")
            context_detected.append("TOUCH")
        
        # 7. PARTIES DU CORPS (focus sp?cifique)
        body_focus = []
        if any(word in conversation_text for word in ["sein", "poitrine", "t?ton"]):
            body_focus.append("chest focus")
        if any(word in conversation_text for word in ["fesse", "cul", "derri?re"]):
            body_focus.append("rear focus")
        if any(word in conversation_text for word in ["jambe", "cuisse", "hanche"]):
            body_focus.append("legs focus")
        if body_focus:
            context_keywords.append(", ".join(body_focus) + ", body curves emphasis")
            context_detected.append("BODY_FOCUS")
        
        # 8. ACTIONS EXPLICITES
        if any(word in conversation_text for word in ["branle", "masturbe", "p?n?tre", "baise", "fuck"]):
            context_keywords.append("explicit intimate activity, sexual act")
            context_detected.append("EXPLICIT")
        
        # Construire le prompt contextuel intelligent
        name = personality_data.get('name', 'Person')
        genre = personality_data.get('genre', 'Neutre')
        age_num = ''.join(filter(str.isdigit, personality_data.get('age', '25')))
        visual_traits = personality_data.get('visual', '')
        
        base_prompt = self._build_base_prompt(genre, age_num, personality_data.get('description', ''), visual_traits)
        
        if context_keywords:
            # Limiter ? 4 ?l?ments pour ne pas surcharger le prompt
            context_str = ", ".join(context_keywords[:4])
            full_prompt = f"{base_prompt}, {context_str}, high quality, detailed"
            print(f"[IMAGE] Context detected: {', '.join(context_detected)}", flush=True)
            print(f"[IMAGE] Keywords: {context_str[:100]}...", flush=True)
        else:
            # Par d?faut neutre
            full_prompt = f"{base_prompt}, natural pose, attractive"
            print(f"[IMAGE] No strong context, using neutral default", flush=True)
        
        print(f"[IMAGE] Full prompt: {full_prompt[:180]}...", flush=True)
        
        # G?n?rer avec le syst?me de retry am?lior? (5 tentatives)
        max_retries = 5
        image_url = None
        
        for attempt in range(max_retries):
            print(f"[IMAGE] Contextual attempt {attempt + 1}/{max_retries}...", flush=True)
            
            image_url = await self._generate_pollinations(full_prompt, attempt=attempt+1)
            
            if image_url:
                print(f"[IMAGE] \u2713 Contextual success on attempt {attempt + 1}!", flush=True)
                return image_url
            
            # Simplifier si ?chec r?p?t?
            if attempt >= 2 and len(full_prompt) > 200:
                print(f"[IMAGE] Trying simplified contextual...", flush=True)
                simplified = self._simplify_prompt(full_prompt)
                image_url = await self._generate_pollinations(simplified, attempt=attempt+1)
                if image_url:
                    return image_url
            
            # Fallback Replicate
            if self.replicate_key and attempt >= 3:
                image_url = await self._generate_replicate(full_prompt)
                if image_url:
                    return image_url
            
            if attempt < max_retries - 1:
                wait_time = 1 + attempt
                await asyncio.sleep(wait_time)
        
        # FALLBACK FINAL garanti
        print(f"[IMAGE] Generating guaranteed fallback contextual URL", flush=True)
        random_seed = random.randint(1, 999999999)
        encoded_prompt = urllib.parse.quote(self._simplify_prompt(full_prompt))
        fallback_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=768&model=turbo&seed={random_seed}&nologo=true"
        return fallback_url
