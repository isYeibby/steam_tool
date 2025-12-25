/**
 * Steam Library Viewer - JavaScript
 * Maneja la interacción del usuario y las llamadas a la API
 */

// Variables globales
let currentSteamId = '';
let allGames = [];

/**
 * Carga la biblioteca de juegos desde el servidor
 */
async function loadGames() {
    const steamId = document.getElementById('steamId').value.trim();
    
    if (!steamId) {
        showError('Por favor ingresa un Steam ID');
        return;
    }

    currentSteamId = steamId;
    
    // Ocultar errores previos y resetear UI
    document.getElementById('error').style.display = 'none';
    document.getElementById('loading').style.display = 'block';
    document.getElementById('playerInfo').style.display = 'none';
    document.getElementById('controls').style.display = 'none';
    document.getElementById('gamesGrid').innerHTML = '';
    
    // Deshabilitar botón
    document.getElementById('loadBtn').disabled = true;

    try {
        const response = await fetch(`/api/games/${steamId}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error al cargar los juegos');
        }

        allGames = data.games;
        displayPlayerInfo(data.player, data.stats);
        displayGames(allGames);
        
        document.getElementById('controls').style.display = 'flex';

    } catch (error) {
        showError(error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('loadBtn').disabled = false;
    }
}

/**
 * Muestra la información del jugador y estadísticas
 * @param {Object} player - Datos del jugador
 * @param {Object} stats - Estadísticas de la biblioteca
 */
function displayPlayerInfo(player, stats) {
    if (player) {
        document.getElementById('playerAvatar').src = player.avatarfull || player.avatar;
        document.getElementById('playerName').textContent = player.personaname;
        document.getElementById('playerUrl').textContent = player.profileurl;
    }

    document.getElementById('totalGames').textContent = stats.total_games;
    document.getElementById('totalHours').textContent = stats.total_hours.toLocaleString();
    document.getElementById('gamesPlayed').textContent = stats.games_played;
    document.getElementById('avgHours').textContent = stats.average_hours;

    document.getElementById('playerInfo').style.display = 'block';
}

/**
 * Muestra los juegos en la cuadrícula
 * @param {Array} games - Lista de juegos a mostrar
 */
function displayGames(games) {
    const grid = document.getElementById('gamesGrid');
    grid.innerHTML = '';

    if (games.length === 0) {
        grid.innerHTML = '<div class="no-games">No se encontraron juegos</div>';
        return;
    }

    games.forEach(game => {
        const card = document.createElement('div');
        card.className = 'game-card';
        
        card.innerHTML = `
            <div class="game-header">
                <img class="game-icon" src="${game.img_icon_url}" 
                     onerror="this.src='https://via.placeholder.com/60?text=Game'" 
                     alt="${game.name}">
                <div class="game-info">
                    <div class="game-name">${game.name}</div>
                </div>
            </div>
            <div class="game-stats">
                <div class="game-stat">
                    <span class="stat-key"><i class="fas fa-clock"></i> Horas jugadas:</span>
                    <span class="stat-value-game">${game.playtime_hours}h</span>
                </div>
                ${game.playtime_2weeks > 0 ? `
                <div class="game-stat">
                    <span class="stat-key"><i class="fas fa-calendar-week"></i> Últimas 2 semanas:</span>
                    <span class="stat-value-game">${game.playtime_2weeks}h</span>
                </div>
                ` : ''}
                <div class="game-stat">
                    <span class="stat-key"><i class="fas fa-history"></i> Última vez:</span>
                    <span class="stat-value-game">${game.last_played}</span>
                </div>
            </div>
        `;
        
        grid.appendChild(card);
    });
}

/**
 * Filtra los juegos según el término de búsqueda
 */
function filterGames() {
    const searchTerm = document.getElementById('searchGames').value.toLowerCase();
    const filteredGames = allGames.filter(game => 
        game.name.toLowerCase().includes(searchTerm)
    );
    displayGames(filteredGames);
}

/**
 * Exporta la biblioteca a CSV
 */
function exportCSV() {
    if (!currentSteamId) return;
    window.location.href = `/api/export/${currentSteamId}`;
}

/**
 * Muestra un mensaje de error
 * @param {string} message - Mensaje de error a mostrar
 */
function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.innerHTML = '<i class="fas fa-exclamation-triangle"></i> ' + message;
    errorDiv.style.display = 'block';
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Permitir presionar Enter para cargar
    const steamIdInput = document.getElementById('steamId');
    if (steamIdInput) {
        steamIdInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                loadGames();
            }
        });
    }
});
