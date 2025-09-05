import React from 'react';
import './Sidebar.css';

const Sidebar = ({ currentView, onViewChange, config }) => {
  const menuItems = [
    {
      id: 'dashboard',
      icon: '📊',
      label: 'Dashboard',
      description: 'Overview & Metrics'
    },
    {
      id: 'investigate',
      icon: '🔍',
      label: 'Investigate',
      description: 'Security Analysis'
    },
    {
      id: 'alerts',
      icon: '🚨',
      label: 'Alerts',
      description: 'Security Alerts'
    },
    {
      id: 'reports',
      icon: '📋',
      label: 'Reports',
      description: 'Investigation Reports'
    },
    {
      id: 'settings',
      icon: '⚙️',
      label: 'Settings',
      description: 'Configuration'
    }
  ];

  return (
    <aside className="app-sidebar">
      <nav className="sidebar-nav">
        <div className="nav-section">
          <h3 className="nav-title">Main</h3>
          <ul className="nav-list">
            {menuItems.map((item) => (
              <li key={item.id} className="nav-item">
                <button
                  onClick={() => onViewChange(item.id)}
                  className={`nav-link ${currentView === item.id ? 'active' : ''}`}
                  title={item.description}
                >
                  <span className="nav-icon">{item.icon}</span>
                  <div className="nav-content">
                    <span className="nav-label">{item.label}</span>
                    <span className="nav-description">{item.description}</span>
                  </div>
                </button>
              </li>
            ))}
          </ul>
        </div>

        <div className="nav-section">
          <h3 className="nav-title">Quick Actions</h3>
          <ul className="nav-list">
            <li className="nav-item">
              <button className="nav-link quick-action" onClick={() => onViewChange('investigate')}>
                <span className="nav-icon">⚡</span>
                <div className="nav-content">
                  <span className="nav-label">Quick Scan</span>
                  <span className="nav-description">Fast Analysis</span>
                </div>
              </button>
            </li>
            <li className="nav-item">
              <button className="nav-link quick-action">
                <span className="nav-icon">📤</span>
                <div className="nav-content">
                  <span className="nav-label">Export Data</span>
                  <span className="nav-description">Download Reports</span>
                </div>
              </button>
            </li>
          </ul>
        </div>

        <div className="nav-section">
          <h3 className="nav-title">System Status</h3>
          <div className="system-status">
            <div className="status-item">
              <div className="status-indicator">
                <span className={`status-dot ${config.demo_mode ? 'warning' : 'success'}`}></span>
                <span className="status-text">
                  {config.demo_mode ? 'Demo Mode' : 'Production'}
                </span>
              </div>
            </div>
            
            <div className="status-item">
              <div className="status-indicator">
                <span className="status-dot success"></span>
                <span className="status-text">System Online</span>
              </div>
            </div>
            
            <div className="status-item">
              <div className="status-indicator">
                <span className={`status-dot ${(config.configured_count || 0) > 5 ? 'success' : 'warning'}`}></span>
                <span className="status-text">
                  {config.configured_count || 0} APIs Ready
                </span>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <div className="sidebar-footer">
        <div className="version-info">
          <span className="version-label">ScamShield AI</span>
          <span className="version-number">v2.0.0</span>
        </div>
        <div className="build-info">
          <span className="build-label">Build:</span>
          <span className="build-number">2025.07.10</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;

