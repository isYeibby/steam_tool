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

// Favoritos y perfiles recientes

export const getRecentProfiles = async () => {
  try {
    const response = await steamApi.get('/profiles/recent');
    return response.data;
  } catch (error) {
    throw new Error('Error al cargar perfiles recientes');
  }
};

export const getFavorites = async () => {
  try {
    const response = await steamApi.get('/favorites');
    return response.data;
  } catch (error) {
    throw new Error('Error al cargar favoritos');
  }
};

export const addFavorite = async (steamId, name, avatar) => {
  try {
    const response = await steamApi.post('/favorites', {
      steam_id: steamId,
      name,
      avatar
    });
    return response.data;
  } catch (error) {
    throw new Error('Error al agregar favorito');
  }
};

export const removeFavorite = async (steamId) => {
  try {
    const response = await steamApi.delete(`/favorites/${steamId}`);
    return response.data;
  } catch (error) {
    throw new Error('Error al eliminar favorito');
  }
};

export const checkFavorite = async (steamId) => {
  try {
    const response = await steamApi.get(`/favorites/${steamId}/check`);
    return response.data.is_favorite;
  } catch (error) {
    return false;
  }
};

/**
 * Obtiene la lista de deseados (wishlist) de un usuario
 * @param {string} steamId - Steam ID del usuario
 * @returns {Promise} Promesa con la wishlist y estadísticas
 */
export const getWishlist = async (steamId) => {
  try {
    const response = await steamApi.get(`/wishlist/${steamId}`);
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.detail || 
      'Error al cargar la wishlist. Verifica que el perfil tenga la lista de deseados pública.'
    );
  }
};

export default steamApi;
