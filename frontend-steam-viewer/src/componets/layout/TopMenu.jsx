import { useState } from 'react';
import { User, Settings, Info, Menu, TrendingUp, Upload } from 'lucide-react';

const TopMenu = ({ activeTab, onTabChange, onSidebarToggle, activeUser }) => {
  const menuItems = [
    { id: 'profile', label: 'Explorar Perfil', icon: User },
    { id: 'priority', label: 'Prioridad de Juegos', icon: TrendingUp },
    { id: 'custom', label: 'Análisis Personalizado', icon: Upload },
    { id: 'about', label: 'Acerca de', icon: Info },
  ];

  return (
    <nav className="top-menu">
      <div className="menu-container">
        <div className="menu-brand">
          <button className="sidebar-toggle-menu" onClick={onSidebarToggle}>
            <Menu size={20} />
          </button>
          <h2>Steam Viewer</h2>
          {activeUser && (
            <div className="active-user-indicator">
              <img src={activeUser.playerData.avatar} alt={activeUser.playerData.personaname} />
              <span>{activeUser.playerData.personaname}</span>
            </div>
          )}
        </div>
        <div className="menu-items">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                className={`menu-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => onTabChange(item.id)}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

export default TopMenu;
