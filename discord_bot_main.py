"""
Bot Discord NSFW avec Boutons Persistants Fonctionnels
Version 3.4 - Boutons corriges et testes
"""

import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
from aiohttp import web
from dotenv import load_dotenv
import copy
import traceback

# Importer les modules existants
from chatbot_manager import ChatbotManager, ChatbotProfile
from enhanced_chatbot_ai import EnhancedChatbotAI
from thread_manager import ThreadManager
from public_chatbots import PUBLIC_CHATBOTS, CATEGORIES
from image_generator import ImageGeneratorNSFW
from level_system import LevelSystem
from level_card_generator import LevelCardGenerator

# Charger .env SEULEMENT s'il existe (local), sinon utiliser les vars d'environnement Render
load_dotenv(override=False)  # Ne pas override les variables système existantes

# Initialiser les gestionnaires
chatbot_manager = ChatbotManager()
chatbot_ai = EnhancedChatbotAI()
thread_manager = ThreadManager()
image_generator = ImageGeneratorNSFW()
level_system = LevelSystem()
card_generator = LevelCardGenerator()

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


# ========== HELPER FUNCTIONS ==========

def check_nsfw_channel(interaction: discord.Interaction) -> bool:
    """Verifie si le canal est NSFW"""
    if isinstance(interaction.channel, discord.DMChannel):
        return False
    return interaction.channel.is_nsfw()


# ========== VUES PERSISTANTES ==========

