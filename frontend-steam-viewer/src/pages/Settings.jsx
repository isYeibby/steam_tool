import { Settings as SettingsIcon, Globe, Palette, Database } from 'lucide-react';

const Settings = () => {
  return (
    <div className="content-section">
      <div className="section-header">
        <h2>Configuración</h2>
        <p className="section-subtitle">
          Personaliza tu experiencia con Steam Viewer
        </p>
      </div>

      <div className="settings-grid">
        <div className="setting-card">
          <div className="setting-icon">
            <Globe size={24} />
          </div>
          <div className="setting-content">
            <h3>Idioma</h3>
            <p>Cambia el idioma de la interfaz</p>
            <select className="setting-select">
              <option>Español</option>
              <option>English</option>
              <option>Português</option>
            </select>
          </div>
        </div>

        <div className="setting-card">
          <div className="setting-icon">
            <Palette size={24} />
          </div>
          <div className="setting-content">
            <h3>Tema</h3>
            <p>Ajusta la apariencia visual</p>
            <select className="setting-select">
              <option>Oscuro (Material Design 3)</option>
              <option>Claro</option>
              <option>Automático</option>
            </select>
          </div>
        </div>

        <div className="setting-card">
          <div className="setting-icon">
            <Database size={24} />
          </div>
          <div className="setting-content">
            <h3>Caché</h3>
            <p>Gestiona los datos almacenados</p>
            <button className="setting-button">Limpiar Caché</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
