"""
Générateur d'images NSFW ultra-performant
Utilise Prodia (gratuit, rapide) et Stable Horde (communautaire, NSFW)
"""

import os
import aiohttp
import asyncio
from typing import Optional, Dict
import base64
from io import BytesIO
import time

class ImageGeneratorNSFW:
    """Générateur d'images NSFW gratuit et rapide"""
    
    def __init__(self, provider: str = "multi"):
        self.provider = provider
        
        # APIs gratuites pour images NSFW
        self.image_apis = [
            {
                "name": "Prodia",
                "url": "https://api.prodia.com/v1/sd/generate",
                "status_url": "https://api.prodia.com/v1/job/",
                "type": "prodia",
                "free": True,
                "nsfw": True,
                "speed": "fast",  # 10-20s
                "priority": 1
            },
            {
                "name": "Stable-Horde",
                "url": "https://stablehorde.net/api/v2/generate/async",
                "status_url": "https://stablehorde.net/api/v2/generate/status/",
                "type": "horde",
                "free": True,
                "nsfw": True,
                "speed": "medium",  # 30-60s selon charge
                "priority": 2
            },
            {
                "name": "Pollinations-NSFW",
                "url": "https://image.pollinations.ai/prompt/",
                "type": "pollinations",
                "free": True,
                "nsfw": True,  # Contournement possible
                "speed": "very_fast",  # 2-5s
                "priority": 1
            }
        ]
        
        # Modèles NSFW recommandés
        self.nsfw_models = {
            "prodia": [
                "dreamshaper_8.safetensors [879db523c3]",  # Excellent NSFW
                "deliberate_v2.safetensors [10ec4b29]",    # Réaliste NSFW
                "revAnimated_v122.safetensors [3f4fefd9]"  # Anime NSFW
            ],
            "horde": [
                "Deliberate",
                "DreamShaper",
                "Anything V5"
            ]
        }
        
        # Clés API
        self.prodia_key = os.getenv('PRODIA_API_KEY', '0000000000')  # Key gratuite publique
        self.horde_key = os.getenv('HORDE_API_KEY', '0000000000')    # Anonymous
    
    def _enhance_prompt_nsfw(self, prompt: str, character_desc: str = "") -> str:
        """Améliore le prompt pour NSFW de qualité"""
        
        # Ajouter des qualifiers de qualité
        quality_tags = "masterpiece, best quality, highly detailed, 8k, photorealistic"
        
        # Construire le prompt complet
        full_prompt = f"{prompt}, {character_desc}, {quality_tags}"
        
        # Nettoyer
        full_prompt = full_prompt.strip(", ")
        
        return full_prompt
    
    def _get_negative_prompt_nsfw(self) -> str:
        """Negative prompt pour éviter les indésirables"""
        return (
            "child, minor, kid, young, underage, teen, loli, shota, "
            "ugly, deformed, bad anatomy, bad proportions, blurry, "
            "low quality, low res, watermark, text"
        )
    
    async def generate_prodia(
        self,
        prompt: str,
        character_desc: str = "",
        negative_prompt: str = ""
    ) -> Optional[str]:
        """Génère une image avec Prodia (rapide, gratuit, NSFW)"""
        
        try:
            enhanced_prompt = self._enhance_prompt_nsfw(prompt, character_desc)
            
            if not negative_prompt:
                negative_prompt = self._get_negative_prompt_nsfw()
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "X-Prodia-Key": self.prodia_key
                }
                
                payload = {
                    "model": self.nsfw_models["prodia"][0],
                    "prompt": enhanced_prompt,
                    "negative_prompt": negative_prompt,
                    "steps": 25,  # Plus rapide
                    "cfg_scale": 7,
                    "seed": -1,
                    "upscale": False,
                    "sampler": "DPM++ 2M Karras",
                    "width": 512,
                    "height": 768
                }
                
                print(f"[DEBUG] Prodia - Génération...")
                start_time = time.time()
                
                # Lancer la génération
                async with session.post(
                    self.image_apis[0]["url"],
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        job_id = data.get("job")
                        
                        if not job_id:
                            print("[ERROR] Prodia - Pas de job ID")
                            return None
                        
                        # Attendre la génération (poll toutes les 2s, max 30s)
                        for _ in range(15):
                            await asyncio.sleep(2)
                            
                            async with session.get(
                                f"{self.image_apis[0]['status_url']}{job_id}",
                                headers=headers
                            ) as status_response:
                                
                                if status_response.status == 200:
                                    status_data = await status_response.json()
                                    status_value = status_data.get("status")
                                    
                                    if status_value == "succeeded":
                                        image_url = status_data.get("imageUrl")
                                        elapsed = time.time() - start_time
                                        print(f"[SUCCESS] Prodia: Image générée en {elapsed:.1f}s")
                                        return image_url
                                    
                                    elif status_value == "failed":
                                        print("[ERROR] Prodia - Génération échouée")
                                        return None
                        
                        print("[TIMEOUT] Prodia - Temps dépassé")
                        return None
                    
                    else:
                        error_text = await response.text()
                        print(f"[ERROR] Prodia - {response.status}: {error_text[:100]}")
                        return None
                        
        except Exception as e:
            print(f"[ERROR] Prodia: {str(e)}")
            return None
    
    async def generate_horde(
        self,
        prompt: str,
        character_desc: str = "",
        negative_prompt: str = ""
    ) -> Optional[str]:
        """Génère avec Stable Horde (gratuit, communautaire, NSFW)"""
        
        try:
            enhanced_prompt = self._enhance_prompt_nsfw(prompt, character_desc)
            
            if not negative_prompt:
                negative_prompt = self._get_negative_prompt_nsfw()
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Content-Type": "application/json",
                    "apikey": self.horde_key
                }
                
                payload = {
                    "prompt": enhanced_prompt,
                    "params": {
                        "sampler_name": "k_euler_a",
                        "cfg_scale": 7,
                        "denoising_strength": 1.0,
                        "seed": "",
                        "height": 768,
                        "width": 512,
                        "karras": True,
                        "steps": 25,
                        "n": 1
                    },
                    "nsfw": True,  # Important!
                    "trusted_workers": True,
                    "models": self.nsfw_models["horde"],
                    "r2": True,  # Utiliser R2 storage
                    "shared": False,
                    "replacement_filter": False  # Désactiver filtre
                }
                
                if negative_prompt:
                    payload["params"]["negative_prompt"] = negative_prompt
                
                print(f"[DEBUG] Stable Horde - Génération...")
                start_time = time.time()
                
                # Lancer génération
                async with session.post(
                    self.image_apis[1]["url"],
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    
                    if response.status == 202:
                        data = await response.json()
                        job_id = data.get("id")
                        
                        if not job_id:
                            print("[ERROR] Horde - Pas de job ID")
                            return None
                        
                        # Poll pour résultat (max 60s)
                        for _ in range(30):
                            await asyncio.sleep(2)
                            
                            async with session.get(
                                f"{self.image_apis[1]['status_url']}{job_id}",
                                headers=headers
                            ) as status_response:
                                
                                if status_response.status == 200:
                                    status_data = await status_response.json()
                                    
                                    if status_data.get("done"):
                                        generations = status_data.get("generations", [])
                                        if generations:
                                            image_url = generations[0].get("img")
                                            elapsed = time.time() - start_time
                                            print(f"[SUCCESS] Horde: Image en {elapsed:.1f}s")
                                            return image_url
                        
                        print("[TIMEOUT] Horde - Temps dépassé")
                        return None
                    
                    else:
                        error_text = await response.text()
                        print(f"[ERROR] Horde - {response.status}: {error_text[:100]}")
                        return None
                        
        except Exception as e:
            print(f"[ERROR] Horde: {str(e)}")
            return None
    
    async def generate_pollinations(
        self,
        prompt: str,
        character_desc: str = ""
    ) -> Optional[str]:
        """Génère avec Pollinations (très rapide, NSFW possible)"""
        
        try:
            enhanced_prompt = self._enhance_prompt_nsfw(prompt, character_desc)
            
            # Encoder le prompt pour URL
            import urllib.parse
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            
            # URL directe
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=768&nologo=true&enhance=true"
            
            print(f"[SUCCESS] Pollinations: URL générée instantanément")
            return image_url
                        
        except Exception as e:
            print(f"[ERROR] Pollinations: {str(e)}")
            return None
    
    async def generate(
        self,
        prompt: str,
        character_desc: str = "",
        negative_prompt: str = "",
        prefer_speed: bool = True
    ) -> Optional[str]:
        """Méthode principale - Essaie les APIs par ordre de priorité"""
        
        print(f"[DEBUG] Génération image NSFW...")
        
        if prefer_speed:
            # Essayer Pollinations en premier (instant)
            print("[DEBUG] Essai Pollinations (instant)...")
            result = await self.generate_pollinations(prompt, character_desc)
            if result:
                return result
        
        # Essayer Prodia (rapide, qualité)
        print("[DEBUG] Essai Prodia (10-20s)...")
        result = await self.generate_prodia(prompt, character_desc, negative_prompt)
        if result:
            return result
        
        # Fallback sur Horde (plus lent mais fiable)
        print("[DEBUG] Fallback Stable Horde (30-60s)...")
        result = await self.generate_horde(prompt, character_desc, negative_prompt)
        if result:
            return result
        
        print("[ERROR] Toutes les APIs image ont échoué")
        return None


# Instance globale
image_generator = ImageGeneratorNSFW(provider="multi")
