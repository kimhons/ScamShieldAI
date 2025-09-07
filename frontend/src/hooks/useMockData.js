import { useState, useEffect } from 'react';

// Mock data for testing dashboards
export function useMockData() {
  const [mockInvestigations, setMockInvestigations] = useState([]);
  const [mockReports, setMockReports] = useState([]);
  const [mockUsers, setMockUsers] = useState([]);
  const [mockAnalytics, setMockAnalytics] = useState({});

  useEffect(() => {
    // Mock investigations data
    setMockInvestigations([
      {
        id: 'inv-001',
        investigation_number: 'SS-2025-001',
        type: 'email',
        subject: 'suspicious.email@scammer.com',
        status: 'in_progress',
        priority: 'high',
        created_at: '2025-01-15T10:30:00Z',
        updated_at: '2025-01-15T14:20:00Z',
        estimated_completion: '2025-01-16T10:30:00Z',
        risk_score: 85,
        description: 'Suspicious email claiming to be from bank requesting account verification'
      },
      {
        id: 'inv-002',
        investigation_number: 'SS-2025-002',
        type: 'phone',
        subject: '+1-555-123-4567',
        status: 'completed',
        priority: 'medium',
        created_at: '2025-01-14T09:15:00Z',
        updated_at: '2025-01-15T11:45:00Z',
        estimated_completion: '2025-01-15T09:15:00Z',
        risk_score: 92,
        description: 'Phone number used in tech support scam targeting elderly users'
      },
      {
        id: 'inv-003',
        investigation_number: 'SS-2025-003',
        type: 'domain',
        subject: 'fake-amazon-security.com',
        status: 'pending',
        priority: 'high',
        created_at: '2025-01-15T16:20:00Z',
        updated_at: '2025-01-15T16:20:00Z',
        estimated_completion: '2025-01-17T16:20:00Z',
        risk_score: 78,
        description: 'Domain impersonating Amazon for phishing attacks'
      },
      {
        id: 'inv-004',
        investigation_number: 'SS-2025-004',
        type: 'ip',
        subject: '192.168.1.100',
        status: 'in_progress',
        priority: 'low',
        created_at: '2025-01-13T14:30:00Z',
        updated_at: '2025-01-15T09:10:00Z',
        estimated_completion: '2025-01-18T14:30:00Z',
        risk_score: 45,
        description: 'IP address associated with suspicious network activity'
      },
      {
        id: 'inv-005',
        investigation_number: 'SS-2025-005',
        type: 'social_media',
        subject: '@fake_support_account',
        status: 'completed',
        priority: 'medium',
        created_at: '2025-01-12T11:00:00Z',
        updated_at: '2025-01-14T15:30:00Z',
        estimated_completion: '2025-01-14T11:00:00Z',
        risk_score: 88,
        description: 'Fake customer support account on social media platform'
      }
    ]);

    // Mock reports data
    setMockReports([
      {
        id: 'rep-001',
        investigation_id: 'inv-002',
        title: 'Phone Scam Investigation Report',
        status: 'completed',
        risk_assessment: 'high',
        findings: 'Confirmed tech support scam operation',
        recommendations: 'Block number, report to authorities',
        created_at: '2025-01-15T11:45:00Z'
      },
      {
        id: 'rep-002',
        investigation_id: 'inv-005',
        title: 'Social Media Impersonation Report',
        status: 'completed',
        risk_assessment: 'high',
        findings: 'Fake account impersonating legitimate business',
        recommendations: 'Report to platform, warn customers',
        created_at: '2025-01-14T15:30:00Z'
      }
    ]);

    // Mock users data (for admin dashboard)
    setMockUsers([
      {
        id: 'user-001',
        full_name: 'John Smith',
        email: 'john.smith@email.com',
        subscription_tier: 'premium',
        status: 'active',
        investigations_count: 12,
        created_at: '2024-12-01T10:00:00Z',
        last_login: '2025-01-15T08:30:00Z'
      },
      {
        id: 'user-002',
        full_name: 'Sarah Johnson',
        email: 'sarah.j@company.com',
        subscription_tier: 'enterprise',
        status: 'active',
        investigations_count: 28,
        created_at: '2024-11-15T14:20:00Z',
        last_login: '2025-01-15T12:15:00Z'
      },
      {
        id: 'user-003',
        full_name: 'Mike Chen',
        email: 'mike.chen@startup.io',
        subscription_tier: 'basic',
        status: 'inactive',
        investigations_count: 3,
        created_at: '2025-01-10T09:45:00Z',
        last_login: '2025-01-12T16:20:00Z'
      }
    ]);

    // Mock analytics data
    setMockAnalytics({
      totalInvestigations: 1247,
      activeInvestigations: 89,
      completedInvestigations: 1158,
      highRiskDetected: 234,
      totalUsers: 156,
      activeUsers: 142,
      premiumUsers: 89,
      enterpriseUsers: 23,
      monthlyRevenue: 45600,
      investigationTypes: {
        email: 456,
        phone: 312,
        domain: 289,
        ip: 134,
        social_media: 56
      },
      riskDistribution: {
        high: 234,
        medium: 567,
        low: 446
      },
      monthlyGrowth: {
        investigations: 12.5,
        users: 8.3,
        revenue: 15.7
      }
    });
  }, []);

  return {
    investigations: mockInvestigations,
    reports: mockReports,
    users: mockUsers,
    analytics: mockAnalytics,
    // Helper functions
    getInvestigationById: (id) => mockInvestigations.find(inv => inv.id === id),
    getReportById: (id) => mockReports.find(rep => rep.id === id),
    getUserById: (id) => mockUsers.find(user => user.id === id)
  };
}

