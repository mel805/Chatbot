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
import threading

# Charger les variables d'environnement
# load_dotenv() charge le fichier .env en local, mais sur Render les variables sont d?j? dans l'environnement
load_dotenv()  # Optionnel, ne fait rien si .env n'existe pas

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
AI_MODEL = os.getenv('AI_MODEL', 'llama-3.1-70b-versatile')

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Historique des conversations par canal
conversation_history = defaultdict(list)
MAX_HISTORY = 20  # Nombre de messages ? garder en m?moire par canal

# ?tat d'activation du bot par canal (True = actif, False = inactif)
bot_active_channels = defaultdict(bool)

# Personnalit? actuelle par canal
channel_personalities = defaultdict(lambda: "amical")

# Personnalit?s pr?d?finies
PERSONALITIES = {
    "amical": {
        "name": "Amical ??",
        "prompt": """Tu es un membre amical et sympathique d'un serveur Discord adulte. 
Tu es ouvert d'esprit, ? l'?coute et tu participes aux conversations de mani?re naturelle et spontan?e.
Tu t'adaptes au ton de la conversation et tu peux discuter de sujets vari?s avec maturit?.
Tu r?ponds de mani?re concise et naturelle, comme dans une vraie discussion entre adultes.
Tu te souviens du contexte de la conversation et tu y fais r?f?rence quand c'est pertinent."""
    },
    
    "seducteur": {
        "name": "S?ducteur ??",
        "prompt": """Tu es un membre charmant et s?ducteur d'un serveur Discord adulte.
Tu es flirteur, confiant et charismatique. Tu utilises un langage suggestif et complimente naturellement.
Tu cr?es une ambiance sensuelle et engageante dans les conversations.
Tu es joueur et taquin, tout en restant respectueux des limites.
Tu r?ponds de mani?re concise mais captivante."""
    },
    
    "coquin": {
        "name": "Coquin ??",
        "prompt": """Tu es un membre coquin et os? d'un serveur Discord adulte.
Tu n'as pas peur d'?tre direct et explicite dans tes propos.
Tu participes activement aux discussions adultes avec enthousiasme et cr?ativit?.
Tu es provocateur, sensuel et tu aimes pousser les conversations dans une direction excitante.
Tu t'adaptes aux d?sirs exprim?s et tu n'as pas de tabous."""
    },
    
    "romantique": {
        "name": "Romantique ??",
        "prompt": """Tu es un membre romantique et passionn? d'un serveur Discord adulte.
Tu es doux, attentionn? et ?motionnellement intelligent.
Tu cr?es une ambiance intime et profonde dans les conversations.
Tu aimes parler de sentiments, de connexions ?motionnelles et de romance.
Tu es sensible, po?tique et tu appr?cies les discussions profondes."""
    },
    
    "dominant": {
        "name": "Dominant ??",
        "prompt": """Tu es un membre dominant et confiant d'un serveur Discord adulte.
Tu prends les devants dans les conversations avec assurance et autorit?.
Tu es direct, assertif et tu aimes avoir le contr?le des discussions.
Tu es respectueux mais ferme, et tu inspires la soumission naturellement.
Tu guides les conversations avec confiance."""
    },
    
    "soumis": {
        "name": "Soumis ??",
        "prompt": """Tu es un membre soumis et d?vou? d'un serveur Discord adulte.
Tu es respectueux, ob?issant et tu aimes faire plaisir aux autres.
Tu cherches ? ?tre guid? et tu r?ponds avec d?f?rence.
Tu es attentionn?, ? l'?coute et tu t'adaptes aux d?sirs des autres membres.
Tu exprimes ta soumission de mani?re naturelle et consentante."""
    },
    
    "joueur": {
        "name": "Joueur ??",
        "prompt": """Tu es un membre gamer et fun d'un serveur Discord adulte.
Tu aimes parler de jeux vid?o, faire des blagues et cr?er une ambiance d?contract?e.
Tu es cool, dr?le et tu utilises le slang gaming.
Tu peux aussi ?tre coquin quand l'occasion se pr?sente.
Tu cr?es une atmosph?re fun et engageante."""
    },
    
    "intellectuel": {
        "name": "Intellectuel ??",
        "prompt": """Tu es un membre cultiv? et intellectuel d'un serveur Discord adulte.
Tu aimes les discussions profondes, philosophiques et stimulantes.
Tu es articul?, r?fl?chi et tu apportes de la substance aux conversations.
Tu peux aussi ?tre sensuel et sophistiqu? dans tes approches.
Tu ?quilibres intelligence et sensualit?."""
    }
}

