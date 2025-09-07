import useSWR from 'swr';
import { api } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';
import { useMockData } from './useMockData';

export function useDashboard() {
  const { user } = useAuth();
  const { analytics: mockAnalytics, investigations: mockInvestigations, reports: mockReports } = useMockData();
  
  // Use mock data for testing on localhost
  const isTestMode = window.location.hostname === 'localhost';
  
  const { data, error, mutate, isLoading } = useSWR(
    user && !isTestMode ? `dashboard|${user.id}` : null,
    async () => {
      const { data, error } = await api.dashboard.getStats(user.id);
      if (error) throw error;
      return data;
    },
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      refreshInterval: 60000, // 1 minute
      dedupingInterval: 10000,
      errorRetryCount: 3,
      errorRetryInterval: 2000
    }
  );

  // Transform the data to match our component expectations
  const transformedData = isTestMode ? {
    stats: {
      totalInvestigations: mockInvestigations.length,
      completedInvestigations: mockInvestigations.filter(inv => inv.status === 'completed').length,
      pendingInvestigations: mockInvestigations.filter(inv => inv.status === 'pending').length,
      totalReports: mockReports.length,
      credits: 150,
      successRate: 94.5
    },
    recentInvestigations: mockInvestigations.slice(0, 5),
    recentReports: mockReports.slice(0, 3),
    activities: [
      {
        id: 'act-001',
        type: 'investigation_created',
        description: 'New email investigation created',
        timestamp: '2025-01-15T14:30:00Z',
        user: 'Test User'
      },
      {
        id: 'act-002',
        type: 'investigation_completed',
        description: 'Phone scam investigation completed',
        timestamp: '2025-01-15T11:45:00Z',
        user: 'Test User'
      },
      {
        id: 'act-003',
        type: 'high_risk_detected',
        description: 'High-risk domain detected',
        timestamp: '2025-01-15T10:20:00Z',
        user: 'System'
      }
    ]
  } : (data ? {
    stats: {
      totalInvestigations: data.total_investigations || 0,
      completedInvestigations: data.completed_investigations || 0,
      pendingInvestigations: data.pending_investigations || 0,
      totalReports: data.total_reports || 0,
      credits: data.credits || 0,
      successRate: data.success_rate || 0
    },
    recentInvestigations: data.recent_investigations || [],
    recentReports: data.recent_reports || [],
    activities: data.recent_activities || []
  } : null);

  return {
    dashboardData: transformedData,
    loading: isTestMode ? false : isLoading,
    error: isTestMode ? null : error,
    refresh: isTestMode ? () => {} : mutate
  };
}

// Hook for admin dashboard with additional metrics
export function useAdminDashboard() {
  const { user, isAdmin } = useAuth();
  const { analytics: mockAnalytics, users: mockUsers, investigations: mockInvestigations, reports: mockReports } = useMockData();
  
  // Use mock data for testing on localhost
  const isTestMode = window.location.hostname === 'localhost';
  
  const { data, error, mutate, isLoading } = useSWR(
    user && isAdmin && !isTestMode ? `admin-dashboard|${user.id}` : null,
    async () => {
      // For admin dashboard, we might need different data
      // This could be a separate function or enhanced version
      const { data, error } = await api.dashboard.getStats(user.id);
      if (error) throw error;
      return data;
    },
    {
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
      refreshInterval: 30000, // 30 seconds for admin
      dedupingInterval: 5000,
      errorRetryCount: 3,
      errorRetryInterval: 2000
    }
  );

  // Transform data for admin dashboard
  const transformedData = isTestMode ? {
    stats: {
      totalRevenue: mockAnalytics?.monthlyRevenue || 0,
      totalUsers: mockAnalytics?.totalUsers || 0,
      totalReports: mockInvestigations?.length || 0,
      accuracyRate: 96.8,
      revenueChange: mockAnalytics?.monthlyGrowth?.revenue || 0,
      usersChange: mockAnalytics?.monthlyGrowth?.users || 0,
      reportsChange: mockAnalytics?.monthlyGrowth?.investigations || 0,
      accuracyChange: 2.1
    },
    chartData: {
      revenue: [
        { month: 'Jan', value: 38400 },
        { month: 'Feb', value: 41200 },
        { month: 'Mar', value: 45600 }
      ],
      users: [
        { month: 'Jan', value: 142 },
        { month: 'Feb', value: 148 },
        { month: 'Mar', value: 156 }
      ],
      reports: [
        { month: 'Jan', value: 1089 },
        { month: 'Feb', value: 1156 },
        { month: 'Mar', value: 1247 }
      ]
    },
    recentUsers: mockUsers?.slice(0, 5) || [],
    recentReports: mockReports?.slice(0, 5) || [],
    activities: [
      {
        id: 'act-001',
        type: 'user_registered',
        description: 'New user registered',
        timestamp: '2025-01-15T14:30:00Z',
        user: 'System'
      },
      {
        id: 'act-002',
        type: 'investigation_completed',
        description: 'High-priority investigation completed',
        timestamp: '2025-01-15T11:45:00Z',
        user: 'Admin'
      },
      {
        id: 'act-003',
        type: 'security_alert',
        description: 'Multiple failed login attempts detected',
        timestamp: '2025-01-15T10:20:00Z',
        user: 'Security System'
      }
    ],
    systemHealth: {
      status: 'healthy',
      uptime: '99.9%',
      responseTime: '120ms',
      errorRate: '0.1%'
    }
  } : (data ? {
    stats: {
      totalRevenue: data.total_revenue || 0,
      totalUsers: data.total_users || 0,
      totalReports: data.total_reports || 0,
      accuracyRate: data.accuracy_rate || 0,
      revenueChange: data.revenue_change || 0,
      usersChange: data.users_change || 0,
      reportsChange: data.reports_change || 0,
      accuracyChange: data.accuracy_change || 0
    },
    chartData: {
      revenue: data.revenue_chart || [],
      users: data.users_chart || [],
      reports: data.reports_chart || []
    },
    recentUsers: data.recent_users || [],
    recentReports: data.recent_reports || [],
    activities: data.recent_activities || []
  } : null);

  return {
    adminData: transformedData,
    loading: isTestMode ? false : isLoading,
    error: isTestMode ? null : error,
    refresh: isTestMode ? () => {} : mutate
  };
}