class MainMenuView(discord.ui.View):
    """Menu principal - Vue temporaire (pas persistante)"""
    
    def __init__(self):
        super().__init__(timeout=300)  # 5 minutes au lieu de None
    
    @discord.ui.button(label="Galerie", style=discord.ButtonStyle.primary, custom_id="main_gallery")
    async def gallery_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Afficher la galerie complete"""
        try:
            print(f"[DEBUG] Bouton Galerie clique par {interaction.user}")
            
            embed = discord.Embed(
                title="Galerie des Chatbots",
                description="Choisissez une categorie :",
                color=discord.Color.blue()
            )
            
            print("[DEBUG] Creation CategoryMenuView...")
            view = CategoryMenuView()
            print("[DEBUG] Envoi du message...")
            
            # EDITER le message original au lieu d'envoyer un nouveau
            await interaction.response.edit_message(embed=embed, view=view)
            print("[DEBUG] Message edite avec succes!")
            
        except Exception as e:
            print(f"[ERREUR] gallery_btn: {e}")
            traceback.print_exc()
            try:
                await interaction.response.send_message(
                    f"[X] Erreur: {str(e)}\nReessayez avec /start",
                    ephemeral=True
                )
            except:
                print("[ERREUR] Impossible d'envoyer message d'erreur")
    
    @discord.ui.button(label="Générer Image", style=discord.ButtonStyle.red, emoji="🎨", custom_id="main_image")
    async def image_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Générer une image NSFW"""
        await interaction.response.defer(ephemeral=False, thinking=True)
        
        try:
            # Vérifier canal NSFW
            if not check_nsfw_channel(interaction):
                await interaction.followup.send(
                    "⚠️ Utilisez un canal NSFW pour générer des images !",
                    ephemeral=True
                )
                return
            
            # Récupérer le chatbot actif pour contextualiser l'image
            user_id = interaction.user.id
            active_chatbot_id = chatbot_manager.get_active_chatbot_id(user_id)
            
            if not active_chatbot_id:
                await interaction.followup.send(
                    "ℹ️ Aucun personnage sélectionné. Génération d'une image générique...",
                    ephemeral=True
                )
                character_desc = ""
                prompt = "a beautiful woman, photorealistic, 8k"
            else:
                profile = chatbot_manager.get_chatbot(user_id, active_chatbot_id)
                character_desc = profile.description if profile else ""
                prompt = f"{profile.name}, {character_desc[:100]}, detailed, high quality"
            
            # Obtenir infos du serveur et du membre
            server_name = interaction.guild.name if interaction.guild else "Discord"
            username = interaction.user.display_name
            
            # Déterminer le type NSFW selon le chatbot actif
            nsfw_type = "artistic"  # Par défaut
            if profile:
                # Adapter le type selon la personnalité du chatbot
                personality_lower = profile.personality.lower()
                if "romantique" in personality_lower or "doux" in personality_lower:
                    nsfw_type = "romantic"
                elif "intense" in personality_lower or "dominant" in personality_lower:
                    nsfw_type = "intense"
                elif "fantaisie" in personality_lower or "magique" in personality_lower:
                    nsfw_type = "fantasy"
                elif "sensuel" in personality_lower:
                    nsfw_type = "softcore"
            
            # Générer l'image avec personnalisation
            await interaction.followup.send(
                f"🎨 Génération unique pour **{username}** sur **{server_name}**...\n"
                f"Style: {nsfw_type.capitalize()}"
            )
            
            image_url = await image_generator.generate(
                prompt=prompt,
                character_desc=character_desc,
                server_name=server_name,
                username=username,
                nsfw_type=nsfw_type
            )
            
            if image_url:
                embed = discord.Embed(
                    title="🎨 Image générée !",
                    description=f"Prompt: {prompt[:200]}",
                    color=discord.Color.purple()
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"✨ Généré uniquement pour {username} sur {server_name}")
                embed.add_field(
                    name="🎭 Style",
                    value=nsfw_type.capitalize(),
                    inline=True
                )
                embed.add_field(
                    name="👤 Membre",
                    value=username,
                    inline=True
                )
                embed.add_field(
                    name="🏠 Serveur",
                    value=server_name,
                    inline=True
                )
                
                await interaction.channel.send(embed=embed)
            else:
                await interaction.followup.send(
                    "❌ Échec de génération. Réessayez !",
                    ephemeral=True
                )
        
        except Exception as e:
            print(f"[ERREUR] image_btn: {e}")
            traceback.print_exc()
            await interaction.followup.send(
                f"❌ Erreur: {str(e)}",
                ephemeral=True
            )
    
    @discord.ui.button(label="Discuter", style=discord.ButtonStyle.green, custom_id="main_chat")
    async def chat_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Creer conversation"""
        # DEFER IMMEDIATEMENT (Discord timeout = 3 secondes !)
        await interaction.response.defer(ephemeral=True)
        
        try:
            print(f"[DEBUG] === DEBUT CREATION THREAD ===")
            user_id = interaction.user.id
            print(f"[DEBUG] User ID: {user_id}")
            
            # Utiliser get_active_chatbot_id() pour avoir l'ID (string)
            active_chatbot_id = chatbot_manager.get_active_chatbot_id(user_id)
            print(f"[DEBUG] Active chatbot ID: {active_chatbot_id}")
            
            if not active_chatbot_id:
                await interaction.followup.send(
                    "[X] Choisissez d'abord un chatbot avec Galerie !",
                    ephemeral=True
                )
                return
            
            # Verifier thread existant
            existing_thread = thread_manager.get_user_thread(user_id)
            if existing_thread:
                thread = interaction.guild.get_thread(existing_thread["thread_id"])
                if thread:
                    await interaction.followup.send(
                        f"[OK] Conversation deja active : {thread.mention}",
                        ephemeral=True
                    )
                    return
            
            # Recuperer le profil
            print(f"[DEBUG] Recuperation profil avec ID: {active_chatbot_id}")
            profile = chatbot_manager.get_chatbot(user_id, active_chatbot_id)
            print(f"[DEBUG] Profile recupere: {profile}")
            
            if profile:
                print(f"[DEBUG] Profile name: {profile.name}")
            else:
                print(f"[DEBUG] Profile est None!")
            
            if not profile:
                print(f"[ERREUR] Profil non trouve pour user_id={user_id}, chatbot_id={active_chatbot_id}")
                await interaction.followup.send(
                    f"[X] Erreur: Chatbot non trouve (ID: {active_chatbot_id})\nReessayez avec Galerie !",
                    ephemeral=True
                )
                return
            
            thread = await interaction.channel.create_thread(
                name=f"?? {profile.name}",
                type=discord.ChannelType.private_thread,
                auto_archive_duration=1440
            )
            
            await thread.add_user(interaction.user)
            
            # create_thread attend 4 parametres : user_id, thread_id, chatbot_name, chatbot_id
            print(f"[DEBUG] Creation entree thread manager...")
            thread_manager.create_thread(user_id, thread.id, profile.name, active_chatbot_id)
            print(f"[DEBUG] Thread manager OK - chatbot_id: {active_chatbot_id}")
            
            # Debut direct de la conversation
            first_message = await chatbot_ai.get_response(
                "Salut", user_id, profile, active_chatbot_id, interaction.user.display_name
            )
            await thread.send(first_message)
            
            await interaction.followup.send(
                f"[OK] Conversation creee ! -> {thread.mention}\nTapez directement !",
                ephemeral=True
            )
            print(f"[DEBUG] === THREAD CREE AVEC SUCCES ===")
            
        except Exception as e:
            print(f"[ERREUR] chat_btn: {e}")
            traceback.print_exc()
            try:
                await interaction.followup.send(f"[X] Erreur: {str(e)[:100]}", ephemeral=True)
            except:
                pass
    
    @discord.ui.button(label="Aide", style=discord.ButtonStyle.gray, custom_id="main_help")
    async def help_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Afficher l'aide"""
        embed = discord.Embed(
            title="Comment Utiliser",
            description="**Interface a boutons simple !**",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="1. Galerie",
            value="Cliquez **Galerie** pour voir les chatbots",
            inline=False
        )
        
        embed.add_field(
            name="2. Choisir",
            value="Selectionnez categorie puis chatbot",
            inline=False
        )
        
        embed.add_field(
            name="3. Discuter",
            value="Cliquez **Discuter** pour creer thread",
            inline=False
        )
        
        embed.add_field(
            name="4. Taper",
            value="Dans le thread, tapez directement !",
            inline=False
        )
        
        # EDITER le message original
        await interaction.response.edit_message(embed=embed, view=self)


