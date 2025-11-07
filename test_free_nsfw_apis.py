#!/usr/bin/env python3
"""
Test script pour v?rifier les nouvelles APIs NSFW gratuites
"""

import asyncio
import sys
sys.path.insert(0, '/workspace')

from image_generator import ImageGenerator

async def test_stable_horde():
    """Test Stable Horde API (gratuit, NSFW OK)"""
    print("\n" + "="*70)
    print("TEST 1: STABLE HORDE (Gratuit illimit?, NSFW OK)")
    print("="*70)
    
    gen = ImageGenerator()
    
    # Prompt explicite pour tester le NSFW
    test_prompt = "PHOTOREALISTIC PHOTO, realistic photograph, mature adult woman 25 years old, explicit fellatio scene, performing oral sex, mouth around penis, actively sucking, realistic photo, NOT anime, NOT cartoon, NOT child, adult only"
    
    print(f"\nPrompt: {test_prompt[:100]}...")
    print(f"\n?tape 1: Soumission de la requ?te...")
    
    image_url = await gen._generate_stable_horde(test_prompt)
    
    if image_url:
        print(f"\n? SUCCESS with Stable Horde!")
        print(f"? Image URL: {image_url[:80]}...")
        print(f"? L'image devrait montrer une sc?ne explicite (fellation)")
        return True
    else:
        print(f"\n? FAILED - Stable Horde timeout ou erreur")
        print(f"? Note: Normal si file d'attente trop longue (>120s)")
        return False

async def test_dezgo():
    """Test Dezgo API (gratuit rapide, NSFW OK)"""
    print("\n" + "="*70)
    print("TEST 2: DEZGO (Gratuit rapide, NSFW OK)")
    print("="*70)
    
    gen = ImageGenerator()
    
    # Prompt explicite pour tester le NSFW
    test_prompt = "PHOTOREALISTIC PHOTO, realistic photograph, mature adult woman 30 years old, explicit penetration scene, man and woman having sex, realistic intercourse, NOT anime, NOT cartoon, NOT child, adult only"
    
    print(f"\nPrompt: {test_prompt[:100]}...")
    print(f"\n?tape 1: Envoi de la requ?te...")
    
    image_url = await gen._generate_dezgo(test_prompt)
    
    if image_url:
        print(f"\n? SUCCESS with Dezgo!")
        if image_url.startswith("data:image"):
            print(f"? Image en base64 (premi?res 80 chars): {image_url[:80]}...")
        else:
            print(f"? Image URL: {image_url[:80]}...")
        print(f"? L'image devrait montrer une sc?ne explicite (p?n?tration)")
        return True
    else:
        print(f"\n? FAILED - Dezgo erreur ou rate limit")
        return False

async def test_full_flow():
    """Test le flow complet avec fallback"""
    print("\n" + "="*70)
    print("TEST 3: FLOW COMPLET (Stable Horde -> Dezgo -> Replicate -> Pollinations)")
    print("="*70)
    
    gen = ImageGenerator()
    
    # Simuler une personnalit? et conversation
    personality_data = {
        'name': 'TestBot',
        'genre': 'F?minin',
        'age': '25 ans',
        'description': 'Femme s?duisante',
        'visual': 'cheveux bruns, yeux bleus, corps athl?tique'
    }
    
    conversation_history = [
        {"role": "user", "content": "Je veux que tu me suces"},
        {"role": "assistant", "content": "Mmm je vais te prendre dans ma bouche toute enti?re..."}
    ]
    
    print(f"\nPersonnalit?: {personality_data['name']}, {personality_data['age']}")
    print(f"Conversation: Fellation explicite")
    print(f"\n?tape 1: G?n?ration avec d?tection du contexte...")
    
    image_url = await gen.generate_contextual_image(personality_data, conversation_history)
    
    if image_url:
        print(f"\n? SUCCESS!")
        print(f"? Image g?n?r?e: {image_url[:80]}...")
        print(f"? L'image devrait correspondre ? la conversation (fellation)")
        return True
    else:
        print(f"\n? FAILED - Tous les services ont ?chou?")
        return False

async def main():
    """Ex?cute tous les tests"""
    print("\n" + "?"*70)
    print("? TEST DES APIs GRATUITES NSFW (Stable Horde + Dezgo)")
    print("?"*70)
    
    print("\nCes tests vont v?rifier que :")
    print("1. Stable Horde g?n?re du contenu NSFW explicite (peut ?tre lent)")
    print("2. Dezgo g?n?re du contenu NSFW explicite (rapide)")
    print("3. Le flow complet fonctionne avec fallback automatique")
    
    print("\n? Note: Stable Horde peut prendre 30s ? 2min (normal)")
    print("? Note: Dezgo peut ?chouer si rate limit (normal)")
    
    results = {}
    
    # Test 1: Stable Horde
    try:
        results['stable_horde'] = await test_stable_horde()
    except Exception as e:
        print(f"\n? ERREUR Stable Horde: {e}")
        results['stable_horde'] = False
    
    # Test 2: Dezgo
    try:
        results['dezgo'] = await test_dezgo()
    except Exception as e:
        print(f"\n? ERREUR Dezgo: {e}")
        results['dezgo'] = False
    
    # Test 3: Flow complet
    try:
        results['full_flow'] = await test_full_flow()
    except Exception as e:
        print(f"\n? ERREUR Flow complet: {e}")
        results['full_flow'] = False
    
    # R?sum?
    print("\n" + "="*70)
    print("R?SUM? DES TESTS")
    print("="*70)
    
    print(f"\n1. Stable Horde (gratuit illimit?, NSFW): {'?' if results['stable_horde'] else '?'}")
    print(f"2. Dezgo (gratuit rapide, NSFW): {'?' if results['dezgo'] else '?'}")
    print(f"3. Flow complet avec fallback: {'?' if results['full_flow'] else '?'}")
    
    # Conclusion
    print("\n" + "="*70)
    if any(results.values()):
        print("? AU MOINS UN SERVICE GRATUIT FONCTIONNE !")
        print("? Vos images NSFW seront g?n?r?es sans censure")
        print("? Le bot est pr?t ? utiliser")
    else:
        print("? TOUS LES SERVICES GRATUITS ONT ?CHOU?")
        print("? V?rifiez votre connexion internet")
        print("? Le bot tombera sur Replicate (payant) ou Pollinations (censur?)")
    print("="*70)
    
    if results.get('stable_horde') or results.get('dezgo'):
        print("\n? R?SULTAT FINAL: SUC?S - Contenu NSFW gratuit disponible!")
        return 0
    else:
        print("\n? R?SULTAT FINAL: ?CHEC - Services gratuits indisponibles")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
