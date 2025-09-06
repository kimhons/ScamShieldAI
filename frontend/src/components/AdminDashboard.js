import React, { useState, useEffect } from 'react';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [orders, setOrders] = useState([]);
  const [users, setUsers] = useState([]);
  const [pricingConfig, setPricingConfig] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // In production, these would be actual API calls
      const mockDashboardData = {
        overview: {
          totalRevenue: 12847.50,
          totalOrders: 1247,
          activeUsers: 342,
          averageOrderValue: 34.99,
          conversionRate: 12.4,
          topTier: 'Professional',
          recentGrowth: 23.5
        },
        revenueByTier: {
          basic: { count: 423, revenue: 4207.77 },
          standard: { count: 312, revenue: 7796.88 },
          professional: { count: 398, revenue: 19900.02 },
          forensic: { count: 114, revenue: 11398.86 }
        },
        monthlyStats: [
          { month: 'Jan', orders: 89, revenue: 2847.50 },
          { month: 'Feb', orders: 124, revenue: 3921.75 },
          { month: 'Mar', orders: 156, revenue: 4832.25 },
          { month: 'Apr', orders: 198, revenue: 6234.50 },
          { month: 'May', orders: 234, revenue: 7456.75 },
          { month: 'Jun', orders: 287, revenue: 8923.25 },
          { month: 'Jul', orders: 342, revenue: 10847.50 },
          { month: 'Aug', orders: 398, revenue: 12847.50 }
        ]
      };

      const mockOrders = [
        {
          id: 'ORD-2024-001',
          customer: 'john.doe@company.com',
          target: 'suspicious-crypto.com',
          tier: 'professional',
          price: 49.99,
          status: 'completed',
          created: '2024-09-05T10:30:00Z',
          completed: '2024-09-05T14:30:00Z',
          investigationType: 'comprehensive'
        },
        {
          id: 'ORD-2024-002',
          customer: 'security@bank.com',
          target: 'phishing-site.net',
          tier: 'forensic',
          price: 99.99,
          status: 'processing',
          created: '2024-09-05T11:15:00Z',
          investigationType: 'domain'
        },
        {
          id: 'ORD-2024-003',
          customer: 'analyst@hedge-fund.com',
          target: 'fake-exchange.io',
          tier: 'standard',
          price: 24.99,
          status: 'pending',
          created: '2024-09-05T12:00:00Z',
          investigationType: 'financial'
        }
      ];

      const mockUsers = [
        {
          id: 'USR-001',
          email: 'john.doe@company.com',
          name: 'John Doe',
          company: 'TechCorp Inc',
          totalOrders: 12,
          totalSpent: 487.50,
          lastOrder: '2024-09-05T10:30:00Z',
          status: 'active'
        },
        {
          id: 'USR-002',
          email: 'security@bank.com',
          name: 'Sarah Wilson',
          company: 'SecureBank',
          totalOrders: 8,
          totalSpent: 699.92,
          lastOrder: '2024-09-05T11:15:00Z',
          status: 'active'
        }
      ];

      const mockPricingConfig = {
        basic: {
          price: 9.99,
          features: ['Identity Verification', 'Basic Analysis', 'PDF Export'],
          deliveryTime: '24 hours',
          enabled: true
        },
        standard: {
          price: 24.99,
          features: ['Comprehensive Analysis', 'Multiple Formats', 'Priority Support'],
          deliveryTime: '12 hours',
          enabled: true
        },
        professional: {
          price: 49.99,
          features: ['Expert Analysis', 'All Sources', 'Phone Support'],
          deliveryTime: '6 hours',
          enabled: true
        },
        forensic: {
          price: 99.99,
          features: ['Legal Documentation', 'Court Ready', 'Expert Certification'],
          deliveryTime: '3 hours',
          enabled: true
        }
      };

      setDashboardData(mockDashboardData);
      setOrders(mockOrders);
      setUsers(mockUsers);
      setPricingConfig(mockPricingConfig);
      
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleOrderStatusUpdate = async (orderId, newStatus) => {
    try {
      // In production, this would make an API call
      setOrders(prev => prev.map(order => 
        order.id === orderId ? { ...order, status: newStatus } : order
      ));
      
      // Show success notification
      alert(`Order ${orderId} status updated to ${newStatus}`);
    } catch (error) {
      console.error('Error updating order status:', error);
      alert('Failed to update order status');
    }
  };

  const handlePricingUpdate = async (tier, newPrice) => {
    try {
      // In production, this would make an API call
      setPricingConfig(prev => ({
        ...prev,
        [tier]: { ...prev[tier], price: newPrice }
      }));
      
      alert(`${tier} tier price updated to $${newPrice}`);
    } catch (error) {
      console.error('Error updating pricing:', error);
      alert('Failed to update pricing');
    }
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

  if (loading) {
    return (
      <div className="admin-dashboard loading">
        <div className="loading-spinner">Loading admin dashboard...</div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <div className="dashboard-header">
        <h1>ScamShield AI Admin Dashboard</h1>
        <div className="header-actions">
          <button className="refresh-btn" onClick={loadDashboardData}>
            🔄 Refresh
          </button>
          <div className="admin-info">
            <span>Admin: System Administrator</span>
            <span>Last Updated: {new Date().toLocaleTimeString()}</span>
          </div>
        </div>
      </div>

      <div className="dashboard-tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button 
          className={`tab ${activeTab === 'orders' ? 'active' : ''}`}
          onClick={() => setActiveTab('orders')}
        >
          📋 Orders
        </button>
        <button 
          className={`tab ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          👥 Users
        </button>
        <button 
          className={`tab ${activeTab === 'pricing' ? 'active' : ''}`}
          onClick={() => setActiveTab('pricing')}
        >
          💰 Pricing
        </button>
        <button 
          className={`tab ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          📈 Analytics
        </button>
      </div>

      <div className="dashboard-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="metrics-grid">
              <div className="metric-card revenue">
                <h3>Total Revenue</h3>
                <div className="metric-value">{formatCurrency(dashboardData.overview.totalRevenue)}</div>
                <div className="metric-change positive">+{dashboardData.overview.recentGrowth}% this month</div>
              </div>
              
              <div className="metric-card orders">
                <h3>Total Orders</h3>
                <div className="metric-value">{dashboardData.overview.totalOrders.toLocaleString()}</div>
                <div className="metric-subtitle">All time</div>
              </div>
              
              <div className="metric-card users">
                <h3>Active Users</h3>
                <div className="metric-value">{dashboardData.overview.activeUsers}</div>
                <div className="metric-subtitle">This month</div>
              </div>
              
              <div className="metric-card aov">
                <h3>Avg Order Value</h3>
                <div className="metric-value">{formatCurrency(dashboardData.overview.averageOrderValue)}</div>
                <div className="metric-subtitle">Per investigation</div>
              </div>
            </div>

            <div className="charts-section">
              <div className="chart-card">
                <h3>Revenue by Tier</h3>
                <div className="tier-revenue-chart">
                  {Object.entries(dashboardData.revenueByTier).map(([tier, data]) => (
                    <div key={tier} className="tier-bar">
                      <div className="tier-label">
                        <span className="tier-name">{tier}</span>
                        <span className="tier-count">{data.count} orders</span>
                      </div>
                      <div className="tier-bar-container">
                        <div 
                          className={`tier-bar-fill ${tier}`}
                          style={{ 
                            width: `${(data.revenue / Math.max(...Object.values(dashboardData.revenueByTier).map(d => d.revenue))) * 100}%` 
                          }}
                        ></div>
                      </div>
                      <span className="tier-revenue">{formatCurrency(data.revenue)}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="chart-card">
                <h3>Monthly Growth</h3>
                <div className="monthly-chart">
                  {dashboardData.monthlyStats.map((month, index) => (
                    <div key={month.month} className="month-bar">
                      <div 
                        className="month-bar-fill"
                        style={{ 
                          height: `${(month.revenue / Math.max(...dashboardData.monthlyStats.map(m => m.revenue))) * 100}%` 
                        }}
                      ></div>
                      <div className="month-label">{month.month}</div>
                      <div className="month-value">{formatCurrency(month.revenue)}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'orders' && (
          <div className="orders-tab">
            <div className="tab-header">
              <h2>Order Management</h2>
              <div className="order-filters">
                <select className="filter-select">
                  <option value="all">All Orders</option>
                  <option value="pending">Pending</option>
                  <option value="processing">Processing</option>
                  <option value="completed">Completed</option>
                  <option value="failed">Failed</option>
                </select>
                <input type="date" className="date-filter" />
              </div>
            </div>

            <div className="orders-table">
              <table>
                <thead>
                  <tr>
                    <th>Order ID</th>
                    <th>Customer</th>
                    <th>Target</th>
                    <th>Tier</th>
                    <th>Price</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map(order => (
                    <tr key={order.id}>
                      <td className="order-id">{order.id}</td>
                      <td>{order.customer}</td>
                      <td className="target">{order.target}</td>
                      <td className={`tier ${order.tier}`}>{order.tier}</td>
                      <td className="price">{formatCurrency(order.price)}</td>
                      <td>{getStatusBadge(order.status)}</td>
                      <td>{formatDate(order.created)}</td>
                      <td className="actions">
                        <select 
                          value={order.status}
                          onChange={(e) => handleOrderStatusUpdate(order.id, e.target.value)}
                          className="status-select"
                        >
                          <option value="pending">Pending</option>
                          <option value="processing">Processing</option>
                          <option value="completed">Completed</option>
                          <option value="failed">Failed</option>
                        </select>
                        <button className="view-btn">👁️</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'users' && (
          <div className="users-tab">
            <div className="tab-header">
              <h2>User Management</h2>
              <button className="add-user-btn">+ Add User</button>
            </div>

            <div className="users-table">
              <table>
                <thead>
                  <tr>
                    <th>User ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Company</th>
                    <th>Orders</th>
                    <th>Total Spent</th>
                    <th>Last Order</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map(user => (
                    <tr key={user.id}>
                      <td className="user-id">{user.id}</td>
                      <td>{user.name}</td>
                      <td>{user.email}</td>
                      <td>{user.company}</td>
                      <td>{user.totalOrders}</td>
                      <td className="spent">{formatCurrency(user.totalSpent)}</td>
                      <td>{formatDate(user.lastOrder)}</td>
                      <td>{getStatusBadge(user.status)}</td>
                      <td className="actions">
                        <button className="edit-btn">✏️</button>
                        <button className="view-btn">👁️</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'pricing' && (
          <div className="pricing-tab">
            <div className="tab-header">
              <h2>Pricing Configuration</h2>
              <button className="save-pricing-btn">💾 Save Changes</button>
            </div>

            <div className="pricing-config">
              {Object.entries(pricingConfig).map(([tier, config]) => (
                <div key={tier} className={`pricing-tier-config ${tier}`}>
                  <div className="tier-header">
                    <h3>{tier.charAt(0).toUpperCase() + tier.slice(1)} Tier</h3>
                    <label className="tier-toggle">
                      <input 
                        type="checkbox" 
                        checked={config.enabled}
                        onChange={(e) => setPricingConfig(prev => ({
                          ...prev,
                          [tier]: { ...prev[tier], enabled: e.target.checked }
                        }))}
                      />
                      <span>Enabled</span>
                    </label>
                  </div>

                  <div className="tier-config-grid">
                    <div className="config-item">
                      <label>Price ($)</label>
                      <input 
                        type="number" 
                        value={config.price}
                        step="0.01"
                        onChange={(e) => handlePricingUpdate(tier, parseFloat(e.target.value))}
                      />
                    </div>

                    <div className="config-item">
                      <label>Delivery Time</label>
                      <input 
                        type="text" 
                        value={config.deliveryTime}
                        onChange={(e) => setPricingConfig(prev => ({
                          ...prev,
                          [tier]: { ...prev[tier], deliveryTime: e.target.value }
                        }))}
                      />
                    </div>
                  </div>

                  <div className="tier-features">
                    <label>Features</label>
                    <div className="features-list">
                      {config.features.map((feature, index) => (
                        <div key={index} className="feature-item">
                          <input 
                            type="text" 
                            value={feature}
                            onChange={(e) => {
                              const newFeatures = [...config.features];
                              newFeatures[index] = e.target.value;
                              setPricingConfig(prev => ({
                                ...prev,
                                [tier]: { ...prev[tier], features: newFeatures }
                              }));
                            }}
                          />
                          <button 
                            className="remove-feature"
                            onClick={() => {
                              const newFeatures = config.features.filter((_, i) => i !== index);
                              setPricingConfig(prev => ({
                                ...prev,
                                [tier]: { ...prev[tier], features: newFeatures }
                              }));
                            }}
                          >
                            ❌
                          </button>
                        </div>
                      ))}
                      <button 
                        className="add-feature"
                        onClick={() => {
                          setPricingConfig(prev => ({
                            ...prev,
                            [tier]: { 
                              ...prev[tier], 
                              features: [...prev[tier].features, 'New Feature'] 
                            }
                          }));
                        }}
                      >
                        + Add Feature
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="analytics-tab">
            <div className="tab-header">
              <h2>Advanced Analytics</h2>
              <div className="analytics-filters">
                <select>
                  <option value="7d">Last 7 days</option>
                  <option value="30d">Last 30 days</option>
                  <option value="90d">Last 90 days</option>
                  <option value="1y">Last year</option>
                </select>
              </div>
            </div>

            <div className="analytics-grid">
              <div className="analytics-card">
                <h3>Conversion Funnel</h3>
                <div className="funnel-chart">
                  <div className="funnel-step">
                    <span>Website Visitors</span>
                    <span>10,247</span>
                  </div>
                  <div className="funnel-step">
                    <span>Quote Requests</span>
                    <span>1,847</span>
                  </div>
                  <div className="funnel-step">
                    <span>Orders Placed</span>
                    <span>1,247</span>
                  </div>
                  <div className="funnel-step">
                    <span>Completed Orders</span>
                    <span>1,198</span>
                  </div>
                </div>
              </div>

              <div className="analytics-card">
                <h3>Popular Investigation Types</h3>
                <div className="investigation-types">
                  <div className="type-item">
                    <span>Domain Investigation</span>
                    <div className="type-bar">
                      <div className="type-fill" style={{width: '65%'}}></div>
                    </div>
                    <span>65%</span>
                  </div>
                  <div className="type-item">
                    <span>Email Investigation</span>
                    <div className="type-bar">
                      <div className="type-fill" style={{width: '45%'}}></div>
                    </div>
                    <span>45%</span>
                  </div>
                  <div className="type-item">
                    <span>Comprehensive</span>
                    <div className="type-bar">
                      <div className="type-fill" style={{width: '38%'}}></div>
                    </div>
                    <span>38%</span>
                  </div>
                  <div className="type-item">
                    <span>Financial</span>
                    <div className="type-bar">
                      <div className="type-fill" style={{width: '22%'}}></div>
                    </div>
                    <span>22%</span>
                  </div>
                </div>
              </div>

              <div className="analytics-card">
                <h3>Customer Satisfaction</h3>
                <div className="satisfaction-metrics">
                  <div className="satisfaction-score">
                    <div className="score-circle">
                      <span>4.8</span>
                      <small>/5.0</small>
                    </div>
                    <p>Average Rating</p>
                  </div>
                  <div className="satisfaction-breakdown">
                    <div className="rating-bar">
                      <span>5★</span>
                      <div className="bar"><div style={{width: '78%'}}></div></div>
                      <span>78%</span>
                    </div>
                    <div className="rating-bar">
                      <span>4★</span>
                      <div className="bar"><div style={{width: '18%'}}></div></div>
                      <span>18%</span>
                    </div>
                    <div className="rating-bar">
                      <span>3★</span>
                      <div className="bar"><div style={{width: '3%'}}></div></div>
                      <span>3%</span>
                    </div>
                    <div className="rating-bar">
                      <span>2★</span>
                      <div className="bar"><div style={{width: '1%'}}></div></div>
                      <span>1%</span>
                    </div>
                    <div className="rating-bar">
                      <span>1★</span>
                      <div className="bar"><div style={{width: '0%'}}></div></div>
                      <span>0%</span>
                    </div>
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

export default AdminDashboard;

