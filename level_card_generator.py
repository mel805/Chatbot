"""
Générateur de cartes de level uniques et personnalisées
Chaque carte a un design différent avec couleurs, gradients et styles variés
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import aiohttp
import io
import random
from typing import Tuple, Optional
import os
import math

class LevelCardGenerator:
    """Génère des cartes de level visuelles uniques pour chaque membre"""
    
    def __init__(self):
        # Dimensions de la carte
        self.width = 900
        self.height = 300
        
        # Palettes de couleurs variées
        self.color_palettes = [
            # Neon Cyberpunk
            {
                "name": "Neon",
                "primary": (255, 0, 255),
                "secondary": (0, 255, 255),
                "accent": (255, 51, 255),
                "text": (255, 255, 255),
                "bg_start": (20, 0, 40),
                "bg_end": (0, 40, 60)
            },
            # Purple Dream
            {
                "name": "Purple",
                "primary": (138, 43, 226),
                "secondary": (186, 85, 211),
                "accent": (218, 112, 214),
                "text": (255, 255, 255),
                "bg_start": (25, 0, 51),
                "bg_end": (75, 0, 130)
            },
            # Ocean Blue
            {
                "name": "Ocean",
                "primary": (0, 119, 182),
                "secondary": (0, 180, 216),
                "accent": (72, 202, 228),
                "text": (255, 255, 255),
                "bg_start": (0, 51, 102),
                "bg_end": (0, 102, 153)
            },
            # Fire Red
            {
                "name": "Fire",
                "primary": (220, 20, 60),
                "secondary": (255, 69, 0),
                "accent": (255, 140, 0),
                "text": (255, 255, 255),
                "bg_start": (51, 0, 0),
                "bg_end": (102, 51, 0)
            },
            # Emerald Green
            {
                "name": "Emerald",
                "primary": (16, 185, 129),
                "secondary": (52, 211, 153),
                "accent": (110, 231, 183),
                "text": (255, 255, 255),
                "bg_start": (4, 47, 46),
                "bg_end": (6, 78, 59)
            },
            # Gold Luxury
            {
                "name": "Gold",
                "primary": (255, 215, 0),
                "secondary": (255, 193, 37),
                "accent": (255, 235, 59),
                "text": (0, 0, 0),
                "bg_start": (51, 51, 0),
                "bg_end": (102, 76, 0)
            },
            # Dark Purple
            {
                "name": "Shadow",
                "primary": (106, 13, 173),
                "secondary": (147, 51, 234),
                "accent": (168, 85, 247),
                "text": (255, 255, 255),
                "bg_start": (17, 24, 39),
                "bg_end": (55, 48, 163)
            },
            # Sunset
            {
                "name": "Sunset",
                "primary": (251, 146, 60),
                "secondary": (251, 113, 133),
                "accent": (244, 63, 94),
                "text": (255, 255, 255),
                "bg_start": (51, 26, 0),
                "bg_end": (76, 29, 76)
            }
        ]
        
        # Styles de design
        self.design_styles = [
            "gradient_diagonal",
            "gradient_radial",
            "gradient_horizontal",
            "geometric_pattern",
            "particle_effect",
            "wave_pattern"
        ]
    
    def get_random_palette(self, seed: Optional[int] = None):
        """Retourne une palette aléatoire (peut être seeded pour cohérence)"""
        if seed:
            random.seed(seed)
        return random.choice(self.color_palettes)
    
    def get_random_style(self, seed: Optional[int] = None):
        """Retourne un style aléatoire"""
        if seed:
            random.seed(seed)
        return random.choice(self.design_styles)
    
    def interpolate_color(
        self, 
        color1: Tuple[int, int, int], 
        color2: Tuple[int, int, int], 
        ratio: float
    ) -> Tuple[int, int, int]:
        """Interpole entre deux couleurs"""
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        return (r, g, b)
    
    def create_gradient_background(
        self, 
        palette: dict, 
        style: str = "gradient_diagonal"
    ) -> Image.Image:
        """Crée un fond avec gradient selon le style choisi"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        if style == "gradient_diagonal":
            # Gradient diagonal
            for i in range(self.height):
                ratio = i / self.height
                color = self.interpolate_color(palette["bg_start"], palette["bg_end"], ratio)
                draw.line([(0, i), (self.width, i)], fill=color)
        
        elif style == "gradient_horizontal":
            # Gradient horizontal
            for i in range(self.width):
                ratio = i / self.width
                color = self.interpolate_color(palette["bg_start"], palette["bg_end"], ratio)
                draw.line([(i, 0), (i, self.height)], fill=color)
        
        elif style == "gradient_radial":
            # Gradient radial
            center_x, center_y = self.width // 2, self.height // 2
            max_dist = math.sqrt(center_x**2 + center_y**2)
            
            for y in range(self.height):
                for x in range(self.width):
                    dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    ratio = min(dist / max_dist, 1.0)
                    color = self.interpolate_color(palette["bg_start"], palette["bg_end"], ratio)
                    draw.point((x, y), fill=color)
        
        elif style == "geometric_pattern":
            # Motif géométrique
            draw.rectangle([(0, 0), (self.width, self.height)], fill=palette["bg_start"])
            
            # Triangles décoratifs
            for i in range(5):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                size = random.randint(50, 150)
                opacity = random.randint(20, 60)
                
                color = palette["primary"]
                color_with_alpha = (*color, opacity)
                
                # Créer un triangle
                triangle = [
                    (x, y),
                    (x + size, y),
                    (x + size//2, y + size)
                ]
                
                overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.polygon(triangle, fill=color_with_alpha)
                
                img = img.convert('RGBA')
                img = Image.alpha_composite(img, overlay)
                img = img.convert('RGB')
        
        else:
            # Gradient par défaut
            for i in range(self.height):
                ratio = i / self.height
                color = self.interpolate_color(palette["bg_start"], palette["bg_end"], ratio)
                draw.line([(0, i), (self.width, i)], fill=color)
        
        # Ajouter un effet de bruit subtil
        return img.filter(ImageFilter.GaussianBlur(radius=1))
    
    def add_decorative_elements(
        self, 
        draw: ImageDraw.Draw, 
        palette: dict,
        style: str
    ):
        """Ajoute des éléments décoratifs selon le style"""
        
        if style == "particle_effect":
            # Particules aléatoires
            for _ in range(30):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                size = random.randint(2, 6)
                color = random.choice([palette["primary"], palette["secondary"], palette["accent"]])
                draw.ellipse([x, y, x+size, y+size], fill=color)
        
        elif style == "wave_pattern":
            # Lignes ondulées
            for i in range(3):
                y_offset = 50 + i * 80
                points = []
                for x in range(0, self.width, 10):
                    y = y_offset + math.sin(x / 50) * 20
                    points.append((x, y))
                
                if len(points) > 1:
                    draw.line(points, fill=palette["accent"], width=2)
    
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
        # Redimensionner
        avatar = avatar.resize((size, size), Image.Resampling.LANCZOS)
        
        # Créer un masque circulaire
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, size, size), fill=255)
        
        # Appliquer le masque
        output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        output.paste(avatar, (0, 0))
        output.putalpha(mask)
        
        return output
    
    def get_font(self, size: int):
        """Obtient une police (utilise une par défaut si besoin)"""
        try:
            # Essayer des polices système communes
            font_paths = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "C:\\Windows\\Fonts\\Arial.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, size)
            
            # Fallback
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
        user_id: int
    ) -> io.BytesIO:
        """
        Génère une carte de level unique
        Retourne un BytesIO de l'image PNG
        """
        
        # Utiliser user_id comme seed pour cohérence (mais changer à chaque appel avec timestamp)
        import time
        seed = user_id + int(time.time())
        
        # Choisir palette et style aléatoirement
        palette = self.get_random_palette(seed)
        style = self.get_random_style(seed)
        
        print(f"[DEBUG] Génération carte - Palette: {palette['name']}, Style: {style}")
        
        # Créer le fond
        img = self.create_gradient_background(palette, style)
        img = img.convert('RGBA')
        
        # Créer une couche de dessin
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Ajouter des éléments décoratifs
        self.add_decorative_elements(draw, palette, style)
        
        # Télécharger et ajouter l'avatar
        avatar = await self.download_avatar(avatar_url)
        if avatar:
            circular_avatar = self.create_circular_avatar(avatar, 150)
            
            # Ajouter bordure colorée à l'avatar
            border_size = 160
            border = Image.new('RGBA', (border_size, border_size), (0, 0, 0, 0))
            border_draw = ImageDraw.Draw(border)
            border_draw.ellipse(
                [0, 0, border_size, border_size], 
                outline=palette["primary"], 
                width=5
            )
            
            overlay.paste(border, (30, 75), border)
            overlay.paste(circular_avatar, (35, 80), circular_avatar)
        
        # Polices
        font_large = self.get_font(40)
        font_medium = self.get_font(28)
        font_small = self.get_font(20)
        
        # Textes
        text_x = 220
        
        # Nom d'utilisateur
        draw.text(
            (text_x, 40), 
            f"{username}#{discriminator}", 
            font=font_large, 
            fill=palette["text"]
        )
        
        # Niveau et Rank
        draw.text(
            (text_x, 100), 
            f"Niveau {level}", 
            font=font_medium, 
            fill=palette["primary"]
        )
        
        draw.text(
            (text_x + 200, 100), 
            f"Rang #{rank}", 
            font=font_medium, 
            fill=palette["secondary"]
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
            fill=(0, 0, 0, 100)
        )
        
        # Progress
        progress_ratio = min(xp / xp_needed, 1.0) if xp_needed > 0 else 0
        progress_width = int(bar_width * progress_ratio)
        
        if progress_width > 0:
            # Gradient pour la barre
            for i in range(progress_width):
                ratio = i / bar_width
                color = self.interpolate_color(palette["primary"], palette["secondary"], ratio)
                draw.line(
                    [(bar_x + i, bar_y + 5), (bar_x + i, bar_y + bar_height - 5)],
                    fill=color,
                    width=1
                )
        
        # Texte XP sur la barre
        xp_text = f"{xp} / {xp_needed} XP"
        # Centrer le texte
        bbox = draw.textbbox((0, 0), xp_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_x_centered = bar_x + (bar_width - text_width) // 2
        
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
        img = Image.alpha_composite(img, overlay)
        
        # Convertir en RGB pour PNG
        final_img = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        final_img.paste(img, (0, 0), img)
        
        # Sauvegarder dans BytesIO
        output = io.BytesIO()
        final_img.save(output, format='PNG', quality=95)
        output.seek(0)
        
        print(f"[SUCCESS] Carte générée - {palette['name']} / {style}")
        
        return output


# Instance globale
card_generator = LevelCardGenerator()
