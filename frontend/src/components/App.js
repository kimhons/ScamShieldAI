import React, { useState, useEffect } from 'react';
import './App.css';

// Components
import Dashboard from './components/Dashboard';
import InvestigationPanel from './components/InvestigationPanel';
import AlertsPanel from './components/AlertsPanel';
import ReportsPanel from './components/ReportsPanel';
import SettingsPanel from './components/SettingsPanel';
import Header from './components/Header';
import Sidebar from './components/Sidebar';

// API Service
import apiService from './services/apiService';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [config, setConfig] = useState({
    demo_mode: true,
    configured_apis: {},
    total_apis: 0,
    configured_count: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      setLoading(true);
      const configData = await apiService.getConfig();
      setConfig(configData);
      setError(null);
    } catch (err) {
      console.error('Failed to load config:', err);
      setError('Failed to load configuration');
    } finally {
      setLoading(false);
    }
  };

  const handleViewChange = (view) => {
    setCurrentView(view);
  };

  const handleToggleDemoMode = async (enableDemo) => {
    try {
      await apiService.toggleDemoMode(enableDemo);
      await loadConfig();
    } catch (err) {
      console.error('Failed to toggle demo mode:', err);
      setError('Failed to toggle demo mode');
    }
  };

  const renderCurrentView = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard config={config} />;
      case 'investigate':
        return <InvestigationPanel config={config} />;
      case 'alerts':
        return <AlertsPanel config={config} />;
      case 'reports':
        return <ReportsPanel config={config} />;
      case 'settings':
        return <SettingsPanel config={config} onConfigUpdate={loadConfig} onToggleDemoMode={handleToggleDemoMode} />;
      default:
        return <Dashboard config={config} />;
    }
  };

  if (loading) {
    return (
      <div className="app-loading">
        <div className="loading-spinner"></div>
        <h2>Loading ScamShield AI...</h2>
        <p>Initializing security intelligence platform</p>
      </div>
    );
  }

  return (
    <div className="app">
      <Header 
        config={config} 
        onToggleDemoMode={handleToggleDemoMode}
        error={error}
        onClearError={() => setError(null)}
      />
      
      <div className="app-body">
        <Sidebar 
          currentView={currentView} 
          onViewChange={handleViewChange}
          config={config}
        />
        
        <main className="app-main">
          {error && (
            <div className="error-banner">
              <span className="error-icon">⚠️</span>
              <span className="error-message">{error}</span>
              <button className="error-close" onClick={() => setError(null)}>×</button>
            </div>
          )}
          
          {renderCurrentView()}
        </main>
      </div>
    </div>
  );
}

export default App;

