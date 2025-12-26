import { Upload } from 'lucide-react';

const CustomAnalysis = ({ activeUser }) => {
  return (
    <div className="content-section">
      <div className="section-header">
        <Upload size={32} />
        <h2>Análisis Personalizado</h2>
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

export default CustomAnalysis;
