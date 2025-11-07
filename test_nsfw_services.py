#!/usr/bin/env python3
"""
Script de test pour les services NSFW gratuits
Teste Stable Horde et Hugging Face pour diagnostiquer les problèmes
"""

import aiohttp
import asyncio
import json

async def test_stable_horde():
    """Test Stable Horde avec modèles NSFW"""
    print("\n" + "="*60)
    print("TEST 1: STABLE HORDE")
    print("="*60)
    
    try:
        submit_url = "https://stablehorde.net/api/v2/generate/async"
        
        # Prompt simple pour test
        prompt = "beautiful woman, photorealistic, high quality"
        
        payload = {
            "prompt": prompt,
            "params": {
                "width": 512,  # Plus petit pour être plus rapide
                "height": 512,
                "steps": 20,
                "cfg_scale": 7.5,
                "sampler_name": "k_euler_a",
                "n": 1
            },
            "nsfw": True,
            "censor_nsfw": False,
            "models": [
                "Deliberate",
                "Realistic Vision V5.1",
                "DreamShaper"
            ]
        }
        
        print(f"✓ Prompt: {prompt}")
        print(f"✓ Modèles: {payload['models']}")
        print(f"✓ URL: {submit_url}")
        print(f"\n⏳ Envoi de la requête...")
        
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(submit_url, json=payload) as resp:
                print(f"✓ Status: {resp.status}")
                
                if resp.status == 202:
                    result = await resp.json()
                    request_id = result.get('id')
                    print(f"✓ Request ID: {request_id}")
                    print(f"✅ STABLE HORDE: Soumission réussie!")
                    print(f"   (La génération prendrait du temps, mais la soumission fonctionne)")
                    return True
                else:
                    error_text = await resp.text()
                    print(f"❌ STABLE HORDE: Échec - Status {resp.status}")
                    print(f"❌ Erreur: {error_text[:500]}")
                    
                    # Analyser l'erreur
                    try:
                        error_json = json.loads(error_text)
                        print(f"\n🔍 DIAGNOSTIC:")
                        if "message" in error_json:
                            print(f"   Message: {error_json['message']}")
                        if "errors" in error_json:
                            print(f"   Erreurs: {error_json['errors']}")
                    except:
                        pass
                    
                    return False
                    
    except Exception as e:
        print(f"❌ STABLE HORDE: Exception - {e}")
        return False

async def test_huggingface():
    """Test Hugging Face Inference API"""
    print("\n" + "="*60)
    print("TEST 2: HUGGING FACE")
    print("="*60)
    
    try:
        model_id = "SG161222/Realistic_Vision_V5.1_noVAE"
        api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        
        prompt = "beautiful woman, photorealistic, high quality"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "width": 512,
                "height": 512,
                "num_inference_steps": 20,
                "guidance_scale": 7.5
            }
        }
        
        print(f"✓ Modèle: {model_id}")
        print(f"✓ Prompt: {prompt}")
        print(f"✓ URL: {api_url}")
        print(f"\n⏳ Envoi de la requête...")
        
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(api_url, json=payload) as resp:
                print(f"✓ Status: {resp.status}")
                
                if resp.status == 200:
                    image_data = await resp.read()
                    print(f"✓ Image reçue: {len(image_data)} bytes")
                    print(f"✅ HUGGING FACE: Génération réussie!")
                    return True
                    
                elif resp.status == 503:
                    result = await resp.json()
                    estimated_time = result.get('estimated_time', 'unknown')
                    print(f"⏳ HUGGING FACE: Modèle en chargement")
                    print(f"   Temps estimé: {estimated_time}s")
                    print(f"✅ Service disponible (juste besoin d'attendre)")
                    return True
                    
                elif resp.status == 429:
                    print(f"⚠️ HUGGING FACE: Rate limit atteint")
                    print(f"   Réessayez dans quelques minutes")
                    return False
                    
                else:
                    error_text = await resp.text()
                    print(f"❌ HUGGING FACE: Échec - Status {resp.status}")
                    print(f"❌ Erreur: {error_text[:500]}")
                    return False
                    
    except Exception as e:
        print(f"❌ HUGGING FACE: Exception - {e}")
        return False