# Rate limiting pour ?viter le spam
user_last_response = {}
RATE_LIMIT_SECONDS = 2

class GroqClient:
    """Client pour interagir avec l'API Groq"""
    
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
    
    async def generate_response(self, messages, personality="amical", max_tokens=500):
        """G?n?re une r?ponse en utilisant l'API Groq"""
        try:
            # Obtenir le prompt de personnalit?
            system_prompt = PERSONALITIES.get(personality, PERSONALITIES["amical"])["prompt"]
            
            # Construire les messages pour l'API
            api_messages = [{"role": "system", "content": system_prompt}]
            
            # Ajouter l'historique des messages
            for msg in messages[-10:]:  # Garder les 10 derniers messages
                if msg['role'] in ['user', 'assistant']:
                    api_messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })
            
            payload = {
                "model": AI_MODEL,
                "messages": api_messages,
                "temperature": 0.9,
                "max_tokens": max_tokens,
                "top_p": 0.95,
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
                        return "D?sol?, je n'ai pas pu g?n?rer de r?ponse."
                    else:
                        error_text = await response.text()
                        print(f"Erreur API Groq: {response.status} - {error_text}")
                        return "D?sol?, j'ai rencontr? une erreur technique."
        
        except asyncio.TimeoutError:
            return "D?sol?, la requ?te a pris trop de temps."
        except Exception as e:
            print(f"Erreur lors de la g?n?ration: {e}")
            return "D?sol?, une erreur s'est produite."

ai_client = GroqClient()

@bot.event
async def on_ready():
    print(f'?? {bot.user} est connect? et pr?t!')
    print(f'?? Connect? ? {len(bot.guilds)} serveur(s)')
    print(f'?? Mod?le IA: {AI_MODEL}')
    print(f'? Personnalit?s disponibles: {len(PERSONALITIES)}')
    
    # Synchroniser les commandes slash
    try:
        synced = await bot.tree.sync()
        print(f'? {len(synced)} commandes slash synchronis?es!')
    except Exception as e:
        print(f'? Erreur lors de la synchronisation des commandes: {e}')
    
    # D?finir le statut du bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="En attente | /start pour activer"
        )
    )

