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
        
    async def generate_personality_image(self, personality_data, prompt_addition=""):
        """
        G?n?re une image bas?e sur la personnalit?
        
        Args:
            personality_data: Dictionnaire avec name, genre, age, description, visual
            prompt_addition: Texte additionnel pour le prompt
        
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
        
        # Essayer diff?rentes APIs (Pollinations en priorit? car gratuit)
        image_url = None
        
        # M?thode 1: Pollinations.ai (GRATUIT, sans cl? API, PRIORITAIRE)
        print(f"[IMAGE] Trying Pollinations.ai (free, unlimited)...", flush=True)
        image_url = await self._generate_pollinations(full_prompt)
        
        # M?thode 2: Replicate (backup si cl? configur?e)
        if not image_url and self.replicate_key:
            print(f"[IMAGE] Pollinations failed, trying Replicate...", flush=True)
            image_url = await self._generate_replicate(full_prompt)
        
        # M?thode 3: Hugging Face (backup si cl? configur?e)
        if not image_url and self.huggingface_key:
            print(f"[IMAGE] Replicate failed, trying Hugging Face...", flush=True)
            image_url = await self._generate_huggingface(full_prompt)
        
        return image_url
    
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
    
    async def _generate_pollinations(self, prompt):
        """G?n?re via Pollinations.ai (gratuit, sans cl? API)"""
        try:
            print(f"[IMAGE] Using Pollinations.ai FREE API", flush=True)
            
            # G?n?rer un seed VRAIMENT al?atoire pour ?viter images identiques
            random_seed = random.randint(1, 999999999) + int(time.time() * 1000)
            print(f"[IMAGE] Using random seed: {random_seed}", flush=True)
            
            # Encoder le prompt pour URL
            encoded_prompt = urllib.parse.quote(prompt)
            
            # Construire l'URL Pollinations (Flux model, haute qualit?, seed al?atoire)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=1024&model=flux&seed={random_seed}&nologo=true&enhance=true"
            
            print(f"[IMAGE] Pollinations.ai URL generated successfully", flush=True)
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
        
        # D?tecter le contexte NSFW/intime (termes subtils)
        if any(word in conversation_text for word in ["nue", "nu", "nud", "d?shabill", "sans v?tements", "corps", "montre", "voir"]):
            context_keywords.append("artistic nude, natural, revealing")
        
        if any(word in conversation_text for word in ["lit", "chambre", "bedroom", "bed"]):
            context_keywords.append("bedroom setting, intimate, on bed")
        
        if any(word in conversation_text for word in ["sexy", "hot", "sensuel", "?rotique", "excit", "belle"]):
            context_keywords.append("sexy, sensual pose, alluring")
        
        if any(word in conversation_text for word in ["lingerie", "sous-v?tements", "underwear", "d?shabille"]):
            context_keywords.append("wearing lingerie, revealing clothing")
        
        if any(word in conversation_text for word in ["position", "pose", "comme ?a", "ainsi"]):
            context_keywords.append("provocative pose, suggestive")
        
        if any(word in conversation_text for word in ["envie", "d?sir", "veux", "besoin"]):
            context_keywords.append("desire, wanting, passionate")
        
        if any(word in conversation_text for word in ["touche", "caresse", "embrasse", "l?che"]):
            context_keywords.append("intimate, sensual, romantic")
        
        # Construire le prompt contextuel
        name = personality_data.get('name', 'Person')
        genre = personality_data.get('genre', 'Neutre')
        age_num = ''.join(filter(str.isdigit, personality_data.get('age', '25')))
        visual_traits = personality_data.get('visual', '')
        
        base_prompt = self._build_base_prompt(genre, age_num, personality_data.get('description', ''), visual_traits)
        
        if context_keywords:
            context_str = ", ".join(context_keywords)
            full_prompt = f"{base_prompt}, {context_str}"
            print(f"[IMAGE] Contextual generation with keywords: {context_str}", flush=True)
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