class CategoryMenuView(discord.ui.View):
    """Menu de selection de categorie"""
    
    def __init__(self):
        super().__init__(timeout=600)
        
        print("[DEBUG] Init CategoryMenuView")
        
        # Menu deroulant SANS emojis (probleme d'encodage)
        options = [
            discord.SelectOption(label="Romantique", value="romantique", description="Emma, Lucas, Alex"),
            discord.SelectOption(label="Intense", value="intense", description="Sophia, Damien, Isabelle"),
            discord.SelectOption(label="Doux", value="doux", description="Lily, Maya, Lucas"),
            discord.SelectOption(label="Dominant", value="dominant", description="Damien, Sophia"),
            discord.SelectOption(label="Soumis", value="soumis", description="Lily, Yuki"),
            discord.SelectOption(label="Fantaisie", value="fantaisie", description="Luna, Aria, Eden"),
            discord.SelectOption(label="Masculin", value="masculin", description="Alex, Damien, Lucas, Sam"),
            discord.SelectOption(label="Feminin", value="feminin", description="Emma, Sophia, Lily..."),
            discord.SelectOption(label="Non-binaire", value="non_binaire", description="Eden, Sam"),
        ]
        
        select = discord.ui.Select(
            placeholder="Choisissez une categorie...",
            options=options,
            custom_id="category_select_menu"
        )
        select.callback = self.category_callback
        self.add_item(select)
        
        print(f"[DEBUG] Select ajoute avec {len(options)} options")
    
    async def category_callback(self, interaction: discord.Interaction):
        """Callback pour la selection de categorie"""
        try:
            print(f"[DEBUG] category_callback appele")
            category = interaction.data["values"][0]
            print(f"[DEBUG] Categorie choisie: {category}")
            
            chatbot_ids = CATEGORIES.get(category, [])
            print(f"[DEBUG] {len(chatbot_ids)} chatbots trouves")
            
            if not chatbot_ids:
                await interaction.response.send_message("[X] Aucun chatbot ici", ephemeral=True)
                return
            
            embed = discord.Embed(
                title=f"Chatbots - {category.capitalize()}",
                description="Cliquez sur un chatbot :",
                color=discord.Color.purple()
            )
            
            view = ChatbotButtonsView(chatbot_ids, category)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            print("[DEBUG] Message avec boutons chatbots envoye")
            
        except Exception as e:
            print(f"[ERREUR] category_callback: {e}")
            traceback.print_exc()
            try:
                await interaction.response.send_message(f"[X] Erreur: {str(e)}", ephemeral=True)
            except:
                pass


class ChatbotButtonsView(discord.ui.View):
    """Boutons pour chaque chatbot"""
    
    def __init__(self, chatbot_ids: list, category: str):
        super().__init__(timeout=600)
        
        print(f"[DEBUG] Init ChatbotButtonsView avec {len(chatbot_ids)} chatbots")
        
        # Limiter a 10 chatbots max
        for idx, chatbot_id in enumerate(chatbot_ids[:10]):
            profile = PUBLIC_CHATBOTS[chatbot_id]
            button = discord.ui.Button(
                label=profile.name,
                style=discord.ButtonStyle.secondary,
                custom_id=f"bot_{chatbot_id}_{idx}",
                row=idx // 5
            )
            button.callback = self.make_chatbot_callback(chatbot_id, profile)
            self.add_item(button)
            print(f"[DEBUG] Bouton ajoute: {profile.name}")
    
    def make_chatbot_callback(self, chatbot_id: str, profile: ChatbotProfile):
        """Creer callback pour un chatbot"""
        async def callback(interaction: discord.Interaction):
            try:
                print(f"[DEBUG] Chatbot selectionne: {profile.name}")
                
                embed = discord.Embed(
                    title=f"{profile.name}",
                    description=profile.personality[:300],
                    color=discord.Color.gold()
                )
                
                embed.add_field(name="Genre", value=profile.gender, inline=True)
                embed.add_field(name="Age", value=f"{profile.age} ans", inline=True)
                embed.add_field(name="Type", value=profile.relationship_type, inline=True)
                
                if profile.appearance:
                    embed.add_field(name="Apparence", value=profile.appearance[:150], inline=False)
                
                view = UseChatbotView(chatbot_id, profile)
                await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
                
            except Exception as e:
                print(f"[ERREUR] chatbot callback: {e}")
                traceback.print_exc()
                try:
                    await interaction.response.send_message("[X] Erreur", ephemeral=True)
                except:
                    pass
        
        return callback


