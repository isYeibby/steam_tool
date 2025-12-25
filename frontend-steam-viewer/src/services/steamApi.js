/**
 * Steam API Service
 * Maneja las peticiones al backend FastAPI
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const steamApi = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Obtiene la biblioteca de juegos de un usuario
 * @param {string} steamId - Steam ID del usuario
 * @returns {Promise} Promesa con los datos del usuario, juegos y estadísticas
 */
export const getGames = async (steamId) => {
  try {
    const response = await steamApi.get(`/games/${steamId}`);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 
      'Error al cargar los juegos. Verifica que el perfil sea público y el Steam ID sea correcto.'
    );
  }
};

/**
 * Exporta la biblioteca de juegos a CSV
 * @param {string} steamId - Steam ID del usuario
 */
export const exportToCSV = (steamId) => {
  window.open(`${API_BASE_URL}/export/${steamId}`, '_blank');
};

/**
 * Obtiene detalles de un juego específico
 * @param {number} appId - ID del juego en Steam
 * @returns {Promise} Detalles del juego
 */
export const getGameDetails = async (appId) => {
  try {
    const response = await steamApi.get(`/game/${appId}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Error al cargar detalles del juego');
  }
};

export default steamApi;
