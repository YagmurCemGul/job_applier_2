import React, { useState } from 'react';
import './App.css';
import Layout from './components/Layout';
import Dashboard from './components/Dashboard';
import Profile from './components/Profile';
import Review from './components/Review';
import Settings from './components/Settings';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');

  const renderView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard />;
      case 'profile':
        return <Profile />;
      case 'review':
        return <Review />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <Layout setCurrentView={setCurrentView}>
      {renderView()}
    </Layout>
  );
}

export default App;
