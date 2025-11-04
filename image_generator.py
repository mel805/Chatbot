"""
G?n?rateur d'images NSFW pour les personnalit?s du bot Discord
Utilise Stable Diffusion via API
"""

import aiohttp
import asyncio
import os
import json

class ImageGenerator:
    """G?n?re des images NSFW bas?es sur les personnalit?s"""
    
    def __init__(self):
        self.replicate_key = os.getenv('REPLICATE_API_KEY', '')
        self.huggingface_key = os.getenv('HUGGINGFACE_API_KEY', '')
        
    async def generate_personality_image(self, personality_data, prompt_addition=""):
        """
        G?n?re une image bas?e sur la personnalit?
        
        Args:
            personality_data: Dictionnaire avec name, genre, age, description
            prompt_addition: Texte additionnel pour le prompt (ex: "in lingerie", "nude")
        
        Returns:
            URL de l'image ou None si erreur
        """
        
        # Construire le prompt bas? sur la personnalit?
        name = personality_data.get('name', 'Person')
        genre = personality_data.get('genre', 'Neutre')
        age = personality_data.get('age', '25 ans')
        description = personality_data.get('description', '')
        
        # Extraire l'?ge num?rique
        age_num = ''.join(filter(str.isdigit, age))
        
        # Construire le prompt Stable Diffusion
        base_prompt = self._build_base_prompt(genre, age_num, description)
        full_prompt = f"{base_prompt}, {prompt_addition}" if prompt_addition else base_prompt
        
        # Prompt n?gatif pour meilleure qualit?
        negative_prompt = "ugly, deformed, disfigured, bad anatomy, bad proportions, blurry, low quality, worst quality, watermark, text"
        
        print(f"[IMAGE] Generating image with prompt: {full_prompt[:100]}...", flush=True)
        
        # Essayer diff?rentes APIs
        image_url = None
        
        # M?thode 1: Replicate (Stable Diffusion)
        if self.replicate_key:
            image_url = await self._generate_replicate(full_prompt, negative_prompt)
        
        # M?thode 2: Hugging Face (backup)
        if not image_url and self.huggingface_key:
            image_url = await self._generate_huggingface(full_prompt, negative_prompt)
        
        # M?thode 3: API publique (backup backup)
        if not image_url:
            image_url = await self._generate_public_api(full_prompt, negative_prompt)
        
        return image_url
    
    def _build_base_prompt(self, genre, age, description):
        """Construit le prompt de base selon la personnalit?"""
        
        # Mapper genre vers descripteurs
        gender_map = {
            "Femme": "beautiful woman, female, feminine",
            "Homme": "handsome man, male, masculine",
            "Trans": "beautiful transgender person, androgynous",
            "Non-binaire": "androgynous person, non-binary",
            "Neutre": "attractive person"
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
            traits.append("playful, mischievous")
        
        traits_str = ", ".join(traits) if traits else "attractive"
        
        # Prompt complet
        prompt = f"high quality portrait, {gender_desc}, {age} years old, {traits_str}, realistic, detailed face, professional photography, cinematic lighting, 8k uhd"
        
        return prompt
    
    async def _generate_replicate(self, prompt, negative_prompt):
        """G?n?re via Replicate API (Stable Diffusion)"""
        try:
            headers = {
                "Authorization": f"Token {self.replicate_key}",
                "Content-Type": "application/json"
            }
            
            # Utiliser SDXL (meilleur mod?le)
            data = {
                "version": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                "input": {
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "width": 768,
                    "height": 1024,
                    "num_outputs": 1,
                    "guidance_scale": 7.5,
                    "num_inference_steps": 30
                }
            }
            
            async with aiohttp.ClientSession() as session:
                # Cr?er la pr?diction
                async with session.post(
                    "https://api.replicate.com/v1/predictions",
                    headers=headers,
                    json=data
                ) as resp:
                    if resp.status == 201:
                        result = await resp.json()
                        prediction_url = result.get('urls', {}).get('get')
                        
                        # Attendre que l'image soit pr?te (max 60s)
                        for _ in range(30):
                            await asyncio.sleep(2)
                            async with session.get(prediction_url, headers=headers) as check_resp:
                                check_result = await check_resp.json()
                                status = check_result.get('status')
                                
                                if status == 'succeeded':
                                    output = check_result.get('output', [])
                                    if output:
                                        print(f"[IMAGE] Replicate generation succeeded", flush=True)
                                        return output[0]
                                elif status == 'failed':
                                    print(f"[IMAGE] Replicate generation failed", flush=True)
                                    return None
                    
                    print(f"[IMAGE] Replicate API error: {resp.status}", flush=True)
                    return None
        except Exception as e:
            print(f"[ERROR] Replicate generation error: {e}", flush=True)
            return None
    
    async def _generate_huggingface(self, prompt, negative_prompt):
        """G?n?re via Hugging Face Inference API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.huggingface_key}",
                "Content-Type": "application/json"
            }
            
            # Utiliser Stable Diffusion 2.1
            api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
            
            data = {
                "inputs": prompt,
                "negative_prompt": negative_prompt,
                "width": 512,
                "height": 768
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, headers=headers, json=data) as resp:
                    if resp.status == 200:
                        # HF retourne l'image en binaire
                        image_bytes = await resp.read()
                        # On devrait uploader ?a quelque part et retourner l'URL
                        # Pour l'instant, on retourne None (? impl?menter)
                        print(f"[IMAGE] HuggingFace generation succeeded (needs upload)", flush=True)
                        return None  # TODO: Upload image et retourner URL
                    else:
                        print(f"[IMAGE] HuggingFace API error: {resp.status}", flush=True)
                        return None
        except Exception as e:
            print(f"[ERROR] HuggingFace generation error: {e}", flush=True)
            return None
    
    async def _generate_public_api(self, prompt, negative_prompt):
        """G?n?re via API publique (backup)"""
        # Pour l'instant, retourner None
        # On pourrait utiliser une API publique comme Pollinations.ai
        print(f"[IMAGE] No public API configured yet", flush=True)
        return None
    
    def get_personality_prompts(self, personality_key):
        """
        Retourne des prompts sugg?r?s pour une personnalit?
        
        Returns:
            Liste de tuples (label, prompt_addition)
        """
        
        base_prompts = [
            ("Portrait", "portrait, face focus, beautiful lighting"),
            ("Tenue D?contract?e", "casual outfit, relaxed pose"),
            ("Tenue ?l?gante", "elegant dress, formal attire"),
            ("Lingerie", "lingerie, sensual pose, bedroom"),
            ("Maillot de Bain", "swimsuit, beach setting"),
        ]
        
        nsfw_prompts = [
            ("Suggestif", "suggestive pose, intimate setting, artistic nude"),
            ("Artistique Nu", "artistic nude, tasteful, professional photography"),
            ("Intime", "intimate scene, bedroom, soft lighting, nsfw"),
        ]
        
        # Retourner tous les prompts
        return base_prompts + nsfw_prompts
