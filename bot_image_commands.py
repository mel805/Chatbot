"""
Commandes Discord pour la g?n?ration d'images
? int?grer dans bot.py
"""

# Ajouter apr?s les autres imports
from image_generator import ImageGenerator

# Initialiser le g?n?rateur d'images
image_gen = ImageGenerator()

# Commande pour g?n?rer une image de la personnalit? actuelle
@bot.tree.command(name="generer_image", description="Genere une image de la personnalite actuelle")
@app_commands.describe(
    style="Style de l'image a generer"
)
@app_commands.choices(style=[
    app_commands.Choice(name="Portrait", value="portrait"),
    app_commands.Choice(name="Tenue Decontractee", value="casual"),
    app_commands.Choice(name="Tenue Elegante", value="elegant"),
    app_commands.Choice(name="Lingerie", value="lingerie"),
    app_commands.Choice(name="Maillot de Bain", value="swimsuit"),
    app_commands.Choice(name="Suggestif", value="suggestive"),
    app_commands.Choice(name="Artistique Nu", value="artistic_nude"),
    app_commands.Choice(name="Intime", value="intimate"),
])
async def generate_image(interaction: discord.Interaction, style: str = "portrait"):
    """G?n?re une image de la personnalit? actuelle"""
    
    channel_id = interaction.channel_id
    
    # V?rifier si le bot est actif
    if not bot_active_channels[channel_id]:
        await interaction.response.send_message(
            "? Le bot n'est pas actif dans ce canal. Utilisez `/start` d'abord.",
            ephemeral=True
        )
        return
    
    # V?rifier si c'est un channel NSFW pour les styles NSFW
    nsfw_styles = ["lingerie", "suggestive", "artistic_nude", "intimate"]
    if style in nsfw_styles:
        if hasattr(interaction.channel, 'is_nsfw') and not interaction.channel.is_nsfw():
            await interaction.response.send_message(
                "?? Les images NSFW ne sont disponibles que dans les channels NSFW.",
                ephemeral=True
            )
            return
    
    # Obtenir la personnalit? actuelle
    personality_key = active_channels.get(str(channel_id))
    if not personality_key:
        await interaction.response.send_message(
            "? Aucune personnalit? active. Utilisez `/start` pour en choisir une.",
            ephemeral=True
        )
        return
    
    personality_data = PERSONALITIES.get(personality_key, PERSONALITIES["amical"])
    
    # Mapping des styles vers prompts
    style_prompts = {
        "portrait": "portrait, face focus, beautiful lighting",
        "casual": "casual outfit, relaxed pose, natural setting",
        "elegant": "elegant dress, formal attire, sophisticated",
        "lingerie": "lingerie, sensual pose, bedroom setting, intimate lighting",
        "swimsuit": "swimsuit, beach setting, summer vibes",
        "suggestive": "suggestive pose, intimate setting, artistic, sensual",
        "artistic_nude": "artistic nude, tasteful, professional photography, soft lighting, nsfw",
        "intimate": "intimate scene, bedroom, romantic lighting, passionate, nsfw"
    }
    
    prompt_addition = style_prompts.get(style, "portrait")
    
    # R?pondre imm?diatement (g?n?ration prend du temps)
    await interaction.response.defer()
    
    try:
        # Cr?er embed de g?n?ration
        embed = discord.Embed(
            title="?? G?n?ration d'Image",
            description=f"G?n?ration d'une image de **{personality_data['name']}** en cours...\n\n"
                       f"**Style:** {style.replace('_', ' ').title()}\n"
                       f"? Cela peut prendre 30-60 secondes...",
            color=personality_data.get('color', 0x3498db)
        )
        embed.set_footer(text="Stable Diffusion XL")
        
        await interaction.edit_original_response(embed=embed)
        
        # G?n?rer l'image
        image_url = await image_gen.generate_personality_image(personality_data, prompt_addition)
        
        if image_url:
            # Succ?s
            embed = discord.Embed(
                title=f"? {personality_data['name']}",
                description=f"**Style:** {style.replace('_', ' ').title()}\n"
                           f"**Personnalit?:** {personality_data['title']}",
                color=personality_data.get('color', 0x3498db)
            )
            embed.set_image(url=image_url)
            embed.set_footer(text=f"G?n?r? avec Stable Diffusion XL ? {personality_data['age']}")
            
            await interaction.edit_original_response(embed=embed)
        else:
            # Erreur
            embed = discord.Embed(
                title="? Erreur de G?n?ration",
                description="La g?n?ration d'image a ?chou?. Causes possibles:\n\n"
                           "? API key manquante ou invalide\n"
                           "? Limite de taux d?pass?e\n"
                           "? Service temporairement indisponible\n\n"
                           "R?essayez dans quelques minutes.",
                color=0xe74c3c
            )
            embed.set_footer(text="V?rifiez la configuration de REPLICATE_API_KEY")
            
            await interaction.edit_original_response(embed=embed)
            
    except Exception as e:
        print(f"[ERROR] Image generation error: {e}", flush=True)
        
        embed = discord.Embed(
            title="? Erreur",
            description=f"Une erreur s'est produite lors de la g?n?ration:\n```{str(e)[:200]}```",
            color=0xe74c3c
        )
        
        try:
            await interaction.edit_original_response(embed=embed)
        except:
            pass


@bot.tree.command(name="galerie", description="Affiche des exemples de styles d'images disponibles")
async def show_gallery(interaction: discord.Interaction):
    """Affiche les styles d'images disponibles"""
    
    embed = discord.Embed(
        title="?? Galerie des Styles Disponibles",
        description="Utilisez `/generer_image` avec ces styles:\n",
        color=0x9b59b6
    )
    
    # Styles SFW
    embed.add_field(
        name="?? Styles Standards",
        value="? **Portrait** - Photo de portrait classique\n"
              "? **Tenue D?contract?e** - Look casual et naturel\n"
              "? **Tenue ?l?gante** - Tenue formelle et sophistiqu?e\n"
              "? **Maillot de Bain** - Ambiance plage/piscine",
        inline=False
    )
    
    # Styles NSFW
    if hasattr(interaction.channel, 'is_nsfw') and interaction.channel.is_nsfw():
        embed.add_field(
            name="?? Styles NSFW (Channel NSFW uniquement)",
            value="? **Lingerie** - Lingerie sensuelle\n"
                  "? **Suggestif** - Pose suggestive artistique\n"
                  "? **Artistique Nu** - Nu artistique tasteful\n"
                  "? **Intime** - Sc?ne intime romantique",
            inline=False
        )
    else:
        embed.add_field(
            name="?? Styles NSFW",
            value="*Les styles NSFW sont disponibles uniquement dans les channels NSFW*",
            inline=False
        )
    
    embed.add_field(
        name="?? Exemple",
        value="```/generer_image style:portrait```",
        inline=False
    )
    
    embed.set_footer(text="La g?n?ration prend 30-60 secondes ? Powered by Stable Diffusion XL")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)
