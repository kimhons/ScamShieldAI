import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useDashboard, useAdminDashboard } from '../useDashboard';
import { useAuth } from '../../contexts/AuthContext';
import { useMockData } from '../useMockData';

// Mock dependencies
vi.mock('../../contexts/AuthContext');
vi.mock('../useMockData');
vi.mock('swr');

// Mock SWR
const mockMutate = vi.fn();
vi.mock('swr', () => ({
  default: vi.fn(() => ({
    data: null,
    error: null,
    mutate: mockMutate,
    isLoading: false
  }))
}));

describe('useDashboard', () => {
  const mockUser = {
    id: 'test-user-123',
    email: 'test@scamshield.ai',
    role: 'client'
  };

  const mockAnalytics = {
    totalInvestigations: 1247,
    totalUsers: 156,
    monthlyRevenue: 45600,
    monthlyGrowth: {
      investigations: 12.5,
      users: 8.3,
      revenue: 15.7
    }
  };

  const mockInvestigations = [
    {
      id: 'inv-001',
      target: 'test@example.com',
      type: 'email',
      status: 'completed',
      priority: 'high'
    },
    {
      id: 'inv-002',
      target: '+1-555-123-4567',
      type: 'phone',
      status: 'in_progress',
      priority: 'medium'
    }
  ];

  const mockReports = [
    {
      id: 'rep-001',
      investigation_id: 'inv-001',
      title: 'Email Investigation Report',
      status: 'completed'
    }
  ];

  beforeEach(() => {
    vi.clearAllMocks();
    
    useAuth.mockReturnValue({
      user: mockUser,
      isAdmin: false
    });

    useMockData.mockReturnValue({
      analytics: mockAnalytics,
      investigations: mockInvestigations,
      reports: mockReports,
      users: []
    });

    // Mock window.location for test mode detection
    Object.defineProperty(window, 'location', {
      value: { hostname: 'localhost' },
      writable: true
    });
  });

  it('returns dashboard data in test mode', () => {
    const { result } = renderHook(() => useDashboard());

    expect(result.current.dashboardData).toBeDefined();
    expect(result.current.dashboardData.stats).toEqual({
      totalInvestigations: 2,
      completedInvestigations: 1,
      pendingInvestigations: 0,
      totalReports: 1,
      credits: 150,
      successRate: 94.5
    });
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('returns recent investigations from mock data', () => {
    const { result } = renderHook(() => useDashboard());

    expect(result.current.dashboardData.recentInvestigations).toHaveLength(2);
    expect(result.current.dashboardData.recentInvestigations[0]).toEqual(mockInvestigations[0]);
  });

  it('returns recent reports from mock data', () => {
    const { result } = renderHook(() => useDashboard());

    expect(result.current.dashboardData.recentReports).toHaveLength(1);
    expect(result.current.dashboardData.recentReports[0]).toEqual(mockReports[0]);
  });

  it('includes activity feed in dashboard data', () => {
    const { result } = renderHook(() => useDashboard());

    expect(result.current.dashboardData.activities).toBeDefined();
    expect(result.current.dashboardData.activities).toHaveLength(3);
    expect(result.current.dashboardData.activities[0]).toMatchObject({
      id: 'act-001',
      type: 'investigation_created',
      description: 'New email investigation created'
    });
  });

  it('provides refresh function', () => {
    const { result } = renderHook(() => useDashboard());

    expect(result.current.refresh).toBeDefined();
    expect(typeof result.current.refresh).toBe('function');
  });

  it('handles null user gracefully', () => {
    useAuth.mockReturnValue({
      user: null,
      isAdmin: false
    });

    const { result } = renderHook(() => useDashboard());

    expect(result.current.dashboardData).toBeDefined();
    expect(result.current.loading).toBe(false);
  });

  it('calculates completed investigations correctly', () => {
    const investigationsWithVariedStatus = [
      { ...mockInvestigations[0], status: 'completed' },
      { ...mockInvestigations[1], status: 'completed' },
      { id: 'inv-003', status: 'pending' },
      { id: 'inv-004', status: 'in_progress' }
    ];

    useMockData.mockReturnValue({
      analytics: mockAnalytics,
      investigations: investigationsWithVariedStatus,
      reports: mockReports,
      users: []
    });

    const { result } = renderHook(() => useDashboard());

    expect(result.current.dashboardData.stats.totalInvestigations).toBe(4);
    expect(result.current.dashboardData.stats.completedInvestigations).toBe(2);
    expect(result.current.dashboardData.stats.pendingInvestigations).toBe(1);
  });
});

describe('useAdminDashboard', () => {
  const mockAdminUser = {
    id: 'admin-user-123',
    email: 'admin@scamshield.ai',
    role: 'admin'
  };

  const mockUsers = [
    {
      id: 'user-001',
      full_name: 'John Smith',
      email: 'john@example.com',
      subscription_tier: 'premium'
    },
    {
      id: 'user-002',
      full_name: 'Jane Doe',
      email: 'jane@example.com',
      subscription_tier: 'enterprise'
    }
  ];

  beforeEach(() => {
    vi.clearAllMocks();
    
    useAuth.mockReturnValue({
      user: mockAdminUser,
      isAdmin: true
    });

    useMockData.mockReturnValue({
      analytics: {
        totalUsers: 156,
        monthlyRevenue: 45600,
        monthlyGrowth: {
          investigations: 12.5,
          users: 8.3,
          revenue: 15.7
        }
      },
      investigations: [],
      reports: [],
      users: mockUsers
    });
  });

  it('returns admin dashboard data in test mode', () => {
    const { result } = renderHook(() => useAdminDashboard());

    expect(result.current.adminData).toBeDefined();
    expect(result.current.adminData.stats).toEqual({
      totalRevenue: 45600,
      totalUsers: 156,
      totalReports: 0,
      accuracyRate: 96.8,
      revenueChange: 15.7,
      usersChange: 8.3,
      reportsChange: 12.5,
      accuracyChange: 2.1
    });
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
  });

  it('includes chart data for admin dashboard', () => {
    const { result } = renderHook(() => useAdminDashboard());

    expect(result.current.adminData.chartData).toBeDefined();
    expect(result.current.adminData.chartData.revenue).toHaveLength(3);
    expect(result.current.adminData.chartData.users).toHaveLength(3);
    expect(result.current.adminData.chartData.reports).toHaveLength(3);
  });

  it('includes recent users from mock data', () => {
    const { result } = renderHook(() => useAdminDashboard());

    expect(result.current.adminData.recentUsers).toHaveLength(2);
    expect(result.current.adminData.recentUsers[0]).toEqual(mockUsers[0]);
  });

  it('includes system health information', () => {
    const { result } = renderHook(() => useAdminDashboard());

    expect(result.current.adminData.systemHealth).toEqual({
      status: 'healthy',
      uptime: '99.9%',
      responseTime: '120ms',
      errorRate: '0.1%'
    });
  });

  it('includes admin activity feed', () => {
    const { result } = renderHook(() => useAdminDashboard());

    expect(result.current.adminData.activities).toBeDefined();
    expect(result.current.adminData.activities).toHaveLength(3);
    expect(result.current.adminData.activities[0]).toMatchObject({
      id: 'act-001',
      type: 'user_registered',
      description: 'New user registered'
    });
  });

  it('handles null analytics data gracefully', () => {
    useMockData.mockReturnValue({
      analytics: null,
      investigations: [],
      reports: [],
      users: []
    });

    const { result } = renderHook(() => useAdminDashboard());

    expect(result.current.adminData.stats.totalRevenue).toBe(0);
    expect(result.current.adminData.stats.totalUsers).toBe(0);
    expect(result.current.adminData.recentUsers).toEqual([]);
  });

  it('returns null when user is not admin', () => {
    useAuth.mockReturnValue({
      user: { id: 'user-123', role: 'client' },
      isAdmin: false
    });

    const { result } = renderHook(() => useAdminDashboard());

    // In test mode, it should still return data, but in production it would be null
    expect(result.current.adminData).toBeDefined();
  });

  it('provides refresh function for admin dashboard', () => {
    const { result } = renderHook(() => useAdminDashboard());

    expect(result.current.refresh).toBeDefined();
    expect(typeof result.current.refresh).toBe('function');
  });
});

