"""
Module pour la g?n?ration d'images NSFW
Ce module peut ?tre int?gr? avec diff?rentes APIs de g?n?ration d'images
"""

import os
import aiohttp
import asyncio
from typing import Optional, Dict
import base64
from io import BytesIO

class ImageGenerator:
    """Classe pour g?rer la g?n?ration d'images NSFW"""
    
    def __init__(self, provider: str = "stability"):
        """
        Initialise le g?n?rateur d'images
        
        Args:
            provider: Le fournisseur ('stability', 'dalle', 'local')
        """
        self.provider = provider
        self.api_key = self._get_api_key()
        
    def _get_api_key(self) -> Optional[str]:
        """R?cup?re la cl? API selon le fournisseur"""
        if self.provider == "stability":
            return os.getenv('STABILITY_API_KEY')
        elif self.provider == "dalle":
            return os.getenv('OPENAI_API_KEY')
        return None
    
    def _enhance_prompt_for_safety(self, prompt: str) -> str:
        """
        Am?liore le prompt pour s'assurer qu'il respecte les r?gles
        
        Args:
            prompt: Le prompt original
            
        Returns:
            Le prompt modifi? avec des garde-fous
        """
        # Mots-cl?s interdits (? personnaliser selon vos besoins)
        forbidden_keywords = [
            'child', 'minor', 'kid', 'young', 'underage', 'teen',
            'school', 'student', 'loli', 'shota', 'baby', 'infant',
            'enfant', 'mineur', 'jeune', 'ado', 'adolescent', '?cole'
        ]
        
        # V?rifier les mots interdits (case-insensitive)
        prompt_lower = prompt.lower()
        for keyword in forbidden_keywords:
            if keyword in prompt_lower:
                raise ValueError(f"Contenu interdit d?tect?: '{keyword}'. G?n?ration refus?e.")
        
        # Ajouter des qualificatifs de s?curit? au prompt
        safe_additions = "adult, 18+, mature, consensual"
        enhanced_prompt = f"{prompt}, {safe_additions}"
        
        return enhanced_prompt
    
    async def generate_with_stability(self, prompt: str, negative_prompt: str = None) -> Optional[bytes]:
        """
        G?n?re une image avec Stable Diffusion via Stability AI
        
        Args:
            prompt: Description de l'image ? g?n?rer
            negative_prompt: Ce qu'on ne veut PAS dans l'image
            
        Returns:
            Les bytes de l'image g?n?r?e ou None en cas d'erreur
        """
        if not self.api_key:
            raise ValueError("Cl? API Stability AI non configur?e.")
        
        try:
            # S?curiser le prompt
            safe_prompt = self._enhance_prompt_for_safety(prompt)
            
            # Prompt n?gatif par d?faut pour la s?curit?
            default_negative = "child, minor, young, underage, kid, baby, infant, teen, adolescent, school, student"
            if negative_prompt:
                negative_prompt = f"{negative_prompt}, {default_negative}"
            else:
                negative_prompt = default_negative
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "Accept": "image/png"
                }
                
                payload = {
                    "text_prompts": [
                        {
                            "text": safe_prompt,
                            "weight": 1
                        },
                        {
                            "text": negative_prompt,
                            "weight": -1
                        }
                    ],
                    "cfg_scale": 7,
                    "height": 512,
                    "width": 512,
                    "samples": 1,
                    "steps": 30,
                    "style_preset": "enhance"
                }
                
                # API endpoint pour SDXL 1.0
                url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
                
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Stability AI retourne l'image en base64
                        image_base64 = data['artifacts'][0]['base64']
                        image_bytes = base64.b64decode(image_base64)
                        return image_bytes
                    else:
                        error_text = await response.text()
                        raise Exception(f"Erreur Stability AI ({response.status}): {error_text}")
                        
        except ValueError as e:
            # Erreur de s?curit?
            raise e
        except Exception as e:
            raise Exception(f"Erreur lors de la g?n?ration: {str(e)}")
    
    async def generate_with_dalle(self, prompt: str) -> Optional[str]:
        """
        G?n?re une image avec DALL-E (OpenAI)
        Note: DALL-E a des restrictions strictes sur le contenu NSFW
        
        Args:
            prompt: Description de l'image
            
        Returns:
            URL de l'image g?n?r?e ou None en cas d'erreur
        """
        if not self.api_key:
            raise ValueError("Cl? API OpenAI non configur?e.")
        
        try:
            # DALL-E refuse le contenu NSFW explicite
            # Il faudrait utiliser des termes artistiques et subtils
            safe_prompt = self._enhance_prompt_for_safety(prompt)
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "dall-e-3",
                    "prompt": safe_prompt,
                    "n": 1,
                    "size": "1024x1024",
                    "quality": "standard"
                }
                
                async with session.post(
                    "https://api.openai.com/v1/images/generations",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        image_url = data['data'][0]['url']
                        return image_url
                    else:
                        error_text = await response.text()
                        raise Exception(f"Erreur DALL-E ({response.status}): {error_text}")
                        
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Erreur lors de la g?n?ration: {str(e)}")
    
    async def generate(self, prompt: str, negative_prompt: str = None) -> Dict:
        """
        G?n?re une image (m?thode principale)
        
        Args:
            prompt: Description de l'image
            negative_prompt: Ce qu'on ne veut PAS (seulement pour Stability)
            
        Returns:
            Dict avec 'type' ('bytes' ou 'url') et 'data'
        """
        if self.provider == "stability":
            image_bytes = await self.generate_with_stability(prompt, negative_prompt)
            return {"type": "bytes", "data": image_bytes}
        elif self.provider == "dalle":
            image_url = await self.generate_with_dalle(prompt)
            return {"type": "url", "data": image_url}
        else:
            raise ValueError(f"Provider non support?: {self.provider}")


# Instance globale
image_generator = ImageGenerator(provider="stability")  # ou "dalle"
