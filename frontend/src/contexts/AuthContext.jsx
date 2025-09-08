import { createContext, useContext, useEffect, useState } from 'react';
import { api, handleSupabaseError } from '../lib/supabase';

const AuthContext = createContext({});

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // For testing purposes, set a mock user immediately
    const testMode = window.location.hostname === 'localhost';
    
    if (testMode) {
      // Set mock user for testing
      const mockUser = {
        id: 'test-admin-123',
        email: 'admin@scamshield.ai',
        full_name: 'Admin User',
        role: 'admin', // Change to 'admin' to test admin dashboard
        created_at: new Date().toISOString(),
        subscription_tier: 'enterprise',
        user_metadata: {
          role: 'admin'
        }
      };
      
      setUser(mockUser);
      setLoading(false);
      return;
    }

    // Get initial session for production
    const getInitialSession = async () => {
      try {
        const { data, error } = await api.auth.getSession();
        if (error) throw error;
        
        if (data.session) {
          setUser(data.session.user);
        }
      } catch (err) {
        console.error('Error getting initial session:', err);
        setError(handleSupabaseError(err).message);
      } finally {
        setLoading(false);
      }
    };

    getInitialSession();

    // Listen for auth changes
    const { data: { subscription } } = api.auth.onAuthStateChange(
      async (event, session) => {
        if (session) {
          setUser(session.user);
        } else {
          setUser(null);
        }
        setLoading(false);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const login = async (email, password) => {
    try {
      setLoading(true);
      setError(null);
      
      const { data, error } = await api.auth.signIn(email, password);
      if (error) throw error;
      
      setUser(data.user);
      return { success: true };
    } catch (err) {
      const errorMessage = handleSupabaseError(err).message;
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const register = async (email, password, fullName) => {
    try {
      setLoading(true);
      setError(null);
      
      const { data, error } = await api.auth.signUp(email, password, fullName);
      if (error) throw error;
      
      // Note: User will be set via onAuthStateChange when confirmation is complete
      return { success: true, needsConfirmation: !data.session };
    } catch (err) {
      const errorMessage = handleSupabaseError(err).message;
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      setLoading(true);
      const { error } = await api.auth.signOut();
      if (error) throw error;
      
      setUser(null);
      return { success: true };
    } catch (err) {
      const errorMessage = handleSupabaseError(err).message;
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const clearError = () => setError(null);

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    clearError,
    setUser, // Add setUser for demo purposes
    isAuthenticated: !!user,
    isAdmin: user?.user_metadata?.role === 'admin' || user?.role === 'admin'
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

