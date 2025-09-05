/**
 * API Service for ScamShield AI Frontend
 * Handles all communication with the backend API
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://5000-itrrkh6uq0x4t4661nmkt-0b63962a.manusvm.computer/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  // Configuration endpoints
  async getConfig() {
    return this.request('/config');
  }

  async toggleDemoMode(enableDemo) {
    return this.request('/config/demo', {
      method: 'POST',
      body: JSON.stringify({ enable_demo: enableDemo }),
    });
  }

  async updateApiKey(service, apiKey) {
    return this.request('/config/api-key', {
      method: 'POST',
      body: JSON.stringify({ service, api_key: apiKey }),
    });
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }

  // Investigation endpoints
  async investigateDomain(domain) {
    return this.request('/investigate/domain', {
      method: 'POST',
      body: JSON.stringify({ domain }),
    });
  }

  async investigateIP(ipAddress) {
    return this.request('/investigate/ip', {
      method: 'POST',
      body: JSON.stringify({ ip_address: ipAddress }),
    });
  }

  async investigateEmail(email) {
    return this.request('/investigate/email', {
      method: 'POST',
      body: JSON.stringify({ email }),
    });
  }

  async investigateCompany(companyName) {
    return this.request('/investigate/company', {
      method: 'POST',
      body: JSON.stringify({ company_name: companyName }),
    });
  }

  async investigateFinancial(symbol) {
    return this.request('/investigate/financial', {
      method: 'POST',
      body: JSON.stringify({ symbol }),
    });
  }

  async comprehensiveInvestigation(target, type = 'auto') {
    return this.request('/investigate/comprehensive', {
      method: 'POST',
      body: JSON.stringify({ target, type }),
    });
  }

  // Dashboard and monitoring
  async getDashboardMetrics() {
    return this.request('/dashboard/metrics');
  }

  async getAlerts() {
    return this.request('/alerts');
  }

  async getReports() {
    return this.request('/reports');
  }

  // Search
  async search(query, type = 'all') {
    return this.request('/search', {
      method: 'POST',
      body: JSON.stringify({ query, type }),
    });
  }

  // Export
  async exportData(format, data) {
    return this.request(`/export/${format}`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Utility methods
  formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleString();
  }

  getRiskLevelColor(riskLevel) {
    switch (riskLevel?.toUpperCase()) {
      case 'LOW':
        return '#28a745';
      case 'MEDIUM':
        return '#ffc107';
      case 'HIGH':
        return '#fd7e14';
      case 'CRITICAL':
        return '#dc3545';
      default:
        return '#6c757d';
    }
  }

  getRiskLevelIcon(riskLevel) {
    switch (riskLevel?.toUpperCase()) {
      case 'LOW':
        return '✅';
      case 'MEDIUM':
        return '⚠️';
      case 'HIGH':
        return '🔴';
      case 'CRITICAL':
        return '🚨';
      default:
        return '❓';
    }
  }

  formatRiskScore(score) {
    if (typeof score !== 'number') return 'N/A';
    return `${score}/100`;
  }

  // Auto-detect investigation type
  detectInvestigationType(target) {
    if (!target) return 'unknown';
    
    // Email detection
    if (target.includes('@') && target.includes('.')) {
      return 'email';
    }
    
    // IP address detection
    if (/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(target)) {
      return 'ip';
    }
    
    // Domain detection
    if (target.includes('.') && !target.includes(' ')) {
      return 'domain';
    }
    
    // Financial symbol detection (simple heuristic)
    if (/^[A-Z]{1,5}$/.test(target.toUpperCase())) {
      return 'financial';
    }
    
    // Default to company
    return 'company';
  }

  // Validation helpers
  validateDomain(domain) {
    const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9](?:\.[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9])*$/;
    return domainRegex.test(domain);
  }

  validateIP(ip) {
    const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    return ipRegex.test(ip);
  }

  validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  // Error handling helpers
  handleApiError(error) {
    console.error('API Error:', error);
    
    if (error.message.includes('Failed to fetch')) {
      return 'Unable to connect to ScamShield AI backend. Please check if the server is running.';
    }
    
    if (error.message.includes('404')) {
      return 'API endpoint not found. Please check the server configuration.';
    }
    
    if (error.message.includes('500')) {
      return 'Internal server error. Please try again later.';
    }
    
    return error.message || 'An unexpected error occurred.';
  }

  // Demo data helpers
  generateDemoAlert() {
    const alertTypes = ['PHISHING_DETECTED', 'MALWARE_FOUND', 'SUSPICIOUS_DOMAIN', 'HIGH_RISK_IP'];
    const severities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
    
    return {
      id: `ALT-${Math.floor(Math.random() * 900000) + 100000}`,
      type: alertTypes[Math.floor(Math.random() * alertTypes.length)],
      severity: severities[Math.floor(Math.random() * severities.length)],
      target: `demo-target-${Math.floor(Math.random() * 1000)}.com`,
      description: 'Demo security alert for testing purposes',
      timestamp: new Date().toISOString(),
      status: 'NEW'
    };
  }

  // Performance monitoring
  async measureApiPerformance(endpoint, operation) {
    const startTime = performance.now();
    
    try {
      const result = await operation();
      const endTime = performance.now();
      const duration = endTime - startTime;
      
      console.log(`API Performance: ${endpoint} took ${duration.toFixed(2)}ms`);
      
      return {
        success: true,
        result,
        duration,
        endpoint
      };
    } catch (error) {
      const endTime = performance.now();
      const duration = endTime - startTime;
      
      console.error(`API Performance: ${endpoint} failed after ${duration.toFixed(2)}ms`, error);
      
      return {
        success: false,
        error,
        duration,
        endpoint
      };
    }
  }
}

// Create and export singleton instance
const apiService = new ApiService();
export default apiService;