async def test_tmpfiles():
    """Test upload vers tmpfiles.org"""
    print("\n" + "="*60)
    print("TEST 3: TMPFILES.ORG (Upload)")
    print("="*60)
    
    try:
        upload_url = "https://tmpfiles.org/api/v1/upload"
        
        # Créer une image de test (1x1 pixel PNG)
        test_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        
        form_data = aiohttp.FormData()
        form_data.add_field('file',
                          test_image,
                          filename='test.png',
                          content_type='image/png')
        
        print(f"✓ URL: {upload_url}")
        print(f"✓ Test image: {len(test_image)} bytes")
        print(f"\n⏳ Upload...")
        
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(upload_url, data=form_data) as resp:
                print(f"✓ Status: {resp.status}")
                
                if resp.status == 200:
                    result = await resp.json()
                    print(f"✓ Réponse: {json.dumps(result, indent=2)}")
                    
                    if result.get('status') == 'success':
                        file_url = result.get('data', {}).get('url', '')
                        print(f"✓ URL: {file_url}")
                        print(f"✅ TMPFILES: Upload réussi!")
                        return True
                    else:
                        print(f"⚠️ TMPFILES: Upload mais statut non-success")
                        return False
                else:
                    error_text = await resp.text()
                    print(f"❌ TMPFILES: Échec - Status {resp.status}")
                    print(f"❌ Erreur: {error_text[:500]}")
                    return False
                    
    except Exception as e:
        print(f"❌ TMPFILES: Exception - {e}")
        return False

async def main():
    """Exécuter tous les tests"""
    print("\n" + "="*60)
    print("🔍 DIAGNOSTIC DES SERVICES NSFW GRATUITS")
    print("="*60)
    
    results = {}
    
    # Test 1: Stable Horde
    results['stable_horde'] = await test_stable_horde()
    await asyncio.sleep(2)
    
    # Test 2: Hugging Face
    results['huggingface'] = await test_huggingface()
    await asyncio.sleep(2)
    
    # Test 3: tmpfiles.org
    results['tmpfiles'] = await test_tmpfiles()
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    
    print(f"\n1. Stable Horde:  {'✅ OK' if results['stable_horde'] else '❌ ÉCHEC'}")
    print(f"2. Hugging Face:  {'✅ OK' if results['huggingface'] else '❌ ÉCHEC'}")
    print(f"3. tmpfiles.org:  {'✅ OK' if results['tmpfiles'] else '❌ ÉCHEC'}")
    
    # Conclusions
    print("\n" + "="*60)
    print("💡 CONCLUSIONS")
    print("="*60)
    
    if results['stable_horde'] and results['huggingface']:
        print("\n✅ Les deux services fonctionnent !")
        print("   Le problème vient peut-être des prompts trop explicites.")
        print("   Solution: Tester avec des prompts plus simples d'abord.")
        
    elif results['stable_horde']:
        print("\n⚠️ Stable Horde fonctionne, mais Hugging Face échoue")
        if not results['huggingface']:
            print("   Possible rate limit sur Hugging Face.")
            print("   Solution: Configurer une clé API Hugging Face ou attendre.")
            
    elif results['huggingface']:
        print("\n⚠️ Hugging Face fonctionne, mais Stable Horde échoue")
        print("   Possible rejet des modèles NSFW ou surcharge.")
        print("   Solution: Hugging Face devrait prendre le relais dans le bot.")
        
    else:
        print("\n❌ Les deux services échouent !")
        print("   Possible problème réseau ou les services sont down.")
        print("   Solution: Configurer Replicate pour une fiabilité 100%.")
    
    if not results['tmpfiles']:
        print("\n⚠️ tmpfiles.org ne fonctionne pas")
        print("   Hugging Face ne pourra pas uploader les images.")
        print("   Solution: Trouver un autre service d'upload gratuit.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    asyncio.run(main())
