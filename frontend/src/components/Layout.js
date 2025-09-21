import React from 'react';
import './Layout.css';

const Layout = ({ children, setCurrentView }) => {
  return (
    <div className="layout">
      <nav className="sidebar">
        <h2>AutoApply</h2>
        <ul>
          <li onClick={() => setCurrentView('dashboard')}>Dashboard</li>
          <li onClick={() => setCurrentView('profile')}>Profile</li>
          <li onClick={() => setCurrentView('review')}>Review Applications</li>
          <li onClick={() => setCurrentView('settings')}>Settings</li>
        </ul>
      </nav>
      <main className="content">
        {children}
      </main>
    </div>
  );
};

export default Layout;
