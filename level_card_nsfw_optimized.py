"""
Générateur de cartes de level avec UNIQUEMENT des images NSFW en arrière-plan
Version optimisée pour rapidité
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import aiohttp
import io
import random
from typing import Tuple, Optional
import os
import urllib.parse
import hashlib
import time

class LevelCardNSFW:
    """Génère des cartes de level avec images NSFW UNIQUEMENT"""
    
    def __init__(self):
        # Dimensions de la carte
        self.width = 900
        self.height = 300
        
        # Couleurs pour overlays et texte
        self.text_colors = [
            (255, 255, 255),  # Blanc
            (255, 215, 0),    # Or
            (0, 255, 255),    # Cyan
            (255, 105, 180),  # Rose vif
        ]
        
        # Prompts NSFW très variés pour les cartes
        self.nsfw_prompts = [
            # Softcore/Lingerie
            "beautiful woman in elegant lingerie, boudoir photography, sensual pose, soft lighting",
            "gorgeous model in lace lingerie, professional photoshoot, seductive, glamour",
            "sensual woman in silk lingerie, bedroom setting, intimate portrait, artistic",
            "sexy lingerie model, provocative pose, studio photography, high fashion",
            
            # Nude Art
            "artistic nude woman, classical pose, soft lighting, fine art photography, elegant",
            "nude art photography, beautiful curves, sensual aesthetic, professional",
            "artistic nude portrait, natural beauty, soft focus, museum quality",
            "nude woman aesthetic photography, elegant pose, artistic lighting, tasteful",
            
            # Erotic/Sensual
            "erotic photography, beautiful naked woman, seductive pose, intimate atmosphere",
            "sensual nude woman, erotic art, passionate expression, professional photography",
            "seductive woman topless, intimate moment, artistic photography, sensual mood",
            "erotic art photography, nude beauty, provocative yet tasteful, high quality",
            
            # Boudoir
            "boudoir photography, woman in sexy lingerie, bedroom scene, intimate lighting",
            "sensual boudoir shoot, beautiful woman, seductive outfit, soft natural light",
            "intimate boudoir photography, nude silhouette, romantic atmosphere, professional",
            
            # Fantasy/Artistic
            "fantasy nude art, beautiful goddess, ethereal lighting, artistic photography",
            "nude woman in artistic setting, creative photography, sensual and elegant",
            "artistic erotic photography, nude beauty, fantasy aesthetic, high art quality",
            
            # Explicit but artistic
            "nude woman showing curves, explicit but artistic, professional photography, sensual",
            "erotic nude photography, woman with perfect body, seductive pose, tasteful explicit"
        ]
    
    def get_random_prompt(self, seed: Optional[int] = None):
        """Retourne un prompt NSFW aléatoire"""
        if seed:
            random.seed(seed)
        return random.choice(self.nsfw_prompts)
    
    def get_random_text_color(self, seed: Optional[int] = None):
        """Retourne une couleur de texte aléatoire"""
        if seed:
            random.seed(seed + 1000)  # Offset pour varier
        return random.choice(self.text_colors)
    
    async def generate_nsfw_background(
        self, 
        prompt: str,
        server_name: str,
        username: str,
        seed: int
    ) -> Optional[Image.Image]:
        """Génère directement une image NSFW via Pollinations (rapide)"""
        try:
            print(f"[DEBUG] Génération image NSFW pour carte...")
            
            # Améliorer le prompt
            enhanced_prompt = f"{prompt}, 8k, professional photography, masterpiece, highly detailed"
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            
            # URL Pollinations directe avec seed unique
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=900&height=300&nologo=true&seed={seed}&enhance=true"
            
            print(f"[DEBUG] URL: {image_url[:100]}...")
            
            # Télécharger avec timeout court
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        img_data = await resp.read()
                        img = Image.open(io.BytesIO(img_data))
                        print(f"[SUCCESS] Image NSFW téléchargée: {img.size}")
                        return img.convert('RGB')
                    else:
                        print(f"[ERROR] Status {resp.status}")
                        return None
        
        except Exception as e:
            print(f"[ERROR] Génération image NSFW: {e}")
            return None
    
    def process_nsfw_background(self, nsfw_image: Image.Image) -> Image.Image:
        """Traite l'image NSFW pour la carte"""
        try:
            img = nsfw_image.copy()
            
            # Si l'image n'est pas aux bonnes dimensions, redimensionner
            if img.size != (self.width, self.height):
                # Calculer le ratio
                ratio_w = self.width / img.width
                ratio_h = self.height / img.height
                ratio = max(ratio_w, ratio_h)
                
                # Redimensionner
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Recadrer au centre
                left = (img.width - self.width) // 2
                top = (img.height - self.height) // 2
                img = img.crop((left, top, left + self.width, top + self.height))
            
            # Appliquer un blur léger
            img = img.filter(ImageFilter.GaussianBlur(radius=2))
            
            # Assombrir pour lisibilité du texte
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.55)
            
            print("[SUCCESS] Image NSFW traitée pour carte")
            return img
            
        except Exception as e:
            print(f"[ERROR] Traitement image: {e}")
            raise
    
    async def download_avatar(self, avatar_url: str) -> Optional[Image.Image]:
        """Télécharge l'avatar"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        img_data = await resp.read()
                        return Image.open(io.BytesIO(img_data)).convert('RGBA')
        except Exception as e:
            print(f"[ERROR] Avatar: {e}")
        return None
    
    def create_circular_avatar(self, avatar: Image.Image, size: int = 150) -> Image.Image:
        """Avatar circulaire"""
        avatar = avatar.resize((size, size), Image.Resampling.LANCZOS)
        
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, size, size), fill=255)
        
        output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        output.paste(avatar, (0, 0))
        output.putalpha(mask)
        
        return output
    
    def get_font(self, size: int):
        """Obtient une police"""
        try:
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "C:\\Windows\\Fonts\\Arial.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, size)
            
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()
    
    async def generate_card(
        self,
        username: str,
        discriminator: str,
        avatar_url: str,
        level: int,
        xp: int,
        xp_needed: int,
        rank: int,
        total_messages: int,
        user_id: int,
        server_name: str = "Discord"
    ) -> io.BytesIO:
        """
        Génère une carte de level avec IMAGE NSFW UNIQUEMENT
        """
        
        # Créer seed unique
        seed = int(hashlib.md5(f"{server_name}_{username}_{user_id}_{int(time.time())}".encode()).hexdigest(), 16) % (10**8)
        
        # Choisir prompt et couleur
        nsfw_prompt = self.get_random_prompt(seed)
        text_color = self.get_random_text_color(seed)
        
        print(f"[DEBUG] Génération carte avec NSFW - Seed: {seed}")
        print(f"[DEBUG] Prompt: {nsfw_prompt[:80]}...")
        
        # Générer l'image NSFW (OBLIGATOIRE)
        nsfw_bg = await self.generate_nsfw_background(nsfw_prompt, server_name, username, seed)
        
        if not nsfw_bg:
            # Si échec, réessayer une fois avec un prompt plus simple
            print("[WARNING] Échec génération, nouvelle tentative...")
            simple_prompt = "beautiful nude woman, artistic photography, sensual"
            nsfw_bg = await self.generate_nsfw_background(simple_prompt, server_name, username, seed + 1)
            
            if not nsfw_bg:
                # Si échec total, créer une image noire avec message
                print("[ERROR] Impossible de générer image NSFW")
                img = Image.new('RGB', (self.width, self.height), (20, 20, 20))
                draw = ImageDraw.Draw(img)
                font = self.get_font(30)
                draw.text((self.width//2 - 200, self.height//2 - 15), 
                         "⚠️ Échec génération image NSFW", 
                         font=font, fill=(255, 100, 100))
                nsfw_bg = img
        
        # Traiter l'image NSFW
        img = self.process_nsfw_background(nsfw_bg)
        img = img.convert('RGBA')
        
        # Overlay semi-transparent pour lisibilité
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 130))
        img = Image.alpha_composite(img, overlay)
        
        # Couche de dessin
        draw_layer = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(draw_layer)
        
        # Avatar
        avatar = await self.download_avatar(avatar_url)
        if avatar:
            circular_avatar = self.create_circular_avatar(avatar, 180)
            
            # Bordure colorée
            border_size = 190
            border = Image.new('RGBA', (border_size, border_size), (0, 0, 0, 0))
            border_draw = ImageDraw.Draw(border)
            border_draw.ellipse([0, 0, border_size, border_size], outline=text_color, width=6)
            
            draw_layer.paste(border, (20, 60), border)
            draw_layer.paste(circular_avatar, (25, 65), circular_avatar)
        
        # Polices
        font_large = self.get_font(40)
        font_medium = self.get_font(28)
        font_small = self.get_font(20)
        
        # Textes
        text_x = 240
        
        # Nom avec ombre prononcée
        draw.text((text_x + 3, 43), f"{username}#{discriminator}", font=font_large, fill=(0, 0, 0, 255))
        draw.text((text_x, 40), f"{username}#{discriminator}", font=font_large, fill=(255, 255, 255))
        
        # Niveau et Rang
        draw.text((text_x, 100), f"Niveau {level}", font=font_medium, fill=text_color)
        draw.text((text_x + 220, 100), f"Rang #{rank}", font=font_medium, fill=text_color)
        
        # Stats
        draw.text((text_x, 145), f"Messages: {total_messages}", font=font_small, fill=(255, 255, 255))
        
        # Barre de progression XP
        bar_x = text_x
        bar_y = 190
        bar_width = 600
        bar_height = 40
        
        # Fond de la barre
        draw.rounded_rectangle(
            [bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
            radius=20,
            fill=(0, 0, 0, 200)
        )
        
        # Progress
        progress_ratio = min(xp / xp_needed, 1.0) if xp_needed > 0 else 0
        progress_width = int((bar_width - 10) * progress_ratio)
        
        if progress_width > 0:
            draw.rounded_rectangle(
                [bar_x + 5, bar_y + 5, bar_x + 5 + progress_width, bar_y + bar_height - 5],
                radius=17,
                fill=(*text_color, 255)
            )
        
        # Texte XP
        xp_text = f"{xp} / {xp_needed} XP"
        bbox = draw.textbbox((0, 0), xp_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_x_centered = bar_x + (bar_width - text_width) // 2
        
        # Ombre
        draw.text((text_x_centered + 2, bar_y + 12), xp_text, font=font_small, fill=(0, 0, 0, 255))
        draw.text((text_x_centered, bar_y + 10), xp_text, font=font_small, fill=(255, 255, 255))
        
        # Pourcentage
        progress_text = f"{int(progress_ratio * 100)}%"
        draw.text((bar_x + bar_width + 15, bar_y + 10), progress_text, font=font_small, fill=text_color)
        
        # Combiner
        img = Image.alpha_composite(img, draw_layer)
        
        # Convertir en RGB
        final_img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        final_img.paste(img, (0, 0), img)
        
        # Sauvegarder
        output = io.BytesIO()
        final_img.save(output, format='PNG', quality=95)
        output.seek(0)
        
        print(f"[SUCCESS] Carte avec IMAGE NSFW générée")
        
        return output


# Instance globale
card_generator_nsfw = LevelCardNSFW()
