"""
Gestionnaire de threads Discord pour conversations priv?es
Chaque utilisateur peut avoir son propre thread pour discuter avec son chatbot
"""

import json
import os
from typing import Optional, Dict
from datetime import datetime

class ThreadManager:
    """G?re les threads de conversation priv?s"""
    
    def __init__(self, database_file: str = "active_threads.json"):
        self.database_file = database_file
        self.data = self.load_database()
    
    def load_database(self) -> Dict:
        """Charge la base de donn?es des threads actifs"""
        if os.path.exists(self.database_file):
            with open(self.database_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_database(self):
        """Sauvegarde la base de donn?es"""
        with open(self.database_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def create_thread(self, user_id: int, thread_id: int, chatbot_name: str, chatbot_id: str = None):
        """Enregistre un nouveau thread pour un utilisateur"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            self.data[user_id_str] = {}
        
        self.data[user_id_str] = {
            "thread_id": thread_id,
            "chatbot_name": chatbot_name,
            "chatbot_id": chatbot_id or chatbot_name,  # Fallback au nom si pas d'ID
            "owner_id": user_id,
            "created_at": datetime.now().isoformat(),
            "message_count": 0,
            "active": True
        }
        
        self.save_database()
    
    def get_user_thread(self, user_id: int) -> Optional[int]:
        """R?cup?re le thread actif d'un utilisateur"""
        user_id_str = str(user_id)
        
        if user_id_str in self.data and self.data[user_id_str].get("active", False):
            return self.data[user_id_str]["thread_id"]
        
        return None
    
    def is_active_thread(self, thread_id: int) -> bool:
        """V?rifie si un thread est actif"""
        for user_data in self.data.values():
            if user_data.get("thread_id") == thread_id and user_data.get("active", False):
                return True
        return False
    
    def get_thread_owner(self, thread_id: int) -> Optional[int]:
        """Recupere le proprietaire d'un thread"""
        for user_id_str, user_data in self.data.items():
            if user_data.get("thread_id") == thread_id:
                return int(user_id_str)
        return None
    
    def get_thread_by_id(self, thread_id: int) -> Optional[Dict]:
        """Recupere les infos d'un thread par son ID"""
        for user_id_str, user_data in self.data.items():
            if user_data.get("thread_id") == thread_id and user_data.get("active", False):
                return user_data
        return None
    
    def close_thread(self, user_id: int):
        """Ferme le thread d'un utilisateur"""
        user_id_str = str(user_id)
        
        if user_id_str in self.data:
            self.data[user_id_str]["active"] = False
            self.data[user_id_str]["closed_at"] = datetime.now().isoformat()
            self.save_database()
    
    def increment_message_count(self, thread_id: int):
        """Incremente le compteur de messages d'un thread"""
        for user_id_str, user_data in self.data.items():
            if user_data.get("thread_id") == thread_id:
                user_data["message_count"] = user_data.get("message_count", 0) + 1
                self.save_database()
                return
    
    def get_stats(self, user_id: int) -> Optional[Dict]:
        """R?cup?re les statistiques d'un thread"""
        user_id_str = str(user_id)
        
        if user_id_str in self.data:
            return self.data[user_id_str]
        
        return None


# Instance globale
thread_manager = ThreadManager()
