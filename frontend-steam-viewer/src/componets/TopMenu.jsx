import { useState } from 'react';
import { User, Settings, Info } from 'lucide-react';

const TopMenu = ({ activeTab, onTabChange }) => {
  const menuItems = [
    { id: 'profile', label: 'Explorar Perfil', icon: User },
    { id: 'settings', label: 'Configuración', icon: Settings },
    { id: 'about', label: 'Acerca de', icon: Info },
  ];

  return (
    <nav className="top-menu">
      <div className="menu-container">
        <div className="menu-brand">
          <h2>Steam Viewer</h2>
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
