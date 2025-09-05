import React, { useState, useEffect } from 'react';
import apiService from '../services/apiService';

const AlertsPanel = ({ config }) => {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      const data = await apiService.getAlerts();
      setAlerts(data.alerts || []);
    } catch (err) {
      console.error('Failed to load alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>🚨 Security Alerts</h1>
      <p>Real-time security alerts and threat notifications</p>
      
      {config.demo_mode && (
        <div style={{ 
          padding: '10px 16px', 
          background: '#fff3cd', 
          border: '1px solid #ffeaa7', 
          borderRadius: '8px',
          marginBottom: '20px'
        }}>
          🧪 Demo Mode: Showing sample alerts for demonstration
        </div>
      )}

      {loading ? (
        <div>Loading alerts...</div>
      ) : (
        <div>
          {alerts.length > 0 ? (
            alerts.map((alert, index) => (
              <div key={index} style={{
                padding: '15px',
                margin: '10px 0',
                background: 'white',
                border: '1px solid #e9ecef',
                borderRadius: '8px',
                borderLeft: `4px solid ${alert.severity === 'HIGH' ? '#dc3545' : alert.severity === 'MEDIUM' ? '#ffc107' : '#28a745'}`
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h4>{alert.type?.replace(/_/g, ' ')}</h4>
                  <span style={{
                    padding: '4px 8px',
                    borderRadius: '12px',
                    fontSize: '0.8rem',
                    background: alert.severity === 'HIGH' ? '#f8d7da' : alert.severity === 'MEDIUM' ? '#fff3cd' : '#d4edda',
                    color: alert.severity === 'HIGH' ? '#721c24' : alert.severity === 'MEDIUM' ? '#856404' : '#155724'
                  }}>
                    {alert.severity}
                  </span>
                </div>
                <p><strong>Target:</strong> {alert.target}</p>
                <p><strong>Description:</strong> {alert.description}</p>
                <p><strong>Detected:</strong> {apiService.formatTimestamp(alert.detected_at)}</p>
              </div>
            ))
          ) : (
            <div style={{ textAlign: 'center', padding: '40px', color: '#6c757d' }}>
              ✅ No active security alerts
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AlertsPanel;

