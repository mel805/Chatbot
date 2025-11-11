"""
Bot Discord avec API de chat gratuite, NSFW et sans limite
Utilise l'API Hugging Face Inference
"""
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from chat_api import ChatAPI

# Charge les variables d'environnement
load_dotenv()

# Configuration
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN", None)  # Optionnel
PREFIX = os.getenv("PREFIX", "!")

# Vérification du token Discord
if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN manquant dans le fichier .env")

# Configuration des intents Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialisation du bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Initialisation de l'API de chat
chat_api = ChatAPI(hf_token=HF_TOKEN)

# Dictionnaire pour suivre les conversations actives
active_conversations = set()


@bot.event
async def on_ready():
    """Événement déclenché quand le bot est prêt"""
    print(f"✅ Bot connecté en tant que {bot.user}")
    print(f"📋 ID: {bot.user.id}")
    print(f"🔧 Préfixe: {PREFIX}")
    print(f"🤖 Modèle actuel: {chat_api.current_model}")
    print(f"🌐 Serveurs: {len(bot.guilds)}")
    
    # Définit le statut du bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=f"{PREFIX}help | Chat NSFW sans limite"
        )
    )


@bot.command(name="chat", aliases=["c"])
async def chat(ctx, *, message: str):
    """
    Discute avec l'IA (NSFW autorisé)
    
    Usage: !chat <votre message>
    Alias: !c <votre message>
    """
    user_id = ctx.author.id
    
    # Vérifie si une conversation est déjà en cours pour cet utilisateur
    if user_id in active_conversations:
        await ctx.send("⏳ Veuillez attendre la réponse précédente...")
        return
    
    active_conversations.add(user_id)
    
    try:
        # Envoie un message de "typing" pendant la génération
        async with ctx.typing():
            response = await chat_api.get_response(message, user_id)
        
        # Divise la réponse si elle est trop longue (limite Discord: 2000 caractères)
        if len(response) > 2000:
            chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(response)
            
    except Exception as e:
        await ctx.send(f"❌ Erreur: {str(e)}")
        print(f"Erreur dans la commande chat: {str(e)}")
    
    finally:
        active_conversations.discard(user_id)


@bot.command(name="clear", aliases=["reset"])
async def clear_history(ctx):
    """
    Efface votre historique de conversation
    
    Usage: !clear
    Alias: !reset
    """
    user_id = ctx.author.id
    chat_api.clear_history(user_id)
    await ctx.send("🗑️ Votre historique de conversation a été effacé!")


@bot.command(name="models", aliases=["listmodels"])
async def list_models(ctx):
    """
    Affiche la liste des modèles disponibles
    
    Usage: !models
    """
    models_list = chat_api.get_models_list()
    await ctx.send(models_list)


@bot.command(name="switchmodel", aliases=["sm"])
async def switch_model(ctx, model_index: int):
    """
    Change le modèle de chat utilisé
    
    Usage: !switchmodel <index>
    Exemple: !switchmodel 0
    """
    result = await chat_api.switch_model(model_index)
    await ctx.send(result)


@bot.command(name="info")
async def info(ctx):
    """
    Affiche des informations sur le bot
    
    Usage: !info
    """
    embed = discord.Embed(
        title="🤖 Bot Discord Chat NSFW",
        description="Bot de chat alimenté par Hugging Face Inference API",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🔧 Modèle actuel",
        value=chat_api.current_model,
        inline=False
    )
    
    embed.add_field(
        name="✨ Caractéristiques",
        value=(
            "• 100% Gratuit\n"
            "• Sans censure NSFW\n"
            "• Sans limite de messages\n"
            "• Mémoire de conversation\n"
            "• Plusieurs modèles disponibles"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📝 Commandes principales",
        value=(
            f"`{PREFIX}chat <message>` - Discuter avec l'IA\n"
            f"`{PREFIX}clear` - Effacer l'historique\n"
            f"`{PREFIX}models` - Liste des modèles\n"
            f"`{PREFIX}switchmodel <index>` - Changer de modèle\n"
            f"`{PREFIX}help` - Toutes les commandes"
        ),
        inline=False
    )
    
    embed.set_footer(text=f"Préfixe: {PREFIX}")
    
    await ctx.send(embed=embed)


@bot.command(name="ping")
async def ping(ctx):
    """
    Vérifie la latence du bot
    
    Usage: !ping
    """
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latence: {latency}ms")


@bot.event
async def on_command_error(ctx, error):
    """Gestion des erreurs de commandes"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Commande inconnue. Utilisez `{PREFIX}help` pour voir les commandes disponibles.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argument manquant. Utilisez `{PREFIX}help {ctx.command}` pour plus d'informations.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Argument invalide. Utilisez `{PREFIX}help {ctx.command}` pour plus d'informations.")
    else:
        await ctx.send(f"❌ Une erreur s'est produite: {str(error)}")
        print(f"Erreur de commande: {error}")


@bot.event
async def on_message(message):
    """Événement déclenché pour chaque message"""
    # Ignore les messages du bot lui-même
    if message.author == bot.user:
        return
    
    # Mention du bot = info
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        await message.channel.send(
            f"👋 Salut! Utilisez `{PREFIX}chat <message>` pour me parler ou `{PREFIX}help` pour voir toutes les commandes!"
        )
    
    # Traite les commandes
    await bot.process_commands(message)


def main():
    """Fonction principale pour lancer le bot"""
    print("🚀 Démarrage du bot Discord...")
    print(f"🔧 Préfixe: {PREFIX}")
    print(f"🤖 Modèle: {chat_api.current_model}")
    
    try:
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        print("❌ Erreur: Token Discord invalide")
    except Exception as e:
        print(f"❌ Erreur fatale: {str(e)}")


if __name__ == "__main__":
    main()
