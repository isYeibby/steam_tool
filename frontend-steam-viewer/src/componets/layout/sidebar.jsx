import { useState, useEffect } from 'react';
import { History, Star, ChevronLeft, ChevronRight, Trash2 } from 'lucide-react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const Sidebar = ({ isOpen, onToggle, onProfileSelect }) => {
  const [activeTab, setActiveTab] = useState('recent');
  const [recentProfiles, setRecentProfiles] = useState([]);
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen, activeTab]);

  const loadData = async () => {
    try {
      if (activeTab === 'recent') {
        const response = await axios.get(`${API_BASE_URL}/profiles/recent`);
        setRecentProfiles(response.data);
      } else {
        const response = await axios.get(`${API_BASE_URL}/favorites`);
        setFavorites(response.data);
      }
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const handleRemoveFavorite = async (steamId, e) => {
    e.stopPropagation();
    try {
      await axios.delete(`${API_BASE_URL}/favorites/${steamId}`);
      loadData();
    } catch (error) {
      console.error('Error removing favorite:', error);
    }
  };

  const handleProfileClick = (steamId) => {
    onProfileSelect(steamId);
    if (window.innerWidth < 768) {
      onToggle();
    }
  };

  const profiles = activeTab === 'recent' ? recentProfiles : favorites;

  return (
    <>
      <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h3>Perfiles</h3>
        </div>

        <div className="sidebar-tabs">
          <button
            className={`sidebar-tab ${activeTab === 'recent' ? 'active' : ''}`}
            onClick={() => setActiveTab('recent')}
          >
            <History size={18} />
            <span>Recientes</span>
          </button>
          <button
            className={`sidebar-tab ${activeTab === 'favorites' ? 'active' : ''}`}
            onClick={() => setActiveTab('favorites')}
          >
            <Star size={18} />
            <span>Favoritos</span>
          </button>
        </div>

        <div className="sidebar-content">
          {profiles.length === 0 ? (
            <div className="sidebar-empty">
              <p>
                {activeTab === 'recent'
                  ? 'No hay perfiles recientes'
                  : 'No hay favoritos guardados'}
              </p>
            </div>
          ) : (
            <div className="sidebar-list">
              {profiles.map((profile) => (
                <div
                  key={profile.steam_id}
                  className="sidebar-item"
                  onClick={() => handleProfileClick(profile.steam_id)}
                >
                  <img
                    src={profile.avatar}
                    alt={profile.name}
                    className="sidebar-avatar"
                  />
                  <div className="sidebar-info">
                    <div className="sidebar-name">{profile.name}</div>
                    <div className="sidebar-meta">
                      {profile.total_games
                        ? `${profile.total_games} juegos`
                        : 'Steam ID'}
                    </div>
                  </div>
                  {activeTab === 'favorites' && (
                    <button
                      className="sidebar-remove"
                      onClick={(e) => handleRemoveFavorite(profile.steam_id, e)}
                      title="Eliminar de favoritos"
                    >
                      <Trash2 size={16} />
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </aside>

      <button className="sidebar-toggle" onClick={onToggle}>
        {isOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
      </button>
    </>
  );
};

export default Sidebar;
