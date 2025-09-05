import React from 'react';
import './Header.css';

const Header = ({ config, onToggleDemoMode, error, onClearError }) => {
  const handleDemoToggle = () => {
    onToggleDemoMode(!config.demo_mode);
  };

  return (
    <header className="app-header">
      <div className="header-left">
        <div className="logo">
          <span className="logo-icon">🛡️</span>
          <span className="logo-text">ScamShield AI</span>
          <span className="logo-subtitle">Nexus Security Intelligence</span>
        </div>
      </div>

      <div className="header-center">
        <div className="status-indicators">
          <div className="status-item">
            <span className="status-label">APIs:</span>
            <span className="status-value">
              {config.configured_count || 0}/{config.total_apis || 0}
            </span>
            <div className="status-bar">
              <div 
                className="status-fill" 
                style={{ 
                  width: `${((config.configured_count || 0) / (config.total_apis || 1)) * 100}%` 
                }}
              ></div>
            </div>
          </div>
          
          <div className="status-item">
            <span className="status-label">Mode:</span>
            <span className={`status-badge ${config.demo_mode ? 'demo' : 'production'}`}>
              {config.demo_mode ? '🧪 Demo' : '🚀 Live'}
            </span>
          </div>
        </div>
      </div>

      <div className="header-right">
        <button 
          onClick={handleDemoToggle}
          className={`mode-toggle ${config.demo_mode ? 'demo' : 'production'}`}
          title={`Switch to ${config.demo_mode ? 'Production' : 'Demo'} Mode`}
        >
          {config.demo_mode ? '🚀 Go Live' : '🧪 Demo Mode'}
        </button>
        
        <div className="user-menu">
          <div className="user-avatar">
            <span>👤</span>
          </div>
          <div className="user-info">
            <span className="user-name">Security Analyst</span>
            <span className="user-role">Administrator</span>
          </div>
        </div>
      </div>

      {error && (
        <div className="header-error">
          <span className="error-icon">⚠️</span>
          <span className="error-text">{error}</span>
          <button onClick={onClearError} className="error-close">×</button>
        </div>
      )}
    </header>
  );
};

export default Header;

