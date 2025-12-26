"""
Servicio para calcular prioridad de juegos
Basado en puntuación de Metacritic y tiempo de juego
"""
import math
from typing import List, Dict, Optional
import csv
import os


class GamePriorityService:
    """Servicio para calcular prioridad de juegos"""
    
    # Ruta al archivo CSV con datos de Metacritic
    CSV_PATH = os.path.join(
        os.path.dirname(__file__), 
        '..', '..', '..', 
        'frontend-steam-viewer', 
        'data', 
        'Rush games - Juegos.csv'
    )
    
    def __init__(self):
        """Inicializa el servicio y carga datos de Metacritic"""
        self.metacritic_data = self._load_metacritic_data()
    
    def _load_metacritic_data(self) -> Dict[str, Dict]:
        """
        Carga datos de Metacritic desde el archivo CSV
        
        Returns:
            Diccionario con nombre del juego como clave y sus datos
        """
        data = {}
        
        if not os.path.exists(self.CSV_PATH):
            print(f"Advertencia: No se encontró el archivo CSV en {self.CSV_PATH}")
            return data
        
        try:
            with open(self.CSV_PATH, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    game_name = row.get('Juegos Pendientes', '').strip()
                    if game_name:
                        # Parsear puntuación (puede estar vacía)
                        score_str = row.get('Puntuación de Usuarios', '').strip()
                        score = float(score_str) if score_str else None
                        
                        # Parsear duración (puede estar vacía)
                        duration_str = row.get('Duración', '').strip()
                        duration = float(duration_str) if duration_str else None
                        
                        data[game_name.lower()] = {
                            'name': game_name,
                            'score': score,
                            'duration': duration,
                            'accounts': row.get('Cuenta', '').strip()
                        }
        except Exception as e:
            print(f"Error cargando datos de Metacritic: {e}")
        
        return data
    
    def calculate_priority(self, score: Optional[float], duration: Optional[float]) -> float:
        """
        Calcula la prioridad de un juego usando la fórmula:
        SI(score < 70, 0, score / LN(duration + 1))
        
        Args:
            score: Puntuación de usuarios de Metacritic (0-100)
            duration: Duración del juego en horas
            
        Returns:
            Prioridad calculada (mayor valor = mayor prioridad)
        """
        # Si no hay score o es menor a 70, prioridad es 0
        if score is None or score < 70:
            return 0.0
        
        # Si no hay duración, usar duración por defecto
        if duration is None or duration <= 0:
            duration = 1.0
        
        # Calcular prioridad: score / ln(duration + 1)
        try:
            priority = score / math.log(duration + 1)
            return round(priority, 2)
        except Exception:
            return 0.0
    
    def get_game_data(self, game_name: str) -> Optional[Dict]:
        """
        Obtiene los datos de un juego desde el CSV
        
        Args:
            game_name: Nombre del juego
            
        Returns:
            Diccionario con datos del juego o None si no existe
        """
        return self.metacritic_data.get(game_name.lower())
    
    def enrich_games_with_priority(self, games: List[Dict]) -> List[Dict]:
        """
        Enriquece una lista de juegos de Steam con datos de prioridad
        
        Args:
            games: Lista de juegos de Steam API
            
        Returns:
            Lista de juegos con campos adicionales:
            - metacritic_score: Puntuación de usuarios
            - duration_hours: Duración estimada
            - priority: Prioridad calculada
            - has_metacritic_data: Si se encontraron datos
        """
        enriched_games = []
        
        for game in games:
            game_name = game.get('name', '')
            enriched_game = game.copy()
            
            # Buscar datos de Metacritic
            game_data = self.get_game_data(game_name)
            
            if game_data:
                score = game_data.get('score')
                duration = game_data.get('duration')
                priority = self.calculate_priority(score, duration)
                
                enriched_game.update({
                    'metacritic_score': score,
                    'duration_hours': duration,
                    'priority': priority,
                    'has_metacritic_data': True,
                    'accounts': game_data.get('accounts')
                })
            else:
                enriched_game.update({
                    'metacritic_score': None,
                    'duration_hours': None,
                    'priority': 0.0,
                    'has_metacritic_data': False,
                    'accounts': None
                })
            
            enriched_games.append(enriched_game)
        
        return enriched_games
    
    def get_prioritized_games(self, games: List[Dict], min_priority: float = 0) -> List[Dict]:
        """
        Obtiene juegos ordenados por prioridad
        
        Args:
            games: Lista de juegos de Steam
            min_priority: Prioridad mínima para filtrar
            
        Returns:
            Lista de juegos ordenados por prioridad (mayor a menor)
        """
        enriched = self.enrich_games_with_priority(games)
        
        # Filtrar por prioridad mínima
        filtered = [g for g in enriched if g['priority'] >= min_priority]
        
        # Ordenar por prioridad descendente
        sorted_games = sorted(filtered, key=lambda x: x['priority'], reverse=True)
        
        return sorted_games


# Instancia global del servicio
game_priority_service = GamePriorityService()
