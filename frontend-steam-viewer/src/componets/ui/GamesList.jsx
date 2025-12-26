import { useState } from 'react';
import { Search, FileDown } from 'lucide-react';
import GameCard from './GameCard';
import { exportToCSV } from '../../services/steamApi';

const GamesList = ({ games, steamId }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredGames = games.filter(game =>
    game.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleExport = () => {
    if (steamId) {
      exportToCSV(steamId);
    }
  };

  if (!games || games.length === 0) {
    return <div className="no-games">No se encontraron juegos</div>;
  }

  return (
    <>
      <div className="controls">
        <div className="search-games">
          <Search className="search-icon" size={18} />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar juegos..."
          />
        </div>
        <button onClick={handleExport}>
          <FileDown size={18} /> Exportar a CSV
        </button>
      </div>

      <div className="games-grid">
        {filteredGames.length > 0 ? (
          filteredGames.map(game => (
            <GameCard key={game.appid} game={game} />
          ))
        ) : (
          <div className="no-games">No se encontraron juegos con ese término</div>
        )}
      </div>
    </>
  );
};

export default GamesList;
