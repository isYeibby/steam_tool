import { Gamepad2, Github, Code, Heart } from 'lucide-react';

const About = () => {
  return (
    <div className="content-section">
      <div className="section-header">
        <h2>Acerca de Steam Viewer</h2>
        <p className="section-subtitle">
          Una aplicación moderna para explorar bibliotecas de Steam
        </p>
      </div>

      <div className="about-content">
        <div className="about-card main-card">
          <Gamepad2 size={48} className="about-icon" />
          <h3>Steam Library Viewer</h3>
          <p>
            Visualiza, analiza y exporta bibliotecas de juegos de Steam de forma
            rápida y elegante. Construido con tecnologías modernas y diseño
            Material Design 3.
          </p>
        </div>

        <div className="features-grid">
          <div className="feature-card">
            <Code size={32} />
            <h4>Tecnología</h4>
            <ul>
              <li>React + Vite</li>
              <li>FastAPI (Python)</li>
              <li>Material Design 3</li>
              <li>Lucide Icons</li>
            </ul>
          </div>

          <div className="feature-card">
            <Heart size={32} />
            <h4>Características</h4>
            <ul>
              <li>Búsqueda de perfiles</li>
              <li>Estadísticas detalladas</li>
              <li>Exportación CSV</li>
              <li>Interfaz moderna</li>
            </ul>
          </div>

          <div className="feature-card">
            <Github size={32} />
            <h4>Código Abierto</h4>
            <p>
              Proyecto de código abierto. Contribuciones bienvenidas en GitHub.
            </p>
            <button className="about-button">
              <Github size={18} /> Ver en GitHub
            </button>
          </div>
        </div>

        <div className="version-info">
          <p>Versión 1.0.0</p>
          <p className="copyright">© 2025 Steam Viewer - Material Design 3</p>
        </div>
      </div>
    </div>
  );
};

export default About;
