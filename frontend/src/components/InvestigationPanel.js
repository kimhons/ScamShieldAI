import React, { useState, useEffect } from 'react';
import apiService from '../services/apiService';
import './InvestigationPanel.css';

const InvestigationPanel = ({ config }) => {
  const [investigationType, setInvestigationType] = useState('auto');
  const [target, setTarget] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // Load investigation history from localStorage
    const savedHistory = localStorage.getItem('scamshield_investigation_history');
    if (savedHistory) {
      try {
        setHistory(JSON.parse(savedHistory));
      } catch (err) {
        console.error('Failed to load investigation history:', err);
      }
    }
  }, []);

  const saveToHistory = (investigation) => {
    const newHistory = [investigation, ...history.slice(0, 9)]; // Keep last 10
    setHistory(newHistory);
    localStorage.setItem('scamshield_investigation_history', JSON.stringify(newHistory));
  };

  const handleInvestigation = async () => {
    if (!target.trim()) {
      setError('Please enter a target to investigate');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      let result;
      const detectedType = apiService.detectInvestigationType(target);
      const finalType = investigationType === 'auto' ? detectedType : investigationType;

      // Validate input based on type
      if (finalType === 'domain' && !apiService.validateDomain(target)) {
        throw new Error('Invalid domain format');
      }
      if (finalType === 'ip' && !apiService.validateIP(target)) {
        throw new Error('Invalid IP address format');
      }
      if (finalType === 'email' && !apiService.validateEmail(target)) {
        throw new Error('Invalid email format');
      }

      // Perform investigation based on type
      switch (finalType) {
        case 'domain':
          result = await apiService.investigateDomain(target);
          break;
        case 'ip':
          result = await apiService.investigateIP(target);
          break;
        case 'email':
          result = await apiService.investigateEmail(target);
          break;
        case 'company':
          result = await apiService.investigateCompany(target);
          break;
        case 'financial':
          result = await apiService.investigateFinancial(target);
          break;
        default:
          result = await apiService.comprehensiveInvestigation(target, finalType);
      }

      setResults({
        ...result,
        investigation_type: finalType,
        target: target,
        timestamp: new Date().toISOString()
      });

      // Save to history
      saveToHistory({
        target,
        type: finalType,
        timestamp: new Date().toISOString(),
        risk_level: result.risk_assessment?.risk_level || result.security_analysis?.risk_level || 'UNKNOWN'
      });

    } catch (err) {
      console.error('Investigation failed:', err);
      setError(apiService.handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleQuickInvestigation = (historyItem) => {
    setTarget(historyItem.target);
    setInvestigationType(historyItem.type);
  };

  const clearResults = () => {
    setResults(null);
    setError(null);
  };

  const exportResults = async (format) => {
    if (!results) return;

    try {
      const exportData = await apiService.exportData(format, results);
      // In a real implementation, this would trigger a download
      alert(`Export to ${format.toUpperCase()} initiated. Check downloads folder.`);
    } catch (err) {
      console.error('Export failed:', err);
      setError(`Export failed: ${err.message}`);
    }
  };

  const renderResults = () => {
    if (!results) return null;

    const investigationType = results.investigation_type;

    return (
      <div className="investigation-results">
        <div className="results-header">
          <div className="results-title">
            <h3>🔍 Investigation Results</h3>
            <span className="results-type">{investigationType.toUpperCase()}</span>
          </div>
          <div className="results-actions">
            <button onClick={() => exportResults('json')} className="btn btn-secondary">
              📄 Export JSON
            </button>
            <button onClick={() => exportResults('pdf')} className="btn btn-secondary">
              📑 Export PDF
            </button>
            <button onClick={clearResults} className="btn btn-outline">
              ✕ Clear
            </button>
          </div>
        </div>

        <div className="results-content">
          {/* Target Information */}
          <div className="result-section">
            <h4>🎯 Target Information</h4>
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Target:</span>
                <span className="info-value">{results.target}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Type:</span>
                <span className="info-value">{investigationType}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Timestamp:</span>
                <span className="info-value">{apiService.formatTimestamp(results.timestamp)}</span>
              </div>
            </div>
          </div>

          {/* Risk Assessment */}
          {(results.risk_assessment || results.security_analysis) && (
            <div className="result-section">
              <h4>⚠️ Risk Assessment</h4>
              <div className="risk-assessment">
                {results.risk_assessment && (
                  <>
                    <div className="risk-level">
                      <span className="risk-icon">
                        {apiService.getRiskLevelIcon(results.risk_assessment.risk_level)}
                      </span>
                      <span className="risk-text">
                        Risk Level: <strong>{results.risk_assessment.risk_level}</strong>
                      </span>
                      {results.risk_assessment.risk_score && (
                        <span className="risk-score">
                          Score: {apiService.formatRiskScore(results.risk_assessment.risk_score)}
                        </span>
                      )}
                    </div>
                    {results.risk_assessment.confidence && (
                      <div className="confidence">
                        Confidence: {results.risk_assessment.confidence}%
                      </div>
                    )}
                  </>
                )}
                
                {results.security_analysis && (
                  <div className="security-indicators">
                    <h5>Security Indicators:</h5>
                    <div className="indicators-grid">
                      {Object.entries(results.security_analysis).map(([key, value]) => (
                        <div key={key} className="indicator-item">
                          <span className="indicator-label">{key.replace(/_/g, ' ')}:</span>
                          <span className={`indicator-value ${typeof value === 'boolean' ? (value ? 'positive' : 'negative') : ''}`}>
                            {typeof value === 'boolean' ? (value ? '✅ Yes' : '❌ No') : value}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Domain-specific results */}
          {investigationType === 'domain' && results.whois_data && (
            <div className="result-section">
              <h4>🌐 Domain Information</h4>
              <div className="domain-info">
                <div className="info-grid">
                  <div className="info-item">
                    <span className="info-label">Registrar:</span>
                    <span className="info-value">{results.whois_data.registrar}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Creation Date:</span>
                    <span className="info-value">{results.whois_data.creation_date}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Expiration:</span>
                    <span className="info-value">{results.whois_data.expiration_date}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Country:</span>
                    <span className="info-value">{results.whois_data.registrant_country}</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* IP-specific results */}
          {investigationType === 'ip' && results.geolocation && (
            <div className="result-section">
              <h4>🌍 Geolocation Information</h4>
              <div className="geolocation-info">
                <div className="info-grid">
                  <div className="info-item">
                    <span className="info-label">Country:</span>
                    <span className="info-value">{results.geolocation.country}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">City:</span>
                    <span className="info-value">{results.geolocation.city}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Coordinates:</span>
                    <span className="info-value">{results.geolocation.latitude}, {results.geolocation.longitude}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Timezone:</span>
                    <span className="info-value">{results.geolocation.timezone}</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Network Information */}
          {results.network_info && (
            <div className="result-section">
              <h4>🔗 Network Information</h4>
              <div className="network-info">
                <div className="info-grid">
                  {Object.entries(results.network_info).map(([key, value]) => (
                    <div key={key} className="info-item">
                      <span className="info-label">{key.replace(/_/g, ' ')}:</span>
                      <span className="info-value">{value}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Investigation Notes */}
          {results.investigation_notes && (
            <div className="result-section">
              <h4>📝 Investigation Notes</h4>
              <div className="investigation-notes">
                <p>{results.investigation_notes}</p>
              </div>
            </div>
          )}

          {/* Raw Data (Collapsible) */}
          <details className="result-section raw-data">
            <summary>🔧 Raw Data (Advanced)</summary>
            <pre className="raw-data-content">
              {JSON.stringify(results, null, 2)}
            </pre>
          </details>
        </div>
      </div>
    );
  };

  return (
    <div className="investigation-panel">
      <div className="panel-header">
        <h1>🔍 Investigation Center</h1>
        <p>Comprehensive fraud investigation and security intelligence analysis</p>
        {config.demo_mode && (
          <div className="demo-notice">
            <span className="demo-icon">🧪</span>
            <span>Demo Mode: Showing sample data for demonstration purposes</span>
          </div>
        )}
      </div>

      <div className="investigation-form">
        <div className="form-section">
          <h3>🎯 New Investigation</h3>
          
          <div className="form-group">
            <label htmlFor="investigation-type">Investigation Type:</label>
            <select
              id="investigation-type"
              value={investigationType}
              onChange={(e) => setInvestigationType(e.target.value)}
              className="form-control"
            >
              <option value="auto">🤖 Auto-detect</option>
              <option value="domain">🌐 Domain</option>
              <option value="ip">🌍 IP Address</option>
              <option value="email">📧 Email</option>
              <option value="company">🏢 Company</option>
              <option value="financial">💰 Financial Symbol</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="target-input">Target to Investigate:</label>
            <div className="input-group">
              <input
                id="target-input"
                type="text"
                value={target}
                onChange={(e) => setTarget(e.target.value)}
                placeholder="Enter domain, IP, email, company name, or financial symbol..."
                className="form-control"
                onKeyPress={(e) => e.key === 'Enter' && handleInvestigation()}
              />
              <button
                onClick={handleInvestigation}
                disabled={loading || !target.trim()}
                className="btn btn-primary"
              >
                {loading ? '🔄 Investigating...' : '🔍 Investigate'}
              </button>
            </div>
          </div>

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Quick Examples */}
        <div className="form-section">
          <h4>⚡ Quick Examples</h4>
          <div className="quick-examples">
            <button onClick={() => setTarget('suspicious-bank.com')} className="example-btn">
              🌐 suspicious-bank.com
            </button>
            <button onClick={() => setTarget('192.168.1.100')} className="example-btn">
              🌍 192.168.1.100
            </button>
            <button onClick={() => setTarget('scammer@phishing-site.biz')} className="example-btn">
              📧 scammer@phishing-site.biz
            </button>
            <button onClick={() => setTarget('Suspicious Holdings Ltd')} className="example-btn">
              🏢 Suspicious Holdings Ltd
            </button>
          </div>
        </div>

        {/* Investigation History */}
        {history.length > 0 && (
          <div className="form-section">
            <h4>📚 Recent Investigations</h4>
            <div className="investigation-history">
              {history.slice(0, 5).map((item, index) => (
                <div key={index} className="history-item" onClick={() => handleQuickInvestigation(item)}>
                  <div className="history-content">
                    <span className="history-target">{item.target}</span>
                    <span className="history-type">{item.type}</span>
                  </div>
                  <div className="history-meta">
                    <span className={`history-risk ${item.risk_level?.toLowerCase()}`}>
                      {apiService.getRiskLevelIcon(item.risk_level)}
                    </span>
                    <span className="history-time">
                      {apiService.formatTimestamp(item.timestamp)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Results */}
      {renderResults()}

      {/* Loading State */}
      {loading && (
        <div className="investigation-loading">
          <div className="loading-spinner"></div>
          <h3>🔍 Investigating {target}...</h3>
          <p>Analyzing security intelligence data from multiple sources</p>
          <div className="loading-steps">
            <div className="loading-step">✅ Validating target</div>
            <div className="loading-step">🔄 Gathering intelligence</div>
            <div className="loading-step">⏳ Analyzing risk factors</div>
            <div className="loading-step">⏳ Generating report</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InvestigationPanel;

