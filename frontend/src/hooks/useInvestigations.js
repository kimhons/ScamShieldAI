import useSWR from 'swr';
import { api } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';
import { useMockData } from './useMockData';

// Fetcher function for SWR
const fetcher = async (key) => {
  const [endpoint, userId] = key.split('|');
  
  switch (endpoint) {
    case 'investigations':
      const { data, error } = await api.investigations.getByUserId(userId);
      if (error) throw error;
      return data;
    default:
      throw new Error(`Unknown endpoint: ${endpoint}`);
  }
};

export function useInvestigations() {
  const { user } = useAuth();
  const { investigations: mockInvestigations } = useMockData();
  
  // Use mock data for testing on localhost
  const isTestMode = window.location.hostname === 'localhost';
  
  const { data, error, mutate, isLoading } = useSWR(
    user && !isTestMode ? `investigations|${user.id}` : null,
    fetcher,
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
      refreshInterval: 30000, // 30 seconds
      dedupingInterval: 5000,
      errorRetryCount: 3,
      errorRetryInterval: 1000
    }
  );

  // Return mock data for testing or real data for production
  const investigations = isTestMode ? mockInvestigations : (data || []);

  const createInvestigation = async (investigationData) => {
    if (isTestMode) {
      // Mock creation for testing
      const newInvestigation = {
        id: `inv-${Date.now()}`,
        investigation_number: `SS-2025-${String(investigations.length + 1).padStart(3, '0')}`,
        ...investigationData,
        status: 'pending',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        risk_score: Math.floor(Math.random() * 100)
      };
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      return { success: true, data: newInvestigation };
    }

    try {
      const { data: newInvestigation, error } = await api.investigations.create({
        user_id: user.id,
        ...investigationData
      });
      
      if (error) throw error;
      
      // Optimistically update the cache
      mutate([...investigations, newInvestigation], false);
      
      return { success: true, data: newInvestigation };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  const updateInvestigation = async (investigationId, updates) => {
    if (isTestMode) {
      // Mock update for testing
      await new Promise(resolve => setTimeout(resolve, 500));
      return { success: true };
    }

    try {
      const { error } = await api.investigations.update(investigationId, updates);
      
      if (error) throw error;
      
      // Update the cache
      const updatedInvestigations = investigations.map(inv => 
        inv.id === investigationId ? { ...inv, ...updates } : inv
      );
      mutate(updatedInvestigations, false);
      
      return { success: true };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  return {
    investigations,
    loading: isTestMode ? false : isLoading,
    error: isTestMode ? null : error,
    refresh: isTestMode ? () => {} : mutate,
    createInvestigation,
    updateInvestigation,
    // Helper functions
    getInvestigationsByStatus: (status) => investigations.filter(inv => inv.status === status),
    getInvestigationsByPriority: (priority) => investigations.filter(inv => inv.priority === priority),
    getInvestigationsByType: (type) => investigations.filter(inv => inv.type === type)
  };
}

export function useInvestigation(id) {
  const { getInvestigationById } = useMockData();
  const isTestMode = window.location.hostname === 'localhost';
  
  const { data, error, mutate, isLoading } = useSWR(
    id && !isTestMode ? `investigation|${id}` : null,
    async () => {
      const { data, error } = await api.investigations.getById(id);
      if (error) throw error;
      return data;
    },
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
      refreshInterval: 10000, // 10 seconds for individual investigation
    }
  );

  // Return mock data for testing or real data for production
  const investigation = isTestMode ? getInvestigationById(id) : data;

  return {
    investigation,
    loading: isTestMode ? false : isLoading,
    error: isTestMode ? null : error,
    refresh: isTestMode ? () => {} : mutate
  };
}

