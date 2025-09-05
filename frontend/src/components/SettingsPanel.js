import React, { useState } from 'react';
import apiService from '../services/apiService';

const SettingsPanel = ({ config, onConfigUpdate, onToggleDemoMode }) => {
  const [apiKeys, setApiKeys] = useState({});
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  const handleApiKeyChange = (service, value) => {
    setApiKeys(prev => ({
      ...prev,
      [service]: value
    }));
  };

  const handleSaveApiKey = async (service) => {
    const apiKey = apiKeys[service];
    if (!apiKey) return;

    setSaving(true);
    try {
      await apiService.updateApiKey(service, apiKey);
      setMessage(`✅ ${service} API key updated successfully`);
      onConfigUpdate();
      setTimeout(() => setMessage(''), 3000);
    } catch (err) {
      setMessage(`❌ Failed to update ${service} API key: ${err.message}`);
      setTimeout(() => setMessage(''), 5000);
    } finally {
      setSaving(false);
    }
  };

  const apiServices = [
    { id: 'rapidapi', name: 'RapidAPI', description: 'Access to 35+ security APIs' },
    { id: 'shodan', name: 'Shodan', description: 'Infrastructure intelligence' },
    { id: 'whoisxml', name: 'WhoisXML', description: 'Domain intelligence' },
    { id: 'opensanctions', name: 'OpenSanctions', description: 'Compliance screening' },
    { id: 'alpha_vantage', name: 'Alpha Vantage', description: 'Financial intelligence' },
    { id: 'cloudflare', name: 'Cloudflare', description: 'DNS & security intelligence' },
    { id: 'ipinfo', name: 'IPinfo', description: 'IP geolocation' },
    { id: 'companies_house', name: 'Companies House', description: 'UK company data' },
    { id: 'virustotal', name: 'VirusTotal', description: 'Malware detection' },
    { id: 'hunter_io', name: 'Hunter.io', description: 'Email discovery' },
  ];

  return (
    <div style={{ padding: '20px' }}>
      <h1>⚙️ Settings & Configuration</h1>
      <p>Configure API keys and system settings</p>

      {message && (
        <div style={{
          padding: '12px 16px',
          margin: '20px 0',
          borderRadius: '8px',
          background: message.includes('✅') ? '#d4edda' : '#f8d7da',
          color: message.includes('✅') ? '#155724' : '#721c24',
          border: `1px solid ${message.includes('✅') ? '#c3e6cb' : '#f5c6cb'}`
        }}>
          {message}
        </div>
      )}

      {/* Demo Mode Toggle */}
      <div style={{
        padding: '20px',
        background: 'white',
        borderRadius: '8px',
        marginBottom: '20px',
        border: '1px solid #e9ecef'
      }}>
        <h3>🧪 Demo Mode</h3>
        <p>Toggle between demo mode (sample data) and production mode (real APIs)</p>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <input
              type="checkbox"
              checked={config.demo_mode}
              onChange={(e) => onToggleDemoMode(e.target.checked)}
            />
            Enable Demo Mode
          </label>
          <span style={{
            padding: '4px 12px',
            borderRadius: '12px',
            fontSize: '0.8rem',
            background: config.demo_mode ? '#fff3cd' : '#d4edda',
            color: config.demo_mode ? '#856404' : '#155724'
          }}>
            {config.demo_mode ? 'Demo Active' : 'Production Active'}
          </span>
        </div>
      </div>

      {/* API Configuration */}
      <div style={{
        padding: '20px',
        background: 'white',
        borderRadius: '8px',
        border: '1px solid #e9ecef'
      }}>
        <h3>🔑 API Configuration</h3>
        <p>Configure API keys for external services</p>
        
        <div style={{ marginBottom: '20px' }}>
          <strong>Status: </strong>
          <span>{config.configured_count || 0} of {config.total_apis || 0} APIs configured</span>
          <div style={{
            width: '100%',
            height: '8px',
            background: '#e9ecef',
            borderRadius: '4px',
            marginTop: '8px',
            overflow: 'hidden'
          }}>
            <div style={{
              width: `${((config.configured_count || 0) / (config.total_apis || 1)) * 100}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #28a745, #20c997)',
              transition: 'width 0.3s ease'
            }}></div>
          </div>
        </div>

        <div style={{ display: 'grid', gap: '20px' }}>
          {apiServices.map(service => (
            <div key={service.id} style={{
              padding: '15px',
              border: '1px solid #e9ecef',
              borderRadius: '8px',
              background: '#f8f9fa'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <div>
                  <h4 style={{ margin: 0 }}>{service.name}</h4>
                  <p style={{ margin: '4px 0 0 0', color: '#6c757d', fontSize: '0.9rem' }}>
                    {service.description}
                  </p>
                </div>
                <span style={{
                  padding: '4px 8px',
                  borderRadius: '12px',
                  fontSize: '0.8rem',
                  background: config.configured_apis?.[service.id] ? '#d4edda' : '#f8d7da',
                  color: config.configured_apis?.[service.id] ? '#155724' : '#721c24'
                }}>
                  {config.configured_apis?.[service.id] ? '✅ Configured' : '❌ Not Configured'}
                </span>
              </div>
              
              <div style={{ display: 'flex', gap: '10px' }}>
                <input
                  type="password"
                  placeholder={`Enter ${service.name} API key...`}
                  value={apiKeys[service.id] || ''}
                  onChange={(e) => handleApiKeyChange(service.id, e.target.value)}
                  style={{
                    flex: 1,
                    padding: '8px 12px',
                    border: '1px solid #ced4da',
                    borderRadius: '4px'
                  }}
                />
                <button
                  onClick={() => handleSaveApiKey(service.id)}
                  disabled={!apiKeys[service.id] || saving}
                  style={{
                    padding: '8px 16px',
                    background: '#007bff',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: apiKeys[service.id] && !saving ? 'pointer' : 'not-allowed',
                    opacity: apiKeys[service.id] && !saving ? 1 : 0.6
                  }}
                >
                  {saving ? 'Saving...' : 'Save'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* System Information */}
      <div style={{
        padding: '20px',
        background: 'white',
        borderRadius: '8px',
        marginTop: '20px',
        border: '1px solid #e9ecef'
      }}>
        <h3>📊 System Information</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
          <div>
            <strong>Version:</strong> ScamShield AI v2.0.0
          </div>
          <div>
            <strong>Build:</strong> 2025.07.10
          </div>
          <div>
            <strong>Mode:</strong> {config.demo_mode ? 'Demo' : 'Production'}
          </div>
          <div>
            <strong>APIs Ready:</strong> {config.configured_count || 0}/{config.total_apis || 0}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPanel;

