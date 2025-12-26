import { TrendingUp } from 'lucide-react';

const GamePriority = ({ activeUser }) => {
  return (
    <div className="content-section">
      <div className="section-header">
        <TrendingUp size={32} />
        <h2>Prioridad de Juegos</h2>
        <p className="section-subtitle">
          {activeUser 
            ? `Usuario activo: ${activeUser.playerData.personaname}` 
            : 'Esta sección está en desarrollo'
          }
        </p>
      </div>
    </div>
  );
};

export default GamePriority;

