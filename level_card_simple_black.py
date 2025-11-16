"""
Générateur de cartes de level avec FOND NOIR SIMPLE
Rapide et fiable
"""

from PIL import Image, ImageDraw, ImageFont
import aiohttp
import io
from typing import Optional
import os

class LevelCardBlack:
    """Génère des cartes de level avec fond noir simple"""
    
    def __init__(self):
        self.width = 900
        self.height = 300
        
        # Couleurs d'accent
        self.accent_colors = [
            (255, 0, 255),    # Magenta
            (0, 255, 255),    # Cyan
            (255, 215, 0),    # Or
            (255, 105, 180),  # Rose
            (138, 43, 226),   # Violet
            (0, 255, 127),    # Vert spring
        ]
    
    def get_accent_color(self, user_id: int):
        """Retourne une couleur d'accent basée sur l'user_id"""
        import time
        seed = user_id + int(time.time())
        import random
        random.seed(seed)
        return random.choice(self.accent_colors)
    
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
        Génère une carte avec FOND NOIR simple
        """
        
        print(f"[DEBUG] Génération carte avec fond noir simple")
        
        # Créer image avec fond noir
        img = Image.new('RGB', (self.width, self.height), (15, 15, 15))
        img = img.convert('RGBA')
        
        # Couche de dessin
        draw = ImageDraw.Draw(img)
        
        # Choisir couleur d'accent
        accent_color = self.get_accent_color(user_id)
        
        # Avatar
        avatar = await self.download_avatar(avatar_url)
        if avatar:
            circular_avatar = self.create_circular_avatar(avatar, 180)
            
            # Bordure colorée
            border_size = 190
            border = Image.new('RGBA', (border_size, border_size), (0, 0, 0, 0))
            border_draw = ImageDraw.Draw(border)
            border_draw.ellipse([0, 0, border_size, border_size], outline=accent_color, width=6)
            
            # Coller sur l'image
            img.paste(border, (20, 60), border)
            img.paste(circular_avatar, (25, 65), circular_avatar)
        
        # Polices
        font_large = self.get_font(40)
        font_medium = self.get_font(28)
        font_small = self.get_font(20)
        
        # Textes
        text_x = 240
        
        # Nom avec ombre
        draw.text((text_x + 2, 42), f"{username}#{discriminator}", font=font_large, fill=(0, 0, 0, 255))
        draw.text((text_x, 40), f"{username}#{discriminator}", font=font_large, fill=(255, 255, 255))
        
        # Niveau et Rang
        draw.text((text_x, 100), f"Niveau {level}", font=font_medium, fill=accent_color)
        draw.text((text_x + 220, 100), f"Rang #{rank}", font=font_medium, fill=accent_color)
        
        # Stats
        draw.text((text_x, 145), f"Messages: {total_messages}", font=font_small, fill=(200, 200, 200))
        
        # Barre de progression XP
        bar_x = text_x
        bar_y = 190
        bar_width = 600
        bar_height = 40
        
        # Fond de la barre (gris foncé)
        draw.rounded_rectangle(
            [bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
            radius=20,
            fill=(40, 40, 40)
        )
        
        # Progress
        progress_ratio = min(xp / xp_needed, 1.0) if xp_needed > 0 else 0
        progress_width = int((bar_width - 10) * progress_ratio)
        
        if progress_width > 0:
            draw.rounded_rectangle(
                [bar_x + 5, bar_y + 5, bar_x + 5 + progress_width, bar_y + bar_height - 5],
                radius=17,
                fill=accent_color
            )
        
        # Texte XP
        xp_text = f"{xp} / {xp_needed} XP"
        bbox = draw.textbbox((0, 0), xp_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_x_centered = bar_x + (bar_width - text_width) // 2
        
        draw.text((text_x_centered + 1, bar_y + 11), xp_text, font=font_small, fill=(0, 0, 0, 255))
        draw.text((text_x_centered, bar_y + 10), xp_text, font=font_small, fill=(255, 255, 255))
        
        # Pourcentage
        progress_text = f"{int(progress_ratio * 100)}%"
        draw.text((bar_x + bar_width + 15, bar_y + 10), progress_text, font=font_small, fill=accent_color)
        
        # Convertir en RGB
        final_img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        final_img.paste(img, (0, 0), img)
        
        # Sauvegarder
        output = io.BytesIO()
        final_img.save(output, format='PNG', quality=95)
        output.seek(0)
        
        print(f"[SUCCESS] Carte générée avec fond noir")
        
        return output


# Instance globale
card_generator_black = LevelCardBlack()
