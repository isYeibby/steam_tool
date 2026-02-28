import { useState, useEffect } from 'react';
import { TrendingUp, Loader, Star } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const GamePriority = ({ activeUser }) => {
  const [loading, setLoading] = useState(false);
  const [gamesWithReviews, setGamesWithReviews] = useState([]);

  useEffect(() => {
    if (activeUser && activeUser.games) {
      loadReviews();
    }
  }, [activeUser]);

  const loadReviews = async () => {
    setLoading(true);

    try {
      // Obtener los appids de los juegos del usuario
      const appids = activeUser.games.map(game => game.appid);
      
      // Solicitar reviews (limitado a primeros 100 para no saturar)
      const response = await axios.post(`${API_BASE_URL}/games/reviews`, appids.slice(0, 100));
      
      // Combinar datos de juegos con reviews
      const combined = activeUser.games.slice(0, 100).map(game => ({
        ...game,
        reviews: response.data[game.appid] || { percentage: null, review_score_desc: 'Sin datos', total_reviews: 0 }
      }));

      // Ordenar por porcentaje descendente
      combined.sort((a, b) => {
        const percentA = a.reviews.percentage ?? -1;
        const percentB = b.reviews.percentage ?? -1;
        return percentB - percentA;
      });

      setGamesWithReviews(combined);
    } catch (error) {
      console.error('Error cargando reviews:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (percentage) => {
    if (percentage === null || percentage === undefined) return 'score-na';
    if (percentage >= 80) return 'score-green';
    if (percentage >= 70) return 'score-yellow';
    if (percentage >= 40) return 'score-orange';
    return 'score-red';
  };

  return (
    <div className="content-section">
      <div className="section-header">
        <TrendingUp size={32} />
        <h2>Prioridad de Juegos</h2>
        <p className="section-subtitle">
          {activeUser 
            ? `Puntuaciones de Steam - ${activeUser.playerData.personaname}` 
            : 'Selecciona un perfil para ver las puntuaciones'
          }
        </p>
      </div>

      {!activeUser && (
        <div className="empty-state">
          <Star size={48} />
          <p>Busca un perfil de Steam para ver las puntuaciones de sus juegos</p>
        </div>
      )}

      {loading && (
        <div className="loading-indicator">
          <Loader size={32} className="spinner" />
          <p>Cargando puntuaciones de Steam...</p>
          <p className="loading-note">Esto puede tardar hasta 30 segundos para 100 juegos</p>
        </div>
      )}

      {!loading && gamesWithReviews.length > 0 && (
        <div className="games-scores-container">
          <div className="games-scores-header">
            <h3>{gamesWithReviews.length} juegos analizados</h3>
          </div>

          <table className="games-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Juego</th>
                <th>Puntuación Steam</th>
              </tr>
            </thead>
            <tbody>
              {gamesWithReviews.map((game, index) => (
                <tr key={game.appid}>
                  <td className="rank-cell">{index + 1}</td>
                  <td className="game-name-cell">
                    <div className="game-info">
                      <img 
                        src={`https://steamcdn-a.akamaihd.net/steam/apps/${game.appid}/header.jpg`}
                        alt={game.name}
                        className="game-icon"
                        onError={(e) => e.target.style.display = 'none'}
                      />
                      <div>
                        <div className="game-name">{game.name}</div>
                        <div className="game-meta">
                          {game.reviews.total_reviews > 0 && (
                            <span>{game.reviews.total_reviews.toLocaleString()} reviews</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="score-cell">
                    {game.reviews.percentage !== null ? (
                      <div className="score-container">
                        <span className={`score-badge ${getScoreColor(game.reviews.percentage)}`}>
                          {game.reviews.percentage}%
                        </span>
                        <span className="score-desc">{game.reviews.review_score_desc}</span>
                      </div>
                    ) : (
                      <span className="score-na">Sin datos</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default GamePriority;

