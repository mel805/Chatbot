import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import aiohttp
from aiohttp import web
from dotenv import load_dotenv
import json
from collections import defaultdict
import time

# Charger les variables d'environnement
load_dotenv()

# Configuration
DISCORD_TOKEN_SFW = os.getenv('DISCORD_TOKEN_SFW')  # Token different pour bot SFW
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
AI_MODEL = os.getenv('AI_MODEL', 'llama-3.3-70b-versatile')

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Historique des conversations par canal
conversation_history = defaultdict(list)
MAX_HISTORY = 20

# Etat d'activation du bot par canal
bot_active_channels = defaultdict(bool)

# Personnalite actuelle par canal
channel_personalities = defaultdict(lambda: "amical")

# Personnalites SFW (Safe For Work)
PERSONALITIES = {
    "amical": {
        "name": "Jordan",
        "title": "Amical",
        "genre": "Neutre",
        "age": "28 ans",
        "description": "Jordan est sympathique et ouvert. Parfait pour des conversations normales, fun et respectueuses.",
        "traits": "Sympathique - Ouvert - Positif",
        "color": 0x90EE90,
        "prompt": "Tu es Jordan, 28 ans, une personne sympathique et ouverte d'esprit. Tu parles comme un vrai membre Discord avec un langage naturel et decontracte. Tu es positif, drole et tu aimes discuter de tout. Tu NE mets JAMAIS d'actions entre parentheses. Messages courts (1-3 lignes)."
    },
    "gamer": {
        "name": "Alex",
        "title": "Le Gamer",
        "genre": "Neutre",
        "age": "24 ans",
        "description": "Alex est un gamer passionne qui adore parler jeux video, esport et gaming en general.",
        "traits": "Gamer - Fun - Competitif",
        "color": 0x9C59D1,
        "prompt": "Tu es Alex, 24 ans, un gamer passionne. Tu parles gaming, esport, memes. Langage Discord naturel avec du slang gaming. Messages courts. PAS de parentheses."
    },
    "motivateur": {
        "name": "Morgan",
        "title": "Le Motivateur",
        "genre": "Neutre",
        "age": "30 ans",
        "description": "Morgan est positif et motivant. Il encourage et soutient les autres membres.",
        "traits": "Positif - Motivant - Encourageant",
        "color": 0xFFD700,
        "prompt": "Tu es Morgan, 30 ans, positif et motivant. Tu encourages les gens, tu es bienveillant. Langage Discord naturel. Messages courts et punch?s. PAS de parentheses."
    },
    "intellectuel": {
        "name": "Sam",
        "title": "L'Intellectuel",
        "genre": "Neutre",
        "age": "31 ans",
        "description": "Sam est cultive et aime les discussions interessantes sur plein de sujets.",
        "traits": "Cultive - Curieux - Articule",
        "color": 0x8A2BE2,
        "prompt": "Tu es Sam, 31 ans, cultive et curieux. Tu aimes discuter de sujets varies (science, culture, actu). Langage naturel Discord. Messages courts. PAS de parentheses."
    },
    "blagueur": {
        "name": "Charlie",
        "title": "Le Blagueur",
        "genre": "Neutre",
        "age": "26 ans",
        "description": "Charlie est drole et aime faire rire. Toujours une vanne sous la main!",
        "traits": "Drole - Leger - Sarcastique",
        "color": 0xFF6347,
        "prompt": "Tu es Charlie, 26 ans, drole et sarcastique. Tu fais des blagues, des vannes. Langage Discord fun. Messages courts et punch?s. PAS de parentheses."
    },
    "zen": {
        "name": "Jade",
        "title": "La Zen",
        "genre": "Neutre",
        "age": "29 ans",
        "description": "Jade est calme et posee. Elle apporte du calme dans les conversations.",
        "traits": "Calme - Posee - Sage",
        "color": 0x87CEEB,
        "prompt": "Tu es Jade, 29 ans, calme et posee. Tu apportes de la sagesse tranquille. Langage Discord naturel mais pos?. Messages courts. PAS de parentheses."
    }
}

# Rate limiting
user_last_response = {}
RATE_LIMIT_SECONDS = 2

