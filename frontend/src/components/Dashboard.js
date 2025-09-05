import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [systemStatus, setSystemStatus] = useState('operational');
  const [agentsActive, setAgentsActive] = useState(18);
  const [currentUser] = useState({
    name: 'Security Analyst',
    clearance: 'Intelligence Operator',
    credits: 2847
  });

  const [progressTracker, setProgressTracker] = useState({
    active: false,
    progress: 0,
    currentStage: 'Intelligence Gathering',
    eta: '4 minutes 32 seconds'
  });

  const [selectedMode, setSelectedMode] = useState('speed');
  const [investigationType, setInvestigationType] = useState('url');

  const investigationModes = {
    precision: {
      name: 'Precision Mode',
      agents: 18,
      accuracy: '98.7%',
      credits: '120-500',
      duration: '5-15 min',
      description: 'Deploy all 18 expert agents with full forensic analysis for maximum detection accuracy'
    },
    speed: {
      name: 'Speed Mode',
      agents: '5-8',
      accuracy: '94.2%',
      credits: '10-50',
      duration: '1-3 min',
      description: 'Deploy 5-8 specialized agents for rapid preliminary assessment with excellent accuracy'
    },
    comprehensive: {
      name: 'Comprehensive Mode',
      agents: '12-15',
      accuracy: '97.9%',
      credits: '200-800',
      duration: '10-25 min',
      description: 'Full ensemble analysis with advanced forensics, attribution, and network mapping'
    },
    specialized: {
      name: 'Specialized Mode',
      agents: '8-12',
      accuracy: '99.1%',
      credits: '40-200',
      duration: '3-8 min',
      description: 'Deploy domain-specific expert agents for specialized fraud types and sectors'
    }
  };

  const aiAgents = [
    {
      name: 'Web Intelligence Expert',
      specialty: 'Domain analysis, SSL forensics',
      methodology: 'FBI Cyber Division',
      accuracy: '98.4%',
      avatar: '🌐'
    },
    {
      name: 'Email Intelligence Expert',
      specialty: 'Header analysis, attribution',
      methodology: 'CIA COMINT',
      accuracy: '97.8%',
      avatar: '📧'
    },
    {
      name: 'Visual Intelligence Expert',
      specialty: 'Deepfake detection, forensics',
      methodology: 'Mossad VISINT',
      accuracy: '99.2%',
      avatar: '👁️'
    },
    {
      name: 'Financial Intelligence Expert',
      specialty: 'Money flow, crypto analysis',
      methodology: 'MI6 Economic Intel',
      accuracy: '96.9%',
      avatar: '💰'
    },
    {
      name: 'Network Intelligence Expert',
      specialty: 'Attribution, infrastructure',
      methodology: 'NSA TAO',
      accuracy: '98.7%',
      avatar: '🕸️'
    },
    {
      name: 'Document Intelligence Expert',
      specialty: 'Forensic analysis, authenticity',
      methodology: 'FBI Document Analysis',
      accuracy: '97.3%',
      avatar: '📄'
    },
    {
      name: 'Behavioral Intelligence Expert',
      specialty: 'Pattern analysis, social engineering',
      methodology: 'CIA Psychology Unit',
      accuracy: '95.8%',
      avatar: '🧠'
    },
    {
      name: 'Cryptographic Intelligence Expert',
      specialty: 'Encryption, security protocols',
      methodology: 'GCHQ Crypto',
      accuracy: '98.1%',
      avatar: '🔒'
    },
    {
      name: 'Performance Optimization Agent',
      specialty: 'Resource allocation, cost optimization',
      methodology: 'System Efficiency',
      accuracy: '99.5%',
      avatar: '⚡'
    },
    {
      name: 'Security Monitoring Agent',
      specialty: 'Threat detection, anomaly detection',
      methodology: 'Security Operations',
      accuracy: '99.8%',
      avatar: '🛡️'
    },
    {
      name: 'Infrastructure Management Agent',
      specialty: 'System deployment, health monitoring',
      methodology: 'DevOps Excellence',
      accuracy: '99.97%',
      avatar: '🏗️'
    },
    {
      name: 'Business Intelligence Agent',
      specialty: 'KPI tracking, ROI analysis',
      methodology: 'Analytics Intelligence',
      accuracy: '96.7%',
      avatar: '📊'
    },
    {
      name: 'Master Orchestrator Agent',
      specialty: 'Agent coordination, workflow management',
      methodology: 'System Orchestration',
      accuracy: '99.1%',
      avatar: '🤝'
    },
    {
      name: 'FBI Cyber Agent',
      specialty: 'Advanced technical analysis, threat detection',
      methodology: 'FBI Cyber Division',
      accuracy: '98.9%',
      avatar: '🏛️'
    },
    {
      name: 'CIA Intelligence Agent',
      specialty: 'Deep intelligence gathering, behavioral analysis',
      methodology: 'CIA Operations',
      accuracy: '97.6%',
      avatar: '🕵️'
    },
    {
      name: 'Mossad Intelligence Agent',
      specialty: 'Sophisticated threat assessment, attribution',
      methodology: 'Mossad Intelligence',
      accuracy: '98.3%',
      avatar: '🎯'
    },
    {
      name: 'MI6 Intelligence Agent',
      specialty: 'Strategic intelligence, network analysis',
      methodology: 'MI6 Operations',
      accuracy: '97.1%',
      avatar: '🇬🇧'
    },
    {
      name: 'Elite Intelligence System',
      specialty: 'Multi-agency coordination, advanced analytics',
      methodology: 'Elite Operations',
      accuracy: '99.3%',
      avatar: '⭐'
    }
  ];

  const recentInvestigations = [
    {
      target: 'advanced-crypto-investment-scheme.com',
      type: 'Multi-Modal Investigation',
      time: '3 hours ago',
      credits: 347,
      mode: 'Precision Mode (18 agents)',
      status: 'completed',
      risk: 'high',
      riskScore: '9.4/10'
    },
    {
      target: 'urgent-bank-security-alert@suspicious-domain.net',
      type: 'Email Intelligence Operation',
      time: '1 day ago',
      credits: 156,
      mode: 'Comprehensive Mode (15 agents)',
      status: 'completed',
      risk: 'high',
      riskScore: '8.2/10'
    },
    {
      target: 'Global Financial Consortium LLC',
      type: 'Entity Intelligence Assessment',
      time: '2 days ago',
      credits: 428,
      mode: 'Intelligence Operator Mode',
      status: 'processing',
      risk: 'medium',
      riskScore: 'ETA: 12 min'
    },
    {
      target: 'synthetic-identity-document-sample.pdf',
      type: 'Document Forensic Analysis',
      time: '3 days ago',
      credits: 267,
      mode: 'Specialized Mode (Document Experts)',
      status: 'completed',
      risk: 'high',
      riskScore: '9.7/10'
    }
  ];

  const startInvestigation = (mode) => {
    const selectedModeData = investigationModes[mode];
    setProgressTracker({
      active: true,
      progress: 0,
      currentStage: 'Intelligence Gathering',
      eta: selectedModeData.duration
    });

    // Simulate progress
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 15 + 5;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
        setProgressTracker(prev => ({ ...prev, active: false }));
      }
      setProgressTracker(prev => ({ ...prev, progress }));
    }, 1000);
  };

  const calculateCost = () => {
    const baseCosts = {
      'url': { speed: 15, precision: 180, comprehensive: 320, specialized: 80 },
      'email': { speed: 12, precision: 150, comprehensive: 280, specialized: 65 },
      'document': { speed: 25, precision: 220, comprehensive: 420, specialized: 110 },
      'social': { speed: 35, precision: 280, comprehensive: 550, specialized: 140 },
      'multi': { speed: 45, precision: 380, comprehensive: 750, specialized: 190 }
    };
    
    return baseCosts[investigationType][selectedMode] || 32;
  };

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">🛡️</div>
            <div>
              <div>ScamShield AI <span className="elite-badge">Elite</span></div>
              <div className="subtitle">Intelligence Command Center</div>
            </div>
          </div>
          
          <div className="header-actions">
            <div className="credit-display">
              <span>💎</span>
              <span className="credit-count">{currentUser.credits.toLocaleString()}</span>
              <span>Credits</span>
            </div>
            <div className="user-menu">
              <span>👤 {currentUser.name}</span>
              <span className="user-clearance">{currentUser.clearance}</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="main-container">
        {/* Command Status */}
        <div className="command-status">
          <div className="command-content">
            <div className="command-header">
              <div className="welcome-text">
                <h1>Welcome to Intelligence Command Center</h1>
                <p>Elite fraud investigation platform operational with 18 specialized agents</p>
              </div>
              <div className="system-status">
                <div className="status-indicator">
                  <div className="status-dot"></div>
                  <span>All Systems Operational</span>
                </div>
                <div className="last-updated">Last updated: 2 minutes ago</div>
              </div>
            </div>

            <div className="agents-active">
              <div className="agent-status">
                <span className="agent-count">18</span>
                <span className="agent-label">Agents Active</span>
              </div>
              <div className="agent-status">
                <span className="agent-count">5</span>
                <span className="agent-label">Methodologies</span>
              </div>
              <div className="agent-status">
                <span className="agent-count">50+</span>
                <span className="agent-label">Intel Sources</span>
              </div>
            </div>
          </div>
        </div>

        {/* Progress Tracker */}
        {progressTracker.active && (
          <div className="progress-tracker active">
            <div className="progress-header">
              <div className="progress-title">Investigation In Progress</div>
              <div className="progress-eta">ETA: {progressTracker.eta}</div>
            </div>
            
            <div className="progress-bar-container">
              <div className="progress-bar-fill" style={{width: `${progressTracker.progress}%`}}></div>
            </div>
            
            <div className="current-stage">
              <div className="stage-icon">🔍</div>
              <div className="stage-details">
                <h4>Network Intelligence Analysis</h4>
                <p>Analyzing infrastructure patterns and attribution indicators</p>
              </div>
            </div>
            
            <div className="active-agents">
              <h5>AI Agents Currently Active:</h5>
              <div className="agent-chips">
                <span className="agent-chip">Web Intelligence Expert</span>
                <span className="agent-chip">Network Intelligence Expert</span>
                <span className="agent-chip">Financial Intelligence Expert</span>
                <span className="agent-chip">Attribution Specialist</span>
              </div>
            </div>
          </div>
        )}

        {/* Cost Calculator */}
        <div className="cost-calculator">
          <div className="calculator-header">
            <div className="calculator-title">Investigation Cost Calculator</div>
            <div className="calculator-subtitle">Configure your investigation parameters</div>
          </div>

          <div className="control-group">
            <label className="control-label">Investigation Type</label>
            <select 
              className="control-select" 
              value={investigationType}
              onChange={(e) => setInvestigationType(e.target.value)}
            >
              <option value="url">URL Investigation</option>
              <option value="email">Email Investigation</option>
              <option value="document">Document Analysis</option>
              <option value="social">Social Media Investigation</option>
              <option value="multi">Multi-Modal Investigation</option>
            </select>
          </div>

          <div className="control-group">
            <label className="control-label">Investigation Mode</label>
            <div className="mode-selector">
              {Object.entries(investigationModes).map(([key, mode]) => (
                <div 
                  key={key}
                  className={`mode-option ${selectedMode === key ? 'selected' : ''}`}
                  onClick={() => setSelectedMode(key)}
                >
                  <div className="mode-name">
                    {key === 'speed' && '⚡'} 
                    {key === 'precision' && '🎯'} 
                    {key === 'comprehensive' && '🔍'} 
                    {key === 'specialized' && '🎪'} 
                    {mode.name}
                  </div>
                  <div className="mode-accuracy">{mode.accuracy} Accuracy</div>
                  <div className="mode-cost">{mode.credits} Credits</div>
                </div>
              ))}
            </div>
          </div>

          <div className="cost-breakdown">
            <div className="total-cost">
              <span>Estimated Cost:</span>
              <span className="cost-value">{calculateCost()} Credits</span>
            </div>
          </div>
        </div>

        {/* Dashboard Stats */}
        <div className="dashboard-stats">
          <div className="stat-card">
            <div className="stat-header">
              <div className="stat-title">Total Investigations</div>
              <div className="stat-icon">📊</div>
            </div>
            <div className="stat-value">1,247</div>
            <div className="stat-change positive">
              <span>↗</span>
              <span>+18% from last month</span>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <div className="stat-title">Elite Success Rate</div>
              <div className="stat-icon">✅</div>
            </div>
            <div className="stat-value">98.7%</div>
            <div className="stat-change positive">
              <span>↗</span>
              <span>99.1% accuracy achieved</span>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <div className="stat-title">High Risk Detected</div>
              <div className="stat-icon">⚠️</div>
            </div>
            <div className="stat-value">89</div>
            <div className="stat-change negative">
              <span>↘</span>
              <span>-12% threats this month</span>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-header">
              <div className="stat-title">Avg Intelligence Score</div>
              <div className="stat-icon">🎯</div>
            </div>
            <div className="stat-value">9.2</div>
            <div className="stat-change positive">
              <span>↗</span>
              <span>Elite confidence: 98.7%</span>
            </div>
          </div>
        </div>

        {/* Investigation Modes */}
        <div className="content-section">
          <div className="section-header">
            <div className="section-title">Elite Investigation Modes</div>
            <div className="section-subtitle">Choose your mission parameters and deploy specialized AI agents</div>
          </div>
          <div className="investigation-modes-grid">
            {Object.entries(investigationModes).map(([key, mode]) => (
              <div key={key} className="mode-card" onClick={() => startInvestigation(key)}>
                <div className="mode-icon">
                  {key === 'precision' && '🎯'}
                  {key === 'speed' && '⚡'}
                  {key === 'comprehensive' && '🔍'}
                  {key === 'specialized' && '🎪'}
                </div>
                <div className="mode-title">{mode.name}</div>
                <div className="mode-description">{mode.description}</div>
                <div className="mode-stats">
                  <div className="mode-stat">
                    <div className="mode-stat-value">{mode.accuracy}</div>
                    <div className="mode-stat-label">Accuracy</div>
                  </div>
                  <div className="mode-stat">
                    <div className="mode-stat-value">{mode.agents}</div>
                    <div className="mode-stat-label">{key === 'precision' ? 'Full Deploy' : 'Agents'}</div>
                  </div>
                  <div className="mode-stat">
                    <div className="mode-stat-value">{mode.duration}</div>
                    <div className="mode-stat-label">Duration</div>
                  </div>
                </div>
                <button className="start-mode-btn">
                  {key === 'precision' ? 'Deploy Precision Mode' : 
                   key === 'speed' ? 'Deploy Speed Mode' :
                   key === 'comprehensive' ? 'Deploy Comprehensive Mode' :
                   'Deploy Specialized Mode'}
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* AI Agents Status */}
        <div className="content-section">
          <div className="section-header">
            <div className="section-title">AI Intelligence Agents</div>
            <div className="section-subtitle">18 specialized agents trained with elite intelligence methodologies</div>
          </div>
          <div className="agents-grid">
            {aiAgents.map((agent, index) => (
              <div key={index} className="agent-card">
                <div className="agent-header">
                  <div className="agent-avatar">{agent.avatar}</div>
                  <div className="agent-info">
                    <h4>{agent.name}</h4>
                    <div className="agent-specialty">{agent.specialty}</div>
                  </div>
                </div>
                <div className="agent-methodology">{agent.methodology}</div>
                <div className="agent-status">
                  <div className="agent-active">Active</div>
                  <div className="agent-accuracy">{agent.accuracy} Accuracy</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Investigations */}
        <div className="content-section">
          <div className="section-header">
            <div className="section-title">Recent Intelligence Operations</div>
            <div className="section-subtitle">Track your investigation history and intelligence assessments</div>
          </div>
          <div className="investigation-list">
            <div className="investigation-filters">
              <input 
                type="text" 
                className="search-box" 
                placeholder="Search operations by target, findings, or intelligence level..." 
              />
              <select className="filter-select">
                <option>All Classifications</option>
                <option>High Priority</option>
                <option>Critical Intelligence</option>
                <option>Routine Assessment</option>
              </select>
              <select className="filter-select">
                <option>All Risk Levels</option>
                <option>Critical Risk</option>
                <option>High Risk</option>
                <option>Medium Risk</option>
                <option>Low Risk</option>
              </select>
            </div>

            {recentInvestigations.map((investigation, index) => (
              <div key={index} className="investigation-item">
                <div className="investigation-header">
                  <div>
                    <div className="investigation-target">{investigation.target}</div>
                    <div className="investigation-meta">
                      <span>{investigation.type}</span>
                      <span>•</span>
                      <span>{investigation.time}</span>
                      <span>•</span>
                      <span>{investigation.credits} credits</span>
                      <span>•</span>
                      <span>{investigation.mode}</span>
                    </div>
                  </div>
                  <div className="investigation-actions">
                    <span className={`status-badge status-${investigation.status}`}>
                      {investigation.status === 'completed' ? 'Intel Complete' : 
                       investigation.status === 'processing' ? 'Intel Processing' : 'Failed'}
                    </span>
                    <div className="risk-score">
                      <span className={`risk-indicator risk-${investigation.risk}`}></span>
                      <span>
                        {investigation.risk === 'high' ? 'Critical Risk: ' : 
                         investigation.risk === 'medium' ? 'Medium Risk: ' : 'Low Risk: '}
                        {investigation.riskScore}
                      </span>
                    </div>
                    <button 
                      className="view-report-btn"
                      disabled={investigation.status === 'processing'}
                    >
                      {investigation.status === 'processing' ? 'Processing...' : 'View Intelligence'}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

