import { User } from 'lucide-react';

const PlayerInfo = ({ player, stats }) => {
  if (!player && !stats) return null;

  return (
    <div className="player-info">
      {player && (
        <div className="player-header">
          <img 
            src={player.avatarfull || player.avatar} 
            alt={player.personaname}
            className="player-avatar"
          />
          <div className="player-details">
            <h2>{player.personaname}</h2>
            <a href={player.profileurl} target="_blank" rel="noopener noreferrer">
              {player.profileurl}
            </a>
          </div>
        </div>
      )}

      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{stats.total_games}</div>
            <div className="stat-label">Total de Juegos</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.total_hours.toLocaleString()}</div>
            <div className="stat-label">Horas Jugadas</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.games_played}</div>
            <div className="stat-label">Juegos Jugados</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.average_hours}</div>
            <div className="stat-label">Promedio Horas/Juego</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlayerInfo;
