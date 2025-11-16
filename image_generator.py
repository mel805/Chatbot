"""
Générateur d'images NSFW SIMPLE et FONCTIONNEL
Version simplifiée qui fonctionne vraiment
"""

import urllib.parse
import hashlib
import time
import random

class ImageGeneratorSimple:
    """Générateur d'images NSFW simple via Pollinations"""
    
    def __init__(self):
        # Prompts NSFW simples et efficaces
        self.nsfw_prompts = {
            "softcore": [
                "beautiful woman in lingerie",
                "sexy model in bedroom",
                "sensual woman posing",
                "girl in underwear"
            ],
            "romantic": [
                "romantic couple intimate",
                "lovers kissing passionately",
                "intimate bedroom scene",
                "couple in bed"
            ],
            "intense": [
                "explicit sex scene",
                "hardcore porn",
                "naked couple fucking",
                "explicit intercourse"
            ],
            "fantasy": [
                "fantasy elf nude",
                "demon succubus sexy",
                "fairy princess naked",
                "fantasy creature sex"
            ],
            "artistic": [
                "nude art photography",
                "artistic naked woman",
                "erotic fine art",
                "nude portrait"
            ],
            "fetish": [
                "latex outfit bdsm",
                "bondage scene",
                "dominatrix leather",
                "tied up rope"
            ],
            "group": [
                "threesome sex",
                "lesbian couple",
                "orgy scene",
                "multiple partners"
            ],
            "extreme": [
                "anal sex",
                "double penetration",
                "extreme porn",
                "hardcore fucking"
            ]
        }
    
    def generate_url(
        self,
        prompt: str,
        nsfw_type: str = "artistic",
        server_name: str = "",
        username: str = ""
    ) -> str:
        """Génère une URL Pollinations directe"""
        
        # Créer seed unique
        seed_string = f"{server_name}_{username}_{int(time.time())}"
        seed = int(hashlib.md5(seed_string.encode()).hexdigest(), 16) % (10**8)
        
        # Choisir un style NSFW aléatoire
        random.seed(seed)
        nsfw_styles = self.nsfw_prompts.get(nsfw_type, self.nsfw_prompts["artistic"])
        nsfw_style = random.choice(nsfw_styles)
        
        # Construire prompt simple
        full_prompt = f"{prompt}, {nsfw_style}, 8k, high quality, detailed"
        
        # Encoder
        encoded_prompt = urllib.parse.quote(full_prompt)
        
        # URL Pollinations
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=768&nologo=true&seed={seed}&enhance=true&model=flux"
        
        print(f"[DEBUG] Génération image NSFW simple")
        print(f"[DEBUG] Prompt: {full_prompt[:100]}")
        print(f"[DEBUG] URL: {image_url[:150]}...")
        
        return image_url
    
    async def generate(
        self,
        prompt: str,
        character_desc: str = "",
        negative_prompt: str = "",
        server_name: str = "",
        username: str = "",
        nsfw_type: str = "artistic",
        prefer_speed: bool = True
    ) -> str:
        """Génère une URL d'image (toujours retourne une URL)"""
        
        print(f"[DEBUG] Génération image NSFW")
        print(f"[DEBUG] Type: {nsfw_type}, User: {username}")
        
        # Générer l'URL directement
        url = self.generate_url(prompt, nsfw_type, server_name, username)
        
        print(f"[SUCCESS] URL générée")
        
        return url


# Instance globale
image_generator = ImageGeneratorSimple()
