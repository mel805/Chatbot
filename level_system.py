"""
Système de niveaux et d'expérience pour les membres Discord
Gère la progression, les niveaux et le classement
"""

import json
import os
from typing import Dict, Optional, List, Tuple
from datetime import datetime
import math

class LevelSystem:
    """Gestion des niveaux et XP des utilisateurs"""
    
    def __init__(self, data_file: str = "user_levels.json"):
        self.data_file = data_file
        self.user_data: Dict[str, Dict] = {}
        self.xp_per_message = 15  # XP de base par message
        self.xp_variance = 10     # Variance aléatoire (5-15)
        self.load_data()
    
    def load_data(self):
        """Charge les données depuis le fichier JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.user_data = json.load(f)
                print(f"[OK] Données de niveau chargées: {len(self.user_data)} utilisateurs")
            except Exception as e:
                print(f"[ERREUR] Chargement données niveau: {e}")
                self.user_data = {}
        else:
            print("[INFO] Nouveau fichier de niveaux créé")
            self.user_data = {}
    
    def save_data(self):
        """Sauvegarde les données dans le fichier JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERREUR] Sauvegarde données niveau: {e}")
    
    def calculate_level(self, xp: int) -> int:
        """Calcule le niveau basé sur l'XP (formule progressive)"""
        # Formule: level = floor(0.1 * sqrt(xp))
        # Level 1 = 100 XP, Level 10 = 10000 XP, Level 50 = 250000 XP
        return int(0.1 * math.sqrt(xp))
    
    def calculate_xp_for_level(self, level: int) -> int:
        """Calcule l'XP nécessaire pour un niveau donné"""
        return int((level * 10) ** 2)
    
    def get_user_data(self, user_id: int) -> Dict:
        """Récupère les données d'un utilisateur"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.user_data:
            self.user_data[user_id_str] = {
                "xp": 0,
                "level": 0,
                "total_messages": 0,
                "last_message_time": None,
                "joined_date": datetime.now().isoformat()
            }
            self.save_data()
        
        return self.user_data[user_id_str]
    
    def add_xp(
        self, 
        user_id: int, 
        xp_amount: Optional[int] = None
    ) -> Tuple[bool, int, int]:
        """
        Ajoute de l'XP à un utilisateur
        Retourne: (level_up, ancien_niveau, nouveau_niveau)
        """
        import random
        
        if xp_amount is None:
            # XP aléatoire entre 10 et 25
            xp_amount = random.randint(
                self.xp_per_message - self.xp_variance,
                self.xp_per_message + self.xp_variance
            )
        
        user_data = self.get_user_data(user_id)
        
        old_level = self.calculate_level(user_data["xp"])
        user_data["xp"] += xp_amount
        user_data["total_messages"] += 1
        user_data["last_message_time"] = datetime.now().isoformat()
        
        new_level = self.calculate_level(user_data["xp"])
        
        self.save_data()
        
        level_up = new_level > old_level
        return level_up, old_level, new_level
    
    def get_level_info(self, user_id: int) -> Dict:
        """Obtient les infos complètes de niveau d'un utilisateur"""
        user_data = self.get_user_data(user_id)
        current_xp = user_data["xp"]
        current_level = self.calculate_level(current_xp)
        
        xp_for_current = self.calculate_xp_for_level(current_level)
        xp_for_next = self.calculate_xp_for_level(current_level + 1)
        
        xp_progress = current_xp - xp_for_current
        xp_needed = xp_for_next - xp_for_current
        
        progress_percent = (xp_progress / xp_needed) * 100 if xp_needed > 0 else 0
        
        return {
            "user_id": user_id,
            "level": current_level,
            "xp": current_xp,
            "xp_progress": xp_progress,
            "xp_needed": xp_needed,
            "xp_for_next": xp_for_next,
            "progress_percent": progress_percent,
            "total_messages": user_data["total_messages"],
            "joined_date": user_data.get("joined_date"),
            "last_message": user_data.get("last_message_time")
        }
    
    def get_leaderboard(self, limit: int = 10) -> List[Tuple[str, Dict]]:
        """
        Retourne le classement des utilisateurs par XP
        Format: [(user_id, user_data), ...]
        """
        sorted_users = sorted(
            self.user_data.items(),
            key=lambda x: x[1]["xp"],
            reverse=True
        )
        
        return sorted_users[:limit]
    
    def get_user_rank(self, user_id: int) -> int:
        """Obtient le rang d'un utilisateur (1 = premier)"""
        user_id_str = str(user_id)
        
        sorted_users = sorted(
            self.user_data.items(),
            key=lambda x: x[1]["xp"],
            reverse=True
        )
        
        for rank, (uid, _) in enumerate(sorted_users, 1):
            if uid == user_id_str:
                return rank
        
        return len(self.user_data) + 1
    
    def reset_user(self, user_id: int):
        """Réinitialise les données d'un utilisateur"""
        user_id_str = str(user_id)
        if user_id_str in self.user_data:
            del self.user_data[user_id_str]
            self.save_data()
    
    def set_level(self, user_id: int, level: int):
        """Définit manuellement le niveau d'un utilisateur"""
        xp_needed = self.calculate_xp_for_level(level)
        user_data = self.get_user_data(user_id)
        user_data["xp"] = xp_needed
        self.save_data()


# Instance globale
level_system = LevelSystem()