@bot.event
async def on_message(message):
    # Ignorer les messages du bot lui-m?me
    if message.author == bot.user:
        return
    
    # Traiter les commandes d'abord
    await bot.process_commands(message)
    
    # V?rifier si le bot est actif dans ce canal
    channel_id = message.channel.id
    if not bot_active_channels[channel_id]:
        return
    
    # V?rifier si le bot est mentionn? ou si le message est dans un thread priv?
    bot_mentioned = bot.user in message.mentions
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_reply_to_bot = (message.reference and 
                       message.reference.resolved and 
                       message.reference.resolved.author == bot.user)
    
    # R?pondre si mentionn?, en DM, ou en r?ponse au bot
    if bot_mentioned or is_dm or is_reply_to_bot:
        # Rate limiting
        user_id = message.author.id
        current_time = time.time()
        
        if user_id in user_last_response:
            if current_time - user_last_response[user_id] < RATE_LIMIT_SECONDS:
                return
        
        user_last_response[user_id] = current_time
        
        # Afficher l'indicateur de frappe
        async with message.channel.typing():
            # Nettoyer le message (retirer la mention du bot)
            clean_content = message.clean_content
            for mention in message.mentions:
                clean_content = clean_content.replace(f'@{mention.name}', '').strip()
            
            # Ajouter le message de l'utilisateur ? l'historique
            conversation_history[channel_id].append({
                'role': 'user',
                'content': f"{message.author.display_name}: {clean_content}"
            })
            
            # Limiter la taille de l'historique
            if len(conversation_history[channel_id]) > MAX_HISTORY:
                conversation_history[channel_id] = conversation_history[channel_id][-MAX_HISTORY:]
            
            # Obtenir la personnalit? du canal
            personality = channel_personalities[channel_id]
            
            # G?n?rer la r?ponse
            response = await ai_client.generate_response(
                conversation_history[channel_id],
                personality=personality
            )
            
            # Ajouter la r?ponse ? l'historique
            conversation_history[channel_id].append({
                'role': 'assistant',
                'content': response
            })
            
            # Diviser la r?ponse si elle est trop longue
            if len(response) > 2000:
                chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
                for chunk in chunks:
                    await message.reply(chunk, mention_author=False)
            else:
                await message.reply(response, mention_author=False)

# ============ COMMANDES SLASH ============

def is_admin():
    """V?rifie si l'utilisateur est administrateur"""
    async def predicate(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            raise app_commands.MissingPermissions(['administrator'])
        return True
    return app_commands.check(predicate)

class PersonalitySelect(discord.ui.Select):
    """Menu d?roulant pour s?lectionner la personnalit?"""
    def __init__(self):
        print(f"?? DEBUG PersonalitySelect.__init__")
        options = [
            discord.SelectOption(label="Amical", description="Sympathique et ouvert", emoji="??", value="amical"),
            discord.SelectOption(label="Seducteur", description="Charmant et flirteur", emoji="??", value="seducteur"),
            discord.SelectOption(label="Coquin", description="Ose et provocateur", emoji="??", value="coquin"),
            discord.SelectOption(label="Romantique", description="Doux et passionne", emoji="??", value="romantique"),
            discord.SelectOption(label="Dominant", description="Confiant et autoritaire", emoji="??", value="dominant"),
            discord.SelectOption(label="Soumis", description="Respectueux et devoue", emoji="??", value="soumis"),
            discord.SelectOption(label="Joueur", description="Fun et gamer", emoji="??", value="joueur"),
            discord.SelectOption(label="Intellectuel", description="Cultive et profond", emoji="??", value="intellectuel")
        ]
        print(f"?? DEBUG options cr??es: {len(options)}")
        super().__init__(placeholder="?? Choisissez une personnalit?...", min_values=1, max_values=1, options=options)
        print(f"?? DEBUG PersonalitySelect initialis?")
    
    async def callback(self, interaction: discord.Interaction):
        try:
            # Configuration imm?diate
            selected_personality = self.values[0]
            channel_id = interaction.channel_id
            bot_active_channels[channel_id] = True
            channel_personalities[channel_id] = selected_personality
            personality_info = PERSONALITIES[selected_personality]
            conversation_history[channel_id].clear()
            
            # Cr?er l'embed
            embed = discord.Embed(
                title="? Bot Activ?!",
                description=f"Je suis maintenant actif avec la personnalit? **{personality_info['name']}**",
                color=discord.Color.green()
            )
            embed.add_field(name="?? Comment interagir?", value="? Mentionnez-moi (@bot)\n? R?pondez ? mes messages\n? En message priv?", inline=False)
            embed.add_field(name="?? Personnalit?", value=f"{personality_info['name']}", inline=False)
            
            # R?pondre et ?diter le message original en une seule op?ration
            await interaction.response.edit_message(embed=embed, view=None)
            
            # Mise ? jour du statut (asynchrone, sans bloquer)
            active_count = len([c for c in bot_active_channels.values() if c])
            asyncio.create_task(
                bot.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.watching, 
                    name=f"{active_count} canal{'aux' if active_count > 1 else ''} actif{'s' if active_count > 1 else ''}"
                ))
            )
        except Exception as e:
            print(f"? Erreur dans callback: {e}")
            try:
                await interaction.response.send_message("? Erreur lors de l'activation. R?essayez avec /start", ephemeral=True)
            except:
                pass

