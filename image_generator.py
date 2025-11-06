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
        
    async def generate_personality_image(self, personality_data, prompt_addition="", max_retries=3):
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
        
        # Essayer avec retry automatique pour 100% de r?ussite
        image_url = None
        
        for attempt in range(max_retries):
            print(f"[IMAGE] Attempt {attempt + 1}/{max_retries}...", flush=True)
            
            # M?thode 1: Pollinations.ai (GRATUIT, sans cl? API, PRIORITAIRE)
            print(f"[IMAGE] Trying Pollinations.ai (free, unlimited)...", flush=True)
            image_url = await self._generate_pollinations(full_prompt)
            
            if image_url:
                print(f"[IMAGE] Success on attempt {attempt + 1}!", flush=True)
                return image_url
            
            # M?thode 2: Replicate (backup si cl? configur?e)
            if self.replicate_key:
                print(f"[IMAGE] Pollinations failed, trying Replicate...", flush=True)
                image_url = await self._generate_replicate(full_prompt)
                
                if image_url:
                    print(f"[IMAGE] Success with Replicate on attempt {attempt + 1}!", flush=True)
                    return image_url
            
            # M?thode 3: Hugging Face (backup si cl? configur?e)
            if self.huggingface_key:
                print(f"[IMAGE] Replicate failed, trying Hugging Face...", flush=True)
                image_url = await self._generate_huggingface(full_prompt)
                
                if image_url:
                    print(f"[IMAGE] Success with Hugging Face on attempt {attempt + 1}!", flush=True)
                    return image_url
            
            if attempt < max_retries - 1:
                print(f"[IMAGE] Attempt {attempt + 1} failed, retrying...", flush=True)
                await asyncio.sleep(2)  # Petite pause avant retry
        
        print(f"[IMAGE] All {max_retries} attempts failed", flush=True)
        return image_url
    
    def _build_base_prompt(self, genre, age, description, visual_traits=""):
        """Construit le prompt de base selon la personnalit?"""
        
        # IMPORTANT: Toujours ajouter des indicateurs de REALISME FORT
        # pour ?viter le style anim?/cartoon
        realism_keywords = "photorealistic, realistic photo, real person, high quality photograph, professional photoshoot, natural lighting, realistic skin texture, detailed face"
        
        # Si des traits visuels sp?cifiques sont fournis, les utiliser en priorit?
        if visual_traits:
            print(f"[IMAGE] Using specific visual traits: {visual_traits[:80]}...", flush=True)
            # Prompt avec REALISME RENFORCE
            prompt = f"{visual_traits}, {age} years old, {realism_keywords}"
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
        
        # Prompt complet avec REALISME RENFORCE
        prompt = f"{gender_desc}, {age} years old, {traits_str}, {realism_keywords}"
        
        return prompt
    
    async def _generate_pollinations(self, prompt):
        """G?n?re via Pollinations.ai (gratuit, sans cl? API)"""
        try:
            print(f"[IMAGE] Using Pollinations.ai FREE API", flush=True)
            
            # G?n?rer un seed VRAIMENT al?atoire pour ?viter images identiques
            random_seed = random.randint(1, 999999999) + int(time.time() * 1000)
            print(f"[IMAGE] Using random seed: {random_seed}", flush=True)
            
            # AJOUTER NEGATIVE PROMPT pour ?viter le style anim?/cartoon
            negative_keywords = "NOT anime, NOT cartoon, NOT illustration, NOT drawing, NOT 3D render, NOT CGI"
            full_prompt_with_negative = f"{prompt}. {negative_keywords}"
            
            # Encoder le prompt pour URL
            encoded_prompt = urllib.parse.quote(full_prompt_with_negative)
            
            # Construire l'URL Pollinations (Flux model, haute qualit?, seed al?atoire)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=1024&model=flux&seed={random_seed}&nologo=true&enhance=true"
            
            print(f"[IMAGE] Pollinations.ai URL generated successfully", flush=True)
            print(f"[IMAGE] Style enforcement: Photorealistic with anti-anime keywords", flush=True)
            return image_url
            
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
        # Analyser les derniers messages pour extraire le contexte
        context_keywords = []
        conversation_text = " ".join(conversation_history[-10:]).lower()
        
        # PRIORITE 1: D?tecter les v?tements sp?cifiques mentionn?s
        # Cela permet de capturer "robe l?g?re", "chemise", "jupe", etc.
        clothing_detected = False
        clothing_items = []
        
        # D?tection de v?tements sp?cifiques
        clothing_keywords = {
            "robe": ["robe l?g?re", "light dress", "robe", "dress"],
            "chemise": ["chemise", "shirt", "blouse"],
            "jupe": ["jupe", "skirt"],
            "pantalon": ["pantalon", "pants", "jeans"],
            "short": ["short", "shorts"],
            "haut": ["haut", "top", "d?bardeur", "tank top"],
            "lingerie": ["lingerie", "sous-v?tements", "underwear", "soutien-gorge", "bra", "culotte", "panties"],
            "maillot": ["maillot de bain", "bikini", "swimsuit"],
            "nuisette": ["nuisette", "d?shabill?", "nightgown", "negligee"],
            "bas_vetement": ["bas r?sille", "bas nylon", "collants", "stockings", "tights"],  # Renomm? pour ?viter conflit avec "baiser"
            "chaussures": ["talons", "heels", "chaussures", "shoes"],
            "accessoires": ["chapeau", "foulard", "bijoux", "jewelry", "collier", "necklace"]
        }
        
        for category, keywords in clothing_keywords.items():
            for keyword in keywords:
                if keyword in conversation_text:
                    clothing_detected = True
                    # Extraire le contexte autour du mot pour capturer les adjectifs
                    idx = conversation_text.find(keyword)
                    if idx != -1:
                        # Prendre 30 caract?res avant et apr?s pour contexte
                        start = max(0, idx - 30)
                        end = min(len(conversation_text), idx + len(keyword) + 30)
                        context_phrase = conversation_text[start:end]
                        
                        # Nettoyer et ajouter
                        context_phrase = context_phrase.strip()
                        if context_phrase and context_phrase not in clothing_items:
                            clothing_items.append(context_phrase)
                            print(f"[IMAGE] Clothing detected: {context_phrase}", flush=True)
                    break
        
        # Si des v?tements sont d?tect?s, les PRIORISER
        if clothing_detected and clothing_items:
            # Joindre les descriptions de v?tements
            clothing_desc = ", ".join(clothing_items[:3])  # Limiter ? 3 pour ne pas surcharger
            context_keywords.append(f"wearing {clothing_desc}")
            print(f"[IMAGE] PRIORITY: Clothing context added: {clothing_desc}", flush=True)
        else:
            # SEULEMENT si AUCUN v?tement n'est mentionn?, v?rifier la nudit?
            # ET s'assurer qu'il n'y a pas de n?gation (ex: "je ne suis pas nue")
            nude_keywords = ["nue", "nu", "nud", "d?shabill", "sans v?tements", "naked", "bare"]
            negation_keywords = ["pas", "plus", "jamais", "not", "no longer"]
            
            # V?rifier si c'est vraiment une nudit? (pas une n?gation)
            is_nude = False
            for nude_word in nude_keywords:
                if nude_word in conversation_text:
                    # V?rifier qu'il n'y a pas de n?gation juste avant
                    idx = conversation_text.find(nude_word)
                    if idx > 10:
                        before_text = conversation_text[max(0, idx-15):idx]
                        if not any(neg in before_text for neg in negation_keywords):
                            is_nude = True
                            break
                    else:
                        is_nude = True
                        break
            
            if is_nude:
                context_keywords.append("nude bare skin, revealing body, natural figure")
                print(f"[IMAGE] Nudity context detected (no clothing mentioned)", flush=True)
        
        # PRIORITE 2: D?tecter les ACTIONS INTIMES SPECIFIQUES (avant les g?n?riques)
        # Ces d?tections ont la priorit? car elles sont plus pr?cises visuellement
        
        action_detected = False
        
        # D?tection d'actions ORALES (bouche, l?cher, sucer, etc.)
        oral_keywords = ["bouche", "l?che", "l?cher", "suce", "sucer", "avale", "avaler", 
                        "langue", "l?vres sur", "embrasse le", "goute", "go?ter",
                        "mouth", "lick", "licking", "suck", "sucking", "oral", "tongue", "taste"]
        
        if any(keyword in conversation_text for keyword in oral_keywords):
            # V?rifier si c'est une action orale intime (pas juste un baiser sur la joue)
            intimate_oral_context = ["bite", "queue", "sexe", "penis", "cock", "dick", 
                                     "chatte", "pussy", "clit", "t?ton", "nipple",
                                     "prendre dans", "avaler", "toute enti?re", "te sucer", 
                                     "te l?cher", "te prendre", "pipe", "fellation", "blowjob"]
            
            is_intimate_oral = any(ctx in conversation_text for ctx in intimate_oral_context)
            
            if is_intimate_oral:
                context_keywords.append("intimate oral scene, mouth open, tongue out, sensual oral action, explicit oral pose")
                action_detected = True
                print(f"[IMAGE] SPECIFIC ACTION: Intimate oral activity detected", flush=True)
            else:
                # Action orale g?n?rique (baiser, l?cher le cou, etc.)
                context_keywords.append("kissing scene, sensual licking, intimate mouth contact")
                action_detected = True
                print(f"[IMAGE] ACTION: General oral/kissing activity detected", flush=True)
        
        # D?tection de P?N?TRATION
        penetration_keywords = ["p?n?tre", "p?n?trer", "rentre en", "enfonce", "enfoncer",
                               "dedans", "en moi", "en toi", "inside", "penetrat", "thrust"]
        
        if any(keyword in conversation_text for keyword in penetration_keywords):
            context_keywords.append("explicit penetration scene, intimate intercourse, sexual position, explicit sexual act")
            action_detected = True
            print(f"[IMAGE] SPECIFIC ACTION: Penetration activity detected", flush=True)
        
        # D?tection de POSITIONS SP?CIFIQUES
        position_keywords = {
            "quatre pattes": "on all fours position, doggystyle pose, bent over",
            "genoux": "on knees position, kneeling pose, submissive kneel",
            "jambes ?cart": "legs spread wide, open legs position, exposed pose",
            "allong": "lying down position, on back pose, horizontal pose",
            "assis sur": "sitting on lap, straddling position, mounted pose",
            "debout contre": "standing against wall, pressed against, upright position"
        }
        
        for pos_keyword, visual_desc in position_keywords.items():
            if pos_keyword in conversation_text:
                context_keywords.append(visual_desc)
                action_detected = True
                print(f"[IMAGE] SPECIFIC POSITION: {pos_keyword} detected", flush=True)
                break
        
        # D?tection de MASTURBATION (v?rifier contexte r?flexif/auto-plaisir)
        masturbation_keywords = ["masturbe", "caresse moi", "me caresse", "touche moi", "me touche", 
                                "touche toi", "te touches", "doigt", "doigter",
                                "frotte", "stimule", "masturbat", "finger", "rub", "touch myself",
                                "me toucher", "te toucher"]
        
        if any(keyword in conversation_text for keyword in masturbation_keywords):
            context_keywords.append("self-pleasure scene, intimate touching, sensual masturbation pose, hand between legs")
            action_detected = True
            print(f"[IMAGE] SPECIFIC ACTION: Masturbation activity detected", flush=True)
        
        # D?tection d'EXPOSITION (montrer, exhiber)
        exposure_keywords = ["montre", "regarde", "vois", "exhibe", "expose", "d?voile",
                            "show", "look at", "watch", "display", "reveal"]
        body_parts = ["sein", "seins", "poitrine", "fesse", "fesses", "chatte", "sexe", 
                     "t?ton", "corps", "breast", "ass", "pussy", "body"]
        
        has_exposure = any(exp in conversation_text for exp in exposure_keywords)
        has_body_part = any(part in conversation_text for part in body_parts)
        
        if has_exposure and has_body_part:
            context_keywords.append("exhibitionist pose, showing body, revealing intimate parts, display pose")
            action_detected = True
            print(f"[IMAGE] SPECIFIC ACTION: Exhibition/showing detected", flush=True)
        
        # PRIORITE 3: D?tecter l'environnement
        if any(word in conversation_text for word in ["lit", "chambre", "bedroom", "bed", "matelas"]):
            context_keywords.append("bedroom intimate setting, on bed, private room")
        
        # PRIORITE 4: D?tecter l'ambiance/attitude (seulement si pas d'action sp?cifique)
        if not action_detected:
            if any(word in conversation_text for word in ["sexy", "hot", "sensuel", "?rotique", "excit", "belle", "bandant", "chaud"]):
                context_keywords.append("sexy sensual pose, seductive alluring, provocative")
            
            # D?tecter les poses g?n?riques
            if any(word in conversation_text for word in ["position", "pose", "comme ?a", "ainsi", "posture"]):
                context_keywords.append("provocative seductive pose, suggestive position, alluring stance")
            
            # D?tecter les ?motions
            if any(word in conversation_text for word in ["envie", "d?sir", "veux", "besoin", "desire"]):
                context_keywords.append("desire wanting, passionate, aroused expression")
            
            # D?tecter les actions intimes g?n?riques
            if any(word in conversation_text for word in ["touche", "caresse", "embrasse", "kiss", "touch"]):
                context_keywords.append("intimate touching, sensual contact, romantic caress")
        
        # D?tecter les parties du corps mentionn?es (toujours actif)
        if any(word in conversation_text for word in ["sein", "poitrine", "fesse", "cul", "jambe", "cuisse"]):
            context_keywords.append("sensual body curves, revealing figure, attractive physique")
        
        # Construire le prompt contextuel
        name = personality_data.get('name', 'Person')
        genre = personality_data.get('genre', 'Neutre')
        age_num = ''.join(filter(str.isdigit, personality_data.get('age', '25')))
        visual_traits = personality_data.get('visual', '')
        
        base_prompt = self._build_base_prompt(genre, age_num, personality_data.get('description', ''), visual_traits)
        
        if context_keywords:
            context_str = ", ".join(context_keywords)
            full_prompt = f"{base_prompt}, {context_str}"
            print(f"[IMAGE] Contextual generation with keywords: {context_str[:100]}...", flush=True)
        else:
            # Par d?faut, g?n?rer une image suggestive
            full_prompt = f"{base_prompt}, suggestive, sensual"
            print(f"[IMAGE] No specific context detected, using suggestive default", flush=True)
        
        print(f"[IMAGE] Contextual prompt: {full_prompt[:150]}...", flush=True)
        
        # G?n?rer l'image
        image_url = await self._generate_pollinations(full_prompt)
        
        if not image_url and self.replicate_key:
            image_url = await self._generate_replicate(full_prompt)
        
        return image_url