// Mock API responses for testing
export const mockApiResponses = {
  investigations: {
    getAll: () => Promise.resolve({ data: mockInvestigations, error: null }),
    getById: (id) => Promise.resolve({ 
      data: mockInvestigations.find(inv => inv.id === id), 
      error: null 
    }),
    create: (data) => Promise.resolve({ 
      data: { ...data, id: `inv-${Date.now()}`, created_at: new Date().toISOString() }, 
      error: null 
    })
  },
  reports: {
    getAll: () => Promise.resolve({ data: mockReports, error: null }),
    getById: (id) => Promise.resolve({ 
      data: mockReports.find(rep => rep.id === id), 
      error: null 
    })
  },
  users: {
    getAll: () => Promise.resolve({ data: mockUsers, error: null }),
    getById: (id) => Promise.resolve({ 
      data: mockUsers.find(user => user.id === id), 
      error: null 
    })
  }
};

const mockInvestigations = [
  {
    id: 'inv-001',
    investigation_number: 'SS-2025-001',
    type: 'email',
    subject: 'suspicious.email@scammer.com',
    status: 'in_progress',
    priority: 'high',
    created_at: '2025-01-15T10:30:00Z',
    updated_at: '2025-01-15T14:20:00Z',
    estimated_completion: '2025-01-16T10:30:00Z',
    risk_score: 85,
    description: 'Suspicious email claiming to be from bank requesting account verification'
  },
  {
    id: 'inv-002',
    investigation_number: 'SS-2025-002',
    type: 'phone',
    subject: '+1-555-123-4567',
    status: 'completed',
    priority: 'medium',
    created_at: '2025-01-14T09:15:00Z',
    updated_at: '2025-01-15T11:45:00Z',
    estimated_completion: '2025-01-15T09:15:00Z',
    risk_score: 92,
    description: 'Phone number used in tech support scam targeting elderly users'
  },
  {
    id: 'inv-003',
    investigation_number: 'SS-2025-003',
    type: 'domain',
    subject: 'fake-amazon-security.com',
    status: 'pending',
    priority: 'high',
    created_at: '2025-01-15T16:20:00Z',
    updated_at: '2025-01-15T16:20:00Z',
    estimated_completion: '2025-01-17T16:20:00Z',
    risk_score: 78,
    description: 'Domain impersonating Amazon for phishing attacks'
  }
];

const mockReports = [
  {
    id: 'rep-001',
    investigation_id: 'inv-002',
    title: 'Phone Scam Investigation Report',
    status: 'completed',
    risk_assessment: 'high',
    findings: 'Confirmed tech support scam operation',
    recommendations: 'Block number, report to authorities',
    created_at: '2025-01-15T11:45:00Z'
  }
];

const mockUsers = [
  {
    id: 'user-001',
    full_name: 'John Smith',
    email: 'john.smith@email.com',
    subscription_tier: 'premium',
    status: 'active',
    investigations_count: 12,
    created_at: '2024-12-01T10:00:00Z',
    last_login: '2025-01-15T08:30:00Z'
  }
];