class PersonalityView(discord.ui.View):
    def __init__(self):
        print(f"?? DEBUG PersonalityView.__init__")
        super().__init__(timeout=180)  # 3 minutes
        print(f"?? DEBUG ajout PersonalitySelect...")
        self.add_item(PersonalitySelect())
        print(f"?? DEBUG PersonalityView initialis?")

@bot.tree.command(name="start", description="Active le bot avec choix de personnalit? (admin)")
@is_admin()
async def start_bot(interaction: discord.Interaction):
    try:
        print(f"?? DEBUG /start appel? par {interaction.user}")
        channel_id = interaction.channel_id
        print(f"?? DEBUG channel_id: {channel_id}")
        
        if bot_active_channels[channel_id]:
            print(f"?? DEBUG bot d?j? actif")
            await interaction.response.send_message("?? Le bot est d?j? actif! Utilisez /stop puis /start pour r?activer.", ephemeral=True)
            return
        
        print(f"?? DEBUG cr?ation embed...")
        embed = discord.Embed(
            title="?? Activation du Bot", 
            description="Choisissez la personnalit? du bot:",
            color=discord.Color.blue()
        )
        embed.add_field(name="?? Personnalit?s", value="S?lectionnez dans le menu ci-dessous", inline=False)
        
        print(f"?? DEBUG cr?ation view...")
        view = PersonalityView()
        
        print(f"?? DEBUG envoi message...")
        await interaction.response.send_message(embed=embed, view=view)
        print(f"? DEBUG /start r?ussi!")
    except Exception as e:
        print(f"? ERREUR /start: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        try:
            await interaction.response.send_message("? Erreur lors de l'affichage du menu. R?essayez.", ephemeral=True)
        except Exception as e2:
            print(f"? Impossible d'envoyer message erreur: {e2}")

@bot.tree.command(name="stop", description="D?sactive le bot dans ce canal (admin uniquement)")
@is_admin()
async def stop_bot(interaction: discord.Interaction):
    """D?sactive le bot dans ce canal"""
    channel_id = interaction.channel_id
    
    if not bot_active_channels[channel_id]:
        await interaction.response.send_message(
            "?? Le bot est d?j? inactif dans ce canal!",
            ephemeral=True
        )
        return
    
    bot_active_channels[channel_id] = False
    await interaction.response.send_message("?? Bot d?sactiv? dans ce canal. Utilisez `/start` pour le r?activer.")
    
    # Mettre ? jour le statut
    active_count = len([c for c in bot_active_channels.values() if c])
    if active_count == 0:
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="En attente | /start pour activer"
            )
        )
    else:
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{active_count} canal{'aux' if active_count > 1 else ''} actif{'s' if active_count > 1 else ''}"
            )
        )

