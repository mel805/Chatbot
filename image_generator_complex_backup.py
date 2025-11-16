"""
Générateur d'images NSFW ultra-performant avec STYLES VARIÉS et EXPLICITES
Utilise Prodia (gratuit, rapide) et Stable Horde (communautaire, NSFW)
VERSION AMÉLIORÉE avec centaines de variations
"""

import os
import aiohttp
import asyncio
from typing import Optional, Dict
import base64
from io import BytesIO
import time

class ImageGeneratorNSFW:
    """Générateur d'images NSFW avec STYLES VRAIMENT VARIÉS et EXPLICITES"""
    
    def __init__(self, provider: str = "multi"):
        self.provider = provider
        
        # Catégories NSFW TRÈS DÉTAILLÉES avec styles explicites
        self.nsfw_categories = {
            "softcore": [
                "sensual tease", "elegant lingerie", "artistic boudoir", 
                "glamour photography", "soft erotic", "implied nude",
                "silk and lace", "morning after aesthetic", "intimate portrait",
                "sensual curves", "teasing glimpse", "romantic undress"
            ],
            "romantic": [
                "passionate lovers embrace", "intimate kissing scene", 
                "romantic candlelit bedroom", "tender caress", "loving touch",
                "sensual couple", "passionate encounter", "intimate connection",
                "romantic undressing", "lovers entwined", "tender intimacy",
                "passionate bedroom scene", "romantic lovemaking", "gentle passion"
            ],
            "intense": [
                "explicit sexual act", "intense pleasure expression", "dominant pose",
                "submissive position", "erotic bondage", "explicit penetration",
                "intense orgasm face", "rough passion", "explicit oral",
                "hardcore sex scene", "intense fucking", "explicit intercourse",
                "wild sexual encounter", "explicit doggy style", "rough sex",
                "explicit missionary", "explicit cowgirl", "explicit blowjob"
            ],
            "fantasy": [
                "magical seduction", "fantasy creature sex", "elf maiden nude",
                "demon succubus", "mythical beast mating", "magical pleasure",
                "fantasy orgy", "dragon rider nude", "witch ritual sex",
                "fantasy harem", "magical tentacles", "fairy seduction",
                "mermaid temptation", "vampire feeding sexually", "fantasy bondage"
            ],
            "artistic": [
                "fine art nude", "classical nude painting", "renaissance nude",
                "artistic erotic photography", "sensual art study", "nude life drawing",
                "erotic sculpture pose", "artistic body worship", "fine art erotica",
                "museum quality nude", "artistic sensuality", "classical eroticism"
            ],
            "fetish": [
                "latex outfit", "leather bondage", "high heels fetish",
                "foot worship", "stockings and garters", "corset fetish",
                "bdsm scene", "rope bondage", "collar and leash",
                "dominatrix pose", "submissive slave", "fetish wear",
                "rubber suit", "pet play", "master and slave"
            ],
            "group": [
                "threesome scene", "lesbian couple", "orgy scene",
                "multiple partners", "group sex", "gangbang",
                "bisexual threeway", "lesbian orgy", "foursome",
                "group pleasure", "multiple penetration", "lesbian passion"
            ],
            "extreme": [
                "anal sex", "double penetration", "extreme insertion",
                "fisting", "gaping", "extreme stretching",
                "bukkake", "creampie", "cum covered",
                "extreme pleasure", "ahegao expression", "fucked silly"
            ]
        }
        
        # Styles visuels TRÈS VARIÉS (50+)
        self.visual_styles = [
            # Photography styles
            "cinematic film photography", "studio flash photography", "natural window light",
            "dramatic noir lighting", "soft diffused light", "golden hour lighting",
            "harsh direct sunlight", "neon lighting", "candlelight photography",
            "backlit silhouette", "rim lighting", "chiaroscuro lighting",
            
            # Camera styles
            "vintage polaroid", "film grain aesthetic", "digital photography",
            "professional DSLR", "smartphone aesthetic", "instant camera look",
            "35mm film", "medium format", "large format photography",
            
            # Artistic styles
            "oil painting style", "watercolor painting", "digital painting",
            "charcoal sketch", "pencil drawing", "ink illustration",
            "renaissance art", "baroque painting", "impressionist style",
            "art nouveau", "pop art style", "hyperrealistic painting",
            
            # Modern styles
            "anime style", "manga aesthetic", "western cartoon style",
            "CGI render", "3D realistic render", "unreal engine render",
            "octane render", "ray tracing", "photorealistic CGI",
            
            # Effects
            "bokeh background", "shallow depth of field", "tilt-shift effect",
            "long exposure", "motion blur", "lens flare",
            "vignette effect", "color grading", "high contrast",
            "desaturated", "vibrant colors", "muted tones"
        ]
        
        # Poses NSFW explicites
        self.poses = [
            # Casual/Soft
            "lying seductively", "sitting provocatively", "standing nude",
            "kneeling position", "on all fours", "bent over pose",
            
            # Sexual positions
            "missionary position", "doggy style position", "cowgirl position",
            "reverse cowgirl", "spooning position", "standing sex pose",
            "sitting on lap", "legs spread wide", "lifted leg position",
            
            # Submissive
            "tied up pose", "restrained position", "on knees submissively",
            "collar and leash", "bound hands", "helpless position",
            
            # Dominant
            "dominant stance", "sitting on face", "riding position",
            "pinning down", "controlling position", "power pose",
            
            # Explicit
            "explicit spread", "presenting pussy", "ass up pose",
            "masturbating pose", "oral sex position", "penetration pose",
            "orgasm position", "cumming pose", "pleasure expression"
        ]
        
        # Angles de caméra
        self.camera_angles = [
            "POV first person view", "from above looking down", "from below looking up",
            "side profile view", "rear view", "frontal view",
            "close-up intimate shot", "extreme close-up", "wide shot full body",
            "dutch angle", "over the shoulder", "through legs view",
            "between breasts view", "ass focus", "pussy focus",
            "face focus", "full body shot", "torso focus"
        ]
        
        # Corps et caractéristiques NSFW
        self.body_features = [
            # Body types
            "petite body", "curvy figure", "athletic body", "thick thighs",
            "slim waist", "hourglass figure", "busty", "small breasts",
            "huge tits", "perfect ass", "bubble butt", "toned body",
            
            # Explicit features
            "visible nipples", "hard nipples", "puffy nipples", "large areolas",
            "shaved pussy", "hairy pussy", "wet pussy", "glistening skin",
            "visible labia", "pussy lips", "tight asshole", "spread legs",
            
            # States
            "sweaty skin", "flushed skin", "aroused state", "dripping wet",
            "cum covered", "creampie dripping", "orgasm face", "pleasure expression"
        ]
        
        # Vêtements et lingerie
        self.clothing = [
            "completely nude", "fully naked", "topless", "bottomless",
            "sheer lingerie", "lace lingerie", "silk lingerie", "leather lingerie",
            "fishnet stockings", "thigh high stockings", "garter belt", "corset",
            "see-through outfit", "micro bikini", "torn clothes", "clothes pulled aside",
            "latex catsuit", "leather straps", "bondage harness", "collar",
            "high heels only", "wearing only jewelry", "partially clothed"
        ]
        
        # Actions NSFW explicites
        self.actions = [
            # Solo
            "masturbating", "fingering herself", "using dildo", "using vibrator",
            "touching herself", "playing with breasts", "spreading pussy", "spreading ass",
            
            # Partner
            "giving blowjob", "deepthroat", "licking cock", "sucking dick",
            "getting fucked", "riding cock", "getting pounded", "taking cock",
            "pussy licking", "eating pussy", "fingering partner", "handjob",
            
            # Cum/Fluids
            "cumming", "squirting", "dripping cum", "covered in cum",
            "cum on face", "cum on tits", "cum in mouth", "cum inside",
            
            # Intense
            "getting railed", "rough fucking", "hard pounding", "deep penetration",
            "anal sex", "ass fucking", "double penetration", "gangbang action"
        ]
        
        # Ambiances NSFW
        self.moods = [
            "sensual", "seductive", "lustful", "passionate", "intense desire",
            "playful tease", "innocent corruption", "confident sexuality",
            "submissive obedience", "dominant control", "raw passion",
            "forbidden pleasure", "wild abandon", "erotic tension",
            "intimate vulnerability", "carnal hunger", "sexual ecstasy",
            "dirty desire", "naughty intentions", "pure lust"
        ]
        
        # Settings/Lieux détaillés
        self.settings = [
            # Indoor luxury
            "luxury penthouse bedroom", "five star hotel suite", "private villa bedroom",
            "mansion master bedroom", "silk sheets bed", "canopy bed",
            
            # Indoor casual  
            "college dorm room", "apartment bedroom", "cozy cabin interior",
            "living room couch", "kitchen counter", "bathroom shower",
            
            # Exotic
            "tropical beach paradise", "private island", "yacht deck",
            "mountain hot spring", "japanese onsen", "luxury spa",
            
            # Public/Risky
            "secluded forest", "hidden beach cove", "rooftop terrace",
            "private pool", "gym locker room", "office after hours",
            
            # Fantasy/Special
            "dungeon chamber", "throne room", "magical realm",
            "fantasy castle", "elven grove", "demon realm",
            
            # Studio/Artistic
            "photography studio", "art studio", "red room",
            "bdsm dungeon", "strip club private room", "brothel bedroom"
        ]
        
        # Éclairage NSFW spécifique
        self.lighting = [
            "soft candlelight", "neon club lighting", "red room lighting",
            "natural sunrise light", "moonlight through window", "fairy lights",
            "dramatic spotlight", "colored gel lighting", "blacklight",
            "dim mood lighting", "harsh interrogation light", "soft diffused glow"
        ]
        
        # APIs gratuites pour images NSFW
        self.image_apis = [
            {
                "name": "Prodia",
                "url": "https://api.prodia.com/v1/sd/generate",
                "status_url": "https://api.prodia.com/v1/job/",
                "type": "prodia",
                "free": True,
                "nsfw": True,
                "speed": "fast",
                "priority": 1
            },
            {
                "name": "Stable-Horde",
                "url": "https://stablehorde.net/api/v2/generate/async",
                "status_url": "https://stablehorde.net/api/v2/generate/status/",
                "type": "horde",
                "free": True,
                "nsfw": True,
                "speed": "medium",
                "priority": 2
            },
            {
                "name": "Pollinations-NSFW",
                "url": "https://image.pollinations.ai/prompt/",
                "type": "pollinations",
                "free": True,
                "nsfw": True,
                "speed": "very_fast",
                "priority": 1
            }
        ]
        
        # Modèles NSFW recommandés
        self.nsfw_models = {
            "prodia": [
                "dreamshaper_8.safetensors [879db523c3]",
                "deliberate_v2.safetensors [10ec4b29]",
                "revAnimated_v122.safetensors [3f4fefd9]"
            ],
            "horde": [
                "Deliberate",
                "DreamShaper",
                "Anything V5"
            ]
        }
        
        # Clés API
        self.prodia_key = os.getenv('PRODIA_API_KEY', '0000000000')
        self.horde_key = os.getenv('HORDE_API_KEY', '0000000000')
    
    def _get_random_elements(self, seed: Optional[int] = None):
        """Obtient des éléments aléatoires TRÈS VARIÉS pour la variation"""
        import random
        if seed:
            random.seed(seed)
        
        return {
            "style": random.choice(self.visual_styles),
            "mood": random.choice(self.moods),
            "setting": random.choice(self.settings),
            "pose": random.choice(self.poses),
            "angle": random.choice(self.camera_angles),
            "body": random.choice(self.body_features),
            "clothing": random.choice(self.clothing),
            "action": random.choice(self.actions) if random.random() > 0.5 else None,
            "lighting": random.choice(self.lighting)
        }
    
    def _enhance_prompt_nsfw(
        self, 
        prompt: str, 
        character_desc: str = "",
        server_name: str = "",
        username: str = "",
        nsfw_type: str = "artistic",
        add_variation: bool = True
    ) -> str:
        """Améliore le prompt pour NSFW de qualité avec BEAUCOUP de variations"""
        import random
        import hashlib
        
        # Créer un seed unique basé sur serveur + user + timestamp
        seed_string = f"{server_name}_{username}_{int(time.time())}"
        seed = int(hashlib.md5(seed_string.encode()).hexdigest(), 16) % (10**8)
        
        # Obtenir des éléments aléatoires basés sur le seed
        elements = self._get_random_elements(seed)
        
        # Choisir un style NSFW selon la catégorie
        category_styles = self.nsfw_categories.get(nsfw_type, self.nsfw_categories["artistic"])
        nsfw_style = random.choice(category_styles)
        
        # Construire le prompt personnalisé DÉTAILLÉ
        prompt_parts = []
        
        # Base prompt
        if prompt:
            prompt_parts.append(prompt)
        
        # Description du personnage
        if character_desc:
            prompt_parts.append(character_desc[:100])
        
        # Style NSFW explicite
        prompt_parts.append(nsfw_style)
        
        # Éléments de variation si demandés
        if add_variation:
            # Pose
            prompt_parts.append(elements["pose"])
            
            # Corps
            prompt_parts.append(elements["body"])
            
            # Vêtements/Nudité
            prompt_parts.append(elements["clothing"])
            
            # Action (optionnelle)
            if elements["action"]:
                prompt_parts.append(elements["action"])
            
            # Ambiance
            prompt_parts.append(elements["mood"])
            
            # Lieu
            prompt_parts.append(f"in {elements['setting']}")
            
            # Angle caméra
            prompt_parts.append(elements["angle"])
            
            # Éclairage
            prompt_parts.append(elements["lighting"])
            
            # Style visuel
            prompt_parts.append(elements["style"])
        
        # Tags de qualité
        quality_tags = "masterpiece, best quality, highly detailed, 8k, professional photography, ultra realistic"
        prompt_parts.append(quality_tags)
        
        # Personnalisation serveur (subtile)
        if server_name:
            server_theme = f"themed after {server_name}"
            prompt_parts.append(server_theme)
        
        # Construire le prompt final
        full_prompt = ", ".join(filter(None, prompt_parts))
        
        # Nettoyer
        full_prompt = full_prompt.strip(", ")
        
        print(f"[DEBUG] Prompt NSFW DÉTAILLÉ généré - Seed: {seed}")
        print(f"[DEBUG] Style NSFW: {nsfw_style}")
        print(f"[DEBUG] Pose: {elements['pose']}")
        print(f"[DEBUG] Action: {elements['action']}")
        print(f"[DEBUG] Body: {elements['body']}")
        print(f"[DEBUG] Clothing: {elements['clothing']}")
        print(f"[DEBUG] Setting: {elements['setting']}")
        print(f"[DEBUG] Angle: {elements['angle']}")
        print(f"[DEBUG] Lighting: {elements['lighting']}")
        print(f"[DEBUG] Visual Style: {elements['style']}")
        
        return full_prompt
    
    def _get_negative_prompt_nsfw(self) -> str:
        """Negative prompt pour éviter les indésirables"""
        return (
            "child, minor, kid, young, underage, teen, loli, shota, "
            "ugly, deformed, bad anatomy, bad proportions, blurry, "
            "low quality, low res, watermark, text, signature, "
            "mutated, disfigured, disgusting, error"
        )
    
    async def generate_prodia(
        self,
        prompt: str,
        character_desc: str = "",
        negative_prompt: str = "",
        server_name: str = "",
        username: str = "",
        nsfw_type: str = "artistic"
    ) -> Optional[str]:
        """Génère une image avec Prodia (rapide, gratuit, NSFW)"""
        
        try:
            enhanced_prompt = self._enhance_prompt_nsfw(
                prompt, character_desc, server_name, username, nsfw_type
            )
            
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
                    "steps": 30,
                    "cfg_scale": 7,
                    "seed": -1,
                    "upscale": False,
                    "sampler": "DPM++ 2M Karras",
                    "width": 512,
                    "height": 768
                }
                
                print(f"[DEBUG] Prodia - Génération avec prompt détaillé...")
                start_time = time.time()
                
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
        negative_prompt: str = "",
        server_name: str = "",
        username: str = "",
        nsfw_type: str = "artistic"
    ) -> Optional[str]:
        """Génère avec Stable Horde (gratuit, communautaire, NSFW)"""
        
        try:
            enhanced_prompt = self._enhance_prompt_nsfw(
                prompt, character_desc, server_name, username, nsfw_type
            )
            
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
                        "steps": 30,
                        "n": 1
                    },
                    "nsfw": True,
                    "trusted_workers": True,
                    "models": self.nsfw_models["horde"],
                    "r2": True,
                    "shared": False,
                    "replacement_filter": False
                }
                
                if negative_prompt:
                    payload["params"]["negative_prompt"] = negative_prompt
                
                print(f"[DEBUG] Stable Horde - Génération...")
                start_time = time.time()
                
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
        character_desc: str = "",
        server_name: str = "",
        username: str = "",
        nsfw_type: str = "artistic"
    ) -> Optional[str]:
        """Génère avec Pollinations (très rapide, NSFW possible)"""
        
        try:
            enhanced_prompt = self._enhance_prompt_nsfw(
                prompt, character_desc, server_name, username, nsfw_type
            )
            
            import urllib.parse
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=768&nologo=true&enhance=true"
            
            print(f"[SUCCESS] Pollinations: URL générée avec prompt détaillé")
            return image_url
                        
        except Exception as e:
            print(f"[ERROR] Pollinations: {str(e)}")
            return None
    
    async def generate(
        self,
        prompt: str,
        character_desc: str = "",
        negative_prompt: str = "",
        server_name: str = "",
        username: str = "",
        nsfw_type: str = "artistic",
        prefer_speed: bool = True
    ) -> Optional[str]:
        """Méthode principale - Génère une image VRAIMENT UNIQUE et VARIÉE"""
        
        print(f"[DEBUG] Génération image NSFW ULTRA VARIÉE...")
        print(f"[DEBUG] Serveur: {server_name} | User: {username} | Type: {nsfw_type}")
        
        if prefer_speed:
            print("[DEBUG] Essai Pollinations (instant)...")
            result = await self.generate_pollinations(
                prompt, character_desc, server_name, username, nsfw_type
            )
            if result:
                return result
        
        print("[DEBUG] Essai Prodia (10-20s)...")
        result = await self.generate_prodia(
            prompt, character_desc, negative_prompt, server_name, username, nsfw_type
        )
        if result:
            return result
        
        print("[DEBUG] Fallback Stable Horde (30-60s)...")
        result = await self.generate_horde(
            prompt, character_desc, negative_prompt, server_name, username, nsfw_type
        )
        if result:
            return result
        
        print("[ERROR] Toutes les APIs image ont échoué")
        return None


# Instance globale
image_generator = ImageGeneratorNSFW(provider="multi")
