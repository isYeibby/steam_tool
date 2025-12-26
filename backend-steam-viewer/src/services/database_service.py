"""
Servicio de base de datos NoSQL usando TinyDB
Almacena perfiles buscados y favoritos
"""
from tinydb import TinyDB, Query
from datetime import datetime
from typing import List, Dict, Optional
import os

# Ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'profiles.json')

# Asegurar que existe el directorio
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Inicializar base de datos
db = TinyDB(DB_PATH)
profiles_table = db.table('profiles')
favorites_table = db.table('favorites')


class DatabaseService:
    """Servicio para gestionar perfiles y favoritos"""
    
    @staticmethod
    def save_profile_search(steam_id: str, player_data: Dict) -> Dict:
        """
        Guarda un perfil buscado en el historial
        
        Args:
            steam_id: Steam ID del usuario
            player_data: Datos del jugador
            
        Returns:
            Perfil guardado
        """
        Profile = Query()
        
        profile = {
            'steam_id': steam_id,
            'name': player_data.get('personaname', 'Unknown'),
            'avatar': player_data.get('avatar', ''),
            'searched_at': datetime.now().isoformat(),
            'total_games': 0  # Se actualizará con stats
        }
        
        # Verificar si ya existe
        existing = profiles_table.get(Profile.steam_id == steam_id)
        
        if existing:
            # Actualizar fecha de búsqueda
            profiles_table.update(
                {'searched_at': profile['searched_at']},
                Profile.steam_id == steam_id
            )
            return {**existing, 'searched_at': profile['searched_at']}
        else:
            # Insertar nuevo
            profiles_table.insert(profile)
            return profile
    
    @staticmethod
    def get_recent_profiles(limit: int = 10) -> List[Dict]:
        """
        Obtiene los perfiles buscados recientemente
        
        Args:
            limit: Número máximo de perfiles a retornar
            
        Returns:
            Lista de perfiles ordenados por fecha
        """
        all_profiles = profiles_table.all()
        # Ordenar por fecha de búsqueda (más reciente primero)
        sorted_profiles = sorted(
            all_profiles,
            key=lambda x: x.get('searched_at', ''),
            reverse=True
        )
        return sorted_profiles[:limit]
    
    @staticmethod
    def add_favorite(steam_id: str, player_data: Dict) -> Dict:
        """
        Agrega un perfil a favoritos
        
        Args:
            steam_id: Steam ID del usuario
            player_data: Datos del jugador
            
        Returns:
            Favorito guardado
        """
        Favorite = Query()
        
        # Verificar si ya existe
        existing = favorites_table.get(Favorite.steam_id == steam_id)
        if existing:
            return existing
        
        favorite = {
            'steam_id': steam_id,
            'name': player_data.get('personaname', 'Unknown'),
            'avatar': player_data.get('avatar', ''),
            'added_at': datetime.now().isoformat()
        }
        
        favorites_table.insert(favorite)
        return favorite
    
    @staticmethod
    def remove_favorite(steam_id: str) -> bool:
        """
        Elimina un perfil de favoritos
        
        Args:
            steam_id: Steam ID del usuario
            
        Returns:
            True si se eliminó, False si no existía
        """
        Favorite = Query()
        removed = favorites_table.remove(Favorite.steam_id == steam_id)
        return len(removed) > 0
    
    @staticmethod
    def get_favorites() -> List[Dict]:
        """
        Obtiene todos los favoritos
        
        Returns:
            Lista de perfiles favoritos ordenados por fecha
        """
        all_favorites = favorites_table.all()
        # Ordenar por fecha de agregado (más reciente primero)
        sorted_favorites = sorted(
            all_favorites,
            key=lambda x: x.get('added_at', ''),
            reverse=True
        )
        return sorted_favorites
    
    @staticmethod
    def is_favorite(steam_id: str) -> bool:
        """
        Verifica si un perfil está en favoritos
        
        Args:
            steam_id: Steam ID del usuario
            
        Returns:
            True si está en favoritos, False si no
        """
        Favorite = Query()
        return favorites_table.contains(Favorite.steam_id == steam_id)
    
    @staticmethod
    def update_profile_stats(steam_id: str, total_games: int):
        """
        Actualiza las estadísticas de un perfil
        
        Args:
            steam_id: Steam ID del usuario
            total_games: Total de juegos
        """
        Profile = Query()
        profiles_table.update(
            {'total_games': total_games},
            Profile.steam_id == steam_id
        )
