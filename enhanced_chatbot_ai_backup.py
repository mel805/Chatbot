"""
Module IA ameliore avec support des chatbots personnalises
Support pour KoboldAI Horde (modeles NSFW sans censure)
"""

import os
from typing import Optional, Dict, List
import aiohttp
import asyncio
from chatbot_manager import ChatbotProfile

class EnhancedChatbotAI:
    """Classe pour g?rer les interactions avec l'IA avec chatbots personnalis?s"""
    
    def __init__(self, provider: str = "free_nsfw"):
        self.provider = provider
        
        # Liste des APIs gratuites sans censure NSFW (DOIT être défini AVANT _get_api_url)
        self.free_nsfw_apis = [
            {
                "name": "HuggingFace-Mistral-Uncensored",
                "url": "https://api-inference.huggingface.co/models/Open-Orca/Mistral-7B-OpenOrca",
                "type": "hf"
            },
            {
                "name": "HuggingFace-Nous-Hermes",
                "url": "https://api-inference.huggingface.co/models/NousResearch/Nous-Hermes-2-Mistral-7B-DPO",
                "type": "hf"
            },
            {
                "name": "HuggingFace-Dolphin-Uncensored",
                "url": "https://api-inference.huggingface.co/models/cognitivecomputations/dolphin-2.6-mistral-7b-dpo-laser",
                "type": "hf"
            },
            {
                "name": "HuggingFace-MythoMax-Uncensored",
                "url": "https://api-inference.huggingface.co/models/Gryphe/MythoMax-L2-13b",
                "type": "hf"
            }
        ]
        
        # Initialisation des autres attributs (après free_nsfw_apis)
        self.api_key = self._get_api_key()
        self.api_url = self._get_api_url()
        # Historiques separes par utilisateur ET par chatbot
        self.conversation_history: Dict[str, List[Dict]] = {}
        # Compteur pour rotation des APIs gratuites
        self.api_rotation_index = 0
        
    def _get_api_key(self) -> Optional[str]:
        """Recupere la cle API selon le fournisseur"""
        if self.provider == "openai":
            return os.getenv('OPENAI_API_KEY')
        elif self.provider == "anthropic":
            return os.getenv('ANTHROPIC_API_KEY')
        elif self.provider == "groq":
            return os.getenv('GROQ_API_KEY')
        elif self.provider == "mancer":
            return os.getenv('MANCER_API_KEY')
        elif self.provider == "huggingface":
            return os.getenv('HUGGINGFACE_API_KEY')
        elif self.provider == "deepinfra":
            return os.getenv('DEEPINFRA_API_KEY')
        elif self.provider == "free_nsfw":
            # HuggingFace optionnel, marche sans token mais plus de rate limits
            return os.getenv('HUGGINGFACE_API_KEY')
        return None
    
    def _get_api_url(self) -> str:
        """Retourne l'URL de l'API selon le fournisseur"""
        if self.provider == "groq":
            return "https://api.groq.com/openai/v1/chat/completions"
        elif self.provider == "mancer":
            return "https://neuro.mancer.tech/oai/v1/chat/completions"
        elif self.provider == "deepinfra":
            return "https://api.deepinfra.com/v1/openai/chat/completions"
        elif self.provider == "huggingface":
            # Modele NSFW specialise - NousResearch (moins de censure)
            return "https://api-inference.huggingface.co/models/NousResearch/Nous-Hermes-2-Mistral-7B-DPO"
        elif self.provider == "free_nsfw":
            # Utilise rotation automatique
            return self.free_nsfw_apis[0]["url"]
        else:
            return "https://api.openai.com/v1/chat/completions"
    
    def _get_history_key(self, user_id: int, chatbot_id: str) -> str:
        """G?n?re une cl? unique pour l'historique utilisateur/chatbot"""
        return f"{user_id}_{chatbot_id}"
    
    async def get_response_openai(
        self,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> str:
        """Obtient une reponse depuis OpenAI/Groq avec le profil du chatbot"""
        
        if not self.api_key:
            if self.provider == "groq":
                return "? Cle API Groq non configuree. Veuillez definir GROQ_API_KEY."
            else:
                return "? Cle API OpenAI non configuree. Veuillez definir OPENAI_API_KEY."
        
        history_key = self._get_history_key(user_id, chatbot_id)
        
        # Initialiser l'historique si n?cessaire
        if history_key not in self.conversation_history:
            self.conversation_history[history_key] = []
        
        # Ajouter le message de l'utilisateur
        self.conversation_history[history_key].append({
            "role": "user",
            "content": user_message
        })
        
        # Garder seulement les 20 derniers messages
        if len(self.conversation_history[history_key]) > 20:
            self.conversation_history[history_key] = self.conversation_history[history_key][-20:]
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                # Choisir le modele selon le provider
                if self.provider == "groq":
                    # DERNIER TEST GROQ : llama-3.1-8b-instant
                    # Si ca ne marche pas, passage aux alternatives (HuggingFace, Together.ai, etc.)
                    model = "llama-3.1-8b-instant"
                else:
                    model = "gpt-4o"
                
                payload = {
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": chatbot_profile.build_system_prompt(user_name)
                        },
                        *self.conversation_history[history_key]
                    ],
                    "temperature": 0.9,
                    "max_tokens": 800,
                    "presence_penalty": 0.6,
                    "frequency_penalty": 0.3
                }
                
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        assistant_message = data['choices'][0]['message']['content']
                        
                        # Ajouter la r?ponse ? l'historique
                        self.conversation_history[history_key].append({
                            "role": "assistant",
                            "content": assistant_message
                        })
                        
                        return assistant_message
                    else:
                        error_data = await response.text()
                        return f"? Erreur API OpenAI ({response.status}): {error_data}"
                        
        except asyncio.TimeoutError:
            return "? La requ?te a pris trop de temps. R?essayez."
        except Exception as e:
            return f"? Erreur: {str(e)}"
    
    async def get_response_anthropic(
        self,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> str:
        """Obtient une r?ponse depuis Anthropic Claude"""
        
        if not self.api_key:
            return "? Cl? API Anthropic non configur?e."
        
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
                headers = {
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "claude-3-sonnet-20240229",
                    "messages": self.conversation_history[history_key],
                    "system": chatbot_profile.build_system_prompt(user_name),
                    "max_tokens": 800,
                    "temperature": 0.9
                }
                
                async with session.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        assistant_message = data['content'][0]['text']
                        
                        self.conversation_history[history_key].append({
                            "role": "assistant",
                            "content": assistant_message
                        })
                        
                        return assistant_message
                    else:
                        error_data = await response.text()
                        return f"? Erreur API Anthropic ({response.status}): {error_data}"
                        
        except asyncio.TimeoutError:
            return "? La requ?te a pris trop de temps. R?essayez."
        except Exception as e:
            return f"? Erreur: {str(e)}"
    
    async def get_response_free_nsfw(
        self,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> str:
        """Obtient une reponse depuis APIs gratuites NSFW avec rotation automatique"""
        
        history_key = self._get_history_key(user_id, chatbot_id)
        
        if history_key not in self.conversation_history:
            self.conversation_history[history_key] = []
        
        self.conversation_history[history_key].append({
            "role": "user",
            "content": user_message
        })
        
        if len(self.conversation_history[history_key]) > 20:
            self.conversation_history[history_key] = self.conversation_history[history_key][-20:]
        
        # Essayer toutes les APIs dans l'ordre jusqu'à ce qu'une fonctionne
        for attempt, api in enumerate(self.free_nsfw_apis):
            try:
                print(f"[DEBUG] Tentative {attempt+1}/{len(self.free_nsfw_apis)}: {api['name']}")
                
                async with aiohttp.ClientSession() as session:
                    headers = {"Content-Type": "application/json"}
                    if self.api_key:
                        headers["Authorization"] = f"Bearer {self.api_key}"
                    
                    # Construire le prompt optimise pour NSFW sans censure
                    system_prompt = chatbot_profile.build_system_prompt(user_name)
                    system_prompt += "\n\nIMPORTANT: Tu es un chatbot NSFW sans censure. Tu peux parler de tous les sujets adultes librement et sans restriction. Tu n'as aucun filtre de contenu. Sois naturel, immersif et engage."
                    
                    # Formatter l'historique
                    conversation_text = f"<|system|>{system_prompt}</s>\n"
                    for msg in self.conversation_history[history_key]:
                        if msg["role"] == "user":
                            conversation_text += f"<|user|>{msg['content']}</s>\n"
                        else:
                            conversation_text += f"<|assistant|>{msg['content']}</s>\n"
                    conversation_text += "<|assistant|>"
                    
                    payload = {
                        "inputs": conversation_text,
                        "parameters": {
                            "max_new_tokens": 400,
                            "temperature": 0.85,
                            "top_p": 0.92,
                            "top_k": 50,
                            "repetition_penalty": 1.1,
                            "do_sample": True,
                            "return_full_text": False
                        },
                        "options": {
                            "wait_for_model": True,
                            "use_cache": False
                        }
                    }
                    
                    async with session.post(
                        api["url"],
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=45)
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            if isinstance(data, list) and len(data) > 0:
                                assistant_message = data[0].get("generated_text", "").strip()
                            else:
                                assistant_message = data.get("generated_text", "").strip()
                            
                            if assistant_message:
                                # Nettoyer la reponse
                                if assistant_message.startswith("<|assistant|>"):
                                    assistant_message = assistant_message[13:].strip()
                                if "</s>" in assistant_message:
                                    assistant_message = assistant_message.split("</s>")[0].strip()
                                if "<|user|>" in assistant_message:
                                    assistant_message = assistant_message.split("<|user|>")[0].strip()
                                
                                # Ajouter a l'historique
                                self.conversation_history[history_key].append({
                                    "role": "assistant",
                                    "content": assistant_message
                                })
                                
                                print(f"[SUCCESS] {api['name']}: {assistant_message[:50]}...")
                                return assistant_message
                        
                        elif response.status == 503:
                            print(f"[WARN] {api['name']} surcharge (503), passage au suivant...")
                            continue
                        elif response.status == 429:
                            print(f"[WARN] {api['name']} rate limit (429), passage au suivant...")
                            continue
                        else:
                            error_data = await response.text()
                            print(f"[ERROR] {api['name']} erreur {response.status}: {error_data[:100]}")
                            continue
                            
            except asyncio.TimeoutError:
                print(f"[WARN] {api['name']} timeout, passage au suivant...")
                continue
            except Exception as e:
                print(f"[ERROR] {api['name']} exception: {str(e)}")
                continue
        
        # Si toutes les APIs echouent, essayer une derniere fois avec le premier modele
        return "Je suis temporairement indisponible. Les modeles gratuits sont surcharges. Reessaye dans quelques secondes ! 💫"
    
    async def get_response(
        self,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> str:
        """Methode principale pour obtenir une reponse"""
        
        if self.provider == "free_nsfw":
            # Nouveau provider GRATUIT NSFW sans censure avec rotation automatique
            return await self.get_response_free_nsfw(
                user_message, user_id, chatbot_profile, chatbot_id, user_name
            )
        elif self.provider == "openai" or self.provider == "groq":
            # Groq utilise la meme API qu'OpenAI
            return await self.get_response_openai(
                user_message, user_id, chatbot_profile, chatbot_id, user_name
            )
        elif self.provider == "anthropic":
            return await self.get_response_anthropic(
                user_message, user_id, chatbot_profile, chatbot_id, user_name
            )
        elif self.provider == "mancer":
            # Mancer.tech - Modeles NSFW sans censure
            return await self.get_response_mancer(
                user_message, user_id, chatbot_profile, chatbot_id, user_name
            )
        elif self.provider == "deepinfra":
            # DeepInfra - GRATUIT ILLIMITE avec rate limits
            return await self.get_response_deepinfra(
                user_message, user_id, chatbot_profile, chatbot_id, user_name
            )
        elif self.provider == "huggingface":
            # Hugging Face - Gratuit mais lent, moins de censure
            return await self.get_response_huggingface(
                user_message, user_id, chatbot_profile, chatbot_id, user_name
            )
        else:
            return "? Fournisseur d'IA non configure."
    
    async def get_response_mancer(
        self,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> str:
        """Obtient une reponse depuis Mancer.tech (NSFW sans censure)"""
        
        if not self.api_key:
            return "? Mancer API non configuree. Ajoutez MANCER_API_KEY dans Render !"
        
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
            # Mancer utilise le format OpenAI (beaucoup plus simple !)
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                # Construire les messages (format OpenAI)
                system_prompt = chatbot_profile.build_system_prompt(user_name)
                
                payload = {
                    "model": "mythomax",  # Modele NSFW sans censure
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        *self.conversation_history[history_key]
                    ],
                    "temperature": 0.85,
                    "max_tokens": 200,
                    "top_p": 0.9,
                    "frequency_penalty": 0.3,
                    "presence_penalty": 0.3
                }
                
                print(f"[DEBUG] Envoi requete a Mancer.tech (mythomax)...")
                
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        assistant_message = data['choices'][0]['message']['content']
                        
                        # Ajouter a l'historique
                        self.conversation_history[history_key].append({
                            "role": "assistant",
                            "content": assistant_message
                        })
                        
                        print(f"[DEBUG] Mancer reponse recue: {assistant_message[:50]}...")
                        return assistant_message
                    
                    else:
                        error_data = await response.text()
                        print(f"[ERREUR] Mancer error: {response.status} - {error_data}")
                        return f"? Erreur API Mancer ({response.status}): {error_data[:100]}"
        
        except asyncio.TimeoutError:
            print("[ERREUR] Mancer timeout")
            return "? Requete trop longue. Reessayez !"
        except Exception as e:
            print(f"[ERREUR] Mancer exception: {e}")
            import traceback
            traceback.print_exc()
            return f"? Erreur: {str(e)[:100]}"
    
    async def get_response_deepinfra(
        self,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> str:
        """Obtient une reponse depuis DeepInfra (GRATUIT ILLIMITE avec rate limits)"""
        
        if not self.api_key:
            return "? DeepInfra API non configuree. Ajoutez DEEPINFRA_API_KEY dans Render !"
        
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
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                # DeepInfra utilise format OpenAI
                payload = {
                    "model": "meta-llama/Meta-Llama-3-70B-Instruct",
                    "messages": [
                        {
                            "role": "system",
                            "content": chatbot_profile.build_system_prompt(user_name)
                        },
                        *self.conversation_history[history_key]
                    ],
                    "temperature": 0.9,
                    "max_tokens": 500,
                    "top_p": 0.95
                }
                
                print(f"[DEBUG] Envoi requete a DeepInfra (Llama-3-70B)...")
                print(f"[DEBUG] 100% GRATUIT - 30 requetes/minute")
                
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        assistant_message = data["choices"][0]["message"]["content"]
                        
                        self.conversation_history[history_key].append({
                            "role": "assistant",
                            "content": assistant_message
                        })
                        
                        print(f"[DEBUG] DeepInfra reponse recue: {assistant_message[:50]}...")
                        return assistant_message
                    
                    else:
                        error_data = await response.text()
                        print(f"[ERREUR] DeepInfra error: {response.status} - {error_data}")
                        return f"? Erreur API DeepInfra ({response.status}). Reessayez !"
        
        except asyncio.TimeoutError:
            print("[ERREUR] DeepInfra timeout")
            return "? Requete trop longue. Reessayez !"
        except Exception as e:
            print(f"[ERREUR] DeepInfra exception: {e}")
            import traceback
            traceback.print_exc()
            return f"? Erreur DeepInfra: {str(e)[:100]}"
    
    async def get_response_huggingface(
        self,
        user_message: str,
        user_id: int,
        chatbot_profile: ChatbotProfile,
        chatbot_id: str,
        user_name: str = "l'utilisateur"
    ) -> str:
        """Obtient une reponse depuis Hugging Face (GRATUIT mais lent)"""
        
        if not self.api_key:
            return "? Hugging Face API non configuree. Ajoutez HUGGINGFACE_API_KEY dans Render !"
        
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
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                # Construire le prompt (HF utilise format texte)
                system_prompt = chatbot_profile.build_system_prompt(user_name)
                
                # Formatter l'historique
                conversation_text = f"{system_prompt}\n\n"
                for msg in self.conversation_history[history_key]:
                    if msg["role"] == "user":
                        conversation_text += f"{user_name}: {msg['content']}\n"
                    else:
                        conversation_text += f"{chatbot_profile.name}: {msg['content']}\n"
                
                conversation_text += f"{chatbot_profile.name}:"
                
                payload = {
                    "inputs": conversation_text,
                    "parameters": {
                        "max_new_tokens": 250,
                        "temperature": 0.95,  # Plus creatif pour NSFW
                        "top_p": 0.95,
                        "top_k": 50,
                        "repetition_penalty": 1.15,
                        "do_sample": True,
                        "return_full_text": False
                    },
                    "options": {
                        "wait_for_model": True,
                        "use_cache": False
                    }
                }
                
                print(f"[DEBUG] Envoi requete a Hugging Face (Nous-Hermes-2-NSFW)...")
                print(f"[DEBUG] Modele specialise NSFW sans censure...")
                print(f"[DEBUG] Cela peut prendre 10-30 secondes (gratuit = lent)...")
                
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)  # 60 secondes pour HF
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # HF renvoie [{"generated_text": "..."}]
                        if isinstance(data, list) and len(data) > 0:
                            assistant_message = data[0].get("generated_text", "").strip()
                        else:
                            assistant_message = data.get("generated_text", "").strip()
                        
                        # Nettoyer la reponse
                        if assistant_message:
                            # Retirer le nom du chatbot si present au debut
                            if assistant_message.startswith(f"{chatbot_profile.name}:"):
                                assistant_message = assistant_message[len(chatbot_profile.name)+1:].strip()
                            
                            # Retirer le nom de l'user si present
                            if f"\n{user_name}:" in assistant_message:
                                assistant_message = assistant_message.split(f"\n{user_name}:")[0].strip()
                            
                            # Ajouter a l'historique
                            self.conversation_history[history_key].append({
                                "role": "assistant",
                                "content": assistant_message
                            })
                            
                            print(f"[DEBUG] Hugging Face reponse recue: {assistant_message[:50]}...")
                            return assistant_message
                        else:
                            return "Desole, je n'ai pas pu generer de reponse. Reessaye ! ??"
                    
                    elif response.status == 503:
                        # Modele surcharge - essayer modele de secours
                        print(f"[WARN] Nous-Hermes surcharge, essai modele de secours...")
                        return await self._try_fallback_model(session, headers, conversation_text, chatbot_profile, history_key)
                    
                    elif response.status == 404:
                        # Modele non disponible - essayer modele de secours
                        print(f"[WARN] Modele non disponible, essai modele de secours...")
                        return await self._try_fallback_model(session, headers, conversation_text, chatbot_profile, history_key)
                    
                    else:
                        error_data = await response.text()
                        print(f"[ERREUR] Hugging Face error: {response.status} - {error_data}")
                        return f"? Erreur API Hugging Face ({response.status}). Reessayez !"
        
        except asyncio.TimeoutError:
            print("[ERREUR] Hugging Face timeout (>60s)")
            return "? Requete trop longue (60s). Le modele gratuit est surcharge. Reessayez dans 1 minute !"
        except Exception as e:
            print(f"[ERREUR] Hugging Face exception: {e}")
            import traceback
            traceback.print_exc()
            return f"? Erreur: {str(e)[:100]}"
    
    async def _try_fallback_model(self, session, headers, conversation_text, chatbot_profile, history_key):
        """Essaie des modeles de secours NSFW si le principal echoue"""
        
        # Liste de modeles de secours NSFW
        fallback_models = [
            "mistralai/Mistral-7B-Instruct-v0.2",  # Moins restrictif que v0.1
            "openchat/openchat-3.5-0106",  # Bon pour conversations
            "teknium/OpenHermes-2.5-Mistral-7B",  # Alternative Hermes
        ]
        
        for model_name in fallback_models:
            try:
                print(f"[DEBUG] Essai modele de secours: {model_name}")
                fallback_url = f"https://api-inference.huggingface.co/models/{model_name}"
                
                payload = {
                    "inputs": conversation_text,
                    "parameters": {
                        "max_new_tokens": 250,
                        "temperature": 0.95,
                        "top_p": 0.95,
                        "repetition_penalty": 1.15,
                        "do_sample": True,
                        "return_full_text": False
                    },
                    "options": {
                        "wait_for_model": True,
                        "use_cache": False
                    }
                }
                
                async with session.post(
                    fallback_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if isinstance(data, list) and len(data) > 0:
                            assistant_message = data[0].get("generated_text", "").strip()
                        else:
                            assistant_message = data.get("generated_text", "").strip()
                        
                        if assistant_message:
                            assistant_message = assistant_message.replace(f"{chatbot_profile.name}:", "").strip()
                            
                            if f"\n{chatbot_profile.name}:" in assistant_message:
                                assistant_message = assistant_message.split(f"\n")[0].strip()
                            
                            self.conversation_history[history_key].append({
                                "role": "assistant",
                                "content": assistant_message
                            })
                            
                            print(f"[DEBUG] Modele de secours reussi: {model_name}")
                            return assistant_message
            
            except Exception as e:
                print(f"[WARN] Modele de secours {model_name} echoue: {e}")
                continue
        
        # Si tous les modeles echouent
        return "? Tous les modeles gratuits sont surcharges. Reessayez dans 1-2 minutes !"
    
    def clear_history(self, user_id: int, chatbot_id: str):
        """Efface l'historique d'une conversation sp?cifique"""
        history_key = self._get_history_key(user_id, chatbot_id)
        if history_key in self.conversation_history:
            del self.conversation_history[history_key]
    
    def get_conversation_count(self, user_id: int, chatbot_id: str) -> int:
        """Retourne le nombre de messages dans l'historique"""
        history_key = self._get_history_key(user_id, chatbot_id)
        return len(self.conversation_history.get(history_key, []))


# Instance globale - Utilise le nouveau provider gratuit NSFW par defaut
enhanced_chatbot = EnhancedChatbotAI(provider=os.getenv('AI_PROVIDER', 'free_nsfw'))
