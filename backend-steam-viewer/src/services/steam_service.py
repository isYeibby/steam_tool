"""
Servicio para interactuar con la API de Steam
"""
import requests
from datetime import datetime
from typing import List, Dict, Optional
from src.config.config import Config


class SteamService:
    """Servicio para obtener datos de Steam API"""
    
    @staticmethod
    def get_owned_games(steam_id: str) -> List[Dict]:
        """
        Obtiene todos los juegos de una cuenta de Steam usando la API oficial
        
        Args:
            steam_id: Steam ID del usuario
            
        Returns:
            Lista de juegos con su información
        """
        params = {
            'key': Config.STEAM_API_KEY,
            'steamid': steam_id,
            'include_appinfo': 1,
            'include_played_free_games': 1,
            'format': 'json'
        }
        
        try:
            response = requests.get(
                Config.STEAM_OWNED_GAMES_URL,
                params=params,
                timeout=Config.REQUEST_TIMEOUT
            )
            data = response.json()
            
            if 'response' in data and 'games' in data['response']:
                return data['response']['games']
            return []
        except Exception as e:
            print(f"Error obteniendo juegos: {e}")
            return []
    
    @staticmethod
    def get_player_summary(steam_id: str) -> Optional[Dict]:
        """
        Obtiene información del perfil del jugador
        
        Args:
            steam_id: Steam ID del usuario
            
        Returns:
            Información del perfil o None si hay error
        """
        params = {
            'key': Config.STEAM_API_KEY,
            'steamids': steam_id,
            'format': 'json'
        }
        
        try:
            response = requests.get(
                Config.STEAM_PLAYER_SUMMARY_URL,
                params=params,
                timeout=Config.REQUEST_TIMEOUT
            )
            data = response.json()
            
            if 'response' in data and 'players' in data['response'] and data['response']['players']:
                return data['response']['players'][0]
            return None
        except Exception as e:
            print(f"Error obteniendo perfil: {e}")
            return None
    
    @staticmethod
    def get_game_details_steamspy(appid: int) -> Dict:
        """
        Obtiene detalles adicionales del juego desde SteamSpy
        
        Args:
            appid: App ID del juego
            
        Returns:
            Detalles del juego o diccionario vacío si hay error
        """
        try:
            params = {
                'request': 'appdetails',
                'appid': appid
            }
            response = requests.get(
                Config.STEAMSPY_API_URL,
                params=params,
                timeout=5
            )
            return response.json()
        except Exception as e:
            print(f"Error obteniendo detalles de SteamSpy para {appid}: {e}")
            return {}
    
    @staticmethod
    def process_games_data(games: List[Dict]) -> List[Dict]:
        """
        Procesa la lista de juegos raw de la API y devuelve datos formateados
        
        Args:
            games: Lista de juegos raw de la API
            
        Returns:
            Lista de juegos procesados con información adicional
        """
        games_list = []
        
        for game in games:
            playtime_hours = game.get('playtime_forever', 0) / 60
            playtime_2weeks = game.get('playtime_2weeks', 0) / 60 if 'playtime_2weeks' in game else 0
            
            # Calcular última vez jugado
            last_played = game.get('rtime_last_played', 0)
            if last_played > 0:
                last_played_str = datetime.fromtimestamp(last_played).strftime('%Y-%m-%d %H:%M')
            else:
                last_played_str = 'Nunca'
            
            appid = game['appid']
            img_icon_url = game.get('img_icon_url', '')
            img_logo_url = game.get('img_logo_url', '')
            
            games_list.append({
                'appid': appid,
                'name': game.get('name', f"AppID {appid}"),
                'playtime_hours': round(playtime_hours, 1),
                'playtime_2weeks': round(playtime_2weeks, 1),
                'last_played': last_played_str,
                'img_icon_url': f"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{img_icon_url}.jpg" if img_icon_url else '',
                'img_logo_url': f"https://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{img_logo_url}.jpg" if img_logo_url else ''
            })
        
        # Ordenar por horas jugadas
        games_list.sort(key=lambda x: x['playtime_hours'], reverse=True)
        
        return games_list
    
    @staticmethod
    def calculate_statistics(games_list: List[Dict]) -> Dict:
        """
        Calcula estadísticas de la biblioteca de juegos
        
        Args:
            games_list: Lista de juegos procesados
            
        Returns:
            Diccionario con estadísticas
        """
        total_games = len(games_list)
        total_hours = sum(g['playtime_hours'] for g in games_list)
        games_played = len([g for g in games_list if g['playtime_hours'] > 0])
        
        return {
            'total_games': total_games,
            'total_hours': round(total_hours, 1),
            'games_played': games_played,
            'games_never_played': total_games - games_played,
            'average_hours': round(total_hours / total_games, 1) if total_games > 0 else 0
        }