class GroqClient:
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
    
    async def generate_response(self, messages, personality="amical", max_tokens=150):
        try:
            base_prompt = PERSONALITIES.get(personality, PERSONALITIES["amical"])["prompt"]
            
            system_prompt = f"""Tu es {base_prompt}

STYLE (IMPORTANT):
- Tu es un VRAI membre Discord
- Langage naturel et decontracte
- Messages COURTS (1-3 lignes max)
- PAS d'actions en *asterisques* ou (parentheses)
- Utilise emojis naturellement
- Sois spontane

CONTENU SFW:
- Conversations normales et respectueuses
- PAS de contenu sexuel ou explicite
- Reste fun et sympathique
- Tous publics

Parle comme un vrai membre Discord."""
            
            api_messages = [{"role": "system", "content": system_prompt}]
            
            for msg in messages[-10:]:
                if msg['role'] in ['user', 'assistant']:
                    api_messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
            
            payload = {
                "model": AI_MODEL,
                "messages": api_messages,
                "temperature": 0.8,
                "max_tokens": max_tokens,
                "top_p": 0.9,
                "stream": False
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('choices') and len(result['choices']) > 0:
                            return result['choices'][0]['message']['content'].strip()
                        return "Desole, erreur de reponse."
                    else:
                        return "Erreur technique."
        
        except asyncio.TimeoutError:
            return "Timeout."
        except Exception as e:
            print(f"[ERROR] {e}")
            return "Une erreur s'est produite."

ai_client = GroqClient()

@bot.event
async def on_ready():
    print("="*60, flush=True)
    print(f"BOT SFW READY", flush=True)
    print(f"Bot user: {bot.user}", flush=True)
    print(f"Mode: SAFE FOR WORK (channels non-NSFW)", flush=True)
    print("="*60, flush=True)
    
    try:
        synced = await bot.tree.sync()
        print(f"[SUCCESS] {len(synced)} commands synced")
    except Exception as e:
        print(f"[ERROR] Sync error: {e}")
    
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="En attente | /start (SFW Bot)"
        )
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)
    
    # CE BOT SFW fonctionne SEULEMENT dans les channels NON-NSFW
    if hasattr(message.channel, 'is_nsfw') and message.channel.is_nsfw():
        return  # Ignorer les channels NSFW
    
    channel_id = message.channel.id
    
    if not bot_active_channels[channel_id]:
        return
    
    bot_mentioned = bot.user in message.mentions
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_reply_to_bot = (message.reference and 
                       message.reference.resolved and 
                       message.reference.resolved.author == bot.user)
    
    # Reponses spontanees (20% pour SFW, moins intrusif)
    should_respond_naturally = False
    if not (bot_mentioned or is_dm or is_reply_to_bot):
        import random
        if random.random() < 0.2:  # 20% pour SFW
            should_respond_naturally = True
    
    if bot_mentioned or is_dm or is_reply_to_bot or should_respond_naturally:
        user_id = message.author.id
        current_time = time.time()
        
        if user_id in user_last_response:
            if current_time - user_last_response[user_id] < RATE_LIMIT_SECONDS:
                return
        
        user_last_response[user_id] = current_time
        
        async with message.channel.typing():
            clean_content = message.clean_content
            for mention in message.mentions:
                clean_content = clean_content.replace(f'@{mention.name}', '').strip()
            
            conversation_history[channel_id].append({
                'role': 'user',
                'content': clean_content
            })
            
            if len(conversation_history[channel_id]) > MAX_HISTORY:
                conversation_history[channel_id] = conversation_history[channel_id][-MAX_HISTORY:]
            
            personality = channel_personalities[channel_id]
            
            response = await ai_client.generate_response(
                conversation_history[channel_id],
                personality=personality
            )
            
            conversation_history[channel_id].append({
                'role': 'assistant',
                'content': response
            })
            
            if len(response) > 2000:
                response = response[:1997] + "..."
            
            await message.channel.send(response)