class UseChatbotView(discord.ui.View):
    """Bouton pour utiliser un chatbot"""
    
    def __init__(self, chatbot_id: str, profile: ChatbotProfile):
        super().__init__(timeout=600)
        self.chatbot_id = chatbot_id
        self.profile = profile
    
    @discord.ui.button(label="Utiliser ce chatbot", style=discord.ButtonStyle.success, custom_id="use_this_bot")
    async def use_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Activer ce chatbot"""
        try:
            print(f"[DEBUG] === DEBUT ACTIVATION ===")
            print(f"[DEBUG] Chatbot: {self.profile.name}")
            print(f"[DEBUG] Chatbot ID: {self.chatbot_id}")
            print(f"[DEBUG] User ID: {interaction.user.id}")
            
            user_id = interaction.user.id
            public_chatbot_id = f"public_{self.chatbot_id}"
            print(f"[DEBUG] Public chatbot ID: {public_chatbot_id}")
            
            # Copier le profil
            print(f"[DEBUG] Copie du profil...")
            try:
                user_profile = copy.deepcopy(self.profile)
                # Ajouter l'attribut is_public manquant
                user_profile.is_public = True
                print(f"[DEBUG] Profil copie OK (is_public ajoute)")
            except Exception as e:
                print(f"[ERREUR] Copie profil: {e}")
                raise
            
            # Verifier existence
            print(f"[DEBUG] Verification existence...")
            try:
                exists = chatbot_manager.chatbot_exists(user_id, public_chatbot_id)
                print(f"[DEBUG] Existe deja: {exists}")
            except Exception as e:
                print(f"[ERREUR] Verification existence: {e}")
                raise
            
            # Creer ou activer
            if exists:
                print(f"[DEBUG] Activation chatbot existant...")
                try:
                    chatbot_manager.set_active_chatbot(user_id, public_chatbot_id)
                    print(f"[DEBUG] Chatbot active OK")
                except Exception as e:
                    print(f"[ERREUR] Activation: {e}")
                    raise
            else:
                print(f"[DEBUG] Creation nouveau chatbot...")
                try:
                    chatbot_manager.create_chatbot(user_id, public_chatbot_id, user_profile)
                    print(f"[DEBUG] Chatbot cree OK")
                    chatbot_manager.set_active_chatbot(user_id, public_chatbot_id)
                    print(f"[DEBUG] Chatbot active OK")
                except Exception as e:
                    print(f"[ERREUR] Creation/Activation: {e}")
                    raise
            
            # Message de succes
            print(f"[DEBUG] Creation embed...")
            embed = discord.Embed(
                title=f"[OK] {self.profile.name} est actif !",
                description=f"**{self.profile.name}** est pret a discuter !",
                color=discord.Color.green()
            )
            
            embed.add_field(
                name="Prochaine etape",
                value="Tapez /start et cliquez **Discuter** !",
                inline=False
            )
            
            print(f"[DEBUG] Envoi message...")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(f"[DEBUG] === ACTIVATION REUSSIE ===")
            
        except Exception as e:
            print(f"[ERREUR] use_btn GENERALE: {e}")
            traceback.print_exc()
            try:
                error_msg = f"[X] Erreur activation: {str(e)[:100]}"
                await interaction.response.send_message(error_msg, ephemeral=True)
            except:
                print(f"[ERREUR] Impossible d'envoyer message d'erreur")
                pass


# ========== EVENEMENTS ==========

@bot.event
async def on_ready():
    """Bot pret"""
    print(f"[OK] Bot connecte : {bot.user}")
    print(f"[OK] Serveurs : {len(bot.guilds)}")
    
    # Note: Plus besoin d'enregistrer la vue car elle n'est plus persistante
    # bot.add_view(MainMenuView()) - RETIRE
    print("[OK] Vues configurees (non-persistantes)")
    
    # Sync commandes
    try:
        synced = await bot.tree.sync()
        print(f"[OK] {len(synced)} commandes synchronisees")
    except Exception as e:
        print(f"[ERREUR] Sync commandes : {e}")
    
    print("[OK] Bot pret !")


@bot.event
async def on_message(message):
    """Gerer les messages dans les threads"""
    if message.author.bot:
        return
    
    await bot.process_commands(message)
    
    # Ajouter XP pour chaque message (sauf les DM)
    if not isinstance(message.channel, discord.DMChannel):
        try:
            level_up, old_level, new_level = level_system.add_xp(message.author.id)
            
            # Si level up, envoyer un message de félicitations
            if level_up:
                embed = discord.Embed(
                    title="🎉 Level Up!",
                    description=f"Félicitations {message.author.mention} !\nTu es maintenant **niveau {new_level}** !",
                    color=discord.Color.gold()
                )
                embed.add_field(
                    name="💡 Astuce",
                    value="Utilise `/rank` pour voir ta carte de level !",
                    inline=False
                )
                await message.channel.send(embed=embed, delete_after=10)
                print(f"[LEVEL UP] {message.author} : {old_level} -> {new_level}")
        except Exception as e:
            print(f"[ERREUR] Ajout XP: {e}")
    
    # Gerer threads prives
    if isinstance(message.channel, discord.Thread):
        print(f"[DEBUG] Message dans thread {message.channel.id} par {message.author}")
        
        try:
            if thread_manager.is_active_thread(message.channel.id):
                print(f"[DEBUG] Thread actif detecte")
                thread_info = thread_manager.get_thread_by_id(message.channel.id)
                print(f"[DEBUG] Thread info: {thread_info}")
                
                if thread_info and thread_info["owner_id"] == message.author.id:
                    print(f"[DEBUG] Owner verifie OK")
                    user_id = message.author.id
                    chatbot_id = thread_info["chatbot_id"]
                    print(f"[DEBUG] Chatbot ID: {chatbot_id}")
                    
                    profile = chatbot_manager.get_chatbot(user_id, chatbot_id)
                    print(f"[DEBUG] Profile: {profile}")
                    
                    if profile:
                        print(f"[DEBUG] Profile trouve, envoi a l'IA...")
                        async with message.channel.typing():
                            try:
                                response = await chatbot_ai.get_response(
                                    message.content, user_id, profile, chatbot_id, message.author.display_name
                                )
                                print(f"[DEBUG] Reponse IA recue: {response[:100]}...")
                            except Exception as e:
                                print(f"[ERREUR] Erreur API IA: {e}")
                                traceback.print_exc()
                                response = f"Desole, j'ai un probleme technique... Reessaye dans un instant ! ??"
                        
                        chatbot_manager.increment_message_count(user_id, chatbot_id)
                        thread_manager.increment_message_count(message.channel.id)
                        
                        await message.channel.send(response)
                        print(f"[DEBUG] Reponse envoyee!")
                    else:
                        print(f"[ERREUR] Profile non trouve pour user {user_id}, chatbot {chatbot_id}")
                else:
                    print(f"[DEBUG] Owner non verifie ou thread_info null")
            else:
                print(f"[DEBUG] Thread non actif")
        except Exception as e:
            print(f"[ERREUR] on_message exception: {e}")
            traceback.print_exc()


# ========== COMMANDES ==========

@bot.tree.command(name="start", description="Menu principal")
async def start_cmd(interaction: discord.Interaction):
    """Afficher le menu principal avec boutons"""
    
    if not check_nsfw_channel(interaction):
        await interaction.response.send_message(
            "[X] Commande NSFW uniquement !",
            ephemeral=True
        )
        return
    
    # Creer une nouvelle instance de vue a chaque fois (pas de persistance)
    view = MainMenuView()
    view.timeout = 300  # 5 minutes au lieu de None
    
    embed = discord.Embed(
        title="Bot Chatbot NSFW",
        description=(
            "**Menu Principal - Interface a Boutons**\n\n"
            "**Galerie** - Voir les 13 chatbots\n"
            "**Discuter** - Creer conversation\n"
            "**Aide** - Guide"
        ),
        color=discord.Color.blue()
    )
    
    embed.set_footer(text="Cliquez sur les boutons !")
    
    await interaction.response.send_message(embed=embed, view=view)
    print(f"[DEBUG] Menu principal envoye a {interaction.user}")


@bot.tree.command(name="stop", description="Terminer conversation")
async def stop_cmd(interaction: discord.Interaction):
    """Terminer la conversation"""
    
    if not check_nsfw_channel(interaction):
        await interaction.response.send_message("[X] NSFW uniquement !", ephemeral=True)
        return
    
    user_id = interaction.user.id
    thread_info = thread_manager.get_user_thread(user_id)
    
    if not thread_info:
        await interaction.response.send_message("[X] Pas de conversation active", ephemeral=True)
        return
    
    thread = interaction.guild.get_thread(thread_info["thread_id"])
    
    if thread:
        msg_count = thread_info["message_count"]
        await thread.send(f"Termine ! {msg_count} messages echanges.")
        await thread.edit(archived=True, locked=True)
    
    thread_manager.close_thread(thread_info["thread_id"])
    
    await interaction.response.send_message("[OK] Conversation terminee !", ephemeral=True)


@bot.tree.command(name="generate_image", description="Générer une image NSFW personnalisée")
async def generate_image_command(
    interaction: discord.Interaction,
    prompt: str
):
    """Commande pour générer une image avec prompt personnalisé"""
    
    # Vérifier canal NSFW
    if not check_nsfw_channel(interaction):
        await interaction.response.send_message(
            "⚠️ Utilisez un canal NSFW pour générer des images !",
            ephemeral=True
        )
        return
    
    await interaction.response.defer(thinking=True)
    
    try:
        # Récupérer le chatbot actif pour contextualiser
        user_id = interaction.user.id
        active_chatbot_id = chatbot_manager.get_active_chatbot_id(user_id)
        
        character_desc = ""
        if active_chatbot_id:
            profile = chatbot_manager.get_chatbot(user_id, active_chatbot_id)
            if profile:
                character_desc = profile.description
        
        # Obtenir infos du serveur et du membre
        server_name = interaction.guild.name if interaction.guild else "Discord"
        username = interaction.user.display_name
        
        # Déterminer le type NSFW selon le chatbot ou le prompt
        nsfw_type = "artistic"  # Par défaut
        if character_desc:
            personality_lower = character_desc.lower()
            if "romantic" in personality_lower or "love" in personality_lower:
                nsfw_type = "romantic"
            elif "intense" in personality_lower or "hard" in personality_lower:
                nsfw_type = "intense"
            elif "fantasy" in personality_lower or "magic" in personality_lower:
                nsfw_type = "fantasy"
        
        # Générer l'image avec personnalisation unique
        await interaction.followup.send(
            f"🎨 Génération unique pour **{username}** sur **{server_name}**...\n"
            f"Prompt: **{prompt[:80]}**... | Style: {nsfw_type.capitalize()}"
        )
        
        image_url = await image_generator.generate(
            prompt=prompt,
            character_desc=character_desc,
            server_name=server_name,
            username=username,
            nsfw_type=nsfw_type
        )
        
        if image_url:
            embed = discord.Embed(
                title="🎨 Image générée !",
                description=f"**Prompt:** {prompt}",
                color=discord.Color.purple()
            )
            embed.set_image(url=image_url)
            embed.set_footer(text=f"✨ Image unique pour {username} sur {server_name}")
            embed.add_field(
                name="🎭 Style NSFW",
                value=nsfw_type.capitalize(),
                inline=True
            )
            embed.add_field(
                name="👤 Créé par",
                value=username,
                inline=True
            )
            embed.add_field(
                name="🏠 Serveur",
                value=server_name,
                inline=True
            )
            
            await interaction.channel.send(embed=embed)
        else:
            await interaction.followup.send(
                "❌ Échec de génération. Réessayez avec un autre prompt !",
                ephemeral=True
            )
    
    except Exception as e:
        print(f"[ERREUR] generate_image_command: {e}")
        traceback.print_exc()
        await interaction.followup.send(
            f"❌ Erreur: {str(e)}",
            ephemeral=True
        )


@bot.tree.command(name="rank", description="Voir ta carte de level unique")
async def rank_command(interaction: discord.Interaction, member: discord.Member = None):
    """Affiche la carte de level d'un membre"""
    
    await interaction.response.defer(thinking=True)
    
    try:
        # Si aucun membre spécifié, utiliser l'auteur de la commande
        target_member = member or interaction.user
        
        # Récupérer les infos de niveau
        level_info = level_system.get_level_info(target_member.id)
        rank = level_system.get_user_rank(target_member.id)
        
        print(f"[DEBUG] Génération carte pour {target_member.name}...")
        
        # Générer la carte
        card_image = await card_generator.generate_card(
            username=target_member.name,
            discriminator=target_member.discriminator,
            avatar_url=str(target_member.display_avatar.url),
            level=level_info["level"],
            xp=level_info["xp_progress"],
            xp_needed=level_info["xp_needed"],
            rank=rank,
            total_messages=level_info["total_messages"],
            user_id=target_member.id
        )
        
        # Créer le fichier Discord
        file = discord.File(card_image, filename=f"rank_{target_member.id}.png")
        
        # Embed avec la carte
        embed = discord.Embed(
            title=f"📊 Carte de Level - {target_member.name}",
            color=discord.Color.purple()
        )
        embed.set_image(url=f"attachment://rank_{target_member.id}.png")
        embed.set_footer(text="✨ Chaque carte a un design unique !")
        
        await interaction.followup.send(embed=embed, file=file)
        print(f"[SUCCESS] Carte envoyée pour {target_member.name}")
        
    except Exception as e:
        print(f"[ERREUR] rank_command: {e}")
        traceback.print_exc()
        await interaction.followup.send(
            f"❌ Erreur lors de la génération de la carte: {str(e)}",
            ephemeral=True
        )


