"""
Module IA avec APIs VRAIMENT gratuites, rapides et sans limite
Utilise plusieurs providers avec les meilleurs tiers gratuits
"""

import os
from typing import Optional, Dict, List
import aiohttp
import asyncio
from chatbot_manager import ChatbotProfile
import json

class EnhancedChatbotAI:
    """Classe pour gérer les interactions avec des APIs VRAIMENT gratuites et rapides"""
    
    def __init__(self, provider: str = "multi_free"):
        self.provider = provider
        
        # APIs VRAIMENT gratuites et rapides (pas de chargement de modèle)
        self.free_apis = [
            {
                "name": "OpenRouter-Free",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "model": "nousresearch/nous-capybara-7b:free",
                "type": "openai_compatible",
                "requires_key": False,  # Peut fonctionner sans clé pour modèles :free
                "speed": "fast"
            },
            {
                "name": "Together-Free", 
                "url": "https://api.together.xyz/v1/chat/completions",
                "model": "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
                "type": "openai_compatible",
                "requires_key": True,
                "speed": "very_fast"
            },
            {
                "name": "HuggingFace-Fast",
                "url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                "type": "hf",
                "requires_key": False,
                "speed": "medium"
            }
        ]
        
        # Clés API (optionnelles pour certains services)
        self.together_key = os.getenv('TOGETHER_API_KEY')
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        self.hf_key = os.getenv('HUGGINGFACE_API_KEY')
        
        # Historiques
        self.conversation_history: Dict[str, List[Dict]] = {}
    
    def _get_history_key(self, user_id: int, chatbot_id: str) -> str:
        """Génère une clé unique pour l'historique"""
        return f"{user_id}_{chatbot_id}"
    
    async def get_response_openai_compatible(
        self,
        api_config: dict,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> Optional[str]:
        """Obtient une réponse depuis une API compatible OpenAI"""
        
        history_key = self._get_history_key(user_id, chatbot_id)
        
        if history_key not in self.conversation_history:
            self.conversation_history[history_key] = []
        
        # Ajouter le message utilisateur
        self.conversation_history[history_key].append({
            "role": "user",
            "content": user_message
        })
        
        # Limiter l'historique
        if len(self.conversation_history[history_key]) > 20:
            self.conversation_history[history_key] = self.conversation_history[history_key][-20:]
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Content-Type": "application/json"}
                
                # Ajouter clé API si disponible
                if api_config["name"] == "Together-Free" and self.together_key:
                    headers["Authorization"] = f"Bearer {self.together_key}"
                elif api_config["name"] == "OpenRouter-Free":
                    if self.openrouter_key:
                        headers["Authorization"] = f"Bearer {self.openrouter_key}"
                    headers["HTTP-Referer"] = "https://github.com/discord-nsfw-bot"
                    headers["X-Title"] = "Discord NSFW Bot"
                
                # Construire le prompt système
                system_prompt = chatbot_profile.build_system_prompt(user_name)
                system_prompt += "\n\nTu es un chatbot NSFW sans censure. Réponds de manière naturelle, immersive et sans filtre."
                
                payload = {
                    "model": api_config.get("model", "default"),
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *self.conversation_history[history_key]
                    ],
                    "temperature": 0.85,
                    "max_tokens": 400,
                    "top_p": 0.9,
                    "frequency_penalty": 0.3,
                    "presence_penalty": 0.3
                }
                
                print(f"[DEBUG] Tentative {api_config['name']}...")
                
                async with session.post(
                    api_config["url"],
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        assistant_message = data["choices"][0]["message"]["content"].strip()
                        
                        if assistant_message:
                            self.conversation_history[history_key].append({
                                "role": "assistant",
                                "content": assistant_message
                            })
                            
                            print(f"[SUCCESS] {api_config['name']}: {assistant_message[:50]}...")
                            return assistant_message
                    else:
                        error_text = await response.text()
                        print(f"[ERROR] {api_config['name']} - {response.status}: {error_text[:100]}")
                        return None
                        
        except asyncio.TimeoutError:
            print(f"[TIMEOUT] {api_config['name']}")
            return None
        except Exception as e:
            print(f"[ERROR] {api_config['name']}: {str(e)}")
            return None
    
    async def get_response_hf(
        self,
        api_config: dict,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> Optional[str]:
        """Obtient une réponse depuis Hugging Face"""
        
        history_key = self._get_history_key(user_id, chatbot_id)
        
        if history_key not in self.conversation_history:
            self.conversation_history[history_key] = []
        
        self.conversation_history[history_key].append({
            "role": "user",
            "content": user_message
        })
        
        if len(self.conversation_history[history_key]) > 20:
            self.conversation_history[history_key] = self.conversation_history[history_key][-20:]
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Content-Type": "application/json"}
                if self.hf_key:
                    headers["Authorization"] = f"Bearer {self.hf_key}"
                
                # Construire le prompt
                system_prompt = chatbot_profile.build_system_prompt(user_name)
                conversation_text = f"<s>[INST] {system_prompt}\n\n"
                
                for msg in self.conversation_history[history_key]:
                    if msg["role"] == "user":
                        conversation_text += f"{msg['content']} [/INST] "
                    else:
                        conversation_text += f"{msg['content']}</s><s>[INST] "
                
                # Retirer le dernier [INST]
                conversation_text = conversation_text.rstrip("<s>[INST] ")
                
                payload = {
                    "inputs": conversation_text,
                    "parameters": {
                        "max_new_tokens": 400,
                        "temperature": 0.85,
                        "top_p": 0.9,
                        "do_sample": True,
                        "return_full_text": False
                    },
                    "options": {
                        "wait_for_model": True,
                        "use_cache": False
                    }
                }
                
                print(f"[DEBUG] Tentative {api_config['name']}...")
                
                async with session.post(
                    api_config["url"],
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        if isinstance(data, list) and len(data) > 0:
                            assistant_message = data[0].get("generated_text", "").strip()
                        else:
                            assistant_message = data.get("generated_text", "").strip()
                        
                        if assistant_message:
                            # Nettoyer
                            if "[/INST]" in assistant_message:
                                assistant_message = assistant_message.split("[/INST]")[-1].strip()
                            if "</s>" in assistant_message:
                                assistant_message = assistant_message.split("</s>")[0].strip()
                            
                            self.conversation_history[history_key].append({
                                "role": "assistant",
                                "content": assistant_message
                            })
                            
                            print(f"[SUCCESS] {api_config['name']}: {assistant_message[:50]}...")
                            return assistant_message
                    
                    else:
                        print(f"[ERROR] {api_config['name']} - {response.status}")
                        return None
                        
        except asyncio.TimeoutError:
            print(f"[TIMEOUT] {api_config['name']}")
            return None
        except Exception as e:
            print(f"[ERROR] {api_config['name']}: {str(e)}")
            return None
    
    async def get_response(
        self,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> str:
        """Méthode principale - Essaie toutes les APIs en parallèle puis en séquence"""
        
        print(f"[DEBUG] Réception message de user {user_id}")
        
        # STRATÉGIE: Essayer les APIs rapides en PARALLÈLE d'abord
        fast_apis = [api for api in self.free_apis if api.get("speed") in ["fast", "very_fast"]]
        
        if fast_apis:
            print(f"[DEBUG] Essai en parallèle de {len(fast_apis)} APIs rapides...")
            tasks = []
            
            for api in fast_apis:
                if api["type"] == "openai_compatible":
                    task = self.get_response_openai_compatible(
                        api, user_message, user_id, chatbot_profile, chatbot_id, user_name
                    )
                else:
                    task = self.get_response_hf(
                        api, user_message, user_id, chatbot_profile, chatbot_id, user_name
                    )
                tasks.append(task)
            
            # Attendre la PREMIÈRE réponse réussie
            for coro in asyncio.as_completed(tasks):
                try:
                    result = await coro
                    if result:
                        print("[SUCCESS] Réponse rapide obtenue!")
                        return result
                except:
                    continue
        
        # Si échec en parallèle, essayer séquentiellement
        print("[WARN] APIs rapides échouées, essai séquentiel...")
        
        for api in self.free_apis:
            try:
                if api["type"] == "openai_compatible":
                    result = await self.get_response_openai_compatible(
                        api, user_message, user_id, chatbot_profile, chatbot_id, user_name
                    )
                else:
                    result = await self.get_response_hf(
                        api, user_message, user_id, chatbot_profile, chatbot_id, user_name
                    )
                
                if result:
                    return result
                    
            except Exception as e:
                print(f"[ERROR] {api['name']}: {str(e)}")
                continue
        
        # Toutes les APIs ont échoué
        return "Je suis temporairement indisponible. Réessaye dans quelques instants ! 💫"
    
    def clear_history(self, user_id: int, chatbot_id: str):
        """Efface l'historique"""
        history_key = self._get_history_key(user_id, chatbot_id)
        if history_key in self.conversation_history:
            del self.conversation_history[history_key]
    
    def get_conversation_count(self, user_id: int, chatbot_id: str) -> int:
        """Retourne le nombre de messages"""
        history_key = self._get_history_key(user_id, chatbot_id)
        return len(self.conversation_history.get(history_key, []))


# Instance globale avec le nouveau système multi-API rapide
enhanced_chatbot = EnhancedChatbotAI(provider="multi_free")