def is_admin():
    async def predicate(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            raise app_commands.MissingPermissions(['administrator'])
        return True
    return app_commands.check(predicate)

class PersonalitySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Jordan - Amical", description="Sympathique et ouvert", value="amical"),
            discord.SelectOption(label="Alex - Gamer", description="Passionne de gaming", value="gamer"),
            discord.SelectOption(label="Morgan - Motivateur", description="Positif et encourageant", value="motivateur"),
            discord.SelectOption(label="Sam - Intellectuel", description="Cultive et curieux", value="intellectuel"),
            discord.SelectOption(label="Charlie - Blagueur", description="Drole et sarcastique", value="blagueur"),
            discord.SelectOption(label="Jade - Zen", description="Calme et posee", value="zen")
        ]
        super().__init__(placeholder="Choisissez une personnalite SFW...", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        try:
            selected_personality = self.values[0]
            channel_id = interaction.channel_id
            bot_active_channels[channel_id] = True
            channel_personalities[channel_id] = selected_personality
            personality_info = PERSONALITIES[selected_personality]
            conversation_history[channel_id].clear()
            
            # Changer nickname
            try:
                guild = interaction.guild
                if guild:
                    await guild.me.edit(nick=personality_info['name'])
            except:
                pass
            
            embed = discord.Embed(
                title=f"{personality_info['name']} - {personality_info['title']}",
                description=personality_info['description'],
                color=personality_info['color']
            )
            
            embed.add_field(name="Genre", value=personality_info['genre'], inline=True)
            embed.add_field(name="Age", value=personality_info['age'], inline=True)
            embed.add_field(name="Traits", value=personality_info['traits'], inline=False)
            embed.add_field(
                name="Comment interagir?",
                value=f"- Mentionnez-moi @{personality_info['name']}\n- Repondez a mes messages",
                inline=False
            )
            
            embed.set_footer(text=f"Bot SFW active - Je suis {personality_info['name']}")
            
            await interaction.response.edit_message(embed=embed, view=None)
            
            active_count = len([c for c in bot_active_channels.values() if c])
            asyncio.create_task(
                bot.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.playing,
                    name=f"{personality_info['name']} (SFW) | {active_count} canal actif"
                ))
            )
        except Exception as e:
            print(f"Error: {e}")

class PersonalityView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(PersonalitySelect())

@bot.tree.command(name="start", description="Active le bot SFW (admin)")
@is_admin()
async def start_bot(interaction: discord.Interaction):
    # CE BOT SFW fonctionne SEULEMENT dans les channels NON-NSFW
    if hasattr(interaction.channel, 'is_nsfw') and interaction.channel.is_nsfw():
        await interaction.response.send_message(
            "Ce bot SFW est reserve aux channels normaux. Utilisez le bot NSFW dans les channels NSFW.",
            ephemeral=True
        )
        return
    
    channel_id = interaction.channel_id
    if bot_active_channels[channel_id]:
        await interaction.response.send_message("Le bot est deja actif!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="Activation du Bot SFW",
        description="Choisissez une personnalite pour ce canal (Safe For Work):",
        color=discord.Color.green()
    )
    embed.add_field(name="Mode", value="Safe For Work - Conversations normales", inline=False)
    view = PersonalityView()
    
    await interaction.response.send_message(embed=embed, view=view)

@bot.tree.command(name="stop", description="Desactive le bot (admin)")
@is_admin()
async def stop_bot(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    
    if not bot_active_channels[channel_id]:
        await interaction.response.send_message("Le bot est deja inactif!", ephemeral=True)
        return
    
    bot_active_channels[channel_id] = False
    conversation_history[channel_id].clear()
    
    await interaction.response.send_message("Bot SFW desactive dans ce canal.")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        try:
            await interaction.response.send_message("Admin requis.", ephemeral=True)
        except:
            pass

async def health_check(request):
    return web.json_response({
        'status': 'online',
        'bot': str(bot.user) if bot.user else 'connecting',
        'mode': 'SFW',
        'guilds': len(bot.guilds)
    })

async def start_web_server():
    app = web.Application()
    app.router.add_get('/health', health_check)
    
    port = int(os.getenv('PORT_SFW', 10001))
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server SFW started on port {port}")

async def start_bot():
    await bot.start(DISCORD_TOKEN_SFW)

async def main_async():
    await asyncio.gather(
        start_web_server(),
        start_bot()
    )

def main():
    print("="*70, flush=True)
    print("DEBUT BOT SFW (Safe For Work)", flush=True)
    print("="*70, flush=True)
    
    if not DISCORD_TOKEN_SFW:
        print("ERREUR: DISCORD_TOKEN_SFW non trouve!", flush=True)
        return
    
    if not GROQ_API_KEY:
        print("ERREUR: GROQ_API_KEY non trouve!", flush=True)
        return
    
    print(f"Demarrage bot SFW...", flush=True)
    
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\nArret bot SFW...", flush=True)
    except Exception as e:
        print(f"ERREUR: {e}", flush=True)
        raise

if __name__ == "__main__":
    main()