@bot.tree.command(name="generate_unique", description="Générer une image NSFW vraiment unique avec style personnalisé")
async def generate_unique_command(
    interaction: discord.Interaction,
    prompt: str,
    style: str = "artistic"
):
    """Commande pour générer une image avec style NSFW choisi"""
    
    # Vérifier canal NSFW
    if not check_nsfw_channel(interaction):
        await interaction.response.send_message(
            "⚠️ Utilisez un canal NSFW pour générer des images !",
            ephemeral=True
        )
        return
    
    await interaction.response.defer(thinking=True)
    
    try:
        # Valider le style
        valid_styles = ["softcore", "romantic", "intense", "fantasy", "artistic"]
        nsfw_type = style.lower() if style.lower() in valid_styles else "artistic"
        
        # Obtenir infos contextuelles
        server_name = interaction.guild.name if interaction.guild else "Discord"
        username = interaction.user.display_name
        
        # Récupérer le chatbot actif pour contexte
        user_id = interaction.user.id
        active_chatbot_id = chatbot_manager.get_active_chatbot_id(user_id)
        
        character_desc = ""
        if active_chatbot_id:
            profile = chatbot_manager.get_chatbot(user_id, active_chatbot_id)
            if profile:
                character_desc = profile.description
        
        # Message de génération
        await interaction.followup.send(
            f"🎨 **Génération UNIQUE en cours...**\n"
            f"📍 Serveur: **{server_name}**\n"
            f"👤 Membre: **{username}**\n"
            f"🎭 Style: **{nsfw_type.capitalize()}**\n"
            f"💭 Prompt: *{prompt[:100]}*..."
        )
        
        # Générer l'image unique
        image_url = await image_generator.generate(
            prompt=prompt,
            character_desc=character_desc,
            server_name=server_name,
            username=username,
            nsfw_type=nsfw_type,
            prefer_speed=True
        )
        
        if image_url:
            embed = discord.Embed(
                title="🎨 Image Unique Générée !",
                description=(
                    f"**Prompt:** {prompt}\n\n"
                    f"Cette image est **100% unique**, générée spécialement pour "
                    f"**{username}** sur le serveur **{server_name}** avec un style **{nsfw_type}** !"
                ),
                color=discord.Color.purple()
            )
            embed.set_image(url=image_url)
            
            # Infos détaillées
            embed.add_field(
                name="🎭 Style NSFW",
                value=nsfw_type.capitalize(),
                inline=True
            )
            embed.add_field(
                name="👤 Créé pour",
                value=username,
                inline=True
            )
            embed.add_field(
                name="🏠 Serveur",
                value=server_name,
                inline=True
            )
            
            embed.set_footer(text=f"✨ Chaque génération est vraiment unique | Seed basé sur {server_name}+{username}+timestamp")
            
            await interaction.channel.send(embed=embed)
        else:
            await interaction.followup.send(
                "❌ Échec de génération. Réessayez avec un autre prompt !",
                ephemeral=True
            )
    
    except Exception as e:
        print(f"[ERREUR] generate_unique_command: {e}")
        traceback.print_exc()
        await interaction.followup.send(
            f"❌ Erreur: {str(e)}",
            ephemeral=True
        )


