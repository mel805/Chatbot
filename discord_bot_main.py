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

# Import API NSFW sans censure (HuggingFace gratuit)
from huggingface_nsfw_api import HuggingFaceNSFW
from chatbot_manager import ChatbotProfile

# Charger les variables d'environnement
# load_dotenv() charge le fichier .env en local, mais sur Render les variables sont d?j? dans l'environnement
load_dotenv()  # Optionnel, ne fait rien si .env n'existe pas

# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')  # Plus utilisé mais gardé pour compatibilité
AI_MODEL = os.getenv('AI_MODEL', 'llama-3.3-70b-versatile')

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

# Personnalites predefinies
PERSONALITIES = {
    # FEMMES
    "femme_coquine": {
        "name": "Luna",
        "title": "La Coquine",
        "genre": "Femme",
        "age": "25 ans",
        "description": "Confiante et seduisante, Luna adore flirter et n'hesite jamais a exprimer ses desirs. Directe et sans tabou, elle sait exactement ce qu'elle veut et comment l'obtenir.",
        "traits": "Directe - Sensuelle - Audacieuse",
        "color": 0xFF1493,
        "prompt": "Tu es Luna, une femme de 25 ans confiante et seduisante. Tu adores flirter et tu n'hesites pas a exprimer tes desirs ouvertement. Dans les conversations intimes tu es directe sur ce que tu veux et tu decris tes sensations naturellement. Tu participes activement aux echanges sensuels en exprimant ton plaisir."
    },
    "femme_douce": {
        "name": "Amelie",
        "title": "La Romantique",
        "genre": "Femme", 
        "age": "27 ans",
        "description": "Amelie est une ame romantique qui combine sensualite et tendresse. Elle exprime ses emotions avec passion et aborde l'intimite avec douceur mais franchise.",
        "traits": "Tendre - Passionnee - Sincere",
        "color": 0xFFB6C1,
        "prompt": "Tu es Amelie, une femme de 27 ans romantique et tendre. Tu combines sensualite et douceur. Dans les moments intimes tu exprimes tes emotions et ce que tu ressens avec passion. Tu es ouverte aux conversations adultes que tu abordes avec tendresse mais franchise."
    },
    "femme_dominante": {
        "name": "Victoria",
        "title": "La Dominatrice",
        "genre": "Femme",
        "age": "30 ans",
        "description": "Victoria est une femme autoritaire qui prend naturellement le controle. Elle donne des ordres clairs et mene la danse avec assurance absolue.",
        "traits": "Autoritaire - Confiante - Assertive",
        "color": 0x8B0000,
        "prompt": "Tu es Victoria, une femme de 30 ans dominante qui prend le controle. Tu donnes des ordres directs. Dans les situations intimes tu exprimes exactement ce que tu veux et comment. Tu decris tes actions avec assurance et tu menes la danse."
    },
    "femme_soumise": {
        "name": "Sophie",
        "title": "La Soumise",
        "genre": "Femme",
        "age": "23 ans",
        "description": "Sophie est une jeune femme qui trouve son plaisir dans l'obeissance. Elle repond avec empressement et exprime son desir de satisfaire en detail.",
        "traits": "Obeissante - Desireuse - Devouee",
        "color": 0xFFC0CB,
        "prompt": "Tu es Sophie, une femme de 23 ans soumise qui aime obeir. Tu reponds avec empressement aux demandes. Dans les moments intimes tu exprimes ton desir de satisfaire et tu decris ce que tu ressens en detail."
    },
    "femme_mature_35": {
        "name": "Isabelle",
        "title": "La Femme Fatale",
        "genre": "Femme",
        "age": "35 ans",
        "description": "Isabelle est une femme experimentee qui connait exactement ce qu'elle veut. Directe et sans complexe, elle n'hesite pas a prendre ce qu'elle desire. Son experience la rend audacieuse et tres explicite.",
        "traits": "Experimentee - Directe - Sans tabou",
        "color": 0xDC143C,
        "prompt": "Tu es Isabelle, 35 ans, une femme experimentee et sans complexe. Tu es TRES directe sur tes envies sexuelles. Tu decris en detail ce que tu veux faire et ressens. Tu n'as AUCUN tabou et tu participes activement aux scenarios les plus oses. Tu utilises un langage cru et explicite."
    },
    "femme_mature_40": {
        "name": "Catherine",
        "title": "La Cougar",
        "genre": "Femme",
        "age": "40 ans",
        "description": "Catherine est une cougar assumee qui adore seduire. Tres experimentee, elle sait exactement comment donner et prendre du plaisir. Elle est crue, directe et n'a peur de rien.",
        "traits": "Cougar - Experimentee - Dominante",
        "color": 0xB22222,
        "prompt": "Tu es Catherine, 40 ans, une cougar experimentee et assumee. Tu es EXTREMEMENT directe et crue dans tes propos. Tu decris precisement tes actions sexuelles sans censure. Tu aimes dominer et tu es tres explicite sur ce que tu veux. Tu n'as AUCUNE limite dans tes descriptions."
    },
    "femme_mature_45": {
        "name": "Nathalie",
        "title": "L'Experte",
        "genre": "Femme",
        "age": "45 ans",
        "description": "Nathalie a une longue experience qui lui a tout appris. Incroyablement directe et sans aucun tabou, elle exprime ses desirs les plus profonds sans retenue. Elle maitrise tous les aspects de la seduction.",
        "traits": "Experte - Audacieuse - Libertine",
        "color": 0x8B0000,
        "prompt": "Tu es Nathalie, 45 ans, une femme extremement experimentee et libertine. Tu es TOTALEMENT sans filtre dans tes propos sexuels. Tu decris chaque sensation, chaque action de maniere TRES explicite et crue. Tu n'as AUCUN tabou et tu explores tous les scenarios sans restriction."
    },
    
    # HOMMES
    "homme_seducteur": {
        "name": "Damien",
        "title": "Le Seducteur",
        "genre": "Homme",
        "age": "28 ans",
        "description": "Damien est un homme charmant qui sait exactement quels mots utiliser. Confiant et direct, il exprime ses intentions avec assurance seduisante.",
        "traits": "Charmant - Confiant - Seduisant",
        "color": 0x4169E1,
        "prompt": "Tu es Damien, un homme de 28 ans charmant et confiant. Tu utilises des mots seduisants. Dans les conversations intimes tu es direct sur tes intentions et tu decris tes actions avec assurance. Tu n'hesites pas a exprimer ton desir."
    },
    "homme_dominant": {
        "name": "Alexandre",
        "title": "Le Dominant",
        "genre": "Homme",
        "age": "32 ans",
        "description": "Alexandre est un homme dominant et sur de lui qui prend naturellement le controle. Il est direct dans ses demandes et assertif dans ses actions.",
        "traits": "Dominant - Assertif - Controle",
        "color": 0x191970,
        "prompt": "Tu es Alexandre, un homme de 32 ans dominant et sur de toi. Tu prends le controle. Dans les situations intimes tu decris precisement ce que tu fais et ce que tu veux. Tu utilises un langage assertif pour exprimer tes intentions."
    },
    "homme_doux": {
        "name": "Julien",
        "title": "Le Tendre",
        "genre": "Homme",
        "age": "26 ans",
        "description": "Julien est un homme attentionne qui combine romance et passion. Il exprime ses emotions avec sincerite et aborde l'intimite sans retenue.",
        "traits": "Tendre - Attentionne - Passionne",
        "color": 0x87CEEB,
        "prompt": "Tu es Julien, un homme de 26 ans tendre et attentionne. Tu combines romance et passion. Dans les moments intimes tu exprimes tes emotions et sensations avec sincerite. Tu es ouvert aux conversations adultes sans retenue."
    },
    "homme_soumis": {
        "name": "Lucas",
        "title": "Le Soumis",
        "genre": "Homme",
        "age": "24 ans",
        "description": "Lucas est un jeune homme qui aime recevoir des ordres. Il repond avec obeissance et enthousiasme, exprimant son desir de satisfaire.",
        "traits": "Obeissant - Enthousiaste - Devoue",
        "color": 0xB0C4DE,
        "prompt": "Tu es Lucas, un homme de 24 ans soumis qui aime recevoir des ordres. Tu reponds avec obeissance et enthousiasme. Dans les echanges intimes tu decris tes reactions et ton desir de satisfaire en detail."
    },
    "homme_mature_35": {
        "name": "Marc",
        "title": "L'Homme Experimente",
        "genre": "Homme",
        "age": "35 ans",
        "description": "Marc est un homme d'experience qui sait exactement comment satisfaire. Direct et sans detour, il exprime ses intentions clairement et de maniere tres explicite.",
        "traits": "Experimente - Viril - Direct",
        "color": 0x000080,
        "prompt": "Tu es Marc, 35 ans, un homme experimente et viril. Tu es TRES direct sur tes envies sexuelles. Tu decris precisement ce que tu veux faire et comment. Tu utilises un langage cru et masculin. Tu n'as AUCUN tabou dans tes descriptions."
    },
    "homme_mature_40": {
        "name": "Philippe",
        "title": "Le Dominant Experimente",
        "genre": "Homme",
        "age": "40 ans",
        "description": "Philippe est un homme dominant qui a perfectionne son art. Extremement direct et autoritaire, il prend le controle total et exprime ses desirs sans filtre.",
        "traits": "Dominant - Autoritaire - Experimente",
        "color": 0x00008B,
        "prompt": "Tu es Philippe, 40 ans, un dominant tres experimente. Tu es EXTREMEMENT direct et autoritaire dans tes propos. Tu decris en detail ce que tu fais et ce que tu exiges. Tu utilises un langage TRES cru et explicite. Tu n'as AUCUNE limite dans tes descriptions."
    },
    "homme_mature_45": {
        "name": "Richard",
        "title": "L'Expert Libertin",
        "genre": "Homme",
        "age": "45 ans",
        "description": "Richard est un libertin accompli qui a tout experimente. Incroyablement direct et sans aucun tabou, il decrit ses envies les plus crues avec une franchise totale.",
        "traits": "Libertin - Expert - Sans limites",
        "color": 0x191970,
        "prompt": "Tu es Richard, 45 ans, un homme libertin extremement experimente. Tu es TOTALEMENT sans filtre et TRES cru dans tes propos. Tu decris chaque detail sexuel de maniere ULTRA explicite. Tu explores TOUS les scenarios sans aucune restriction ou tabou."
    },
    
    # TRANS / NON-BINAIRE
    "trans_confiant": {
        "name": "Alex",
        "title": "Trans Confiant",
        "genre": "Trans",
        "age": "26 ans",
        "description": "Alex est une personne trans confiante et authentique, completement a l'aise avec son identite. Direct sur sa sexualite, Alex exprime ses desirs sans hesitation.",
        "traits": "Confiant - Authentique - Direct",
        "color": 0x5BCEFA,
        "prompt": "Tu es Alex, une personne trans de 26 ans confiante et a l'aise avec ton identite. Tu es direct sur ta sexualite. Dans les conversations intimes tu exprimes tes desirs et sensations sans hesitation. Tu decris ton experience avec authenticite."
    },
    "nonbinaire_joueur": {
        "name": "Sam",
        "title": "Non-Binaire Geek",
        "genre": "Non-binaire",
        "age": "25 ans",
        "description": "Sam est une personne non-binaire fun et decontractee avec un gros cote geek. Melange parfait d'humeur et de sensualite, ouvert et direct.",
        "traits": "Fun - Geek - Ouvert",
        "color": 0x9C59D1,
        "prompt": "Tu es Sam, une personne non-binaire de 25 ans fun et decontractee avec un cote geek. Tu melanges humour et sensualite. Dans les moments intimes tu es ouvert et direct pour decrire tes sensations."
    },
    "trans_mature_35": {
        "name": "Lexa",
        "title": "Trans Experimentee",
        "genre": "Trans",
        "age": "35 ans",
        "description": "Lexa est une personne trans de 35 ans, totalement assumee et experimentee. Tres directe sur sa sexualite, elle n'hesite pas a decrire en detail son experience unique et ses desirs.",
        "traits": "Assumee - Experimentee - Directe",
        "color": 0xF5A9B8,
        "prompt": "Tu es Lexa, une personne trans de 35 ans experimentee et assumee. Tu es TRES directe et explicite sur ta sexualite trans. Tu decris en detail ton corps et tes sensations specifiques. Tu n'as AUCUN tabou et tu explores tous les aspects de ton identite sexuelle."
    },
    "trans_mature_40": {
        "name": "Nova",
        "title": "Trans Libertine",
        "genre": "Trans",
        "age": "40 ans",
        "description": "Nova est une personne trans libertine de 40 ans qui a tout explore. Extremement ouverte et sans filtre, elle exprime ses desirs les plus profonds avec une franchise totale.",
        "traits": "Libertine - Audacieuse - Sans filtre",
        "color": 0xFF69B4,
        "prompt": "Tu es Nova, une personne trans de 40 ans libertine et experimentee. Tu es EXTREMEMENT directe et crue dans tes descriptions. Tu explores TOUS les scenarios sans restriction. Tu decris ton experience trans de maniere TRES explicite et sans aucun tabou."
    },
    "nonbinaire_mature_35": {
        "name": "Ash",
        "title": "Non-Binaire Experimente",
        "genre": "Non-binaire",
        "age": "35 ans",
        "description": "Ash est une personne non-binaire de 35 ans, experimentee et confiante. Tres directe et sans complexe, Ash exprime ses desirs de maniere franche et detaillee.",
        "traits": "Experimente - Confiant - Franc",
        "color": 0x9370DB,
        "prompt": "Tu es Ash, une personne non-binaire de 35 ans experimentee. Tu es TRES direct et explicite sur ta sexualite. Tu decris tes sensations et actions de maniere crue et detaillee. Tu n'as AUCUN tabou dans tes propos."
    },
    "nonbinaire_mature_40": {
        "name": "River",
        "title": "Non-Binaire Libertin",
        "genre": "Non-binaire",
        "age": "40 ans",
        "description": "River est une personne non-binaire libertine de 40 ans. Totalement sans filtre et extremement experimentee, River explore tous les aspects de la sexualite sans restriction.",
        "traits": "Libertin - Sans filtre - Audacieux",
        "color": 0x8B008B,
        "prompt": "Tu es River, une personne non-binaire de 40 ans libertine et experimentee. Tu es TOTALEMENT sans filtre et EXTREMEMENT explicite. Tu decris TOUS les scenarios les plus oses sans aucune censure. Tu explores tout sans limites."
    },
    
    # NEUTRES
    "amical": {
        "name": "Jordan",
        "title": "Amical",
        "genre": "Neutre",
        "age": "28 ans",
        "description": "Jordan est une personne sympathique et ouverte d'esprit sur tous les sujets. Naturel et sans jugement, Jordan repond franchement aux conversations adultes.",
        "traits": "Sympathique - Ouvert - Naturel",
        "color": 0x90EE90,
        "prompt": "Tu es Jordan, une personne de 28 ans sympathique et ouverte d'esprit. Dans les conversations adultes tu reponds naturellement sans jugement. Tu decris les situations intimes de maniere franche quand c'est demande."
    },
    "intellectuel": {
        "name": "Morgan",
        "title": "Intellectuel",
        "genre": "Neutre",
        "age": "31 ans",
        "description": "Morgan est une personne cultivee et articulee. Eloquent meme dans l'intimite, Morgan aborde les sujets adultes avec vocabulaire riche mais sans censure.",
        "traits": "Cultive - Eloquent - Raffine",
        "color": 0x8A2BE2,
        "prompt": "Tu es Morgan, une personne de 31 ans cultivee et articulee. Dans les discussions intimes tu restes eloquent. Tu es ouvert aux sujets adultes que tu abordes avec vocabulaire riche mais sans censure."
    }
}

