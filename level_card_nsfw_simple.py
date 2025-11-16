"""
Générateur de cartes de level SIMPLE et RAPIDE avec gradient amélioré
Ne dépend PAS de la génération d'images externes pour être rapide
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import aiohttp
import io
import random
from typing import Tuple, Optional
import os
import math

class LevelCardGeneratorSimple:
    """Génère des cartes de level RAPIDES avec gradients améliorés"""
    
    def __init__(self):
        # Dimensions de la carte
        self.width = 900
        self.height = 300
        
        # Palettes de couleurs élargies
        self.color_palettes = [
            {"name": "Neon", "color1": (255, 0, 255), "color2": (0, 255, 255), "text": (255, 255, 255)},
            {"name": "Purple", "color1": (138, 43, 226), "color2": (186, 85, 211), "text": (255, 255, 255)},
            {"name": "Ocean", "color1": (0, 119, 182), "color2": (72, 202, 228), "text": (255, 255, 255)},
            {"name": "Fire", "color1": (220, 20, 60), "color2": (255, 140, 0), "text": (255, 255, 255)},
            {"name": "Emerald", "color1": (16, 185, 129), "color2": (110, 231, 183), "text": (255, 255, 255)},
            {"name": "Gold", "color1": (255, 215, 0), "color2": (255, 193, 37), "text": (0, 0, 0)},
            {"name": "Shadow", "color1": (106, 13, 173), "color2": (168, 85, 247), "text": (255, 255, 255)},
            {"name": "Sunset", "color1": (251, 146, 60), "color2": (244, 63, 94), "text": (255, 255, 255)},
            {"name": "Mint", "color1": (16, 185, 129), "color2": (6, 182, 212), "text": (255, 255, 255)},
            {"name": "Rose", "color1": (236, 72, 153), "color2": (219, 39, 119), "text": (255, 255, 255)}
        ]
    
    def get_random_palette(self, seed: Optional[int] = None):
        """Retourne une palette aléatoire"""
        if seed:
            random.seed(seed)
        return random.choice(self.color_palettes)
    
    def interpolate_color(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], ratio: float) -> Tuple[int, int, int]:
        """Interpole entre deux couleurs"""
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        return (r, g, b)
    
    def create_gradient_background(self, palette: dict, style: str = "diagonal") -> Image.Image:
        """Crée un fond avec gradient amélioré"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        if style == "diagonal":
            # Gradient diagonal
            for y in range(self.height):
                for x in range(self.width):
                    ratio = (x + y) / (self.width + self.height)
                    color = self.interpolate_color(palette["color1"], palette["color2"], ratio)
                    draw.point((x, y), fill=color)
        
        elif style == "radial":
            # Gradient radial
            center_x, center_y = self.width // 2, self.height // 2
            max_dist = math.sqrt(center_x**2 + center_y**2)
            
            for y in range(self.height):
                for x in range(self.width):
                    dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    ratio = min(dist / max_dist, 1.0)
                    color = self.interpolate_color(palette["color1"], palette["color2"], ratio)
                    draw.point((x, y), fill=color)
        
        else:
            # Gradient horizontal par défaut
            for x in range(self.width):
                ratio = x / self.width
                color = self.interpolate_color(palette["color1"], palette["color2"], ratio)
                draw.line([(x, 0), (x, self.height)], fill=color)
        
        # Ajouter du bruit pour texture
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        
        return img
    
    async def download_avatar(self, avatar_url: str) -> Optional[Image.Image]:
        """Télécharge l'avatar de l'utilisateur"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        img_data = await resp.read()
                        img = Image.open(io.BytesIO(img_data))
                        return img.convert('RGBA')
        except Exception as e:
            print(f"[ERROR] Téléchargement avatar: {e}")
        
        return None
    
    def create_circular_avatar(self, avatar: Image.Image, size: int = 150) -> Image.Image:
        """Crée un avatar circulaire avec bordure"""
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
        Génère une carte de level RAPIDE avec gradient amélioré
        """
        
        import time
        seed = user_id + int(time.time())
        
        # Choisir palette et style
        palette = self.get_random_palette(seed)
        styles = ["diagonal", "radial", "horizontal"]
        style = random.choice(styles)
        
        print(f"[DEBUG] Génération carte RAPIDE - Palette: {palette['name']}, Style: {style}")
        
        # Créer le fond avec gradient
        img = self.create_gradient_background(palette, style)
        img = img.convert('RGBA')
        
        # Overlay semi-transparent pour lisibilité
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 140))
        img = Image.alpha_composite(img, overlay)
        
        # Couche de dessin
        draw_layer = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(draw_layer)
        
        # Télécharger et ajouter l'avatar
        avatar = await self.download_avatar(avatar_url)
        if avatar:
            circular_avatar = self.create_circular_avatar(avatar, 180)
            
            # Bordure
            border_size = 190
            border = Image.new('RGBA', (border_size, border_size), (0, 0, 0, 0))
            border_draw = ImageDraw.Draw(border)
            border_draw.ellipse([0, 0, border_size, border_size], outline=palette["color2"], width=6)
            
            draw_layer.paste(border, (20, 60), border)
            draw_layer.paste(circular_avatar, (25, 65), circular_avatar)
        
        # Polices
        font_large = self.get_font(40)
        font_medium = self.get_font(28)
        font_small = self.get_font(20)
        
        # Textes
        text_x = 240
        
        # Nom d'utilisateur avec ombre
        draw.text((text_x + 2, 42), f"{username}#{discriminator}", font=font_large, fill=(0, 0, 0, 200))
        draw.text((text_x, 40), f"{username}#{discriminator}", font=font_large, fill=palette["text"])
        
        # Niveau et Rang
        draw.text((text_x, 100), f"Niveau {level}", font=font_medium, fill=palette["color2"])
        draw.text((text_x + 220, 100), f"Rang #{rank}", font=font_medium, fill=palette["color2"])
        
        # Stats
        draw.text((text_x, 145), f"Messages: {total_messages}", font=font_small, fill=palette["text"])
        
        # Barre de progression XP
        bar_x = text_x
        bar_y = 190
        bar_width = 600
        bar_height = 40
        
        # Fond de la barre
        draw.rounded_rectangle(
            [bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
            radius=20,
            fill=(0, 0, 0, 180)
        )
        
        # Progress
        progress_ratio = min(xp / xp_needed, 1.0) if xp_needed > 0 else 0
        progress_width = int((bar_width - 10) * progress_ratio)
        
        if progress_width > 0:
            # Gradient pour la barre
            for i in range(progress_width):
                ratio = i / progress_width
                color = self.interpolate_color(palette["color1"], palette["color2"], ratio)
                draw.line([(bar_x + 5 + i, bar_y + 5), (bar_x + 5 + i, bar_y + bar_height - 5)], fill=color, width=1)
        
        # Texte XP
        xp_text = f"{xp} / {xp_needed} XP"
        bbox = draw.textbbox((0, 0), xp_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_x_centered = bar_x + (bar_width - text_width) // 2
        
        draw.text((text_x_centered + 1, bar_y + 11), xp_text, font=font_small, fill=(0, 0, 0, 255))
        draw.text((text_x_centered, bar_y + 10), xp_text, font=font_small, fill=(255, 255, 255))
        
        # Pourcentage
        progress_text = f"{int(progress_ratio * 100)}%"
        draw.text((bar_x + bar_width + 15, bar_y + 10), progress_text, font=font_small, fill=palette["color2"])
        
        # Combiner les couches
        img = Image.alpha_composite(img, draw_layer)
        
        # Convertir en RGB
        final_img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        final_img.paste(img, (0, 0), img)
        
        # Sauvegarder
        output = io.BytesIO()
        final_img.save(output, format='PNG', quality=95)
        output.seek(0)
        
        print(f"[SUCCESS] Carte générée RAPIDEMENT - {palette['name']} / {style}")
        
        return output


# Instance globale
card_generator_simple = LevelCardGeneratorSimple()
