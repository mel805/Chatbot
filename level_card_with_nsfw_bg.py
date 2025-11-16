"""
Générateur de cartes de level avec VRAIE IMAGE NSFW en arrière-plan
L'image est générée comme avec /generate_unique (serveur + membre)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import aiohttp
import io
from typing import Optional
import os
from image_generator import ImageGeneratorSimple

class LevelCardWithNSFW:
    """Génère des cartes de level avec vraie image NSFW générée"""
    
    def __init__(self):
        self.width = 900
        self.height = 300
        self.image_gen = ImageGeneratorSimple()
        
        # Prompts NSFW pour les cartes
        self.card_prompts = [
            "beautiful nude woman artistic pose",
            "sensual woman in lingerie bedroom",
            "erotic art photography glamour",
            "sexy model professional photoshoot",
            "nude artistic portrait elegant",
            "woman in sexy lingerie seductive",
            "boudoir photography intimate",
            "artistic nude soft lighting",
            "sensual curves photography",
            "erotic glamour professional",
        ]
    
    def get_card_prompt(self, user_id: int):
        """Choisit un prompt pour la carte"""
        import random
        import time
        random.seed(user_id + int(time.time()))
        return random.choice(self.card_prompts)
    
    async def download_image(self, url: str) -> Optional[Image.Image]:
        """Télécharge une image depuis une URL"""
        try:
            print(f"[DEBUG] Téléchargement image: {url[:100]}...")
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 200:
                        img_data = await resp.read()
                        img = Image.open(io.BytesIO(img_data))
                        print(f"[SUCCESS] Image téléchargée: {img.size}")
                        return img.convert('RGB')
                    else:
                        print(f"[ERROR] Status {resp.status}")
                        return None
        except Exception as e:
            print(f"[ERROR] Téléchargement image: {e}")
            return None
    
    def process_background(self, bg_image: Image.Image) -> Image.Image:
        """Traite l'image d'arrière-plan"""
        try:
            img = bg_image.copy()
            
            # Redimensionner pour remplir la carte
            ratio_w = self.width / img.width
            ratio_h = self.height / img.height
            ratio = max(ratio_w, ratio_h)
            
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Recadrer au centre
            left = (img.width - self.width) // 2
            top = (img.height - self.height) // 2
            img = img.crop((left, top, left + self.width, top + self.height))
            
            # Blur pour arrière-plan
            img = img.filter(ImageFilter.GaussianBlur(radius=3))
            
            # Assombrir pour lisibilité
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.5)
            
            print("[SUCCESS] Image traitée pour arrière-plan")
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
        """Crée un avatar circulaire"""
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
        Génère une carte avec VRAIE IMAGE NSFW générée
        """
        
        print(f"[DEBUG] Génération carte avec IMAGE NSFW pour {username} sur {server_name}")
        
        # 1. Générer l'URL de l'image NSFW
        card_prompt = self.get_card_prompt(user_id)
        print(f"[DEBUG] Prompt: {card_prompt}")
        
        image_url = self.image_gen.generate_url(
            prompt=card_prompt,
            nsfw_type="artistic",
            server_name=server_name,
            username=username
        )
        
        print(f"[DEBUG] URL générée: {image_url[:100]}...")
        
        # 2. Télécharger l'image
        bg_image = await self.download_image(image_url)
        
        if not bg_image:
            print("[WARNING] Échec téléchargement, création fond noir")
            bg_image = Image.new('RGB', (self.width, self.height), (20, 20, 20))
        
        # 3. Traiter l'image pour arrière-plan
        img = self.process_background(bg_image)
        img = img.convert('RGBA')
        
        # 4. Overlay semi-transparent
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 140))
        img = Image.alpha_composite(img, overlay)
        
        # 5. Créer couche de dessin
        draw = ImageDraw.Draw(img)
        
        # 6. Avatar
        avatar = await self.download_avatar(avatar_url)
        if avatar:
            circular_avatar = self.create_circular_avatar(avatar, 180)
            
            # Bordure
            border_size = 190
            border = Image.new('RGBA', (border_size, border_size), (0, 0, 0, 0))
            border_draw = ImageDraw.Draw(border)
            border_draw.ellipse([0, 0, border_size, border_size], outline=(255, 215, 0), width=6)
            
            img.paste(border, (20, 60), border)
            img.paste(circular_avatar, (25, 65), circular_avatar)
        
        # 7. Polices
        font_large = self.get_font(40)
        font_medium = self.get_font(28)
        font_small = self.get_font(20)
        
        # 8. Textes
        text_x = 240
        
        # Nom avec ombre
        draw.text((text_x + 3, 43), f"{username}#{discriminator}", font=font_large, fill=(0, 0, 0, 255))
        draw.text((text_x, 40), f"{username}#{discriminator}", font=font_large, fill=(255, 255, 255))
        
        # Niveau et Rang
        draw.text((text_x, 100), f"Niveau {level}", font=font_medium, fill=(255, 215, 0))
        draw.text((text_x + 220, 100), f"Rang #{rank}", font=font_medium, fill=(255, 215, 0))
        
        # Stats
        draw.text((text_x, 145), f"Messages: {total_messages}", font=font_small, fill=(255, 255, 255))
        
        # 9. Barre de progression XP
        bar_x = text_x
        bar_y = 190
        bar_width = 600
        bar_height = 40
        
        # Fond barre
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
                fill=(255, 215, 0, 255)
            )
        
        # Texte XP
        xp_text = f"{xp} / {xp_needed} XP"
        bbox = draw.textbbox((0, 0), xp_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_x_centered = bar_x + (bar_width - text_width) // 2
        
        draw.text((text_x_centered + 2, bar_y + 12), xp_text, font=font_small, fill=(0, 0, 0, 255))
        draw.text((text_x_centered, bar_y + 10), xp_text, font=font_small, fill=(255, 255, 255))
        
        # Pourcentage
        progress_text = f"{int(progress_ratio * 100)}%"
        draw.text((bar_x + bar_width + 15, bar_y + 10), progress_text, font=font_small, fill=(255, 215, 0))
        
        # 10. Convertir et sauvegarder
        final_img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        final_img.paste(img, (0, 0), img)
        
        output = io.BytesIO()
        final_img.save(output, format='PNG', quality=95)
        output.seek(0)
        
        print(f"[SUCCESS] Carte avec IMAGE NSFW générée")
        
        return output


# Instance globale
card_generator_nsfw_bg = LevelCardWithNSFW()
