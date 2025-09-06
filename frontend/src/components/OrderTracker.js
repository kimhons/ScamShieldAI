import React, { useState, useEffect } from 'react';
import './OrderTracker.css';

const OrderTracker = ({ orderId, onClose }) => {
  const [orderData, setOrderData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshInterval, setRefreshInterval] = useState(null);

  // Fetch order status
  const fetchOrderStatus = async () => {
    try {
      const response = await fetch(`http://localhost:5006/api/orders/${orderId}/status`);
      const data = await response.json();
      
      if (data.success) {
        setOrderData(data);
        setError(null);
      } else {
        setError(data.error || 'Failed to fetch order status');
      }
    } catch (err) {
      setError('Network error: Unable to fetch order status');
    } finally {
      setLoading(false);
    }
  };

  // Set up auto-refresh for active orders
  useEffect(() => {
    fetchOrderStatus();

    // Auto-refresh every 10 seconds for active orders
    if (orderId) {
      const interval = setInterval(() => {
        if (orderData && orderData.status !== 'delivered' && orderData.status !== 'cancelled') {
          fetchOrderStatus();
        }
      }, 10000);
      
      setRefreshInterval(interval);
      
      return () => clearInterval(interval);
    }
  }, [orderId]);

  // Clean up interval
  useEffect(() => {
    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, [refreshInterval]);

  const getStatusColor = (status) => {
    const colors = {
      'pending_payment': '#f59e0b',
      'payment_confirmed': '#10b981',
      'investigation_queued': '#3b82f6',
      'investigation_in_progress': '#8b5cf6',
      'investigation_completed': '#06b6d4',
      'report_generating': '#f97316',
      'report_ready': '#84cc16',
      'delivered': '#22c55e',
      'failed': '#ef4444',
      'cancelled': '#6b7280'
    };
    return colors[status] || '#6b7280';
  };

  const getStatusIcon = (status) => {
    const icons = {
      'pending_payment': '💳',
      'payment_confirmed': '✅',
      'investigation_queued': '⏳',
      'investigation_in_progress': '🔍',
      'investigation_completed': '📊',
      'report_generating': '📄',
      'report_ready': '📋',
      'delivered': '🎉',
      'failed': '❌',
      'cancelled': '🚫'
    };
    return icons[status] || '📦';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString();
  };

  const downloadReport = async (format) => {
    try {
      const accessCode = orderData.delivery_info?.access_code;
      const response = await fetch(
        `http://localhost:5006/api/reports/${orderId}/download/${format}?code=${accessCode}`
      );
      const data = await response.json();
      
      if (data.success) {
        // In a real implementation, this would trigger the actual download
        alert(`Report download initiated: ${data.download_url}`);
      } else {
        alert(`Download failed: ${data.error}`);
      }
    } catch (err) {
      alert('Network error: Unable to download report');
    }
  };

  if (loading) {
    return (
      <div className="order-tracker-overlay">
        <div className="order-tracker-modal">
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading order details...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="order-tracker-overlay">
        <div className="order-tracker-modal">
          <div className="error-container">
            <h2>❌ Error</h2>
            <p>{error}</p>
            <button onClick={onClose} className="close-btn">Close</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="order-tracker-overlay">
      <div className="order-tracker-modal">
        <div className="tracker-header">
          <h2>🔍 Order Tracking</h2>
          <button onClick={onClose} className="close-btn">✕</button>
        </div>

        <div className="order-summary">
          <div className="order-id">
            <strong>Order ID:</strong> {orderData.order_id}
          </div>
          <div className="order-target">
            <strong>Target:</strong> {orderData.target}
          </div>
          <div className="order-tier">
            <strong>Tier:</strong> {orderData.tier}
          </div>
        </div>

        <div className="status-section">
          <div className="current-status">
            <div className="status-icon" style={{ color: getStatusColor(orderData.status) }}>
              {getStatusIcon(orderData.status)}
            </div>
            <div className="status-info">
              <h3>{orderData.status_description}</h3>
              <p>Progress: {orderData.progress}%</p>
            </div>
          </div>

          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ 
                width: `${orderData.progress}%`,
                backgroundColor: getStatusColor(orderData.status)
              }}
            ></div>
          </div>
        </div>

        <div className="milestones-section">
          <h3>Progress Milestones</h3>
          <div className="milestones-list">
            {orderData.milestones?.map((milestone, index) => (
              <div 
                key={index} 
                className={`milestone ${milestone.completed ? 'completed' : 'pending'}`}
              >
                <div className="milestone-icon">
                  {milestone.completed ? '✅' : '⏳'}
                </div>
                <div className="milestone-info">
                  <span className="milestone-step">{milestone.step}</span>
                  <span className="milestone-progress">{milestone.progress}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {orderData.investigation_summary && (
          <div className="investigation-summary">
            <h3>Investigation Summary</h3>
            <div className="summary-grid">
              <div className="summary-item">
                <span className="label">Risk Level:</span>
                <span className={`value risk-${orderData.investigation_summary.risk_level?.toLowerCase()}`}>
                  {orderData.investigation_summary.risk_level}
                </span>
              </div>
              <div className="summary-item">
                <span className="label">Confidence:</span>
                <span className="value">
                  {(orderData.investigation_summary.confidence * 100).toFixed(1)}%
                </span>
              </div>
              <div className="summary-item">
                <span className="label">Findings:</span>
                <span className="value">
                  {orderData.investigation_summary.findings_count} items
                </span>
              </div>
            </div>
          </div>
        )}

        {orderData.delivery_info && Object.keys(orderData.delivery_info).length > 0 && (
          <div className="delivery-section">
            <h3>📥 Report Delivery</h3>
            <div className="delivery-info">
              <div className="access-code">
                <strong>Access Code:</strong> {orderData.delivery_info.access_code}
              </div>
              <div className="expires-at">
                <strong>Expires:</strong> {formatDate(orderData.delivery_info.expires_at)}
              </div>
            </div>
            
            {orderData.status === 'delivered' && (
              <div className="download-section">
                <h4>Download Report</h4>
                <div className="download-buttons">
                  <button 
                    onClick={() => downloadReport('pdf')} 
                    className="download-btn pdf"
                  >
                    📄 PDF Report
                  </button>
                  <button 
                    onClick={() => downloadReport('html')} 
                    className="download-btn html"
                  >
                    🌐 HTML Report
                  </button>
                  <button 
                    onClick={() => downloadReport('json')} 
                    className="download-btn json"
                  >
                    📊 JSON Data
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        <div className="order-details">
          <h3>Order Details</h3>
          <div className="details-grid">
            <div className="detail-item">
              <span className="label">Created:</span>
              <span className="value">{formatDate(orderData.created_at)}</span>
            </div>
            <div className="detail-item">
              <span className="label">Last Updated:</span>
              <span className="value">{formatDate(orderData.updated_at)}</span>
            </div>
            {orderData.estimated_completion && (
              <div className="detail-item">
                <span className="label">Estimated Completion:</span>
                <span className="value">{formatDate(orderData.estimated_completion)}</span>
              </div>
            )}
            <div className="detail-item">
              <span className="label">Customer:</span>
              <span className="value">{orderData.customer_email}</span>
            </div>
          </div>
        </div>

        <div className="tracker-actions">
          <button onClick={fetchOrderStatus} className="refresh-btn">
            🔄 Refresh Status
          </button>
          {orderData.status !== 'delivered' && orderData.status !== 'cancelled' && (
            <button 
              onClick={() => {
                if (confirm('Are you sure you want to cancel this order?')) {
                  // Cancel order logic would go here
                  alert('Order cancellation requested');
                }
              }} 
              className="cancel-btn"
            >
              🚫 Cancel Order
            </button>
          )}
          <button onClick={onClose} className="close-btn">
            Close Tracker
          </button>
        </div>
      </div>
    </div>
  );
};

export default OrderTracker;