@bot.tree.command(name="leaderboard", description="Voir le classement des niveaux")
async def leaderboard_command(interaction: discord.Interaction, top: int = 10):
    """Affiche le classement des meilleurs joueurs"""
    
    await interaction.response.defer()
    
    try:
        # Limiter à 25 max
        top = min(max(top, 1), 25)
        
        # Récupérer le leaderboard
        leaderboard = level_system.get_leaderboard(limit=top)
        
        if not leaderboard:
            await interaction.followup.send(
                "📊 Aucune donnée de classement disponible !",
                ephemeral=True
            )
            return
        
        # Créer l'embed
        embed = discord.Embed(
            title=f"🏆 Classement - Top {top}",
            description="Les membres les plus actifs du serveur !",
            color=discord.Color.gold()
        )
        
        # Ajouter les utilisateurs
        leaderboard_text = ""
        for idx, (user_id_str, user_data) in enumerate(leaderboard, 1):
            user_id = int(user_id_str)
            
            # Essayer de récupérer le membre
            try:
                member = await interaction.guild.fetch_member(user_id)
                name = member.display_name
            except:
                name = f"Utilisateur {user_id}"
            
            level = level_system.calculate_level(user_data["xp"])
            xp = user_data["xp"]
            messages = user_data["total_messages"]
            
            # Emojis pour le top 3
            medal = ""
            if idx == 1:
                medal = "🥇 "
            elif idx == 2:
                medal = "🥈 "
            elif idx == 3:
                medal = "🥉 "
            
            leaderboard_text += (
                f"{medal}**#{idx} - {name}**\n"
                f"├ Niveau: {level} | XP: {xp:,}\n"
                f"└ Messages: {messages:,}\n\n"
            )
        
        embed.description = leaderboard_text
        
        # Ajouter la position de l'utilisateur s'il n'est pas dans le top
        user_rank = level_system.get_user_rank(interaction.user.id)
        if user_rank > top:
            user_info = level_system.get_level_info(interaction.user.id)
            embed.add_field(
                name="📍 Ta position",
                value=(
                    f"Rang: #{user_rank}\n"
                    f"Niveau: {user_info['level']} | XP: {user_info['xp']:,}\n"
                    f"Messages: {user_info['total_messages']:,}"
                ),
                inline=False
            )
        
        embed.set_footer(text="💡 Utilise /rank pour voir ta carte unique !")
        
        await interaction.followup.send(embed=embed)
        print(f"[SUCCESS] Leaderboard envoyé (top {top})")
        
    except Exception as e:
        print(f"[ERREUR] leaderboard_command: {e}")
        traceback.print_exc()
        await interaction.followup.send(
            f"❌ Erreur: {str(e)}",
            ephemeral=True
        )


