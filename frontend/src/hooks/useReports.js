import useSWR from 'swr';
import { api } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';

export function useReports(investigationId = null) {
  const { user } = useAuth();
  
  const { data, error, mutate, isLoading } = useSWR(
    user ? `reports|${investigationId || user.id}` : null,
    async () => {
      if (investigationId) {
        const { data, error } = await api.reports.getByInvestigationId(investigationId);
        if (error) throw error;
        return data;
      } else {
        const { data, error } = await api.reports.getByUserId(user.id);
        if (error) throw error;
        return data;
      }
    },
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
      refreshInterval: 30000, // 30 seconds
      dedupingInterval: 5000,
      errorRetryCount: 3,
      errorRetryInterval: 1000
    }
  );

  return {
    reports: data || [],
    loading: isLoading,
    error,
    refresh: mutate
  };
}

export function useReport(reportId) {
  const { data, error, mutate, isLoading } = useSWR(
    reportId ? `report|${reportId}` : null,
    async () => {
      const { data, error } = await api.reports.getById(reportId);
      if (error) throw error;
      return data;
    },
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
      refreshInterval: 10000, // 10 seconds for individual report
    }
  );

  return {
    report: data,
    loading: isLoading,
    error,
    refresh: mutate
  };
}

