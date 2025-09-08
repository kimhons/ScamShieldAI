import useSWR from 'swr';
import { api } from '../lib/supabase';
import { useAuth } from '../contexts/AuthContext';

export function useApiKeys() {
  const { user } = useAuth();
  
  const { data, error, mutate, isLoading } = useSWR(
    user ? `api-keys|${user.id}` : null,
    async () => {
      const { data, error } = await api.apiKeys.getByUserId(user.id);
      if (error) throw error;
      return data;
    },
    {
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
      refreshInterval: 60000, // 1 minute
      dedupingInterval: 10000,
      errorRetryCount: 3,
      errorRetryInterval: 2000
    }
  );

  const generateApiKey = async (keyName, permissions = [], rateLimit = 1000) => {
    try {
      const { data: newApiKey, error } = await api.apiKeys.generate(
        user.id,
        keyName,
        permissions,
        rateLimit
      );
      
      if (error) throw error;
      
      // Optimistically update the cache
      mutate([...(data || []), newApiKey], false);
      
      return { success: true, data: newApiKey };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  const revokeApiKey = async (keyId) => {
    try {
      const { error } = await api.apiKeys.revoke(keyId);
      
      if (error) throw error;
      
      // Remove from cache
      mutate(data?.filter(key => key.id !== keyId), false);
      
      return { success: true };
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  return {
    apiKeys: data || [],
    loading: isLoading,
    error,
    refresh: mutate,
    generateApiKey,
    revokeApiKey
  };
}

