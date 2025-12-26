"""
Rutas principales de la aplicación Steam Library Viewer
"""
from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
import io
import csv
from typing import List, Dict
from src.services.steam_service import SteamService
from src.services.database_service import DatabaseService
from src.services.game_priority_service import game_priority_service

# Crear router
router = APIRouter(prefix="/api", tags=["steam"])

# Instanciar servicios
steam_service = SteamService()
db_service = DatabaseService()


class FavoriteRequest(BaseModel):
    steam_id: str
    name: str
    avatar: str


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
    
    # Guardar en historial
    if player:
        db_service.save_profile_search(steam_id, player)
        db_service.update_profile_stats(steam_id, stats['total_games'])
    
    # Verificar si es favorito
    is_favorite = db_service.is_favorite(steam_id)
    
    return {
        'player': player,
        'games': games_list,
        'stats': stats,
        'is_favorite': is_favorite
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


# Endpoints para favoritos y historial

@router.get("/profiles/recent")
async def get_recent_profiles():
    """Obtiene los perfiles buscados recientemente"""
    return db_service.get_recent_profiles(limit=10)


@router.get("/favorites")
async def get_favorites():
    """Obtiene todos los perfiles favoritos"""
    return db_service.get_favorites()


@router.post("/favorites")
async def add_favorite(request: FavoriteRequest):
    """Agrega un perfil a favoritos"""
    player_data = {
        'personaname': request.name,
        'avatar': request.avatar
    }
    favorite = db_service.add_favorite(request.steam_id, player_data)
    return {"success": True, "favorite": favorite}


@router.delete("/favorites/{steam_id}")
async def remove_favorite(steam_id: str):
    """Elimina un perfil de favoritos"""
    success = db_service.remove_favorite(steam_id)
    if not success:
        raise HTTPException(status_code=404, detail='Favorito no encontrado')
    return {"success": True}


@router.get("/favorites/{steam_id}/check")
async def check_favorite(steam_id: str):
    """Verifica si un perfil está en favoritos"""
    is_favorite = db_service.is_favorite(steam_id)
    return {"is_favorite": is_favorite}


@router.get("/wishlist/{steam_id}")
async def get_wishlist(steam_id: str):
    """
    Obtiene la lista de deseados (wishlist) de un usuario de Steam
    
    Args:
        steam_id: Steam ID del usuario
        
    Returns:
        JSON con la wishlist del usuario y estadísticas
    """
    wishlist = steam_service.get_wishlist(steam_id)
    
    if not wishlist:
        raise HTTPException(
            status_code=400,
            detail='No se pudo obtener la wishlist. Verifica que:\n'
                   '1. El Steam ID sea correcto (debe ser el ID numérico de 17 dígitos)\n'
                   '2. El perfil tenga la wishlist configurada como pública\n'
                   '3. La lista de deseados no esté vacía\n\n'
                   'Para hacer pública tu wishlist: Perfil → Editar Perfil → Configuración de Privacidad → "Game details" → Público'
        )
    
    # Calcular estadísticas
    total_items = len(wishlist)
    free_games = len([g for g in wishlist if g.get('is_free_game')])
    with_positive_reviews = len([g for g in wishlist if g.get('reviews_percent', 0) >= 70])
    
    # Categorías de reviews
    overwhelmingly_positive = len([g for g in wishlist if g.get('reviews_percent', 0) >= 95])
    very_positive = len([g for g in wishlist if 80 <= g.get('reviews_percent', 0) < 95])
    positive = len([g for g in wishlist if 70 <= g.get('reviews_percent', 0) < 80])
    mixed = len([g for g in wishlist if 40 <= g.get('reviews_percent', 0) < 70])
    negative = len([g for g in wishlist if g.get('reviews_percent', 0) < 40])
    
    stats = {
        'total_items': total_items,
        'free_games': free_games,
        'paid_games': total_items - free_games,
        'with_positive_reviews': with_positive_reviews,
        'review_categories': {
            'overwhelmingly_positive': overwhelmingly_positive,
            'very_positive': very_positive,
            'positive': positive,
            'mixed': mixed,
            'negative': negative
        }
    }
    
    return {
        'wishlist': wishlist,
        'stats': stats
    }


@router.get("/games/{steam_id}/priority")
async def get_games_with_priority(
    steam_id: str,
    min_priority: float = Query(0, description="Prioridad mínima para filtrar juegos"),
    sort_by_priority: bool = Query(True, description="Ordenar por prioridad")
):
    """
    Obtiene los juegos de un usuario con cálculo de prioridad
    basado en puntuación de Metacritic y duración
    
    Args:
        steam_id: Steam ID del usuario
        min_priority: Prioridad mínima para filtrar (0 por defecto)
        sort_by_priority: Si ordenar por prioridad o no
        
    Returns:
        JSON con juegos enriquecidos con datos de prioridad:
        - metacritic_score: Puntuación de usuarios
        - duration_hours: Duración estimada
        - priority: Prioridad calculada (mayor = más prioritario)
        - has_metacritic_data: Si se encontraron datos
    """
    # Obtener juegos de Steam
    games = steam_service.get_owned_games(steam_id)
    player = steam_service.get_player_summary(steam_id)
    
    if not games:
        raise HTTPException(
            status_code=400,
            detail='No se pudieron obtener los juegos. '
                   'Verifica que el perfil sea público y el Steam ID sea correcto.'
        )
    
    # Procesar juegos básicos
    games_list = steam_service.process_games_data(games)
    
    # Enriquecer con prioridad
    if sort_by_priority:
        prioritized_games = game_priority_service.get_prioritized_games(
            games_list, 
            min_priority=min_priority
        )
    else:
        prioritized_games = game_priority_service.enrich_games_with_priority(games_list)
        if min_priority > 0:
            prioritized_games = [g for g in prioritized_games if g['priority'] >= min_priority]
    
    # Calcular estadísticas
    stats = steam_service.calculate_statistics(games_list)
    stats['with_metacritic_data'] = sum(1 for g in prioritized_games if g['has_metacritic_data'])
    stats['avg_priority'] = round(
        sum(g['priority'] for g in prioritized_games) / len(prioritized_games), 2
    ) if prioritized_games else 0
    
    # Guardar en historial
    if player:
        db_service.save_profile_search(steam_id, player)
        db_service.update_profile_stats(steam_id, stats['total_games'])
    
    # Verificar si es favorito
    is_favorite = db_service.is_favorite(steam_id)
    
    return {
        'player': player,
        'games': prioritized_games,
        'stats': stats,
        'is_favorite': is_favorite
    }


@router.post("/custom/analyze")
async def analyze_custom_csv(file: UploadFile = File(...)):
    """
    Analiza un CSV personalizado con el formato:
    Juegos Pendientes, Cuenta, Puntuación de Usuarios, Duración, Prioridad
    
    Returns:
        Análisis del CSV con estadísticas y recomendaciones
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail='El archivo debe ser un CSV')
    
    try:
        # Leer contenido del archivo
        contents = await file.read()
        decoded = contents.decode('utf-8')
        
        # Parsear CSV
        csv_reader = csv.DictReader(io.StringIO(decoded))
        games_data = []
        
        for row in csv_reader:
            # Parsear puntuación
            score_str = row.get('Puntuación de Usuarios', '').strip()
            score = float(score_str) if score_str else None
            
            # Parsear duración
            duration_str = row.get('Duración', '').strip()
            duration = float(duration_str) if duration_str else None
            
            # Calcular prioridad
            priority = game_priority_service.calculate_priority(score, duration)
            
            games_data.append({
                'name': row.get('Juegos Pendientes', '').strip(),
                'accounts': row.get('Cuenta', '').strip(),
                'score': score,
                'duration': duration,
                'priority': priority
            })
        
        # Filtrar juegos con datos válidos
        valid_games = [g for g in games_data if g['score'] is not None]
        priority_games = [g for g in games_data if g['priority'] > 0]
        
        # Estadísticas
        stats = {
            'total_games': len(games_data),
            'with_score': len(valid_games),
            'with_priority': len(priority_games),
            'avg_score': round(sum(g['score'] for g in valid_games) / len(valid_games), 2) if valid_games else 0,
            'avg_duration': round(sum(g['duration'] for g in valid_games if g['duration']) / len([g for g in valid_games if g['duration']]), 2) if valid_games else 0,
            'avg_priority': round(sum(g['priority'] for g in priority_games) / len(priority_games), 2) if priority_games else 0,
        }
        
        # Ordenar por prioridad
        sorted_games = sorted(games_data, key=lambda x: x['priority'], reverse=True)
        
        # Top recomendaciones
        top_recommendations = sorted_games[:20]
        
        return {
            'stats': stats,
            'all_games': sorted_games,
            'recommendations': top_recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error procesando CSV: {str(e)}')


@router.post("/custom/match-steam")
async def match_csv_with_steam(steam_id: str, file: UploadFile = File(...)):
    """
    Cruza datos del CSV con la biblioteca de Steam del usuario
    Muestra qué juegos del CSV tiene el usuario y sus estadísticas
    
    Returns:
        Juegos del CSV que están en la biblioteca con horas jugadas
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail='El archivo debe ser un CSV')
    
    try:
        # Obtener juegos de Steam
        steam_games = steam_service.get_owned_games(steam_id)
        if not steam_games:
            raise HTTPException(status_code=400, detail='No se pudieron obtener los juegos de Steam')
        
        # Crear diccionario de juegos de Steam por nombre
        steam_dict = {}
        for game in steam_games:
            name = game.get('name', '').lower().strip()
            steam_dict[name] = {
                'appid': game.get('appid'),
                'playtime_minutes': game.get('playtime_forever', 0),
                'playtime_hours': round(game.get('playtime_forever', 0) / 60, 1)
            }
        
        # Leer CSV
        contents = await file.read()
        decoded = contents.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(decoded))
        
        matched_games = []
        unmatched_games = []
        
        for row in csv_reader:
            game_name = row.get('Juegos Pendientes', '').strip()
            game_name_lower = game_name.lower()
            
            # Parsear datos del CSV
            score_str = row.get('Puntuación de Usuarios', '').strip()
            score = float(score_str) if score_str else None
            
            duration_str = row.get('Duración', '').strip()
            duration = float(duration_str) if duration_str else None
            
            priority = game_priority_service.calculate_priority(score, duration)
            
            game_data = {
                'name': game_name,
                'accounts': row.get('Cuenta', '').strip(),
                'score': score,
                'duration': duration,
                'priority': priority
            }
            
            # Buscar coincidencia en Steam
            if game_name_lower in steam_dict:
                steam_data = steam_dict[game_name_lower]
                matched_games.append({
                    **game_data,
                    'in_library': True,
                    'appid': steam_data['appid'],
                    'playtime_hours': steam_data['playtime_hours'],
                    'played': steam_data['playtime_hours'] > 0
                })
            else:
                unmatched_games.append({
                    **game_data,
                    'in_library': False
                })
        
        # Ordenar matched por prioridad
        matched_sorted = sorted(matched_games, key=lambda x: x['priority'], reverse=True)
        
        # Estadísticas
        stats = {
            'total_csv_games': len(matched_games) + len(unmatched_games),
            'in_library': len(matched_games),
            'not_in_library': len(unmatched_games),
            'played': len([g for g in matched_games if g['played']]),
            'unplayed': len([g for g in matched_games if not g['played']]),
            'avg_priority_owned': round(sum(g['priority'] for g in matched_games if g['priority'] > 0) / len([g for g in matched_games if g['priority'] > 0]), 2) if matched_games else 0
        }
        
        return {
            'stats': stats,
            'matched_games': matched_sorted,
            'unmatched_games': unmatched_games
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error procesando datos: {str(e)}')
