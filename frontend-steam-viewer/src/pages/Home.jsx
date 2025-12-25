import { useState } from 'react';
import TopMenu from '../componets/TopMenu';
import ProfileExplorer from './ProfileExplorer';
import Settings from './Settings';
import About from './About';

const Home = () => {
  const [activeTab, setActiveTab] = useState('profile');

  const renderContent = () => {
    switch (activeTab) {
      case 'profile':
        return <ProfileExplorer />;
      case 'settings':
        return <Settings />;
      case 'about':
        return <About />;
      default:
        return <ProfileExplorer />;
    }
  };

  return (
    <div className="home-container">
      <TopMenu activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="main-content">
        {renderContent()}
      </main>
    </div>
  );
};

export default Home;