# ========== HTTP SERVER ==========

async def health_check(request):
    return web.Response(text="OK", status=200)

async def root(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bot Discord NSFW - V3.4</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 50px auto; padding: 20px; background: #f0f0f0; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #5865F2; }
            .status { color: #43B581; font-size: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bot Discord NSFW - Boutons Fonctionnels</h1>
            <p class="status">[OK] Bot en ligne</p>
            <h2>Version 3.4 - Boutons corriges et testes</h2>
            <p>Interface a boutons avec debug complet</p>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', root)
    app.router.add_get('/health', health_check)
    
    port = int(os.getenv('PORT', 10000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print(f"[OK] HTTP server sur port {port}")


# ========== MAIN ==========

async def main():
    asyncio.create_task(start_web_server())
    await asyncio.sleep(1)
    
    # Debug: afficher TOUTES les variables d'environnement
    print("\n" + "="*80)
    print("🔍 DIAGNOSTIC COMPLET DES VARIABLES D'ENVIRONNEMENT 🔍")
    print("="*80)
    print("[DEBUG] ========================================")
    print("[DEBUG] Vérification des variables d'environnement...")
    print(f"[DEBUG] Nombre total de variables: {len(os.environ)}")
    print("[DEBUG] ========================================")
    
    print(f"[DEBUG] Variables contenant 'TOKEN' ou 'DISCORD':")
    found_discord = False
    for key in os.environ.keys():
        if 'TOKEN' in key.upper() or 'DISCORD' in key.upper():
            value = os.environ[key]
            print(f"[DEBUG]   ✓ {key}: {value[:20] if value else '[VIDE]'}...")
            found_discord = True
    
    if not found_discord:
        print("[DEBUG]   ✗ AUCUNE variable contenant TOKEN ou DISCORD trouvée !")
    
    print("[DEBUG] ========================================")
    print("[DEBUG] Toutes les variables d'environnement disponibles:")
    for key in sorted(os.environ.keys()):
        value = os.environ[key]
        # Masquer les valeurs sensibles mais montrer qu'elles existent
        if any(secret in key.upper() for secret in ['TOKEN', 'KEY', 'SECRET', 'PASSWORD']):
            print(f"[DEBUG]   - {key}: [MASQUÉ - {len(value)} caractères]")
        else:
            print(f"[DEBUG]   - {key}: {value[:50]}...")
    print("[DEBUG] ========================================")
    
    # Essayer plusieurs méthodes pour obtenir le token
    print("[DEBUG] Tentatives de récupération du token:")
    
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    print(f"[DEBUG] 1. os.getenv('DISCORD_BOT_TOKEN'): {'✓ TROUVÉ' if TOKEN else '✗ NON TROUVÉ'}")
    
    if not TOKEN:
        TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
        print(f"[DEBUG] 2. os.environ.get('DISCORD_BOT_TOKEN'): {'✓ TROUVÉ' if TOKEN else '✗ NON TROUVÉ'}")
    
    if not TOKEN:
        # Essayer de lire directement depuis environ
        try:
            TOKEN = os.environ['DISCORD_BOT_TOKEN']
            print(f"[DEBUG] 3. os.environ['DISCORD_BOT_TOKEN']: ✓ TROUVÉ")
        except KeyError:
            print(f"[DEBUG] 3. os.environ['DISCORD_BOT_TOKEN']: ✗ NON TROUVÉ (KeyError)")
    
    print("[DEBUG] ========================================")
    print("="*80)
    print("🎯 RÉSULTAT DU DIAGNOSTIC 🎯")
    print("="*80)
    
    if not TOKEN:
        print("\n❌ ❌ ❌ TOKEN MANQUANT ❌ ❌ ❌")
        print("[X] Token manquant !")
        print("[ERREUR] DISCORD_BOT_TOKEN n'est pas défini dans l'environnement")
        print("[SOLUTION] Dans Render Dashboard:")
        print("  1. Environment → Add Environment Variable")
        print("  2. Key: DISCORD_BOT_TOKEN")
        print("  3. Value: [votre token Discord]")
        print("  4. Save Changes → Redéployer")
        print("="*80 + "\n")
        return
    
    print(f"\n✅ ✅ ✅ TOKEN TROUVÉ ✅ ✅ ✅")
    print(f"[OK] Token Discord trouvé ({len(TOKEN)} caractères)")
    print("="*80 + "\n")
    
    print("[OK] Demarrage bot avec boutons persistants...")
    await bot.start(TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[OK] Bot arrete")