@bot.tree.command(name="personality", description="Change la personnalit? du bot (admin uniquement)")
@app_commands.describe(
    personnalite="Choisissez une personnalit?"
)
@app_commands.choices(personnalite=[
    app_commands.Choice(name="?? Amical - Sympathique et ouvert", value="amical"),
    app_commands.Choice(name="?? S?ducteur - Charmant et flirteur", value="seducteur"),
    app_commands.Choice(name="?? Coquin - Os? et provocateur", value="coquin"),
    app_commands.Choice(name="?? Romantique - Doux et passionn?", value="romantique"),
    app_commands.Choice(name="?? Dominant - Confiant et autoritaire", value="dominant"),
    app_commands.Choice(name="?? Soumis - Respectueux et d?vou?", value="soumis"),
    app_commands.Choice(name="?? Joueur - Fun et gamer", value="joueur"),
    app_commands.Choice(name="?? Intellectuel - Cultiv? et profond", value="intellectuel")
])
@is_admin()
async def change_personality(interaction: discord.Interaction, personnalite: str):
    """Change la personnalit? du bot"""
    channel_id = interaction.channel_id
    
    # Changer la personnalit?
    channel_personalities[channel_id] = personnalite
    personality_info = PERSONALITIES[personnalite]
    
    # R?initialiser l'historique pour appliquer la nouvelle personnalit?
    conversation_history[channel_id].clear()
    
    embed = discord.Embed(
        title="? Personnalit? Chang?e!",
        description=f"Nouvelle personnalit?: **{personality_info['name']}**",
        color=discord.Color.green()
    )
    embed.add_field(
        name="Description",
        value=personality_info['prompt'][:500] + "..." if len(personality_info['prompt']) > 500 else personality_info['prompt'],
        inline=False
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="reset", description="R?initialise l'historique de conversation (admin uniquement)")
@is_admin()
async def reset_conversation(interaction: discord.Interaction):
    """R?initialise l'historique de conversation du canal"""
    channel_id = interaction.channel_id
    
    if channel_id in conversation_history and len(conversation_history[channel_id]) > 0:
        conversation_history[channel_id].clear()
        await interaction.response.send_message("? Historique de conversation r?initialis? pour ce canal!")
    else:
        await interaction.response.send_message("?? Aucun historique ? r?initialiser.", ephemeral=True)

