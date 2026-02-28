"""
Servicio para obtener puntuaciones de Steam Reviews
"""
import requests
from typing import Dict, List
import time


class SteamReviewsService:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_game_reviews(self, appid: int) -> Dict:
        """
        Obtiene las puntuaciones de reviews de un juego en Steam
        
        Args:
            appid: ID del juego en Steam
            
        Returns:
            Dict con información de reviews
        """
        try:
            url = f"https://store.steampowered.com/appreviews/{appid}"
            params = {
                'json': 1,
                'language': 'all',
                'purchase_type': 'all',
                'num_per_page': 0  # Solo queremos el summary
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success') == 1:
                    query_summary = data.get('query_summary', {})
                    
                    total_positive = query_summary.get('total_positive', 0)
                    total_negative = query_summary.get('total_negative', 0)
                    total_reviews = query_summary.get('total_reviews', 0)
                    
                    # Calcular porcentaje
                    percentage = 0
                    if total_reviews > 0:
                        percentage = round((total_positive / total_reviews) * 100, 1)
                    
                    return {
                        'success': True,
                        'review_score': query_summary.get('review_score', 0),
                        'review_score_desc': query_summary.get('review_score_desc', 'No hay suficientes reviews'),
                        'total_positive': total_positive,
                        'total_negative': total_negative,
                        'total_reviews': total_reviews,
                        'percentage': percentage
                    }
            
            return {
                'success': False,
                'percentage': None,
                'review_score_desc': 'Sin datos',
                'total_reviews': 0
            }
            
        except Exception as e:
            print(f"Error getting reviews for appid {appid}: {e}")
            return {
                'success': False,
                'percentage': None,
                'review_score_desc': 'Error',
                'total_reviews': 0
            }
    
    def get_multiple_reviews(self, appids: List[int], delay: float = 0.3) -> Dict[int, Dict]:
        """
        Obtiene reviews de múltiples juegos
        
        Args:
            appids: Lista de IDs de juegos
            delay: Delay entre peticiones en segundos
            
        Returns:
            Dict con appid como key y datos de reviews como value
        """
        results = {}
        
        for appid in appids:
            reviews = self.get_game_reviews(appid)
            results[appid] = reviews
            
            # Rate limiting
            if delay > 0:
                time.sleep(delay)
        
        return results


# Instancia global del servicio
steam_reviews_service = SteamReviewsService()
