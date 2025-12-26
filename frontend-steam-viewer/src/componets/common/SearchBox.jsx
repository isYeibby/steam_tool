import { useState } from 'react';
import { Download, Loader2 } from 'lucide-react';

const SearchBox = ({ onSearch, loading }) => {
  const [steamId, setSteamId] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (steamId.trim()) {
      onSearch(steamId.trim());
    }
  };

  return (
    <div className="search-box">
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="text"
            value={steamId}
            onChange={(e) => setSteamId(e.target.value)}
            placeholder="Ingresa tu Steam ID (76561198...)"
            disabled={loading}
          />
          <button type="submit" disabled={loading}>
            {loading ? (
              <>
                <Loader2 className="spinner" size={18} /> Cargando...
              </>
            ) : (
              <>
                <Download size={18} /> Cargar Biblioteca
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default SearchBox;