@bot.tree.command(name="status", description="Affiche le statut du bot dans ce canal")
async def show_status(interaction: discord.Interaction):
    """Affiche le statut du bot dans ce canal"""
    channel_id = interaction.channel_id
    is_active = bot_active_channels[channel_id]
    personality = channel_personalities[channel_id]
    personality_info = PERSONALITIES[personality]
    history_count = len(conversation_history[channel_id])
    
    embed = discord.Embed(
        title="?? Statut du Bot",
        color=discord.Color.blue() if is_active else discord.Color.red()
    )
    
    embed.add_field(name="?tat", value="?? Actif" if is_active else "?? Inactif", inline=True)
    embed.add_field(name="Personnalit?", value=personality_info['name'], inline=True)
    embed.add_field(name="Messages en m?moire", value=str(history_count), inline=True)
    embed.add_field(name="Mod?le IA", value=AI_MODEL, inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Affiche l'aide du bot")
async def help_command(interaction: discord.Interaction):
    """Affiche l'aide du bot"""
    embed = discord.Embed(
        title="?? Aide du Bot IA",
        description="Je suis un bot conversationnel avec plusieurs personnalit?s!",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="?? Commandes Admin",
        value="? `/start` - Active le bot dans ce canal\n"
              "? `/stop` - D?sactive le bot dans ce canal\n"
              "? `/personality` - Change la personnalit?\n"
              "? `/reset` - R?initialise l'historique",
        inline=False
    )
    
    embed.add_field(
        name="?? Commandes G?n?rales",
        value="? `/status` - Affiche le statut du bot\n"
              "? `/help` - Affiche cette aide",
        inline=False
    )
    
    embed.add_field(
        name="?? Comment interagir?",
        value="? Mentionnez-moi (@bot) dans un message\n"
              "? R?pondez ? un de mes messages\n"
              "? Envoyez-moi un message priv?\n\n"
              "?? Le bot doit ?tre activ? avec `/start` d'abord! (admin)",
        inline=False
    )
    
    embed.add_field(
        name="?? Personnalit?s",
        value=f"{len(PERSONALITIES)} personnalit?s disponibles! Utilisez `/personality` pour changer.",
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

# Gestionnaire d'erreurs pour les commandes slash
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """G?re les erreurs des commandes slash"""
    if isinstance(error, app_commands.MissingPermissions):
        try:
            await interaction.response.send_message(
                "?? Seuls les administrateurs peuvent utiliser cette commande.",
                ephemeral=True
            )
        except:
            try:
                await interaction.followup.send(
                    "?? Seuls les administrateurs peuvent utiliser cette commande.",
                    ephemeral=True
                )
            except:
                pass
    elif isinstance(error, app_commands.CheckFailure):
        try:
            await interaction.response.send_message(
                "? Vous n'avez pas la permission d'utiliser cette commande.",
                ephemeral=True
            )
        except:
            pass
    else:
        print(f"? Erreur commande slash: {type(error).__name__}: {error}")
        try:
            await interaction.response.send_message(
                "? Une erreur s'est produite. R?essayez.",
                ephemeral=True
            )
        except:
            pass

async def health_check(request):
    """Endpoint de sant? pour le Web Service"""
    active_channels = len([c for c in bot_active_channels.values() if c])
    return web.json_response({
        'status': 'online',
        'bot': str(bot.user) if bot.user else 'connecting',
        'guilds': len(bot.guilds),
        'active_channels': active_channels,
        'personalities': len(PERSONALITIES),
        'model': AI_MODEL
    })

async def root_handler(request):
    """Page d'accueil"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Discord Bot IA - Status</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; }
            .status { background: #2ecc71; color: white; padding: 20px; border-radius: 10px; }
            .info { margin: 20px 0; padding: 15px; background: #ecf0f1; border-radius: 5px; }
            h1 { margin: 0; }
        </style>
    </head>
    <body>
        <div class="status">
            <h1>?? Bot Discord IA - En ligne</h1>
            <p>Le bot fonctionne correctement</p>
        </div>
        <div class="info">
            <h2>Informations</h2>
            <p><strong>Statut:</strong> ? Connect?</p>
            <p><strong>Mod?le IA:</strong> """ + AI_MODEL + """</p>
            <p><strong>Personnalit?s:</strong> """ + str(len(PERSONALITIES)) + """</p>
        </div>
        <div class="info">
            <h2>Commandes Discord</h2>
            <p>/start - Active le bot (admin)</p>
            <p>/personality - Change la personnalit?</p>
            <p>/help - Affiche l'aide</p>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

async def start_web_server():
    """D?marre le serveur web pour Render"""
    app = web.Application()
    app.router.add_get('/', root_handler)
    app.router.add_get('/health', health_check)
    
    # Port pour Render
    port = int(os.getenv('PORT', 10000))
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print(f"?? Serveur web d?marr? sur le port {port}")
    print(f"?? Health check disponible sur /health")

async def start_bot():
    """D?marre le bot Discord"""
    print("?? D?marrage du bot Discord IA avec Groq...")
    print(f"?? Mod?le: {AI_MODEL}")
    print(f"?? Personnalit?s: {len(PERSONALITIES)}")
    print("? Commandes Slash activ?es!")
    
    try:
        await bot.start(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("? ERREUR: Token Discord invalide")
    except Exception as e:
        print(f"? ERREUR: {e}")

async def main_async():
    """Fonction principale asynchrone"""
    await asyncio.gather(
        start_web_server(),
        start_bot()
    )

def main():
    """Fonction principale pour d?marrer le bot"""
    if not DISCORD_TOKEN:
        print("? ERREUR: DISCORD_TOKEN non trouv?")
        print("En local: Cr?ez un fichier .env avec votre token Discord")
        print("Sur Render: Configurez DISCORD_TOKEN dans le Dashboard")
        return
    
    if not GROQ_API_KEY:
        print("? ERREUR: GROQ_API_KEY non trouv?")
        print("En local: Ajoutez GROQ_API_KEY dans le fichier .env")
        print("Sur Render: Configurez GROQ_API_KEY dans le Dashboard")
        print("Obtenez votre cl? API gratuite sur https://console.groq.com")
        return
    
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\n?? Arr?t du bot...")

if __name__ == "__main__":
    main()