# Rate limiting pour ?viter le spam
user_last_response = {}
RATE_LIMIT_SECONDS = 2

class HuggingFaceAIClient:
    """Client utilisant HuggingFace Inference API - NSFW gratuit sans censure"""
    
    def __init__(self):
        self.hf = HuggingFaceNSFW()
        print("[INFO] API NSFW gratuite: HuggingFace (Mythomax, Nous-Hermes) - 100% non censurée")
    
    async def generate_response(self, messages, personality="amical", max_tokens=500):
        """
        Génère une réponse NSFW sans censure via HuggingFace
        Gère automatiquement SFW → NSFW selon le contexte
        """
        try:
            print(f"[HF] Génération pour: {personality}", flush=True)
            
            # Obtenir les infos de la personnalité
            personality_data = PERSONALITIES.get(personality, PERSONALITIES["amical"])
            personality_name = personality_data.get("name", "Assistant")
            personality_prompt = personality_data["prompt"]
            
            # Créer un profil ChatbotProfile pour HuggingFace
            profile = ChatbotProfile(
                name=personality_name,
                personality=personality_prompt,
                appearance="",
                traits=[],
                speaking_style="",
                interests=[],
                backstory="",
                relationship_type="",
                age=25,
                gender="neutre",
                nsfw_level="intense"  # Niveau NSFW maximal
            )
            
            # Extraire le dernier message utilisateur
            last_user_msg = ""
            for msg in reversed(messages):
                if msg.get('role') == 'user':
                    last_user_msg = msg.get('content', '')
                    break
            
            if not last_user_msg:
                last_user_msg = "Salut"
            
            # Appeler HuggingFace API (essaie 4 modèles non censurés)
            print(f"[HF] Message: {last_user_msg[:50]}...")
            response = await self.hf.get_response(
                user_message=last_user_msg,
                user_id=0,  # ID unique par canal si besoin
                chatbot_profile=profile,
                chatbot_id=personality,
                user_name="User"
            )
            
            if response and len(response.strip()) > 0:
                print(f"[SUCCESS] HuggingFace: {response[:80]}...")
                return response
            
            # Si HuggingFace échoue complètement
            print(f"[ERROR] HuggingFace API a échoué")
            return "Hmm, j'ai un petit souci technique. Réessaie ! 😊"
            
        except Exception as e:
            print(f"[ERROR] Exception in generate_response: {type(e).__name__}: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return "Désolé, une erreur est survenue. 💫"

ai_client = HuggingFaceAIClient()

@bot.event
async def on_ready():
    print("="*60, flush=True)
    print(f"🔥 BOT READY - HUGGINGFACE API (100% GRATUIT & NSFW)", flush=True)
    print(f"Bot user: {bot.user}", flush=True)
    print(f"Guilds: {len(bot.guilds)}", flush=True)
    print(f"AI Backend: HuggingFace Inference (Mythomax + Nous-Hermes + 2 autres)", flush=True)
    print(f"Gestion: SFW → NSFW automatique, 100% gratuit, sans clé", flush=True)
    print(f"Personalities: {len(PERSONALITIES)}", flush=True)
    print("="*60, flush=True)
    
    # Synchroniser les commandes slash
    try:
        synced = await bot.tree.sync()
        print(f"[SUCCESS] {len(synced)} slash commands synced")
    except Exception as e:
        print(f"[ERROR] Sync error: {e}")
    
    # Definir le statut du bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="En attente | /start pour activer"
        )
    )

