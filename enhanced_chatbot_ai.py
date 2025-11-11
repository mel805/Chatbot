"""
Module IA ULTRA-RAPIDE avec Chai API et autres APIs optimisées
Réponses en moins de 1 seconde
"""

import os
from typing import Optional, Dict, List
import aiohttp
import asyncio
from chatbot_manager import ChatbotProfile
import json
import time

class EnhancedChatbotAI:
    """APIs ULTRA-RAPIDES pour réponses instantanées"""
    
    def __init__(self, provider: str = "ultra_fast"):
        self.provider = provider
        
        # APIs ULTRA-RAPIDES classées par vitesse
        self.ultra_fast_apis = [
            {
                "name": "Chai-Research",
                "url": "https://api.chai-research.com/v1/chat/completions",
                "model": "default",
                "type": "chai",
                "requires_key": False,
                "speed": "ultra_fast",  # < 1 seconde
                "priority": 1
            },
            {
                "name": "Kobold-Horde",
                "url": "https://stablehorde.net/api/v2/generate/text/async",
                "type": "horde",
                "requires_key": False,
                "speed": "very_fast",
                "priority": 2
            },
            {
                "name": "OpenRouter-Free",
                "url": "https://openrouter.ai/api/v1/chat/completions",
                "model": "nousresearch/nous-capybara-7b:free",
                "type": "openai_compatible",
                "requires_key": False,
                "speed": "fast",
                "priority": 3
            },
            {
                "name": "Together-Fast",
                "url": "https://api.together.xyz/v1/chat/completions",
                "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "type": "openai_compatible",
                "requires_key": True,
                "speed": "very_fast",
                "priority": 2
            }
        ]
        
        # Clés API
        self.together_key = os.getenv('TOGETHER_API_KEY')
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        
        # Historiques
        self.conversation_history: Dict[str, List[Dict]] = {}
        
        # Cache pour réponses rapides
        self.response_cache = {}
    
    def _get_history_key(self, user_id: int, chatbot_id: str) -> str:
        return f"{user_id}_{chatbot_id}"
    
    async def get_response_chai(
        self,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> Optional[str]:
        """Chai API - Ultra rapide < 1s"""
        
        history_key = self._get_history_key(user_id, chatbot_id)
        
        if history_key not in self.conversation_history:
            self.conversation_history[history_key] = []
        
        self.conversation_history[history_key].append({
            "role": "user",
            "content": user_message
        })
        
        if len(self.conversation_history[history_key]) > 15:
            self.conversation_history[history_key] = self.conversation_history[history_key][-15:]
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "DiscordBot/1.0"
                }
                
                system_prompt = chatbot_profile.build_system_prompt(user_name)
                system_prompt += "\n\nSois concis, naturel et réactif. NSFW autorisé."
                
                # Format simple pour Chai
                payload = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *self.conversation_history[history_key][-10:]  # Derniers 10 messages
                    ],
                    "temperature": 0.8,
                    "max_tokens": 200  # Court = plus rapide
                }
                
                print(f"[DEBUG] Chai API - Envoi...")
                start_time = time.time()
                
                async with session.post(
                    "https://api.chai-research.com/v1/chat",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=5)  # Timeout court
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        assistant_message = data.get("response", "").strip()
                        
                        if assistant_message:
                            elapsed = time.time() - start_time
                            self.conversation_history[history_key].append({
                                "role": "assistant",
                                "content": assistant_message
                            })
                            
                            print(f"[SUCCESS] Chai API: {assistant_message[:50]}... ({elapsed:.2f}s)")
                            return assistant_message
                    
                    print(f"[ERROR] Chai API - Status {response.status}")
                    return None
                        
        except asyncio.TimeoutError:
            print("[TIMEOUT] Chai API")
            return None
        except Exception as e:
            print(f"[ERROR] Chai API: {str(e)}")
            return None
    
    async def get_response_horde(
        self,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> Optional[str]:
        """Kobold Horde - Gratuit, communautaire, rapide"""
        
        history_key = self._get_history_key(user_id, chatbot_id)
        
        if history_key not in self.conversation_history:
            self.conversation_history[history_key] = []
        
        self.conversation_history[history_key].append({
            "role": "user",
            "content": user_message
        })
        
        if len(self.conversation_history[history_key]) > 15:
            self.conversation_history[history_key] = self.conversation_history[history_key][-15:]
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Content-Type": "application/json",
                    "apikey": "0000000000"  # Anonymous key
                }
                
                system_prompt = chatbot_profile.build_system_prompt(user_name)
                
                # Construire le contexte
                context = f"{system_prompt}\n\n"
                for msg in self.conversation_history[history_key][-8:]:
                    if msg["role"] == "user":
                        context += f"User: {msg['content']}\n"
                    else:
                        context += f"Assistant: {msg['content']}\n"
                context += "Assistant:"
                
                payload = {
                    "prompt": context,
                    "params": {
                        "max_length": 200,
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "rep_pen": 1.1
                    },
                    "models": ["koboldcpp/Mixtral-8x7B"],  # Modèle rapide NSFW
                    "trusted_workers": True
                }
                
                print(f"[DEBUG] Kobold Horde - Envoi...")
                start_time = time.time()
                
                # Requête async
                async with session.post(
                    "https://stablehorde.net/api/v2/generate/text/async",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=3)
                ) as response:
                    
                    if response.status == 202:
                        data = await response.json()
                        job_id = data.get("id")
                        
                        # Poll pour résultat (max 5 tentatives)
                        for _ in range(5):
                            await asyncio.sleep(0.5)
                            
                            async with session.get(
                                f"https://stablehorde.net/api/v2/generate/text/status/{job_id}",
                                headers=headers
                            ) as status_response:
                                
                                if status_response.status == 200:
                                    status_data = await status_response.json()
                                    
                                    if status_data.get("done"):
                                        generations = status_data.get("generations", [])
                                        if generations:
                                            assistant_message = generations[0].get("text", "").strip()
                                            
                                            if assistant_message:
                                                elapsed = time.time() - start_time
                                                self.conversation_history[history_key].append({
                                                    "role": "assistant",
                                                    "content": assistant_message
                                                })
                                                
                                                print(f"[SUCCESS] Horde: {assistant_message[:50]}... ({elapsed:.2f}s)")
                                                return assistant_message
                    
                    return None
                        
        except asyncio.TimeoutError:
            print("[TIMEOUT] Kobold Horde")
            return None
        except Exception as e:
            print(f"[ERROR] Kobold Horde: {str(e)}")
            return None
    
    async def get_response_openai_compatible(
        self,
        api_config: dict,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> Optional[str]:
        """APIs compatibles OpenAI - optimisées vitesse"""
        
        history_key = self._get_history_key(user_id, chatbot_id)
        
        if history_key not in self.conversation_history:
            self.conversation_history[history_key] = []
        
        self.conversation_history[history_key].append({
            "role": "user",
            "content": user_message
        })
        
        if len(self.conversation_history[history_key]) > 15:
            self.conversation_history[history_key] = self.conversation_history[history_key][-15:]
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Content-Type": "application/json"}
                
                if api_config["name"] == "Together-Fast" and self.together_key:
                    headers["Authorization"] = f"Bearer {self.together_key}"
                elif api_config["name"] == "OpenRouter-Free":
                    if self.openrouter_key:
                        headers["Authorization"] = f"Bearer {self.openrouter_key}"
                    headers["HTTP-Referer"] = "https://discord-bot.app"
                
                system_prompt = chatbot_profile.build_system_prompt(user_name)
                system_prompt += "\n\nSois concis et réactif. NSFW autorisé."
                
                payload = {
                    "model": api_config.get("model", "default"),
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *self.conversation_history[history_key][-10:]
                    ],
                    "temperature": 0.8,
                    "max_tokens": 200,  # Court = rapide
                    "stream": False
                }
                
                print(f"[DEBUG] {api_config['name']} - Envoi...")
                start_time = time.time()
                
                async with session.post(
                    api_config["url"],
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=8)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        assistant_message = data["choices"][0]["message"]["content"].strip()
                        
                        if assistant_message:
                            elapsed = time.time() - start_time
                            self.conversation_history[history_key].append({
                                "role": "assistant",
                                "content": assistant_message
                            })
                            
                            print(f"[SUCCESS] {api_config['name']}: {assistant_message[:50]}... ({elapsed:.2f}s)")
                            return assistant_message
                    
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
        """Méthode principale - ULTRA RAPIDE avec priorités"""
        
        print(f"[DEBUG] Message user {user_id} - Stratégie ultra-rapide")
        start_total = time.time()
        
        # STRATÉGIE 1: Essayer Chai en premier (le plus rapide < 1s)
        print("[DEBUG] Priorité 1: Chai API...")
        result = await self.get_response_chai(
            user_message, user_id, chatbot_profile, chatbot_id, user_name
        )
        
        if result:
            total_time = time.time() - start_total
            print(f"[SUCCESS TOTAL] Réponse en {total_time:.2f}s")
            return result
        
        # STRATÉGIE 2: APIs rapides EN PARALLÈLE
        print("[DEBUG] Chai échoué, essai parallèle...")
        
        fast_apis = [api for api in self.ultra_fast_apis if api["speed"] in ["very_fast", "fast"]]
        tasks = []
        
        for api in fast_apis:
            if api["type"] == "openai_compatible":
                task = self.get_response_openai_compatible(
                    api, user_message, user_id, chatbot_profile, chatbot_id, user_name
                )
                tasks.append(task)
            elif api["type"] == "horde":
                task = self.get_response_horde(
                    user_message, user_id, chatbot_profile, chatbot_id, user_name
                )
                tasks.append(task)
        
        # Prendre la première réponse
        for coro in asyncio.as_completed(tasks):
            try:
                result = await coro
                if result:
                    total_time = time.time() - start_total
                    print(f"[SUCCESS TOTAL] Réponse parallèle en {total_time:.2f}s")
                    return result
            except:
                continue
        
        # Toutes les APIs ont échoué
        print("[ERROR] Toutes les APIs ont échoué")
        return "Je suis temporairement indisponible. Réessaye ! 💫"
    
    def clear_history(self, user_id: int, chatbot_id: str):
        history_key = self._get_history_key(user_id, chatbot_id)
        if history_key in self.conversation_history:
            del self.conversation_history[history_key]
    
    def get_conversation_count(self, user_id: int, chatbot_id: str) -> int:
        history_key = self._get_history_key(user_id, chatbot_id)
        return len(self.conversation_history.get(history_key, []))


# Instance globale ultra-rapide
enhanced_chatbot = EnhancedChatbotAI(provider="ultra_fast")
