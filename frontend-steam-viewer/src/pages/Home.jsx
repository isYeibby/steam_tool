import { useState } from 'react';
import TopMenu from '../componets/layout/TopMenu';
import Sidebar from '../componets/layout/Sidebar';
import ProfileExplorer from './ProfileExplorer';
import GamePriority from './GamePriority';
import CustomAnalysis from './CustomAnalysis';
import About from './About';

const Home = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedSteamId, setSelectedSteamId] = useState(null);

  const handleProfileSelect = (steamId) => {
    setSelectedSteamId(steamId);
    setActiveTab('profile');
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'profile':
        return <ProfileExplorer initialSteamId={selectedSteamId} />;
      case 'priority':
        return <GamePriority />;
      case 'custom':
        return <CustomAnalysis />;
      case 'about':
        return <About />;
      default:
        return <ProfileExplorer />;
    }
  };

  return (
    <div className="home-container">
      <TopMenu 
        activeTab={activeTab} 
        onTabChange={setActiveTab}
        onSidebarToggle={() => setSidebarOpen(!sidebarOpen)}
      />
      <div className="content-wrapper">
        <Sidebar 
          isOpen={sidebarOpen} 
          onToggle={() => setSidebarOpen(!sidebarOpen)}
          onProfileSelect={handleProfileSelect}
        />
        <main className={`main-content ${sidebarOpen ? 'sidebar-open' : ''}`}>
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default Home;
