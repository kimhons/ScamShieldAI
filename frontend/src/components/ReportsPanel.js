import React, { useState, useEffect } from 'react';
import apiService from '../services/apiService';

const ReportsPanel = ({ config }) => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      const data = await apiService.getReports();
      setReports(data.reports || []);
    } catch (err) {
      console.error('Failed to load reports:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>📋 Investigation Reports</h1>
      <p>Comprehensive investigation reports and analysis summaries</p>
      
      {config.demo_mode && (
        <div style={{ 
          padding: '10px 16px', 
          background: '#fff3cd', 
          border: '1px solid #ffeaa7', 
          borderRadius: '8px',
          marginBottom: '20px'
        }}>
          🧪 Demo Mode: Showing sample reports for demonstration
        </div>
      )}

      {loading ? (
        <div>Loading reports...</div>
      ) : (
        <div>
          {reports.length > 0 ? (
            <div style={{ display: 'grid', gap: '15px' }}>
              {reports.map((report, index) => (
                <div key={index} style={{
                  padding: '20px',
                  background: 'white',
                  border: '1px solid #e9ecef',
                  borderRadius: '8px',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                    <h4 style={{ margin: 0 }}>{report.title}</h4>
                    <span style={{
                      padding: '4px 8px',
                      borderRadius: '12px',
                      fontSize: '0.8rem',
                      background: report.risk_level === 'HIGH' ? '#f8d7da' : report.risk_level === 'MEDIUM' ? '#fff3cd' : '#d4edda',
                      color: report.risk_level === 'HIGH' ? '#721c24' : report.risk_level === 'MEDIUM' ? '#856404' : '#155724'
                    }}>
                      {report.risk_level}
                    </span>
                  </div>
                  <p><strong>Target:</strong> {report.target}</p>
                  <p><strong>Type:</strong> {report.type}</p>
                  <p><strong>Status:</strong> {report.status}</p>
                  <p><strong>Created:</strong> {apiService.formatTimestamp(report.created_at)}</p>
                  <p>{report.summary}</p>
                  <div style={{ marginTop: '15px' }}>
                    <button style={{
                      padding: '8px 16px',
                      background: '#007bff',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      marginRight: '10px'
                    }}>
                      📄 View Report
                    </button>
                    <button style={{
                      padding: '8px 16px',
                      background: '#6c757d',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}>
                      📤 Export
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '40px', color: '#6c757d' }}>
              📋 No investigation reports available
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ReportsPanel;

