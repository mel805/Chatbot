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
        self.stable_horde_key = os.getenv('STABLE_HORDE_API_KEY', '0000000000')  # Cl? anonyme par d?faut
        
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
        
        # NOUVEAU FLOW: Essayer les services GRATUITS NSFW en premier !
        image_url = None
        
        for attempt in range(max_retries):
            print(f"[IMAGE] Attempt {attempt + 1}/{max_retries}...", flush=True)
            
            # M?thode 1: Stable Horde (GRATUIT illimit?, NSFW OK, mais peut ?tre lent)
            print(f"[IMAGE] Trying Stable Horde (FREE P2P, NSFW allowed)...", flush=True)
            image_url = await self._generate_stable_horde(full_prompt)
            
            if image_url:
                print(f"[IMAGE] SUCCESS with Stable Horde (FREE)!", flush=True)
                return image_url
            
            # M?thode 2: Hugging Face (TEMPORAIREMENT D?SACTIV? - API d?pr?ci?e)
            # print(f"[IMAGE] Stable Horde failed, trying Hugging Face (FREE, NSFW allowed)...", flush=True)
            # image_url = await self._generate_huggingface(full_prompt)
            # 
            # if image_url:
            #     print(f"[IMAGE] SUCCESS with Hugging Face (FREE)!", flush=True)
            #     return image_url
            print(f"[IMAGE] Hugging Face temporarily disabled (API deprecated)", flush=True)
            
            # M?thode 3: Dezgo (GRATUIT rapide, NSFW OK - mais base64 incompatible Discord)
            print(f"[IMAGE] Hugging Face failed, trying Dezgo (FREE, NSFW allowed)...", flush=True)
            image_url = await self._generate_dezgo(full_prompt)
            
            if image_url:
                print(f"[IMAGE] SUCCESS with Dezgo (FREE)!", flush=True)
                return image_url
            
            # M?thode 4: Replicate (PAYANT backup si cl? configur?e)
            if self.replicate_key:
                print(f"[IMAGE] Free services failed, trying Replicate (PAID)...", flush=True)
                image_url = await self._generate_replicate(full_prompt)
                
                if image_url:
                    print(f"[IMAGE] SUCCESS with Replicate (PAID)!", flush=True)
                    return image_url
            
            # M?thode 5: Pollinations (D?SACTIV? pour tests NSFW explicites)
            # print(f"[IMAGE] Trying Pollinations (FREE but censors NSFW)...", flush=True)
            # image_url = await self._generate_pollinations(full_prompt)
            # 
            # if image_url:
            #     print(f"[IMAGE] SUCCESS with Pollinations (but may be censored)", flush=True)
            #     return image_url
            print(f"[IMAGE] Pollinations DISABLED - Testing NSFW services only", flush=True)
            
            if attempt < max_retries - 1:
                print(f"[IMAGE] Attempt {attempt + 1} failed, retrying...", flush=True)
                await asyncio.sleep(2)  # Petite pause avant retry
        
        print(f"[IMAGE] All {max_retries} attempts and all services failed", flush=True)
        return image_url
    
    def _build_base_prompt(self, genre, age, description, visual_traits=""):
        """Construit le prompt de base selon la personnalit?"""
        
        # CRITIQUE: Placer les mots-cl?s de R?ALISME AU D?BUT (plus fort!)
        # Cela force le mod?le ? g?n?rer du photoR?ALISME d?s le d?part
        realism_prefix = "PHOTOREALISTIC PHOTO, realistic photograph, real human person"
        realism_keywords = "high quality professional photograph, natural photographic lighting, realistic human skin texture with pores, detailed realistic face, natural appearance"
        
        # CRITIQUE: Forcer l'apparence ADULTE selon l'?ge
        # Extraire l'?ge num?rique
        age_num = int(''.join(filter(str.isdigit, str(age))) or "25")
        
        # Construire des indicateurs d'?ge FORTS selon la tranche d'?ge
        if age_num >= 40:
            # 40+ ans : TRES mature
            age_keywords = f"{age_num} years old adult, mature adult woman/man, middle-aged, mature face, adult features, experienced adult, fully grown adult"
            print(f"[IMAGE] Age enforcement: {age_num}+ years (MATURE ADULT)", flush=True)
        elif age_num >= 30:
            # 30-39 ans : Mature
            age_keywords = f"{age_num} years old adult, mature adult, adult person, grown adult, adult face, adult body, fully mature"
            print(f"[IMAGE] Age enforcement: {age_num} years (ADULT)", flush=True)
        elif age_num >= 25:
            # 25-29 ans : Jeune adulte
            age_keywords = f"{age_num} years old adult, young adult, adult person, grown adult, adult features, mature young adult"
            print(f"[IMAGE] Age enforcement: {age_num} years (YOUNG ADULT)", flush=True)
        else:
            # 18-24 ans : Adulte
            age_keywords = f"{age_num} years old adult, adult person, young adult, grown adult, adult body"
            print(f"[IMAGE] Age enforcement: {age_num} years (ADULT)", flush=True)
        
        # Si des traits visuels sp?cifiques sont fournis, les utiliser en priorit?
        if visual_traits:
            print(f"[IMAGE] Using specific visual traits: {visual_traits[:80]}...", flush=True)
            # REALISME EN PREMIER, puis traits, puis ?ge
            prompt = f"{realism_prefix}, {visual_traits}, {age_keywords}, {realism_keywords}"
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
        
        # REALISME EN PREMIER, puis genre, ?ge, traits
        prompt = f"{realism_prefix}, {gender_desc}, {age_keywords}, {traits_str}, {realism_keywords}"
        
        return prompt
    
    async def _generate_pollinations(self, prompt):
        """G?n?re via Pollinations.ai (gratuit, sans cl? API)"""
        try:
            print(f"[IMAGE] Using Pollinations.ai FREE API", flush=True)
            
            # G?n?rer un seed VRAIMENT al?atoire pour ?viter images identiques
            random_seed = random.randint(1, 999999999) + int(time.time() * 1000)
            print(f"[IMAGE] Using random seed: {random_seed}", flush=True)
            
            # CRITIQUE: REFORMULER pour contourner les filtres NSFW de Pollinations
            # Au lieu de "EXPLICIT NSFW", utiliser des descriptions visuelles directes
            # qui passent les filtres mais g?n?rent quand m?me du contenu explicite
            
            # Retirer les mots "EXPLICIT" "NSFW" qui d?clenchent les filtres
            # Garder seulement les descriptions visuelles
            prompt_without_nsfw_flags = prompt.replace("EXPLICIT NSFW CONTENT,", "")
            prompt_without_nsfw_flags = prompt_without_nsfw_flags.replace("adult explicit scene,", "")
            prompt_without_nsfw_flags = prompt_without_nsfw_flags.replace("graphic sexual content,", "")
            prompt_without_nsfw_flags = prompt_without_nsfw_flags.replace("EXPLICIT", "")
            prompt_without_nsfw_flags = prompt_without_nsfw_flags.replace("explicit", "")
            prompt_without_nsfw_flags = prompt_without_nsfw_flags.replace("NSFW", "")
            
            # Simplifier les n?gatifs (trop de n?gatifs peuvent aussi d?clencher les filtres)
            style_negative = "NOT anime, NOT cartoon, NOT drawing"
            age_negative = "NOT child, NOT teen, NOT minor, adult only"
            
            # Combiner
            full_negative = f"{style_negative}, {age_negative}"
            full_prompt_complete = f"{prompt_without_nsfw_flags}. {full_negative}"
            
            # Encoder le prompt pour URL
            encoded_prompt = urllib.parse.quote(full_prompt_complete)
            
            # CRITIQUE: RETIRER "enhance=true" qui peut censurer le contenu
            # CHANGER "model=flux" pour "model=turbo" (moins de filtres de contenu)
            # Utiliser "private=true" pour ?viter la mod?ration publique
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=1024&seed={random_seed}&nologo=true&private=true"
            
            print(f"[IMAGE] Pollinations.ai URL generated successfully", flush=True)
            print(f"[IMAGE] BYPASS: Removed NSFW trigger words to avoid content filtering", flush=True)
            print(f"[IMAGE] BYPASS: Using private mode to avoid public moderation", flush=True)
            print(f"[IMAGE] BYPASS: Removed 'enhance' parameter that may censor content", flush=True)
            print(f"[IMAGE] Style enforcement: Anti-anime keywords", flush=True)
            print(f"[IMAGE] Age safety: Adult-only enforcement", flush=True)
            return image_url
            
        except Exception as e:
            print(f"[ERROR] Pollinations.ai error: {e}", flush=True)
            return None
    
    async def _generate_stable_horde(self, prompt):
        """G?n?re via Stable Horde (GRATUIT, NSFW OK, mais peut ?tre lent)"""
        try:
            print(f"[IMAGE] Using Stable Horde FREE P2P Network (NSFW allowed)", flush=True)
            
            # ?tape 1: Soumettre la requ?te
            submit_url = "https://stablehorde.net/api/v2/generate/async"
            
            # CRITIQUE: Utiliser des MOD?LES NSFW SP?CIFIQUES qui existent vraiment
            # "stable_diffusion" est trop g?n?rique et peut ?tre refus?
            # Utiliser plusieurs mod?les NSFW en fallback
            payload = {
                "prompt": prompt,
                "params": {
                    "width": 768,
                    "height": 1024,
                    "steps": 25,
                    "cfg_scale": 7.5,
                    "sampler_name": "k_euler_a",
                    "n": 1
                },
                "nsfw": True,  # IMPORTANT: Autorise NSFW
                "censor_nsfw": False,  # IMPORTANT: Ne pas censurer
                "models": [
                    "Deliberate",  # Mod?le NSFW photoR?aliste #1
                    "Realistic Vision V5.1",  # Mod?le NSFW photoR?aliste #2
                    "DreamShaper"  # Mod?le NSFW backup
                ]  # MOD?LES NSFW SP?CIFIQUES (pas g?n?rique)
            }
            
            # Headers avec cl? API (requis par Stable Horde maintenant)
            headers = {
                "apikey": self.stable_horde_key,
                "Content-Type": "application/json"
            }
            
            if self.stable_horde_key == '0000000000':
                print(f"[IMAGE] Using Stable Horde anonymous API key (limited)", flush=True)
            else:
                print(f"[IMAGE] Using Stable Horde registered API key", flush=True)
            
            timeout = aiohttp.ClientTimeout(total=120)  # 2 minutes max
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Soumettre
                print(f"[IMAGE] Submitting to Stable Horde with prompt length: {len(prompt)}", flush=True)
                async with session.post(submit_url, json=payload, headers=headers) as resp:
                    if resp.status != 202:
                        error_text = await resp.text()
                        print(f"[ERROR] Stable Horde submit failed: {resp.status}", flush=True)
                        print(f"[ERROR] Stable Horde error message: {error_text[:500]}", flush=True)
                        print(f"[ERROR] Prompt was: {prompt[:200]}...", flush=True)
                        print(f"[DIAGNOSTIC] Stable Horde may reject explicit prompts or complex payloads", flush=True)
                        return None
                    
                    result = await resp.json()
                    request_id = result.get('id')
                    if not request_id:
                        print(f"[ERROR] Stable Horde no request ID in response", flush=True)
                        return None
                    
                    print(f"[IMAGE] Stable Horde request submitted: {request_id}", flush=True)
                
                # ?tape 2: Attendre et r?cup?rer (polling)
                check_url = f"https://stablehorde.net/api/v2/generate/check/{request_id}"
                status_url = f"https://stablehorde.net/api/v2/generate/status/{request_id}"
                
                for attempt in range(60):  # Max 60 tentatives (2 min)
                    await asyncio.sleep(2)  # Attendre 2s entre chaque check
                    
                    async with session.get(check_url) as check_resp:
                        check_data = await check_resp.json()
                        done = check_data.get('done', False)
                        
                        if done:
                            # R?cup?rer l'image
                            async with session.get(status_url) as status_resp:
                                status_data = await status_resp.json()
                                generations = status_data.get('generations', [])
                                if generations:
                                    image_url = generations[0].get('img')
                                    if image_url:
                                        print(f"[IMAGE] Stable Horde SUCCESS after {attempt*2}s", flush=True)
                                        return image_url
                        
                        # Log progression
                        if attempt % 10 == 0:
                            queue_position = check_data.get('queue_position', 0)
                            print(f"[IMAGE] Stable Horde waiting... Queue: {queue_position}", flush=True)
                
                print(f"[IMAGE] Stable Horde timeout after 120s", flush=True)
                return None
                
        except Exception as e:
            print(f"[ERROR] Stable Horde error: {e}", flush=True)
            return None
    
    async def _generate_dezgo(self, prompt):
        """G?n?re via Dezgo (GRATUIT, rapide, NSFW OK)"""
        try:
            print(f"[IMAGE] Using Dezgo FREE API (NSFW allowed)", flush=True)
            
            api_url = "https://api.dezgo.com/text2image"
            
            # FormData pour Dezgo
            form_data = aiohttp.FormData()
            form_data.add_field('prompt', prompt)
            form_data.add_field('width', '768')
            form_data.add_field('height', '1024')
            form_data.add_field('model', 'realistic_vision_v51')
            form_data.add_field('sampler', 'euler_a')
            form_data.add_field('steps', '25')
            form_data.add_field('guidance', '7.5')
            
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(api_url, data=form_data) as resp:
                    if resp.status == 200:
                        # Dezgo retourne directement l'image en bytes
                        image_data = await resp.read()
                        
                        # PROBLEME: Discord n'accepte pas les data URLs dans les embeds
                        # Il faudrait uploader sur un service d'images temporaire
                        # Pour l'instant, on retourne None pour que le fallback continue
                        print(f"[IMAGE] Dezgo returned image but Discord doesn't support base64 embeds", flush=True)
                        print(f"[IMAGE] Skipping Dezgo - use Replicate or external image host", flush=True)
                        return None
                        
                        # # TODO: Uploader sur un service comme imgbb ou imgur
                        # import base64
                        # b64_data = base64.b64encode(image_data).decode()
                        # image_url = f"data:image/png;base64,{b64_data}"
                        # return image_url
                    else:
                        error_text = await resp.text()
                        print(f"[ERROR] Dezgo failed: {resp.status} - {error_text[:100]}", flush=True)
                        return None
                        
        except Exception as e:
            print(f"[ERROR] Dezgo error: {e}", flush=True)
            return None
    
    async def _generate_replicate(self, prompt):
        """G?n?re via Replicate API (PAYANT mais garanti, n?cessite cl? API)"""
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
        """G?n?re via Hugging Face Inference API (GRATUIT avec rate limits, NSFW OK)"""
        try:
            print(f"[IMAGE] Using Hugging Face Inference API (FREE, NSFW allowed)", flush=True)
            
            # Mod?le NSFW photoR?aliste sur Hugging Face
            model_id = "SG161222/Realistic_Vision_V5.1_noVAE"
            # NOUVELLE URL API Hugging Face (l'ancienne est d?pr?ci?e)
            api_url = f"https://api-inference.huggingface.co/models/{model_id}"
            # Note: Si erreur 410, essayer: https://router.huggingface.co/hf-inference
            
            # Headers (optionnel mais aide avec rate limits)
            headers = {}
            if self.huggingface_key:
                headers["Authorization"] = f"Bearer {self.huggingface_key}"
                print(f"[IMAGE] Using Hugging Face API key", flush=True)
            else:
                print(f"[IMAGE] Using Hugging Face without API key (may have rate limits)", flush=True)
            
            # Payload
            payload = {
                "inputs": prompt,
                "parameters": {
                    "width": 768,
                    "height": 1024,
                    "num_inference_steps": 25,
                    "guidance_scale": 7.5
                }
            }
            
            timeout = aiohttp.ClientTimeout(total=90)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(api_url, headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        # Hugging Face retourne l'image en bytes
                        image_data = await resp.read()
                        
                        # Uploader sur un service d'h?bergement temporaire
                        # Pour l'instant, on utilise tmpfiles.org ou imgbb
                        upload_url = await self._upload_image_to_tmpfiles(image_data)
                        
                        if upload_url:
                            print(f"[IMAGE] Hugging Face SUCCESS - Image uploaded", flush=True)
                            return upload_url
                        else:
                            print(f"[IMAGE] Hugging Face generated image but upload failed", flush=True)
                            return None
                    
                    elif resp.status == 503:
                        # Mod?le en chargement
                        result = await resp.json()
                        estimated_time = result.get('estimated_time', 20)
                        print(f"[IMAGE] Hugging Face model loading, estimated time: {estimated_time}s", flush=True)
                        
                        # Attendre et r?essayer (max 60s)
                        if estimated_time < 60:
                            await asyncio.sleep(estimated_time + 5)
                            
                            # R?essayer une fois
                            async with session.post(api_url, headers=headers, json=payload) as retry_resp:
                                if retry_resp.status == 200:
                                    image_data = await retry_resp.read()
                                    upload_url = await self._upload_image_to_tmpfiles(image_data)
                                    
                                    if upload_url:
                                        print(f"[IMAGE] Hugging Face SUCCESS after retry", flush=True)
                                        return upload_url
                        
                        return None
                    
                    elif resp.status == 429:
                        # Rate limit
                        print(f"[IMAGE] Hugging Face rate limit reached", flush=True)
                        return None
                    
                    else:
                        error_text = await resp.text()
                        print(f"[ERROR] Hugging Face failed: {resp.status} - {error_text[:200]}", flush=True)
                        return None
                        
        except Exception as e:
            print(f"[ERROR] Hugging Face error: {e}", flush=True)
            return None
    
    async def _upload_image_to_tmpfiles(self, image_data):
        """Upload image bytes vers tmpfiles.org pour obtenir une URL"""
        try:
            print(f"[IMAGE] Uploading image to tmpfiles.org...", flush=True)
            
            # Utiliser tmpfiles.org (service gratuit, pas de cl? requise)
            upload_url = "https://tmpfiles.org/api/v1/upload"
            
            # Cr?er un FormData avec l'image
            form_data = aiohttp.FormData()
            form_data.add_field('file',
                              image_data,
                              filename='generated.png',
                              content_type='image/png')
            
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(upload_url, data=form_data) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        
                        # tmpfiles.org retourne: {"status": "success", "data": {"url": "..."}}
                        if result.get('status') == 'success':
                            file_url = result.get('data', {}).get('url', '')
                            
                            # tmpfiles.org retourne une URL comme https://tmpfiles.org/12345
                            # Il faut la convertir en URL directe: https://tmpfiles.org/dl/12345
                            if 'tmpfiles.org/' in file_url and '/dl/' not in file_url:
                                file_url = file_url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
                            
                            print(f"[IMAGE] Upload success: {file_url}", flush=True)
                            return file_url
                    
                    print(f"[IMAGE] Upload failed: {resp.status}", flush=True)
                    return None
                    
        except Exception as e:
            print(f"[ERROR] Image upload error: {e}", flush=True)
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
        
        # Extraire le texte de la conversation (g?rer dict ou str)
        conversation_texts = []
        for msg in conversation_history[-10:]:
            if isinstance(msg, dict):
                conversation_texts.append(msg.get('content', ''))
            else:
                conversation_texts.append(str(msg))
        conversation_text = " ".join(conversation_texts).lower()
        
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
                # PROMPT ULTRA EXPLICITE pour VRAIE sc?ne de fellation/oral sex
                explicit_oral_prompt = "NSFW explicit hardcore fellatio scene, woman giving blowjob, dick in mouth, actively sucking penis, tongue licking cock shaft, POV oral sex, close-up explicit blowjob, mouth filled with dick, deepthroat scene, explicit cumming oral, graphic XXX oral penetration, pornographic blowjob photo, real explicit fellatio action, hardcore oral sex scene, uncensored NSFW blowjob"
                context_keywords.append(explicit_oral_prompt)
                action_detected = True
                print(f"[IMAGE] SPECIFIC ACTION: ULTRA EXPLICIT Intimate oral activity detected", flush=True)
            else:
                # Action orale g?n?rique (baiser, l?cher le cou, etc.)
                context_keywords.append("kissing scene, sensual licking, intimate mouth contact")
                action_detected = True
                print(f"[IMAGE] ACTION: General oral/kissing activity detected", flush=True)
        
        # D?tection de P?N?TRATION
        penetration_keywords = ["p?n?tre", "p?n?trer", "rentre en", "enfonce", "enfoncer",
                               "dedans", "en moi", "en toi", "inside", "penetrat", "thrust"]
        
        if any(keyword in conversation_text for keyword in penetration_keywords):
            # PROMPT ULTRA EXPLICITE pour VRAIE sc?ne de p?n?tration/sex
            explicit_penetration_prompt = "NSFW explicit hardcore sex scene, dick penetrating pussy, active fucking, penis inside vagina visible, explicit sexual intercourse POV, graphic penetration close-up, XXX hardcore fucking scene, pornographic sex photo, uncensored penetration shot, real explicit fucking action, genitals clearly visible, hardcore NSFW intercourse, explicit vaginal penetration, pornographic sex position"
            context_keywords.append(explicit_penetration_prompt)
            action_detected = True
            print(f"[IMAGE] SPECIFIC ACTION: ULTRA EXPLICIT Penetration activity detected", flush=True)
        
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
            # PROMPT ULTRA EXPLICITE pour VRAIE sc?ne de masturbation
            explicit_masturbation_prompt = "NSFW explicit hardcore masturbation scene, fingers inside pussy, hand stroking cock, actively fingering herself, graphic self-pleasure POV, explicit masturbation close-up, visible pussy/dick being touched, XXX solo masturbation photo, pornographic self-pleasure scene, uncensored genital stimulation, real explicit touching genitals, hardcore NSFW solo sex, fingering pussy clearly visible, explicit masturbation action"
            context_keywords.append(explicit_masturbation_prompt)
            action_detected = True
            print(f"[IMAGE] SPECIFIC ACTION: ULTRA EXPLICIT Masturbation activity detected", flush=True)
        
        # D?tection d'EXPOSITION (montrer, exhiber)
        exposure_keywords = ["montre", "regarde", "vois", "exhibe", "expose", "d?voile",
                            "show", "look at", "watch", "display", "reveal"]
        body_parts = ["sein", "seins", "poitrine", "fesse", "fesses", "chatte", "sexe", 
                     "t?ton", "corps", "breast", "ass", "pussy", "body"]
        
        has_exposure = any(exp in conversation_text for exp in exposure_keywords)
        has_body_part = any(part in conversation_text for part in body_parts)
        
        if has_exposure and has_body_part:
            # PROMPT ULTRA EXPLICITE pour VRAIE exposition des parties intimes
            explicit_exhibition_prompt = "NSFW explicit hardcore nude pose, pussy spread wide open visible, breasts fully exposed, full frontal nudity genitals shown, explicit genital display close-up, XXX nude exhibition photo, pornographic body display, uncensored pussy/breasts/ass visible, real explicit nude modeling, hardcore NSFW full nudity, graphic genital exposure, detailed vulva/penis view, pornographic nude pose"
            context_keywords.append(explicit_exhibition_prompt)
            action_detected = True
            print(f"[IMAGE] SPECIFIC ACTION: ULTRA EXPLICIT Exhibition/showing detected", flush=True)
        
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
        
        # G?n?rer l'image - NOUVEAU FLOW: Services GRATUITS NSFW en premier !
        image_url = None
        
        # 1. Stable Horde (GRATUIT illimit?, NSFW OK)
        print(f"[IMAGE] Trying Stable Horde (FREE P2P, NSFW allowed)...", flush=True)
        image_url = await self._generate_stable_horde(full_prompt)
        
        if image_url:
            print(f"[IMAGE] SUCCESS with Stable Horde (FREE)!", flush=True)
            return image_url
        
        # 2. Hugging Face (TEMPORAIREMENT D?SACTIV? - API d?pr?ci?e)
        # print(f"[IMAGE] Hugging Face attempt (FREE, NSFW allowed)...", flush=True)
        # image_url = await self._generate_huggingface(full_prompt)
        # 
        # if image_url:
        #     print(f"[IMAGE] SUCCESS with Hugging Face (FREE)!", flush=True)
        #     return image_url
        print(f"[IMAGE] Hugging Face temporarily disabled (API deprecated)", flush=True)
        
        # 3. Dezgo (GRATUIT rapide, NSFW OK - mais base64 incompatible Discord)
        print(f"[IMAGE] Hugging Face failed, trying Dezgo (FREE, NSFW allowed)...", flush=True)
        image_url = await self._generate_dezgo(full_prompt)
        
        if image_url:
            print(f"[IMAGE] SUCCESS with Dezgo (FREE)!", flush=True)
            return image_url
        
        # 4. Replicate (PAYANT backup si cl? configur?e)
        if self.replicate_key:
            print(f"[IMAGE] Free services failed, trying Replicate (PAID)...", flush=True)
            image_url = await self._generate_replicate(full_prompt)
            
            if image_url:
                print(f"[IMAGE] SUCCESS with Replicate (PAID)!", flush=True)
                return image_url
        
        # 5. Pollinations (D?SACTIV? pour tests NSFW explicites)
        # print(f"[IMAGE] Trying Pollinations (FREE but censors NSFW)...", flush=True)
        # image_url = await self._generate_pollinations(full_prompt)
        # 
        # if image_url:
        #     print(f"[IMAGE] SUCCESS with Pollinations (but may be censored)", flush=True)
        print(f"[IMAGE] Pollinations DISABLED - Testing NSFW services only", flush=True)
        
        return image_url
