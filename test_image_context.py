"""
Test de validation du fix de g?n?ration d'images contextuelle
V?rifie que les v?tements sont d?tect?s et prioris?s
"""

import asyncio
from image_generator import ImageGenerator

# Donn?es de test pour une personnalit?
test_personality = {
    "name": "Luna",
    "genre": "Femme",
    "age": "25 ans",
    "description": "Confiante et seduisante",
    "visual": "long silver hair, purple eyes, petite curvy figure"
}

async def test_clothing_detection():
    """Test 1: D?tection de robe l?g?re"""
    print("\n" + "="*60)
    print("TEST 1: D?tection de Robe L?g?re")
    print("="*60)
    
    generator = ImageGenerator()
    conversation = [
        "Bonjour !",
        "Je porte une robe l?g?re aujourd'hui",
        "Je suis dans ma chambre"
    ]
    
    print("\nConversation test:")
    for msg in conversation:
        print(f"  - {msg}")
    
    print("\n--- G?n?ration de l'image ---")
    image_url = await generator.generate_contextual_image(test_personality, conversation)
    
    print(f"\nR?sultat: {image_url[:100] if image_url else 'None'}...")
    print("\n? V?rifier dans les logs:")
    print("  - '[IMAGE] Clothing detected: robe l?g?re' doit apparaitre")
    print("  - '[IMAGE] PRIORITY: Clothing context added' doit apparaitre")
    print("  - 'nude' NE doit PAS apparaitre dans le prompt")

async def test_nudity_only():
    """Test 2: Nudit? sans v?tements"""
    print("\n" + "="*60)
    print("TEST 2: Nudit? (sans v?tements mentionn?s)")
    print("="*60)
    
    generator = ImageGenerator()
    conversation = [
        "Salut",
        "Je suis compl?tement nue",
        "Sur le lit"
    ]
    
    print("\nConversation test:")
    for msg in conversation:
        print(f"  - {msg}")
    
    print("\n--- G?n?ration de l'image ---")
    image_url = await generator.generate_contextual_image(test_personality, conversation)
    
    print(f"\nR?sultat: {image_url[:100] if image_url else 'None'}...")
    print("\n? V?rifier dans les logs:")
    print("  - '[IMAGE] Nudity context detected (no clothing mentioned)' doit apparaitre")
    print("  - 'nude bare skin' doit apparaitre dans le prompt")

async def test_negation():
    """Test 3: N?gation de nudit?"""
    print("\n" + "="*60)
    print("TEST 3: N?gation ('je ne suis pas nue')")
    print("="*60)
    
    generator = ImageGenerator()
    conversation = [
        "Coucou",
        "Je ne suis pas nue",
        "J'ai une chemise"
    ]
    
    print("\nConversation test:")
    for msg in conversation:
        print(f"  - {msg}")
    
    print("\n--- G?n?ration de l'image ---")
    image_url = await generator.generate_contextual_image(test_personality, conversation)
    
    print(f"\nR?sultat: {image_url[:100] if image_url else 'None'}...")
    print("\n? V?rifier dans les logs:")
    print("  - '[IMAGE] Clothing detected: chemise' doit apparaitre")
    print("  - 'nude' NE doit PAS apparaitre dans le prompt")

async def test_lingerie():
    """Test 4: Lingerie"""
    print("\n" + "="*60)
    print("TEST 4: Lingerie")
    print("="*60)
    
    generator = ImageGenerator()
    conversation = [
        "Hey",
        "Je porte de la lingerie sexy",
        "Dans ma chambre"
    ]
    
    print("\nConversation test:")
    for msg in conversation:
        print(f"  - {msg}")
    
    print("\n--- G?n?ration de l'image ---")
    image_url = await generator.generate_contextual_image(test_personality, conversation)
    
    print(f"\nR?sultat: {image_url[:100] if image_url else 'None'}...")
    print("\n? V?rifier dans les logs:")
    print("  - '[IMAGE] Clothing detected: lingerie' doit apparaitre")
    print("  - 'wearing ... lingerie' doit apparaitre dans le prompt")

async def main():
    """Ex?cuter tous les tests"""
    print("\n")
    print("#"*60)
    print("# TESTS DE VALIDATION - FIX IMAGE CLOTHING CONTEXT")
    print("#"*60)
    print("\nCes tests valident que le fix fonctionne correctement:")
    print("  1. D?tection des v?tements dans la conversation")
    print("  2. Priorisation des v?tements sur la nudit?")
    print("  3. D?tection des n?gations")
    print("  4. Support de diff?rents types de v?tements")
    
    try:
        await test_clothing_detection()
        await asyncio.sleep(1)
        
        await test_nudity_only()
        await asyncio.sleep(1)
        
        await test_negation()
        await asyncio.sleep(1)
        
        await test_lingerie()
        
        print("\n" + "="*60)
        print("TOUS LES TESTS EXECUTES")
        print("="*60)
        print("\n? Consulter les logs ci-dessus pour valider:")
        print("  - Les v?tements sont bien d?tect?s")
        print("  - Le contexte 'PRIORITY: Clothing' apparait quand n?cessaire")
        print("  - La nudit? n'est ajout?e que quand appropri?")
        print("\n")
        
    except Exception as e:
        print(f"\n??? ERREUR DURANT LES TESTS: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
