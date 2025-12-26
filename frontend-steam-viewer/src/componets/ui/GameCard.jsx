import { Clock, Calendar, History } from 'lucide-react';

const GameCard = ({ game }) => {
  return (
    <div className="game-card">
      <div className="game-header">
        <img 
          src={game.img_icon_url} 
          alt={game.name}
          className="game-icon"
          onError={(e) => {
            e.target.src = 'https://via.placeholder.com/60?text=Game';
          }}
        />
        <div className="game-info">
          <div className="game-name">{game.name}</div>
        </div>
      </div>
      
      <div className="game-stats">
        <div className="game-stat">
          <span className="stat-key">
            <Clock size={14} /> Horas jugadas:
          </span>
          <span className="stat-value-game">{game.playtime_hours}h</span>
        </div>
        
        {game.playtime_2weeks > 0 && (
          <div className="game-stat">
            <span className="stat-key">
              <Calendar size={14} /> Últimas 2 semanas:
            </span>
            <span className="stat-value-game">{game.playtime_2weeks}h</span>
          </div>
        )}
        
        <div className="game-stat">
          <span className="stat-key">
            <History size={14} /> Última vez:
          </span>
          <span className="stat-value-game">{game.last_played}</span>
        </div>
      </div>
    </div>
  );
};

export default GameCard;
