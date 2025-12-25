"""
Configuración de la aplicación Steam Library Viewer
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class Config:
    """Configuración base de la aplicación"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Steam API
    STEAM_API_KEY = os.getenv('STEAM_API_KEY')
    
    # URLs de Steam API
    STEAM_API_BASE_URL = 'http://api.steampowered.com'
    STEAM_OWNED_GAMES_URL = f'{STEAM_API_BASE_URL}/IPlayerService/GetOwnedGames/v0001/'
    STEAM_PLAYER_SUMMARY_URL = f'{STEAM_API_BASE_URL}/ISteamUser/GetPlayerSummaries/v0002/'
    
    # URLs de SteamSpy
    STEAMSPY_API_URL = 'https://steamspy.com/api.php'
    
    # Timeouts para requests
    REQUEST_TIMEOUT = 10
    
    @classmethod
    def validate(cls):
        """Valida que la configuración esté completa"""
        if not cls.STEAM_API_KEY:
            raise ValueError(
                "No se encontró STEAM_API_KEY. "
                "Por favor configura tu .env con STEAM_API_KEY=tu_api_key"
            )
        return True


# Validar configuración al importar
Config.validate()
