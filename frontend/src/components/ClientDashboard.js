import React, { useState, useEffect } from 'react';
import './ClientDashboard.css';

const ClientDashboard = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [user, setUser] = useState(null);
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      setLoading(true);
      
      // Mock user data - in production this would come from authentication
      const mockUser = {
        id: 'USR-001',
        name: 'John Doe',
        email: 'john.doe@company.com',
        company: 'TechCorp Inc',
        memberSince: '2024-01-15',
        totalOrders: 12,
        totalSpent: 487.50,
        plan: 'Professional',
        credits: 150
      };

      // Mock orders data
      const mockOrders = [
        {
          id: 'ORD-2024-001',
          target: 'suspicious-crypto.com',
          type: 'comprehensive',
          tier: 'professional',
          price: 49.99,
          status: 'completed',
          created: '2024-09-05T10:30:00Z',
          completed: '2024-09-05T14:30:00Z',
          deliveryTime: '4 hours',
          reportUrl: '/reports/ORD-2024-001.pdf',
          confidence: 94.7,
          riskLevel: 'HIGH'
        },
        {
          id: 'ORD-2024-002',
          target: 'phishing-email@fake.com',
          type: 'email',
          tier: 'standard',
          price: 24.99,
          status: 'processing',
          created: '2024-09-05T11:15:00Z',
          estimatedCompletion: '2024-09-05T23:15:00Z',
          progress: 65
        },
        {
          id: 'ORD-2024-003',
          target: 'fake-exchange.io',
          type: 'domain',
          tier: 'basic',
          price: 9.99,
          status: 'pending',
          created: '2024-09-05T12:00:00Z',
          estimatedCompletion: '2024-09-06T12:00:00Z',
          progress: 0
        },
        {
          id: 'ORD-2024-004',
          target: 'scam-investment.net',
          type: 'financial',
          tier: 'forensic',
          price: 99.99,
          status: 'completed',
          created: '2024-09-04T09:00:00Z',
          completed: '2024-09-04T12:00:00Z',
          deliveryTime: '3 hours',
          reportUrl: '/reports/ORD-2024-004.pdf',
          confidence: 98.2,
          riskLevel: 'CRITICAL'
        }
      ];

      // Mock notifications
      const mockNotifications = [
        {
          id: 'NOT-001',
          type: 'order_completed',
          title: 'Investigation Complete',
          message: 'Your investigation of suspicious-crypto.com is ready for download.',
          timestamp: '2024-09-05T14:30:00Z',
          read: false,
          orderId: 'ORD-2024-001'
        },
        {
          id: 'NOT-002',
          type: 'order_progress',
          title: 'Investigation In Progress',
          message: 'Your email investigation is 65% complete.',
          timestamp: '2024-09-05T13:45:00Z',
          read: false,
          orderId: 'ORD-2024-002'
        },
        {
          id: 'NOT-003',
          type: 'system',
          title: 'New Feature Available',
          message: 'Cryptocurrency investigation now includes wallet clustering analysis.',
          timestamp: '2024-09-04T16:00:00Z',
          read: true
        }
      ];

      setUser(mockUser);
      setOrders(mockOrders);
      setNotifications(mockNotifications);
      
    } catch (error) {
      console.error('Error loading user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReport = (orderId) => {
    // In production, this would download the actual report
    alert(`Downloading report for order ${orderId}`);
  };

  const handleOrderAgain = (originalOrder) => {
    // In production, this would redirect to order form with pre-filled data
    alert(`Reordering investigation for ${originalOrder.target}`);
  };

  const markNotificationRead = (notificationId) => {
    setNotifications(prev => prev.map(notification => 
      notification.id === notificationId 
        ? { ...notification, read: true }
        : notification
    ));
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadge = (status) => {
    const statusClasses = {
      completed: 'status-completed',
      processing: 'status-processing',
      pending: 'status-pending',
      failed: 'status-failed'
    };
    
    return <span className={`status-badge ${statusClasses[status]}`}>{status}</span>;
  };

  const getRiskBadge = (riskLevel) => {
    const riskClasses = {
      LOW: 'risk-low',
      MEDIUM: 'risk-medium',
      HIGH: 'risk-high',
      CRITICAL: 'risk-critical'
    };
    
    return <span className={`risk-badge ${riskClasses[riskLevel]}`}>{riskLevel}</span>;
  };

  const getProgressBar = (progress) => {
    return (
      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${progress}%` }}
        ></div>
        <span className="progress-text">{progress}%</span>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="client-dashboard loading">
        <div className="loading-spinner">Loading your dashboard...</div>
      </div>
    );
  }

  return (
    <div className="client-dashboard">
      <div className="dashboard-header">
        <div className="user-welcome">
          <h1>Welcome back, {user.name}</h1>
          <p>{user.company} • Member since {new Date(user.memberSince).toLocaleDateString()}</p>
        </div>
        <div className="header-actions">
          <div className="notifications-dropdown">
            <button className="notifications-btn">
              🔔 
              {notifications.filter(n => !n.read).length > 0 && (
                <span className="notification-count">
                  {notifications.filter(n => !n.read).length}
                </span>
              )}
            </button>
          </div>
          <div className="user-menu">
            <div className="user-avatar">{user.name.charAt(0)}</div>
            <span>{user.name}</span>
          </div>
        </div>
      </div>

      <div className="dashboard-tabs">
        <button 
          className={`tab ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Dashboard
        </button>
        <button 
          className={`tab ${activeTab === 'orders' ? 'active' : ''}`}
          onClick={() => setActiveTab('orders')}
        >
          📋 My Orders
        </button>
        <button 
          className={`tab ${activeTab === 'reports' ? 'active' : ''}`}
          onClick={() => setActiveTab('reports')}
        >
          📄 Reports
        </button>
        <button 
          className={`tab ${activeTab === 'account' ? 'active' : ''}`}
          onClick={() => setActiveTab('account')}
        >
          ⚙️ Account
        </button>
        <button 
          className={`tab new-order-tab`}
          onClick={() => window.location.href = '/order'}
        >
          ➕ New Investigation
        </button>
      </div>

      <div className="dashboard-content">
        {activeTab === 'dashboard' && (
          <div className="dashboard-tab">
            {/* Quick Stats */}
            <div className="quick-stats">
              <div className="stat-card">
                <div className="stat-icon">📊</div>
                <div className="stat-content">
                  <div className="stat-value">{user.totalOrders}</div>
                  <div className="stat-label">Total Investigations</div>
                </div>
              </div>
              
              <div className="stat-card">
                <div className="stat-icon">💰</div>
                <div className="stat-content">
                  <div className="stat-value">{formatCurrency(user.totalSpent)}</div>
                  <div className="stat-label">Total Spent</div>
                </div>
              </div>
              
              <div className="stat-card">
                <div className="stat-icon">⚡</div>
                <div className="stat-content">
                  <div className="stat-value">{user.credits}</div>
                  <div className="stat-label">Available Credits</div>
                </div>
              </div>
              
              <div className="stat-card">
                <div className="stat-icon">🎯</div>
                <div className="stat-content">
                  <div className="stat-value">94.7%</div>
                  <div className="stat-label">Avg Accuracy</div>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="recent-activity">
              <h2>Recent Activity</h2>
              <div className="activity-list">
                {orders.slice(0, 3).map(order => (
                  <div key={order.id} className="activity-item">
                    <div className="activity-icon">
                      {order.status === 'completed' ? '✅' : 
                       order.status === 'processing' ? '🔄' : '⏳'}
                    </div>
                    <div className="activity-content">
                      <div className="activity-title">
                        Investigation of {order.target}
                      </div>
                      <div className="activity-details">
                        {order.tier} tier • {formatCurrency(order.price)} • {getStatusBadge(order.status)}
                      </div>
                      <div className="activity-time">
                        {formatDate(order.created)}
                      </div>
                    </div>
                    {order.status === 'completed' && (
                      <button 
                        className="download-btn"
                        onClick={() => handleDownloadReport(order.id)}
                      >
                        📥 Download
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="quick-actions">
              <h2>Quick Actions</h2>
              <div className="actions-grid">
                <button className="action-card" onClick={() => window.location.href = '/order'}>
                  <div className="action-icon">🔍</div>
                  <div className="action-title">New Investigation</div>
                  <div className="action-description">Start a new fraud investigation</div>
                </button>
                
                <button className="action-card" onClick={() => setActiveTab('reports')}>
                  <div className="action-icon">📄</div>
                  <div className="action-title">View Reports</div>
                  <div className="action-description">Access your completed reports</div>
                </button>
                
                <button className="action-card" onClick={() => setActiveTab('account')}>
                  <div className="action-icon">⚙️</div>
                  <div className="action-title">Account Settings</div>
                  <div className="action-description">Manage your account preferences</div>
                </button>
                
                <button className="action-card">
                  <div className="action-icon">💬</div>
                  <div className="action-title">Support</div>
                  <div className="action-description">Get help from our experts</div>
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'orders' && (
          <div className="orders-tab">
            <div className="tab-header">
              <h2>My Orders</h2>
              <div className="order-filters">
                <select>
                  <option value="all">All Orders</option>
                  <option value="completed">Completed</option>
                  <option value="processing">Processing</option>
                  <option value="pending">Pending</option>
                </select>
                <input type="date" />
              </div>
            </div>

            <div className="orders-grid">
              {orders.map(order => (
                <div key={order.id} className="order-card">
                  <div className="order-header">
                    <div className="order-id">{order.id}</div>
                    <div className="order-status">{getStatusBadge(order.status)}</div>
                  </div>
                  
                  <div className="order-content">
                    <div className="order-target">
                      <strong>Target:</strong> {order.target}
                    </div>
                    <div className="order-details">
                      <span className="order-type">{order.type}</span>
                      <span className="order-tier">{order.tier}</span>
                      <span className="order-price">{formatCurrency(order.price)}</span>
                    </div>
                    
                    {order.status === 'processing' && (
                      <div className="order-progress">
                        <div className="progress-label">Progress</div>
                        {getProgressBar(order.progress)}
                        <div className="estimated-completion">
                          Est. completion: {formatDate(order.estimatedCompletion)}
                        </div>
                      </div>
                    )}
                    
                    {order.status === 'completed' && (
                      <div className="order-results">
                        <div className="result-metrics">
                          <div className="metric">
                            <span>Confidence:</span>
                            <span>{order.confidence}%</span>
                          </div>
                          <div className="metric">
                            <span>Risk Level:</span>
                            {getRiskBadge(order.riskLevel)}
                          </div>
                          <div className="metric">
                            <span>Delivery Time:</span>
                            <span>{order.deliveryTime}</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                  
                  <div className="order-actions">
                    <div className="order-date">
                      Created: {formatDate(order.created)}
                    </div>
                    <div className="action-buttons">
                      {order.status === 'completed' && (
                        <>
                          <button 
                            className="download-btn"
                            onClick={() => handleDownloadReport(order.id)}
                          >
                            📥 Download
                          </button>
                          <button 
                            className="reorder-btn"
                            onClick={() => handleOrderAgain(order)}
                          >
                            🔄 Order Again
                          </button>
                        </>
                      )}
                      {order.status === 'processing' && (
                        <button className="track-btn">
                          👁️ Track Progress
                        </button>
                      )}
                      <button className="details-btn">
                        ℹ️ Details
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'reports' && (
          <div className="reports-tab">
            <div className="tab-header">
              <h2>My Reports</h2>
              <div className="report-filters">
                <select>
                  <option value="all">All Reports</option>
                  <option value="high-risk">High Risk</option>
                  <option value="medium-risk">Medium Risk</option>
                  <option value="low-risk">Low Risk</option>
                </select>
                <button className="bulk-download-btn">📦 Bulk Download</button>
              </div>
            </div>

            <div className="reports-grid">
              {orders.filter(order => order.status === 'completed').map(order => (
                <div key={order.id} className="report-card">
                  <div className="report-header">
                    <div className="report-icon">📄</div>
                    <div className="report-info">
                      <div className="report-title">{order.target}</div>
                      <div className="report-subtitle">{order.type} investigation</div>
                    </div>
                    {getRiskBadge(order.riskLevel)}
                  </div>
                  
                  <div className="report-metrics">
                    <div className="metric-item">
                      <span>Confidence</span>
                      <span>{order.confidence}%</span>
                    </div>
                    <div className="metric-item">
                      <span>Tier</span>
                      <span>{order.tier}</span>
                    </div>
                    <div className="metric-item">
                      <span>Completed</span>
                      <span>{formatDate(order.completed)}</span>
                    </div>
                  </div>
                  
                  <div className="report-actions">
                    <button 
                      className="primary-btn"
                      onClick={() => handleDownloadReport(order.id)}
                    >
                      📥 Download PDF
                    </button>
                    <button className="secondary-btn">👁️ Preview</button>
                    <button className="secondary-btn">📧 Share</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'account' && (
          <div className="account-tab">
            <div className="account-sections">
              <div className="account-section">
                <h2>Profile Information</h2>
                <div className="profile-form">
                  <div className="form-group">
                    <label>Full Name</label>
                    <input type="text" value={user.name} readOnly />
                  </div>
                  <div className="form-group">
                    <label>Email Address</label>
                    <input type="email" value={user.email} readOnly />
                  </div>
                  <div className="form-group">
                    <label>Company</label>
                    <input type="text" value={user.company} readOnly />
                  </div>
                  <div className="form-group">
                    <label>Plan</label>
                    <input type="text" value={user.plan} readOnly />
                  </div>
                </div>
              </div>

              <div className="account-section">
                <h2>Billing & Usage</h2>
                <div className="billing-info">
                  <div className="billing-item">
                    <span>Total Spent</span>
                    <span>{formatCurrency(user.totalSpent)}</span>
                  </div>
                  <div className="billing-item">
                    <span>Available Credits</span>
                    <span>{user.credits}</span>
                  </div>
                  <div className="billing-item">
                    <span>Current Plan</span>
                    <span>{user.plan}</span>
                  </div>
                </div>
                <button className="upgrade-btn">⬆️ Upgrade Plan</button>
              </div>

              <div className="account-section">
                <h2>Preferences</h2>
                <div className="preferences-form">
                  <div className="preference-item">
                    <label>
                      <input type="checkbox" defaultChecked />
                      Email notifications for completed investigations
                    </label>
                  </div>
                  <div className="preference-item">
                    <label>
                      <input type="checkbox" defaultChecked />
                      SMS alerts for high-risk findings
                    </label>
                  </div>
                  <div className="preference-item">
                    <label>
                      <input type="checkbox" />
                      Marketing communications
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClientDashboard;

