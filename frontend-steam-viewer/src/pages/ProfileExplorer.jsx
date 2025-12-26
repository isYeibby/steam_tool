import { useState, useEffect } from 'react';
import SearchBox from '../componets/common/SearchBox';
import PlayerInfo from '../componets/ui/PlayerInfo';
import GamesList from '../componets/ui/GamesList';
import FavoriteButton from '../componets/common/FavoriteButton';
import { getGames, addFavorite, removeFavorite } from '../services/steamApi';
import { AlertTriangle } from 'lucide-react';

const ProfileExplorer = ({ initialSteamId }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [playerData, setPlayerData] = useState(null);
  const [currentSteamId, setCurrentSteamId] = useState('');
  const [isFavorite, setIsFavorite] = useState(false);

  const handleSearch = async (steamId) => {
    setLoading(true);
    setError(null);
    setPlayerData(null);
    setCurrentSteamId(steamId);

    try {
      const data = await getGames(steamId);
      setPlayerData(data);
      setIsFavorite(data.is_favorite || false);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleFavorite = async (steamId, player) => {
    try {
      if (isFavorite) {
        await removeFavorite(steamId);
        setIsFavorite(false);
      } else {
        await addFavorite(steamId, player.personaname, player.avatar);
        setIsFavorite(true);
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  // Efecto para cargar perfil cuando cambia initialSteamId
  useEffect(() => {
    if (initialSteamId && initialSteamId !== currentSteamId) {
      handleSearch(initialSteamId);
    }
  }, [initialSteamId]);

  return (
    <div className="content-section">
      <div className="section-header">
        <h2>Explorar Perfil de Steam</h2>
        <p className="section-subtitle">
          Busca cualquier perfil público de Steam para ver su biblioteca de juegos
        </p>
      </div>

      <SearchBox onSearch={handleSearch} loading={loading} />

      {error && (
        <div className="error-message">
          <AlertTriangle size={20} /> {error}
        </div>
      )}

      {playerData && (
        <>
          <div className="profile-actions">
            <FavoriteButton
              steamId={currentSteamId}
              playerData={playerData.player}
              isFavorite={isFavorite}
              onToggle={handleToggleFavorite}
            />
          </div>
          
          <PlayerInfo 
            player={playerData.player} 
            stats={playerData.stats} 
          />

          <GamesList 
            games={playerData.games} 
            steamId={currentSteamId} 
          />
        </>
      )}
    </div>
  );
};

export default ProfileExplorer;