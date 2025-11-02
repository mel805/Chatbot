import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
import aiohttp
from dotenv import load_dotenv
import json
from collections import defaultdict
import time

# Charger les variables d'environnement
load_dotenv()

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
            await interaction.response.send_message(
                "? Seuls les administrateurs peuvent utiliser cette commande.",
                ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)

@bot.tree.command(name="start", description="Active le bot dans ce canal (admin uniquement)")
@is_admin()
async def start_bot(interaction: discord.Interaction):
    """Active le bot dans ce canal"""
    channel_id = interaction.channel_id
    
    if bot_active_channels[channel_id]:
        await interaction.response.send_message(
            "?? Le bot est d?j? actif dans ce canal!",
            ephemeral=True
        )
        return
    
    bot_active_channels[channel_id] = True
    personality = channel_personalities[channel_id]
    personality_info = PERSONALITIES[personality]
    
    embed = discord.Embed(
        title="? Bot Activ?!",
        description=f"Je suis maintenant actif dans ce canal avec la personnalit? **{personality_info['name']}**",
        color=discord.Color.green()
    )
    embed.add_field(
        name="?? Comment interagir?",
        value="? Mentionnez-moi (@bot)\n? R?pondez ? mes messages\n? En message priv?",
        inline=False
    )
    await interaction.response.send_message(embed=embed)
    
    # Mettre ? jour le statut
    active_count = len([c for c in bot_active_channels.values() if c])
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{active_count} canal{'aux' if active_count > 1 else ''} actif{'s' if active_count > 1 else ''}"
        )
    )

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

def main():
    """Fonction principale pour d?marrer le bot"""
    if not DISCORD_TOKEN:
        print("? ERREUR: DISCORD_TOKEN non trouv? dans le fichier .env")
        print("Veuillez cr?er un fichier .env avec votre token Discord.")
        return
    
    if not GROQ_API_KEY:
        print("? ERREUR: GROQ_API_KEY non trouv? dans le fichier .env")
        print("Obtenez votre cl? API gratuite sur https://console.groq.com")
        return
    
    print("?? D?marrage du bot Discord IA avec Groq...")
    print(f"?? Mod?le: {AI_MODEL}")
    print(f"?? Personnalit?s: {len(PERSONALITIES)}")
    print("? Commandes Slash activ?es!")
    
    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("? ERREUR: Token Discord invalide")
    except Exception as e:
        print(f"? ERREUR: {e}")

if __name__ == "__main__":
    main()
