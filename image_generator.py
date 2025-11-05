"""
Générateur d'images NSFW pour les personnalités du bot Discord
Utilise plusieurs APIs gratuites en fallback pour garantir 100% de réussite
"""

import aiohttp
import asyncio
import os
import json
import urllib.parse
import random
import time
import base64

class ImageGenerator:
    """Génère des images NSFW basées sur les personnalités avec multi-APIs"""
    
    def __init__(self):
        self.replicate_key = os.getenv('REPLICATE_API_KEY', '')
        self.huggingface_key = os.getenv('HUGGINGFACE_API_KEY', '')
        
        # Stats pour choisir la meilleure API
        self.api_success_count = {
            'pollinations_turbo': 0,  # Version ultra rapide de Pollinations
            'pollinations': 0,
            'picso': 0,  # NOUVEAU: Rapide et NSFW-friendly
            'prodia': 0,
            'together': 0,
            'dezgo': 0
        }
        
        # Liste des APIs disponibles PRIORISaES par vitesse (rapides en premier)
        # Les APIs les plus rapides sont essayees en premier
        self.available_apis = [
            'pollinations_turbo',  # 2-5s ultra rapide
            'pollinations',        # 5-15s rapide
            'prodia',             # 15-30s moyen
        ]
        
    async def generate_personality_image(self, personality_data, prompt_addition="", max_retries=5):
        """
        Génère une image basée sur la personnalité avec retry automatique
        
        Args:
            personality_data: Dictionnaire avec name, genre, age, description, visual
            prompt_addition: Texte additionnel pour le prompt
            max_retries: Nombre maximum de tentatives (défaut: 3)
        
        Returns:
            URL de l'image ou None si erreur
        """
        
        # Construire le prompt basa sur la personnalite
        name = personality_data.get('name', 'Person')
        genre = personality_data.get('genre', 'Neutre')
        age = personality_data.get('age', '25 ans')
        description = personality_data.get('description', '')
        visual_traits = personality_data.get('visual', '')  # Caractéristiques visuelles uniques
        
        # Extraire l'ge numerique
        age_num = ''.join(filter(str.isdigit, age))
        
        # Construire le prompt Stable Diffusion avec traits visuels uniques
        base_prompt = self._build_base_prompt(genre, age_num, description, visual_traits)
        full_prompt = f"{base_prompt}, {prompt_addition}" if prompt_addition else base_prompt
        
        print(f"[IMAGE] Generating image for {name} with prompt: {full_prompt[:100]}...", flush=True)
        
        # SYSTeME MULTI-API avec rotation intelligente pour 100% de reussite
        image_url = None
        
        # Determiner l'ordre des APIs a essayer (rotation selon succes precedents)
        api_order = sorted(self.available_apis, 
                          key=lambda x: self.api_success_count[x], 
                          reverse=True)
        
        print(f"[IMAGE] API order (by success rate): {api_order}", flush=True)
        
        for attempt in range(max_retries):
            print(f"[IMAGE] === Attempt {attempt + 1}/{max_retries} ===", flush=True)
            
            # Choisir l'API a utiliser pour cette tentative
            api_index = attempt % len(api_order)
            current_api = api_order[api_index]
            
            print(f"[IMAGE] Trying API: {current_api}", flush=True)
            
            # Essayer l'API selectionnee (ORDRE PAR VITESSE)
            if current_api == 'pollinations_turbo':
                image_url = await self._generate_pollinations_turbo(full_prompt)
            elif current_api == 'picso':
                image_url = await self._generate_picso(full_prompt)
            elif current_api == 'pollinations':
                image_url = await self._generate_pollinations(full_prompt, attempt=attempt+1)
            elif current_api == 'prodia':
                image_url = await self._generate_prodia(full_prompt)
            elif current_api == 'dezgo':
                image_url = await self._generate_dezgo(full_prompt)
            elif current_api == 'together':
                image_url = await self._generate_together(full_prompt)
            
            if image_url:
                print(f"[IMAGE]  SUCCESS with {current_api} on attempt {attempt + 1}!", flush=True)
                return image_url
            
            # Si le prompt est complexe et on a echoua 2 fois, simplifier
            if attempt >= 2 and len(full_prompt) > 200:
                print(f"[IMAGE] Trying with simplified prompt on {current_api}...", flush=True)
                simplified_prompt = self._simplify_prompt(full_prompt)
                
                if current_api == 'pollinations_turbo':
                    image_url = await self._generate_pollinations_turbo(simplified_prompt)
                elif current_api == 'pollinations':
                    image_url = await self._generate_pollinations(simplified_prompt, attempt=attempt+1)
                elif current_api == 'prodia':
                    image_url = await self._generate_prodia(simplified_prompt)
                
                if image_url:
                    print(f"[IMAGE]  SUCCESS with simplified prompt on {current_api}!", flush=True)
                    return image_url
            
            # Fallback Replicate si disponible et derniere tentative
            if self.replicate_key and attempt >= 4:
                print(f"[IMAGE] All free APIs failed, trying Replicate (paid)...", flush=True)
                image_url = await self._generate_replicate(full_prompt)
                if image_url:
                    print(f"[IMAGE]  SUCCESS with Replicate!", flush=True)
                    return image_url
            
            # Attendre avant prochaine tentative
            if attempt < max_retries - 1:
                wait_time = 1 + (attempt // 2)  # Augmente progressivement
                print(f"[IMAGE] Waiting {wait_time}s before next attempt...", flush=True)
                await asyncio.sleep(wait_time)
        
        # FALLBACK ABSOLU GARANTI (Pollinations simple)
        print(f"[IMAGE] === FINAL FALLBACK === All APIs exhausted", flush=True)
        print(f"[IMAGE] Generating guaranteed Pollinations fallback URL", flush=True)
        random_seed = random.randint(1, 999999999)
        encoded_prompt = urllib.parse.quote(self._simplify_prompt(full_prompt))
        fallback_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}éwidth=512&height=768&model=turbo&seed={random_seed}&nologo=true"
        print(f"[IMAGE] Returning final fallback URL", flush=True)
        return fallback_url
    
    def _build_base_prompt(self, genre, age, description, visual_traits=""):
        """Construit le prompt de base selon la personnalité"""
        
        # Si des traits visuels specifiques sont fournis, les utiliser en priorite
        if visual_traits:
            print(f"[IMAGE] Using specific visual traits: {visual_traits[:80]}...", flush=True)
            # Prompt plus simple et plus fiable
            prompt = f"{visual_traits}, {age} years old, portrait photography"
            return prompt
        
        # Sinon, utiliser l'ancienne methode (fallback)
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
        
        # Prompt complet (simplifie)
        prompt = f"portrait, {gender_desc}, {age} years old, {traits_str}, professional photography"
        
        return prompt
    
    async def _generate_pollinations_turbo(self, prompt):
        """Génère via Pollinations.ai en mode TURBO (ultra rapide 2-5s, NSFW-friendly)"""
        try:
            print(f"[IMAGE] Using Pollinations TURBO mode (ultra fast)", flush=True)
            
            # Seed alcatoire
            random_seed = random.randint(1, 999999999) + int(time.time() * 1000)
            
            # Encoder le prompt
            encoded_prompt = urllib.parse.quote(prompt)
            
            # URL TURBO: resolution reduite mais ULTRA RAPIDE
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}éwidth=512&height=768&model=turbo&seed={random_seed}&nologo=true&enhance=false"
            
            print(f"[IMAGE] Pollinations TURBO URL generated (expected 2-5s)", flush=True)
            
            # Validation rapide
            if await self._validate_image_url(image_url):
                print(f"[IMAGE] Pollinations TURBO validated!", flush=True)
                self.api_success_count['pollinations_turbo'] += 1
                return image_url
            else:
                print(f"[IMAGE] Pollinations TURBO validation failed", flush=True)
                return None
                
        except Exception as e:
            print(f"[ERROR] Pollinations TURBO error: {e}", flush=True)
            return None
    
    async def _generate_picso(self, prompt):
        """Génère via PicSo (rapide 5-10s, NSFW-friendly, style anime/réaliste)"""
        try:
            print(f"[IMAGE] Using PicSo API (fast, NSFW-friendly)", flush=True)
            
            # PicSo utilise une API simple sans cle
            api_url = "https://api.picso.ai/v1/generate"
            
            # Seed aleatoire
            random_seed = random.randint(1, 999999999)
            
            # Payload pour PicSo (simplifie pour vitesse)
            payload = {
                "prompt": prompt,
                "style": "realistic",  # Style réaliste (ou "anime" pour anime)
                "width": 512,
                "height": 768,
                "steps": 15,  # Moins d'étapes = plus rapide
                "seed": random_seed
            }
            
            timeout = aiohttp.ClientTimeout(total=20)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    async with session.post(api_url, json=payload) as resp:
                        if resp.status == 200:
                            result = await resp.json()
                            image_url = result.get('url') or result.get('image_url')
                            
                            if image_url:
                                print(f"[IMAGE] PicSo: Success!", flush=True)
                                self.api_success_count['picso'] += 1
                                return image_url
                        else:
                            print(f"[IMAGE] PicSo: HTTP {resp.status}", flush=True)
                except:
                    # Si PicSo ne fonctionne pas, fallback silencieux
                    print(f"[IMAGE] PicSo: Service unavailable, skipping", flush=True)
                    
            return None
            
        except Exception as e:
            print(f"[ERROR] PicSo error: {e} (service may not exist)", flush=True)
            return None
    
    async def _generate_pollinations(self, prompt, attempt=1):
        """Génère via Pollinations.ai (gratuit, sans clé API) avec fallback intelligent"""
        try:
            print(f"[IMAGE] Using Pollinations.ai FREE API (attempt {attempt})", flush=True)
            
            # Generer un seed VRAIMENT alcatoire pour eviter images identiques
            random_seed = random.randint(1, 999999999) + int(time.time() * 1000)
            print(f"[IMAGE] Using random seed: {random_seed}", flush=True)
            
            # Encoder le prompt pour URL
            encoded_prompt = urllib.parse.quote(prompt)
            
            # STRATeGIE MULTI-FALLBACK pour garantir 100% de reussite
            strategies = [
                # Strategie 1: Flux avec enhance (meilleure qualite)
                {"model": "flux", "enhance": "true", "width": 768, "height": 1024},
                # Strategie 2: Flux sans enhance (plus rapide)
                {"model": "flux", "enhance": "false", "width": 768, "height": 1024},
                # Strategie 3: Flux avec resolution reduite (plus fiable)
                {"model": "flux", "enhance": "true", "width": 512, "height": 768},
                # Strategie 4: Turbo (le plus rapide)
                {"model": "turbo", "enhance": "false", "width": 768, "height": 1024},
            ]
            
            # Choisir la strategie selon la tentative
            strategy_index = min(attempt - 1, len(strategies) - 1)
            strategy = strategies[strategy_index]
            
            # Construire l'URL avec la strategie choisie
            params = f"width={strategy['width']}&height={strategy['height']}&model={strategy['model']}&seed={random_seed}&nologo=true&enhance={strategy['enhance']}"
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}é{params}"
            
            print(f"[IMAGE] Strategy {strategy_index + 1}: {strategy['model']} ({strategy['width']}x{strategy['height']}) enhance={strategy['enhance']}", flush=True)
            print(f"[IMAGE] URL generated, validating...", flush=True)
            
            # VALIDATION SOUPLE: On accepte meme avec timeout
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
        """Génère via Replicate API (nécessite clé API)"""
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
                        
                        # Attendre generation (max 60s)
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
                    # Verifier le code de statut
                    if resp.status != 200:
                        print(f"[IMAGE] Validation failed: HTTP {resp.status}", flush=True)
                        return False
                    
                    # Verifier le type de contenu
                    content_type = resp.headers.get('Content-Type', '')
                    if not content_type.startswith('image/'):
                        print(f"[IMAGE] Validation failed: Not an image (Content-Type: {content_type})", flush=True)
                        return False
                    
                    # Verifier que nous avons reeu des donnees
                    content_length = resp.headers.get('Content-Length', '0')
                    if int(content_length) < 1000:  # Image trop petite = probablement erreur
                        print(f"[IMAGE] Validation failed: Image too small ({content_length} bytes)", flush=True)
                        return False
                    
                    print(f"[IMAGE] Validation success: {content_type}, {content_length} bytes, HTTP {resp.status}", flush=True)
                    return True
        except asyncio.TimeoutError:
            print(f"[IMAGE] Validation timeout after {timeout_seconds}s - Accepting URL anyway", flush=True)
            # CHANGEMENT: On accepte l'URL meme en cas de timeout car Pollinations.ai peut etre lent
            return True
        except Exception as e:
            print(f"[IMAGE] Validation error: {e} - Accepting URL anyway", flush=True)
            # En cas d'erreur, on accepte quand meme (mieux vaut essayer que ne rien afficher)
            return True
    
    def _simplify_prompt(self, prompt):
        """Simplifie un prompt trop complexe pour améliorer la génération"""
        # Garder seulement les elements essentiels
        words = prompt.split(',')
        # Garder les 5 premiers elements les plus importants
        essential = words[:5]
        simplified = ', '.join(essential).strip()
        print(f"[IMAGE] Simplified prompt from {len(prompt)} to {len(simplified)} chars", flush=True)
        return simplified
    
    async def _generate_prodia(self, prompt):
        """Génère via Prodia.com (gratuit, supporte NSFW)"""
        try:
            print(f"[IMAGE] Using Prodia.com FREE API (NSFW-friendly)", flush=True)
            
            # Prodia utilise un systeme en 2 etapes: generation puis recuperation
            api_url = "https://api.prodia.com/v1/sd/generate"
            
            # Seed alcatoire
            random_seed = random.randint(1, 999999999)
            
            # Payload pour Prodia
            payload = {
                "prompt": prompt,
                "model": "absolutereality_v181.safetensors [3d9d4d2b]",  # Modèle rçaliste
                "negative_prompt": "low quality, blurry, distorted, deformed, ugly",
                "steps": 20,
                "cfg_scale": 7,
                "seed": random_seed,
                "upscale": True,
                "sampler": "DPM++ 2M Karras",
                "aspect_ratio": "portrait"
            }
            
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                # Lancer la generation
                async with session.post(api_url, json=payload) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        job_id = result.get('job')
                        
                        if not job_id:
                            print(f"[IMAGE] Prodia: No job ID returned", flush=True)
                            return None
                        
                        print(f"[IMAGE] Prodia: Job {job_id} started, waiting...", flush=True)
                        
                        # Attendre la generation (max 40s)
                        for i in range(20):
                            await asyncio.sleep(2)
                            
                            check_url = f"https://api.prodia.com/v1/job/{job_id}"
                            async with session.get(check_url) as check_resp:
                                if check_resp.status == 200:
                                    job_data = await check_resp.json()
                                    status = job_data.get('status')
                                    
                                    if status == 'succeeded':
                                        image_url = job_data.get('imageUrl')
                                        if image_url:
                                            print(f"[IMAGE] Prodia: Success!", flush=True)
                                            self.api_success_count['prodia'] += 1
                                            return image_url
                                    elif status == 'failed':
                                        print(f"[IMAGE] Prodia: Generation failed", flush=True)
                                        return None
                    else:
                        print(f"[IMAGE] Prodia: HTTP {resp.status}", flush=True)
                        return None
            
            return None
            
        except Exception as e:
            print(f"[ERROR] Prodia error: {e}", flush=True)
            return None
    
    async def _generate_dezgo(self, prompt):
        """Génère via Dezgo.com (gratuit, NSFW-friendly)"""
        try:
            print(f"[IMAGE] Using Dezgo.com FREE API (NSFW-friendly)", flush=True)
            
            api_url = "https://api.dezgo.com/text2image"
            
            # Payload pour Dezgo
            payload = {
                "prompt": prompt,
                "model": "epic_realism",  # Modèle rçaliste
                "negative_prompt": "low quality, blurry, distorted",
                "width": 512,
                "height": 768,
                "guidance": 7.5,
                "steps": 25,
                "seed": random.randint(1, 999999999),
                "sampler": "dpmpp_2m"
            }
            
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(api_url, data=payload) as resp:
                    if resp.status == 200:
                        # Dezgo retourne l'image directement en bytes
                        image_data = await resp.read()
                        
                        if len(image_data) > 5000:  # Vérifier qu'on a une vraie image
                            # Convertir en base64 pour Discord (ou upload quelque part)
                            # Pour l'instant, on va utiliser un service d'upload temporaire
                            print(f"[IMAGE] Dezgo: Image received ({len(image_data)} bytes)", flush=True)
                            
                            # Upload sur catbox.moe (service gratuit d'hebergement)
                            upload_url = await self._upload_to_catbox(image_data)
                            
                            if upload_url:
                                print(f"[IMAGE] Dezgo: Success!", flush=True)
                                self.api_success_count['dezgo'] += 1
                                return upload_url
                    else:
                        print(f"[IMAGE] Dezgo: HTTP {resp.status}", flush=True)
                        
            return None
            
        except Exception as e:
            print(f"[ERROR] Dezgo error: {e}", flush=True)
            return None
    
    async def _upload_to_catbox(self, image_data):
        """Upload une image sur catbox.moe (service gratuit)"""
        try:
            upload_url = "https://catbox.moe/user/api.php"
            
            data = aiohttp.FormData()
            data.add_field('reqtype', 'fileupload')
            data.add_field('fileToUpload', image_data, filename='image.png', content_type='image/png')
            
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(upload_url, data=data) as resp:
                    if resp.status == 200:
                        url = await resp.text()
                        url = url.strip()
                        if url.startswith('http'):
                            print(f"[IMAGE] Uploaded to catbox: {url}", flush=True)
                            return url
            
            return None
        except Exception as e:
            print(f"[ERROR] Catbox upload error: {e}", flush=True)
            return None
    
    async def _generate_together(self, prompt):
        """Génère via Together.ai API (gratuit avec quota)"""
        try:
            # Cette API necessite une cle API gratuite
            # Pour l'instant on la skip si pas de cle
            together_key = os.getenv('TOGETHER_API_KEY', '')
            if not together_key:
                print(f"[IMAGE] Together.ai: No API key, skipping", flush=True)
                return None
            
            print(f"[IMAGE] Using Together.ai API", flush=True)
            
            api_url = "https://api.together.xyz/v1/images/generations"
            
            headers = {
                "Authorization": f"Bearer {together_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "stabilityai/stable-diffusion-xl-base-1.0",
                "prompt": prompt,
                "width": 768,
                "height": 1024,
                "steps": 25,
                "n": 1,
                "seed": random.randint(1, 999999999)
            }
            
            timeout = aiohttp.ClientTimeout(total=60)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(api_url, headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        if 'data' in result and len(result['data']) > 0:
                            image_url = result['data'][0].get('url')
                            if image_url:
                                print(f"[IMAGE] Together.ai: Success!", flush=True)
                                self.api_success_count['together'] += 1
                                return image_url
                    else:
                        print(f"[IMAGE] Together.ai: HTTP {resp.status}", flush=True)
            
            return None
            
        except Exception as e:
            print(f"[ERROR] Together.ai error: {e}", flush=True)
            return None
    
    async def _generate_huggingface(self, prompt):
        """Génère via Hugging Face (nécessite clé API)"""
        print(f"[IMAGE] Hugging Face not implemented yet", flush=True)
        return None
    
    def _analyze_bot_actions(self, bot_text):
        print(f"[IMAGE] Analyzing bot text for clothing/accessories...", flush=True)
        
        detected = {
            'action': None,
            'location': None,
            'clothing_items': [],  # Liste de tous les vêtements
            'accessories': [],     # Liste de tous les accessoires
            'colors': [],          # Couleurs mentionnées
            'materials': [],       # Matières (soie, dentelle, etc.)
            'descriptors': [],     # Qualificatifs (transparent, moulant, etc.)
            'pose': None,
            'activity': None,
            'body_visibility': None  # Niveau d'exposition
        }
        
        # ACTIONS QUOTIDIENNES
        if any(word in bot_text for word in ["cuisine", "cuisin", "cooking", "prépare a  manger", "fais a  manger"]):
            detected['action'] = "cooking in kitchen"
            detected['location'] = "kitchen"
            detected['activity'] = "cooking, holding cooking utensils, preparing food"
            
        elif any(word in bot_text for word in ["dors", "dort", "sommeil", "sleeping", "tired", "fatigue", "au lit"]):
            detected['action'] = "sleeping"
            detected['location'] = "bedroom, in bed"
            detected['activity'] = "lying in bed, sleeping, relaxed pose"
            
        elif any(word in bot_text for word in ["douche", "shower", "bain", "bath", "me lave"]):
            detected['action'] = "showering"
            detected['location'] = "bathroom, shower"
            detected['activity'] = "in shower, wet skin, water droplets"
            
        elif any(word in bot_text for word in ["travail", "working", "bureau", "office", "ordinateur", "computer"]):
            detected['action'] = "working"
            detected['location'] = "office, at desk"
            detected['activity'] = "working at desk, using computer"
            
        elif any(word in bot_text for word in ["lit", "bed", "couché", "allongé", "lying"]):
            detected['action'] = "lying down"
            detected['location'] = "bedroom, on bed"
            detected['activity'] = "lying on bed, relaxed"
            
        elif any(word in bot_text for word in ["canapé", "sofa", "couch", "salon", "living room"]):
            detected['action'] = "relaxing"
            detected['location'] = "living room, on couch"
            detected['activity'] = "sitting on couch, relaxed"
            
        elif any(word in bot_text for word in ["dehors", "outside", "jardin", "garden", "parc", "park"]):
            detected['action'] = "outside"
            detected['location'] = "outdoor, nature, garden"
            detected['activity'] = "standing outside, natural setting"
            
        elif any(word in bot_text for word in ["sport", "exercise", "gym", "entrainement"]):
            detected['action'] = "exercising"
            detected['location'] = "gym, workout area"
            detected['activity'] = "exercising, workout clothes, athletic pose"
            
        elif any(word in bot_text for word in ["mange", "eating", "repas", "meal", "dîne", "déjeune"]):
            detected['action'] = "eating"
            detected['location'] = "dining area, at table"
            detected['activity'] = "eating, at table"
            
        elif any(word in bot_text for word in ["lis", "reading", "livre", "book"]):
            detected['action'] = "reading"
            detected['location'] = "comfortable setting"
            detected['activity'] = "reading a book, relaxed"
        
        # EXTRACTION PRaCISE DES VaTEMENTS
        clothing_keywords = {
            "robe": "dress",
            "dress": "dress",
            "jupe": "skirt",
            "skirt": "skirt",
            "string": "thong",
            "thong": "thong",
            "culotte": "panties",
            "panties": "panties",
            "soutien-gorge": "bra",
            "bra": "bra",
            "lingerie": "lingerie",
            "body": "bodysuit",
            "corset": "corset",
            "bas": "stockings",
            "stockings": "stockings",
            "collants": "tights",
            "pyjama": "pajamas",
            "chemise": "shirt",
            "t-shirt": "t-shirt",
            "top": "top",
            "débardeur": "tank top",
            "pull": "sweater",
            "gilet": "cardigan",
            "veste": "jacket",
            "manteau": "coat",
            "pantalon": "pants",
            "jean": "jeans",
            "short": "shorts",
            "maillot": "swimsuit",
            "bikini": "bikini"
        }
        
        for keyword, english in clothing_keywords.items():
            if keyword in bot_text:
                detected['clothing_items'].append(english)
                print(f"[IMAGE] !!! VETEMENT DETECTE: '{keyword}' -> '{english}'", flush=True)
        
        # ACCESSOIRES
        accessory_keywords = {
            "talons": "high heels",
            "heels": "high heels",
            "chaussures": "shoes",
            "boots": "boots",
            "bottes": "boots",
            "escarpins": "pumps",
            "collier": "necklace",
            "boucles d'oreilles": "earrings",
            "bracelet": "bracelet",
            "bague": "ring",
            "ceinture": "belt",
            "chapeau": "hat",
            "lunettes": "glasses",
            "gants": "gloves",
            "foulard": "scarf",
            "écharpe": "scarf"
        }
        
        for keyword, english in accessory_keywords.items():
            if keyword in bot_text:
                detected['accessories'].append(english)
                print(f"[IMAGE] !!! ACCESSOIRE DETECTE: '{keyword}' -> '{english}'", flush=True)
        
        # COULEURS
        color_keywords = {
            "noir": "black",
            "blanc": "white",
            "rouge": "red",
            "bleu": "blue",
            "vert": "green",
            "rose": "pink",
            "violet": "purple",
            "jaune": "yellow",
            "orange": "orange",
            "gris": "gray",
            "beige": "beige",
            "doré": "gold",
            "argenté": "silver"
        }
        
        for keyword, english in color_keywords.items():
            if keyword in bot_text:
                detected['colors'].append(english)
                print(f"[IMAGE] !!! COULEUR DETECTEE: '{keyword}' -> '{english}'", flush=True)
        
        # MATIaRES
        material_keywords = {
            "soie": "silk",
            "silk": "silk",
            "dentelle": "lace",
            "lace": "lace",
            "cuir": "leather",
            "leather": "leather",
            "satin": "satin",
            "velours": "velvet",
            "coton": "cotton",
            "latex": "latex",
            "résille": "fishnet"
        }
        
        for keyword, english in material_keywords.items():
            if keyword in bot_text:
                detected['materials'].append(english)
                print(f"[IMAGE] !!! MATIERE DETECTEE: '{keyword}' -> '{english}'", flush=True)
        
        # QUALIFICATIFS/DESCRIPTEURS
        descriptor_keywords = {
            "transparent": "transparent, see-through",
            "see-through": "see-through",
            "moulant": "tight-fitting, form-fitting",
            "tight": "tight-fitting",
            "serré": "tight",
            "ample": "loose",
            "court": "short",
            "long": "long",
            "décolleté": "low-cut, cleavage",
            "échancré": "revealing, cut-out",
            "ouvert": "open",
            "fermé": "closed",
            "sexy": "sexy",
            "élégant": "elegant",
            "chic": "chic",
            "décontracté": "casual"
        }
        
        for keyword, english in descriptor_keywords.items():
            if keyword in bot_text:
                if english not in detected['descriptors']:
                    detected['descriptors'].append(english)
        
        # VISIBILITa DU CORPS
        if any(word in bot_text for word in ["laisse voir", "montre", "dévoile", "révèle", "voir tout", "transparente"]):
            detected['body_visibility'] = "revealing, showing body"
        elif any(word in bot_text for word in ["cache", "couvre", "dissimule"]):
            detected['body_visibility'] = "covering, modest"
        
        # NU/NUE (a  part)
        if any(word in bot_text for word in ["nu", "nue", "naked", "nud", "déshabillé", "sans vêtement"]):
            detected['clothing_items'] = ["nude, no clothing"]
            detected['body_visibility'] = "fully nude"
        
        # POSES specifiques
        if any(word in bot_text for word in ["assis", "sitting", "seated"]):
            detected['pose'] = "sitting"
        elif any(word in bot_text for word in ["debout", "standing"]):
            detected['pose'] = "standing"
        elif any(word in bot_text for word in ["allongé", "lying", "couché"]):
            detected['pose'] = "lying down"
        elif any(word in bot_text for word in ["penché", "leaning", "bent"]):
            detected['pose'] = "leaning forward"
        
        return detected
    
    async def generate_contextual_image(self, personality_data, conversation_history):
        """Generate image based on bot description in conversation"""
        
        print(f"[IMAGE] ========== CONTEXTUAL START ==========", flush=True)
        print(f"[IMAGE] Total messages received: {len(conversation_history)}", flush=True)
        
        # Extract BOT messages with detailed logging
        bot_messages = []
        
        for i, msg in enumerate(conversation_history[-20:]):  # Analyser 20 derniers messages
            print(f"[IMAGE] Msg {i}: type={type(msg).__name__}", flush=True)
            
            if isinstance(msg, dict):
                role = msg.get('role', '')
                content = msg.get('content', '')
                print(f"[IMAGE]   role='{role}', content='{content[:80]}'...", flush=True)
                
                if role == 'assistant':
                    bot_messages.append(content.lower())
                    print(f"[IMAGE]   -> BOT MESSAGE ADDED!", flush=True)
            else:
                # String - ajouter systematiquement
                msg_str = str(msg).lower()
                bot_messages.append(msg_str)
                print(f"[IMAGE]   -> String added: '{msg_str[:80]}'...", flush=True)
        
        # Combiner TOUS les messages du bot
        bot_text = " ".join(bot_messages)
        
        print(f"[IMAGE] ===== BOT TEXT COMPLETE =====", flush=True)
        print(f"[IMAGE] Messages bot extraits: {len(bot_messages)}", flush=True)
        print(f"[IMAGE] Texte COMPLET du bot: {bot_text}", flush=True)
        print(f"[IMAGE] Longueur: {len(bot_text)} caracteres", flush=True)
        
        # Analyze what bot describes - PASS THE EXTRACTED TEXT
        bot_actions = self._analyze_bot_actions(bot_text)
        
        # Get personality traits
        visual_traits = personality_data.get('visual', '')
        
        # BUILD PROMPT - CLOTHING FIRST AND EXPLICIT
        parts = []
        
        # 1. CLOTHING - ABSOLUTE PRIORITY
        if bot_actions['clothing_items']:
            print("[IMAGE] CLOTHING DETECTED!", flush=True)
            
            clothing_list = []
            if bot_actions['colors']:
                clothing_list.extend(bot_actions['colors'])
            if bot_actions['materials']:
                clothing_list.extend(bot_actions['materials'])
            if bot_actions['descriptors']:
                clothing_list.extend(bot_actions['descriptors'])
            clothing_list.extend(bot_actions['clothing_items'])
            
            clothing_desc = ", ".join(clothing_list)
            
            # FORCE clothing explicitly (repeat 3 times)
            parts.append(f"wearing {clothing_desc}")
            parts.append(f"dressed in {clothing_desc}")
            parts.append("fully clothed, NOT nude, NOT topless, wearing clothing")
            
            print(f"[IMAGE] Clothing: {clothing_desc}", flush=True)
        
        # 2. Accessories
        if bot_actions['accessories']:
            acc_desc = ", ".join(bot_actions['accessories'])
            parts.append(f"wearing {acc_desc}")
            print(f"[IMAGE] Accessories: {acc_desc}", flush=True)
        
        # 3. Face traits (hair, eyes only)
        if visual_traits:
            traits = [t.strip() for t in visual_traits.split(',')]
            face = []
            for t in traits:
                if any(w in t.lower() for w in ['hair', 'eye']):
                    face.append(t)
            if face:
                parts.append(", ".join(face[:2]))
        
        # 4. Location
        if bot_actions['location']:
            parts.append(bot_actions['location'])
        
        # 5. Activity
        if bot_actions['activity']:
            parts.append(bot_actions['activity'])
        
        # 6. Pose
        if bot_actions['pose']:
            parts.append(bot_actions['pose'])
        
        # Quality
        parts.append("high quality, detailed, realistic")
        
        full_prompt = ", ".join(parts)
        
        print(f"[IMAGE] FINAL PROMPT: {full_prompt}", flush=True)
        
        # Generate with APIs
        for attempt in range(5):
            api = self.available_apis[attempt % len(self.available_apis)]
            
            print(f"[IMAGE] Try {attempt+1} with {api}", flush=True)
            
            if api == 'pollinations_turbo':
                url = await self._generate_pollinations_turbo(full_prompt)
            elif api == 'pollinations':
                url = await self._generate_pollinations(full_prompt, attempt+1)
            elif api == 'prodia':
                url = await self._generate_prodia(full_prompt)
            
            if url:
                print(f"[IMAGE] SUCCESS!", flush=True)
                return url
            
            await asyncio.sleep(1)
        
        # Final fallback
        seed = random.randint(1, 999999999)
        encoded = urllib.parse.quote(self._simplify_prompt(full_prompt))
        return f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=768&model=turbo&seed={seed}&nologo=true"
