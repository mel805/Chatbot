import discord
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
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')  # Optionnel pour certains mod?les
AI_MODEL = os.getenv('AI_MODEL', 'mistralai/Mistral-7B-Instruct-v0.2')

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Historique des conversations par canal
conversation_history = defaultdict(list)
MAX_HISTORY = 20  # Nombre de messages ? garder en m?moire par canal

# Personnalit? du bot (peut ?tre personnalis?e)
SYSTEM_PROMPT = """Tu es un membre actif et amical d'un serveur Discord. 
Tu participes aux conversations de mani?re naturelle et spontan?e.
Tu as une personnalit? engageante et tu t'adaptes au ton de la conversation.
Tu r?ponds de mani?re concise et naturelle, comme dans une vraie discussion.
Tu te souviens du contexte de la conversation et tu y fais r?f?rence quand c'est pertinent."""

# Rate limiting pour ?viter le spam
user_last_response = {}
RATE_LIMIT_SECONDS = 2

class AIClient:
    """Client pour interagir avec l'API Hugging Face"""
    
    def __init__(self):
        self.api_url = f"https://api-inference.huggingface.co/models/{AI_MODEL}"
        self.headers = {}
        if HUGGINGFACE_TOKEN:
            self.headers["Authorization"] = f"Bearer {HUGGINGFACE_TOKEN}"
    
    async def generate_response(self, messages, max_length=500):
        """G?n?re une r?ponse en utilisant l'API Hugging Face"""
        try:
            # Construire le prompt
            prompt = self._build_prompt(messages)
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_length,
                    "temperature": 0.9,
                    "top_p": 0.95,
                    "do_sample": True,
                    "return_full_text": False
                }
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
                        if isinstance(result, list) and len(result) > 0:
                            return result[0].get('generated_text', '').strip()
                        return "D?sol?, je n'ai pas pu g?n?rer de r?ponse."
                    elif response.status == 503:
                        return "Le mod?le est en train de se charger, r?essayez dans quelques secondes..."
                    else:
                        error_text = await response.text()
                        print(f"Erreur API: {response.status} - {error_text}")
                        return "D?sol?, j'ai rencontr? une erreur technique."
        
        except asyncio.TimeoutError:
            return "D?sol?, la requ?te a pris trop de temps."
        except Exception as e:
            print(f"Erreur lors de la g?n?ration: {e}")
            return "D?sol?, une erreur s'est produite."
    
    def _build_prompt(self, messages):
        """Construit le prompt pour le mod?le"""
        prompt = f"{SYSTEM_PROMPT}\n\n"
        
        for msg in messages[-10:]:  # Garder les 10 derniers messages
            role = msg['role']
            content = msg['content']
            if role == 'user':
                prompt += f"Utilisateur: {content}\n"
            elif role == 'assistant':
                prompt += f"Assistant: {content}\n"
        
        prompt += "Assistant:"
        return prompt

ai_client = AIClient()

@bot.event
async def on_ready():
    print(f'{bot.user} est connect? et pr?t!')
    print(f'Connect? ? {len(bot.guilds)} serveur(s)')
    
    # D?finir le statut du bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="les conversations | Mentionnez-moi!"
        )
    )

@bot.event
async def on_message(message):
    # Ignorer les messages du bot lui-m?me
    if message.author == bot.user:
        return
    
    # Traiter les commandes d'abord
    await bot.process_commands(message)
    
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
            
            # Obtenir l'historique du canal
            channel_id = message.channel.id
            
            # Ajouter le message de l'utilisateur ? l'historique
            conversation_history[channel_id].append({
                'role': 'user',
                'content': f"{message.author.display_name}: {clean_content}"
            })
            
            # Limiter la taille de l'historique
            if len(conversation_history[channel_id]) > MAX_HISTORY:
                conversation_history[channel_id] = conversation_history[channel_id][-MAX_HISTORY:]
            
            # G?n?rer la r?ponse
            response = await ai_client.generate_response(conversation_history[channel_id])
            
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

@bot.command(name='reset')
async def reset_conversation(ctx):
    """R?initialise l'historique de conversation du canal"""
    channel_id = ctx.channel.id
    if channel_id in conversation_history:
        conversation_history[channel_id].clear()
        await ctx.send("? Historique de conversation r?initialis? pour ce canal!")
    else:
        await ctx.send("?? Aucun historique ? r?initialiser.")

@bot.command(name='personality')
async def change_personality(ctx, *, new_personality: str = None):
    """Change la personnalit? du bot (admin uniquement)"""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("? Seuls les administrateurs peuvent changer la personnalit? du bot.")
        return
    
    if new_personality:
        global SYSTEM_PROMPT
        SYSTEM_PROMPT = new_personality
        await ctx.send(f"? Personnalit? mise ? jour!\n\n**Nouvelle personnalit?:**\n{new_personality}")
    else:
        await ctx.send(f"**Personnalit? actuelle:**\n{SYSTEM_PROMPT}")

@bot.command(name='model')
async def change_model(ctx, *, model_name: str = None):
    """Change le mod?le d'IA utilis? (admin uniquement)"""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("? Seuls les administrateurs peuvent changer le mod?le.")
        return
    
    if model_name:
        global AI_MODEL
        AI_MODEL = model_name
        ai_client.api_url = f"https://api-inference.huggingface.co/models/{AI_MODEL}"
        await ctx.send(f"? Mod?le chang? pour: `{model_name}`")
    else:
        await ctx.send(f"**Mod?le actuel:** `{AI_MODEL}`")

@bot.command(name='help_bot')
async def help_command(ctx):
    """Affiche l'aide du bot"""
    embed = discord.Embed(
        title="?? Aide du Bot IA",
        description="Je suis un bot conversationnel aliment? par l'IA!",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="?? Comment interagir?",
        value="? Mentionnez-moi (@bot) dans un message\n"
              "? R?pondez ? un de mes messages\n"
              "? Envoyez-moi un message priv?",
        inline=False
    )
    
    embed.add_field(
        name="?? Commandes",
        value="? `!reset` - R?initialise l'historique de conversation\n"
              "? `!personality [texte]` - Change/affiche la personnalit? (admin)\n"
              "? `!model [nom]` - Change/affiche le mod?le IA (admin)\n"
              "? `!help_bot` - Affiche cette aide",
        inline=False
    )
    
    embed.add_field(
        name="?? Fonctionnalit?s",
        value="? M?moire contextuelle des conversations\n"
              "? R?ponses naturelles et adaptatives\n"
              "? Support des discussions multi-utilisateurs",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """Gestion des erreurs de commandes"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"? Argument manquant. Utilisez `!help_bot` pour voir la syntaxe.")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignorer les commandes inconnues
    else:
        print(f"Erreur: {error}")

def main():
    """Fonction principale pour d?marrer le bot"""
    if not DISCORD_TOKEN:
        print("? ERREUR: DISCORD_TOKEN non trouv? dans le fichier .env")
        print("Veuillez cr?er un fichier .env avec votre token Discord.")
        return
    
    print("?? D?marrage du bot Discord IA...")
    print(f"?? Mod?le IA: {AI_MODEL}")
    
    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("? ERREUR: Token Discord invalide")
    except Exception as e:
        print(f"? ERREUR: {e}")

if __name__ == "__main__":
    main()
