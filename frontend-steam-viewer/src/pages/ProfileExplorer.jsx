import { useState } from 'react';
import SearchBox from '../componets/SearchBox';
import PlayerInfo from '../componets/PlayerInfo';
import GamesList from '../componets/GamesList';
import { getGames } from '../services/steamApi';
import { AlertTriangle } from 'lucide-react';

const ProfileExplorer = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [playerData, setPlayerData] = useState(null);
  const [currentSteamId, setCurrentSteamId] = useState('');

  const handleSearch = async (steamId) => {
    setLoading(true);
    setError(null);
    setPlayerData(null);
    setCurrentSteamId(steamId);

    try {
      const data = await getGames(steamId);
      setPlayerData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

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
