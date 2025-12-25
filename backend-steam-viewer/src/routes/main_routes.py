"""
Rutas principales de la aplicación Steam Library Viewer
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
from datetime import datetime
import io
from src.services.steam_service import SteamService

# Crear router
router = APIRouter(prefix="/api", tags=["steam"])

# Instanciar servicio
steam_service = SteamService()


@router.get("/games/{steam_id}")
async def get_games(steam_id: str):
    """
    API endpoint para obtener los juegos de un usuario
    
    Args:
        steam_id: Steam ID del usuario
        
    Returns:
        JSON con información del jugador, juegos y estadísticas
    """
    # Obtener datos de Steam
    games = steam_service.get_owned_games(steam_id)
    player = steam_service.get_player_summary(steam_id)
    
    if not games:
        raise HTTPException(
            status_code=400,
            detail='No se pudieron obtener los juegos. '
                   'Verifica que el perfil sea público y el Steam ID sea correcto.'
        )
    
    # Procesar los datos
    games_list = steam_service.process_games_data(games)
    
    # Calcular estadísticas
    stats = steam_service.calculate_statistics(games_list)
    
    return {
        'player': player,
        'games': games_list,
        'stats': stats
    }


@router.get("/export/{steam_id}")
async def export_csv(steam_id: str):
    """
    Exporta los juegos a CSV
    
    Args:
        steam_id: Steam ID del usuario
        
    Returns:
        Archivo CSV con la biblioteca de juegos
    """
    games = steam_service.get_owned_games(steam_id)
    
    if not games:
        raise HTTPException(status_code=400, detail='No se pudieron obtener los juegos')
    
    # Procesar datos
    games_list = steam_service.process_games_data(games)
    
    # Crear DataFrame
    games_data = []
    for game in games_list:
        games_data.append({
            'AppID': game['appid'],
            'Nombre': game['name'],
            'Horas_Jugadas': game['playtime_hours'],
            'Ultima_Vez_Jugado': game['last_played']
        })
    
    df = pd.DataFrame(games_data)
    
    # Crear archivo CSV en memoria
    output = io.StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    
    # Nombre del archivo
    filename = f'steam_games_{steam_id}_{datetime.now().strftime("%Y%m%d")}.csv'
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )


@router.get("/game/{appid}")
async def get_game_details(appid: int):
    """
    Obtiene detalles adicionales de un juego específico
    
    Args:
        appid: App ID del juego
        
    Returns:
        JSON con detalles del juego desde SteamSpy
    """
    details = steam_service.get_game_details_steamspy(appid)
    
    if not details:
        raise HTTPException(status_code=404, detail='No se pudieron obtener los detalles del juego')
    
    return details

