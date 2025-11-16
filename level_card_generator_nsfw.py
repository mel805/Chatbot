"""
Générateur de cartes de level avec IMAGES NSFW en arrière-plan
Chaque carte a une image NSFW unique générée en arrière-plan
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import aiohttp
import io
import random
from typing import Tuple, Optional
import os
import math

class LevelCardGeneratorNSFW:
    """Génère des cartes de level avec images NSFW en arrière-plan"""
    
    def __init__(self):
        # Dimensions de la carte
        self.width = 900
        self.height = 300
        
        # Palettes de couleurs pour les overlays
        self.color_palettes = [
            {"name": "Neon", "overlay": (255, 0, 255, 180), "text": (255, 255, 255), "accent": (0, 255, 255)},
            {"name": "Purple", "overlay": (138, 43, 226, 180), "text": (255, 255, 255), "accent": (218, 112, 214)},
            {"name": "Ocean", "overlay": (0, 119, 182, 180), "text": (255, 255, 255), "accent": (72, 202, 228)},
            {"name": "Fire", "overlay": (220, 20, 60, 180), "text": (255, 255, 255), "accent": (255, 140, 0)},
            {"name": "Emerald", "overlay": (16, 185, 129, 180), "text": (255, 255, 255), "accent": (110, 231, 183)},
            {"name": "Gold", "overlay": (255, 215, 0, 180), "text": (0, 0, 0), "accent": (255, 235, 59)},
            {"name": "Shadow", "overlay": (106, 13, 173, 180), "text": (255, 255, 255), "accent": (168, 85, 247)},
            {"name": "Sunset", "overlay": (251, 146, 60, 180), "text": (255, 255, 255), "accent": (244, 63, 94)}
        ]
        
        # Prompts NSFW pour arrière-plans
        self.nsfw_bg_prompts = [
            "beautiful nude woman artistic pose",
            "sensual lingerie model elegant",
            "seductive woman bedroom aesthetic",
            "erotic art photography glamour",
            "nude artistic portrait soft lighting",
            "sensual curves artistic photography",
            "lingerie photoshoot professional",
            "boudoir photography elegant",
            "nude art renaissance style",
            "erotic glamour photography",
            "sensual portrait intimate",
            "artistic nude soft focus",
            "bedroom scene sensual aesthetic",
            "nude woman artistic lighting",
            "erotic portrait photography"
        ]
    
    def get_random_palette(self, seed: Optional[int] = None):
        """Retourne une palette aléatoire"""
        if seed:
            random.seed(seed)
        return random.choice(self.color_palettes)
    
    def get_random_nsfw_prompt(self, seed: Optional[int] = None):
        """Retourne un prompt NSFW aléatoire"""
        if seed:
            random.seed(seed)
        return random.choice(self.nsfw_bg_prompts)
    
    async def download_nsfw_background(
        self, 
        prompt: str,
        server_name: str,
        username: str
    ) -> Optional[Image.Image]:
        """Télécharge une image NSFW pour l'arrière-plan"""
        try:
            # Importer le générateur d'images
            from image_generator import image_generator
            
            print(f"[DEBUG] Génération image NSFW pour arrière-plan de carte...")
            
            # Générer l'image NSFW
            image_url = await image_generator.generate(
                prompt=prompt,
                character_desc="",
                server_name=server_name,
                username=username,
                nsfw_type="artistic",  # Style artistique pour les cartes
                prefer_speed=True
            )
            
            if not image_url:
                print("[ERROR] Échec génération image NSFW")
                return None
            
            print(f"[DEBUG] Image générée, téléchargement: {image_url[:100]}")
            
            # Télécharger l'image
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status == 200:
                        img_data = await resp.read()
                        img = Image.open(io.BytesIO(img_data))
                        print(f"[SUCCESS] Image NSFW téléchargée: {img.size}")
                        return img.convert('RGB')
                    else:
                        print(f"[ERROR] Téléchargement échoué: {resp.status}")
                        return None
        
        except Exception as e:
            print(f"[ERROR] download_nsfw_background: {e}")
            return None
    
    def create_background_with_nsfw(
        self, 
        nsfw_image: Optional[Image.Image],
        palette: dict
    ) -> Image.Image:
        """Crée un fond avec image NSFW ou dégradé de fallback"""
        
        if nsfw_image:
            # Redimensionner et recadrer l'image NSFW
            img = nsfw_image.copy()
            
            # Calculer le ratio pour remplir la carte
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
            
            # Appliquer un blur léger pour l'arrière-plan
            img = img.filter(ImageFilter.GaussianBlur(radius=3))
            
            # Assombrir légèrement
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.6)
            
            print("[DEBUG] Image NSFW utilisée comme arrière-plan")
            return img
        
        else:
            # Fallback : gradient simple
            print("[DEBUG] Fallback sur gradient (pas d'image NSFW)")
            img = Image.new('RGB', (self.width, self.height))
            draw = ImageDraw.Draw(img)
            
            # Gradient simple
            for i in range(self.height):
                ratio = i / self.height
                r = int(palette["overlay"][0] * (1 - ratio * 0.5))
                g = int(palette["overlay"][1] * (1 - ratio * 0.5))
                b = int(palette["overlay"][2] * (1 - ratio * 0.5))
                draw.line([(0, i), (self.width, i)], fill=(r, g, b))
            
            return img
    
    async def download_avatar(self, avatar_url: str) -> Optional[Image.Image]:
        """Télécharge l'avatar de l'utilisateur"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(avatar_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
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
        Génère une carte de level avec image NSFW en arrière-plan
        """
        
        import time
        seed = user_id + int(time.time())
        
        # Choisir palette et prompt NSFW
        palette = self.get_random_palette(seed)
        nsfw_prompt = self.get_random_nsfw_prompt(seed)
        
        print(f"[DEBUG] Génération carte avec arrière-plan NSFW")
        print(f"[DEBUG] Palette: {palette['name']}, Prompt: {nsfw_prompt}")
        
        # Générer/télécharger l'image NSFW pour l'arrière-plan
        nsfw_bg = await self.download_nsfw_background(
            nsfw_prompt,
            server_name,
            username
        )
        
        # Créer le fond avec l'image NSFW
        img = self.create_background_with_nsfw(nsfw_bg, palette)
        img = img.convert('RGBA')
        
        # Créer overlay semi-transparent pour la lisibilité
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 120))
        img = Image.alpha_composite(img.convert('RGBA'), overlay)
        
        # Créer couche de dessin
        draw_layer = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(draw_layer)
        
        # Panel semi-transparent pour les infos
        panel_color = (*palette["overlay"][:3], 150)
        draw.rounded_rectangle(
            [200, 20, self.width - 20, self.height - 20],
            radius=15,
            fill=panel_color
        )
        
        # Télécharger et ajouter l'avatar
        avatar = await self.download_avatar(avatar_url)
        if avatar:
            circular_avatar = self.create_circular_avatar(avatar, 180)
            
            # Bordure
            border_size = 190
            border = Image.new('RGBA', (border_size, border_size), (0, 0, 0, 0))
            border_draw = ImageDraw.Draw(border)
            border_draw.ellipse(
                [0, 0, border_size, border_size], 
                outline=palette["accent"], 
                width=6
            )
            
            draw_layer.paste(border, (20, 60), border)
            draw_layer.paste(circular_avatar, (25, 65), circular_avatar)
        
        # Polices
        font_large = self.get_font(40)
        font_medium = self.get_font(28)
        font_small = self.get_font(20)
        
        # Textes
        text_x = 240
        
        # Nom d'utilisateur avec ombre
        shadow_offset = 2
        draw.text(
            (text_x + shadow_offset, 40 + shadow_offset), 
            f"{username}#{discriminator}", 
            font=font_large, 
            fill=(0, 0, 0, 200)
        )
        draw.text(
            (text_x, 40), 
            f"{username}#{discriminator}", 
            font=font_large, 
            fill=palette["text"]
        )
        
        # Niveau et Rang
        draw.text(
            (text_x, 100), 
            f"Niveau {level}", 
            font=font_medium, 
            fill=palette["accent"]
        )
        
        draw.text(
            (text_x + 220, 100), 
            f"Rang #{rank}", 
            font=font_medium, 
            fill=palette["accent"]
        )
        
        # Stats
        draw.text(
            (text_x, 145), 
            f"Messages: {total_messages}", 
            font=font_small, 
            fill=palette["text"]
        )
        
        # Barre de progression XP
        bar_x = text_x
        bar_y = 190
        bar_width = 600
        bar_height = 40
        
        # Fond de la barre
        draw.rounded_rectangle(
            [bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
            radius=20,
            fill=(0, 0, 0, 150)
        )
        
        # Progress
        progress_ratio = min(xp / xp_needed, 1.0) if xp_needed > 0 else 0
        progress_width = int((bar_width - 10) * progress_ratio)
        
        if progress_width > 0:
            draw.rounded_rectangle(
                [bar_x + 5, bar_y + 5, bar_x + 5 + progress_width, bar_y + bar_height - 5],
                radius=17,
                fill=palette["accent"]
            )
        
        # Texte XP centré
        xp_text = f"{xp} / {xp_needed} XP"
        bbox = draw.textbbox((0, 0), xp_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_x_centered = bar_x + (bar_width - text_width) // 2
        
        # Ombre pour lisibilité
        draw.text(
            (text_x_centered + 1, bar_y + 11),
            xp_text,
            font=font_small,
            fill=(0, 0, 0, 255)
        )
        draw.text(
            (text_x_centered, bar_y + 10),
            xp_text,
            font=font_small,
            fill=(255, 255, 255)
        )
        
        # Pourcentage
        progress_text = f"{int(progress_ratio * 100)}%"
        draw.text(
            (bar_x + bar_width + 15, bar_y + 10),
            progress_text,
            font=font_small,
            fill=palette["accent"]
        )
        
        # Combiner les couches
        img = Image.alpha_composite(img, draw_layer)
        
        # Convertir en RGB
        final_img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        final_img.paste(img, (0, 0), img)
        
        # Sauvegarder
        output = io.BytesIO()
        final_img.save(output, format='PNG', quality=95)
        output.seek(0)
        
        print(f"[SUCCESS] Carte générée avec arrière-plan NSFW - {palette['name']}")
        
        return output


# Instance globale
card_generator_nsfw = LevelCardGeneratorNSFW()
