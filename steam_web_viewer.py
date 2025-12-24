from flask import Flask, render_template, jsonify, send_file, request
import requests
import pandas as pd
from datetime import datetime
import io
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Obtener Steam API Key desde variable de entorno
STEAM_API_KEY = os.getenv('STEAM_API_KEY')

if not STEAM_API_KEY:
    raise ValueError("No se encontró STEAM_API_KEY. Por favor configura tu .env")

def get_owned_games(steam_id):
    """Obtiene todos los juegos de una cuenta de Steam usando la API oficial"""
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    params = {
        'key': STEAM_API_KEY,
        'steamid': steam_id,
        'include_appinfo': 1,
        'include_played_free_games': 1,
        'format': 'json'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'response' in data and 'games' in data['response']:
            return data['response']['games']
        return []
    except Exception as e:
        print(f"Error obteniendo juegos: {e}")
        return []

def get_player_summary(steam_id):
    """Obtiene información del perfil del jugador"""
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        'key': STEAM_API_KEY,
        'steamids': steam_id,
        'format': 'json'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'response' in data and 'players' in data['response'] and data['response']['players']:
            return data['response']['players'][0]
        return None
    except Exception as e:
        print(f"Error obteniendo perfil: {e}")
        return None

def get_game_details_steamspy(appid):
    """Obtiene detalles adicionales del juego desde SteamSpy"""
    try:
        url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
        response = requests.get(url, timeout=5)
        return response.json()
    except:
        return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/games/<steam_id>')
def get_games(steam_id):
    """API endpoint para obtener los juegos de un usuario"""
    games = get_owned_games(steam_id)
    player = get_player_summary(steam_id)
    
    if not games:
        return jsonify({'error': 'No se pudieron obtener los juegos. Verifica que el perfil sea público y el Steam ID sea correcto.'}), 400
    
    # Procesar los datos
    games_list = []
    for game in games:
        playtime_hours = game.get('playtime_forever', 0) / 60  # Convertir minutos a horas
        playtime_2weeks = game.get('playtime_2weeks', 0) / 60 if 'playtime_2weeks' in game else 0
        
        # Calcular última vez jugado
        last_played = game.get('rtime_last_played', 0)
        if last_played > 0:
            last_played_str = datetime.fromtimestamp(last_played).strftime('%Y-%m-%d %H:%M')
        else:
            last_played_str = 'Nunca'
        
        games_list.append({
            'appid': game['appid'],
            'name': game.get('name', f"AppID {game['appid']}"),
            'playtime_hours': round(playtime_hours, 1),
            'playtime_2weeks': round(playtime_2weeks, 1),
            'last_played': last_played_str,
            'img_icon_url': f"https://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game.get('img_icon_url', '')}.jpg" if game.get('img_icon_url') else '',
            'img_logo_url': f"https://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game.get('img_logo_url', '')}.jpg" if game.get('img_logo_url') else ''
        })
    
    # Ordenar por horas jugadas
    games_list.sort(key=lambda x: x['playtime_hours'], reverse=True)
    
    # Estadísticas
    total_games = len(games_list)
    total_hours = sum(g['playtime_hours'] for g in games_list)
    games_played = len([g for g in games_list if g['playtime_hours'] > 0])
    
    return jsonify({
        'player': player,
        'games': games_list,
        'stats': {
            'total_games': total_games,
            'total_hours': round(total_hours, 1),
            'games_played': games_played,
            'games_never_played': total_games - games_played,
            'average_hours': round(total_hours / total_games, 1) if total_games > 0 else 0
        }
    })

@app.route('/api/export/<steam_id>')
def export_csv(steam_id):
    """Exporta los juegos a CSV"""
    games = get_owned_games(steam_id)
    
    if not games:
        return jsonify({'error': 'No se pudieron obtener los juegos'}), 400
    
    # Crear DataFrame
    games_data = []
    for game in games:
        playtime_hours = game.get('playtime_forever', 0) / 60
        last_played = game.get('rtime_last_played', 0)
        last_played_str = datetime.fromtimestamp(last_played).strftime('%Y-%m-%d %H:%M') if last_played > 0 else 'Nunca'
        
        games_data.append({
            'AppID': game['appid'],
            'Nombre': game.get('name', f"AppID {game['appid']}"),
            'Horas_Jugadas': round(playtime_hours, 1),
            'Ultima_Vez_Jugado': last_played_str
        })
    
    df = pd.DataFrame(games_data)
    df = df.sort_values('Horas_Jugadas', ascending=False)
    
    # Crear archivo CSV en memoria
    output = io.BytesIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')
    output.seek(0)
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'steam_games_{steam_id}_{datetime.now().strftime("%Y%m%d")}.csv'
    )

if __name__ == '__main__':
    print("Steam Library Viewer")
    print("Servidor iniciando en http://localhost:5000")
    print("API Key configurada")
    app.run(debug=True, host='0.0.0.0', port=5000)