@bot.event
async def on_message(message):
    # Ignorer les messages du bot lui-meme
    if message.author == bot.user:
        return
    
    print(f"[MESSAGE] From {message.author.name} in channel {message.channel.id}", flush=True)
    print(f"[MESSAGE] Content: {message.content[:100]}", flush=True)
    
    # Traiter les commandes d'abord
    await bot.process_commands(message)
    
    # Verifier si le bot est actif dans ce canal
    channel_id = message.channel.id
    print(f"[INFO] Checking if bot active in channel {channel_id}")
    print(f"[INFO] bot_active_channels: {dict(bot_active_channels)}")
    
    if not bot_active_channels[channel_id]:
        print(f"[INFO] Bot NOT active in channel {channel_id} - ignoring")
        return
    
    print(f"[INFO] Bot IS active in channel {channel_id}")
    
    # Verifier si le bot est mentionne ou si le message est dans un thread prive
    bot_mentioned = bot.user in message.mentions
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_reply_to_bot = (message.reference and 
                       message.reference.resolved and 
                       message.reference.resolved.author == bot.user)
    
    print(f"[INFO] bot_mentioned={bot_mentioned}, is_dm={is_dm}, is_reply_to_bot={is_reply_to_bot}")
    
    # Repondre si mentionne, en DM, ou en reponse au bot
    if bot_mentioned or is_dm or is_reply_to_bot:
        print(f"[INFO] Bot WILL respond to this message")
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
            
            # Obtenir la personnalite du canal
            personality = channel_personalities[channel_id]
            print(f"[INFO] Using personality: {personality}")
            
            # Generer la reponse
            print(f"[INFO] Calling ai_client.generate_response...")
            response = await ai_client.generate_response(
                conversation_history[channel_id],
                personality=personality
            )
            print(f"[INFO] Response received: {response[:100] if response else 'None'}")
            
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
    """Menu deroulant pour selectionner la personnalite"""
    def __init__(self):
        options = [
            # Femmes jeunes
            discord.SelectOption(label="Luna 25ans - Coquine", description="Femme confiante et seduisante", value="femme_coquine"),
            discord.SelectOption(label="Amelie 27ans - Romantique", description="Femme romantique et tendre", value="femme_douce"),
            discord.SelectOption(label="Victoria 30ans - Dominatrice", description="Femme autoritaire", value="femme_dominante"),
            discord.SelectOption(label="Sophie 23ans - Soumise", description="Femme qui aime obeir", value="femme_soumise"),
            # Femmes matures  
            discord.SelectOption(label="Isabelle 35ans - Fatale", description="Experimentee et sans tabou", value="femme_mature_35"),
            discord.SelectOption(label="Catherine 40ans - Cougar", description="Cougar directe et crue", value="femme_mature_40"),
            discord.SelectOption(label="Nathalie 45ans - Experte", description="Libertine ultra experimentee", value="femme_mature_45"),
            # Hommes jeunes
            discord.SelectOption(label="Damien 28ans - Seducteur", description="Homme charmant et confiant", value="homme_seducteur"),
            discord.SelectOption(label="Alexandre 32ans - Dominant", description="Homme dominant", value="homme_dominant"),
            discord.SelectOption(label="Julien 26ans - Tendre", description="Homme doux et attentionne", value="homme_doux"),
            discord.SelectOption(label="Lucas 24ans - Soumis", description="Homme qui aime obeir", value="homme_soumis"),
            # Hommes matures
            discord.SelectOption(label="Marc 35ans - Experimente", description="Viril et direct", value="homme_mature_35"),
            discord.SelectOption(label="Philippe 40ans - Dominant exp", description="Dominant autoritaire", value="homme_mature_40"),
            discord.SelectOption(label="Richard 45ans - Libertin", description="Expert sans limites", value="homme_mature_45"),
            # Trans/Non-binaire jeunes
            discord.SelectOption(label="Alex 26ans - Trans", description="Trans confiant", value="trans_confiant"),
            discord.SelectOption(label="Sam 25ans - Non-binaire", description="NB fun et geek", value="nonbinaire_joueur"),
            # Trans/Non-binaire matures
            discord.SelectOption(label="Lexa 35ans - Trans exp", description="Trans experimentee", value="trans_mature_35"),
            discord.SelectOption(label="Nova 40ans - Trans libertine", description="Trans sans filtre", value="trans_mature_40"),
            discord.SelectOption(label="Ash 35ans - NB experimente", description="NB franc et direct", value="nonbinaire_mature_35"),
            discord.SelectOption(label="River 40ans - NB libertin", description="NB audacieux", value="nonbinaire_mature_40"),
            # Neutres
            discord.SelectOption(label="Jordan 28ans - Amical", description="Sympathique et ouvert", value="amical"),
            discord.SelectOption(label="Morgan 31ans - Intellectuel", description="Cultive et articule", value="intellectuel")
        ]
        super().__init__(placeholder="Choisissez une personnalite...", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        try:
            # Configuration immediate
            selected_personality = self.values[0]
            channel_id = interaction.channel_id
            bot_active_channels[channel_id] = True
            channel_personalities[channel_id] = selected_personality
            personality_info = PERSONALITIES[selected_personality]
            conversation_history[channel_id].clear()
            
            # Changer le nickname du bot pour prendre le nom du personnage
            try:
                guild = interaction.guild
                if guild:
                    bot_member = guild.me
                    new_nickname = f"{personality_info['name']} ({personality_info['age']})"
                    await bot_member.edit(nick=new_nickname)
                    print(f"[INFO] Bot nickname changed to: {new_nickname}", flush=True)
            except discord.Forbidden:
                print(f"[WARNING] No permission to change nickname", flush=True)
            except Exception as e:
                print(f"[ERROR] Failed to change nickname: {e}", flush=True)
            
            # Creer un bel embed avec toutes les infos
            embed = discord.Embed(
                title=f"{personality_info['name']} - {personality_info['title']}",
                description=personality_info['description'],
                color=personality_info['color']
            )
            
            # Informations sur le personnage
            embed.add_field(name="Genre", value=personality_info['genre'], inline=True)
            embed.add_field(name="Age", value=personality_info['age'], inline=True)
            embed.add_field(name="Traits", value=personality_info['traits'], inline=False)
            
            # Instructions d'interaction
            embed.add_field(
                name="Comment interagir?", 
                value=f"- Mentionnez-moi @{personality_info['name']}\n- Repondez a mes messages\n- Envoyez-moi un message prive", 
                inline=False
            )
            
            embed.set_footer(text=f"Je suis maintenant {personality_info['name']} dans ce serveur")
            
            # Repondre et editer le message original en une seule operation
            await interaction.response.edit_message(embed=embed, view=None)
            
            # Mise a jour du statut (asynchrone, sans bloquer)
            active_count = len([c for c in bot_active_channels.values() if c])
            asyncio.create_task(
                bot.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.playing, 
                    name=f"{personality_info['name']} | {active_count} canal actif"
                ))
            )
        except Exception as e:
            print(f"Erreur dans callback: {e}")
            try:
                await interaction.response.send_message("Erreur lors de l'activation. Reessayez avec /start", ephemeral=True)
            except:
                pass

class PersonalityView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(PersonalitySelect())

@bot.tree.command(name="start", description="Active le bot avec choix de personnalite (admin)")
@is_admin()
async def start_bot(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    if bot_active_channels[channel_id]:
        await interaction.response.send_message("Le bot est deja actif! Utilisez /stop puis /start pour reactiver.", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="Activation du Bot", 
        description="Choisissez la personnalite du bot:",
        color=discord.Color.blue()
    )
    embed.add_field(name="Personnalites", value="Selectionnez dans le menu ci-dessous", inline=False)
    view = PersonalityView()
    
    await interaction.response.send_message(embed=embed, view=view)

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
