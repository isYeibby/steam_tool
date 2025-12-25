"""
Rutas principales de la aplicación Steam Library Viewer
"""
from flask import Blueprint, render_template, jsonify, send_file, request
import pandas as pd
from datetime import datetime
import io
from src.services.steam_service import SteamService

# Crear Blueprint
main_bp = Blueprint('main', __name__)

# Instanciar servicio
steam_service = SteamService()


@main_bp.route('/')
def index():
    """Página principal de la aplicación"""
    return render_template('index.html')


@main_bp.route('/api/games/<steam_id>')
def get_games(steam_id):
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
        return jsonify({
            'error': 'No se pudieron obtener los juegos. '
                    'Verifica que el perfil sea público y el Steam ID sea correcto.'
        }), 400
    
    # Procesar los datos
    games_list = steam_service.process_games_data(games)
    
    # Calcular estadísticas
    stats = steam_service.calculate_statistics(games_list)
    
    return jsonify({
        'player': player,
        'games': games_list,
        'stats': stats
    })


@main_bp.route('/api/export/<steam_id>')
def export_csv(steam_id):
    """
    Exporta los juegos a CSV
    
    Args:
        steam_id: Steam ID del usuario
        
    Returns:
        Archivo CSV con la biblioteca de juegos
    """
    games = steam_service.get_owned_games(steam_id)
    
    if not games:
        return jsonify({'error': 'No se pudieron obtener los juegos'}), 400
    
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
    output = io.BytesIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    
    # Nombre del archivo
    filename = f'steam_games_{steam_id}_{datetime.now().strftime("%Y%m%d")}.csv'
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )


@main_bp.route('/api/game/<int:appid>')
def get_game_details(appid):
    """
    Obtiene detalles adicionales de un juego específico
    
    Args:
        appid: App ID del juego
        
    Returns:
        JSON con detalles del juego desde SteamSpy
    """
    details = steam_service.get_game_details_steamspy(appid)
    
    if not details:
        return jsonify({'error': 'No se pudieron obtener los detalles del juego'}), 404
    
    return jsonify(details)
