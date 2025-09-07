import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '../AuthContext';
import React from 'react';

// Mock Supabase
const mockSupabase = {
  auth: {
    signInWithPassword: vi.fn(),
    signUp: vi.fn(),
    signOut: vi.fn(),
    getSession: vi.fn(),
    onAuthStateChange: vi.fn(() => ({
      data: { subscription: { unsubscribe: vi.fn() } }
    }))
  }
};

vi.mock('../../lib/supabase', () => ({
  supabase: mockSupabase
}));

describe('AuthContext', () => {
  const wrapper = ({ children }) => (
    <AuthProvider>{children}</AuthProvider>
  );

  beforeEach(() => {
    vi.clearAllMocks();
    
    // Mock window.location for test mode
    Object.defineProperty(window, 'location', {
      value: { hostname: 'localhost' },
      writable: true
    });
  });

  it('provides initial auth state', () => {
    const { result } = renderHook(() => useAuth(), { wrapper });

    expect(result.current.user).toBeDefined();
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe(null);
    expect(typeof result.current.login).toBe('function');
    expect(typeof result.current.register).toBe('function');
    expect(typeof result.current.logout).toBe('function');
  });

  it('sets mock user in test mode', () => {
    const { result } = renderHook(() => useAuth(), { wrapper });

    expect(result.current.user).toMatchObject({
      id: 'test-user-123',
      email: 'admin@scamshield.ai',
      full_name: 'Admin User',
      role: 'admin'
    });
  });

  it('determines admin status correctly', () => {
    const { result } = renderHook(() => useAuth(), { wrapper });

    expect(result.current.isAdmin).toBe(true);
  });

  it('handles login function call', async () => {
    mockSupabase.auth.signInWithPassword.mockResolvedValueOnce({
      data: {
        user: {
          id: 'user-123',
          email: 'test@example.com'
        },
        session: { access_token: 'token' }
      },
      error: null
    });

    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      await result.current.login({
        email: 'test@example.com',
        password: 'password123'
      });
    });

    expect(mockSupabase.auth.signInWithPassword).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });

  it('handles login error', async () => {
    mockSupabase.auth.signInWithPassword.mockResolvedValueOnce({
      data: { user: null, session: null },
      error: { message: 'Invalid credentials' }
    });

    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      await result.current.login({
        email: 'wrong@example.com',
        password: 'wrongpassword'
      });
    });

    expect(result.current.error).toEqual({ message: 'Invalid credentials' });
  });

  it('handles register function call', async () => {
    mockSupabase.auth.signUp.mockResolvedValueOnce({
      data: {
        user: {
          id: 'new-user-123',
          email: 'newuser@example.com'
        },
        session: null
      },
      error: null
    });

    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      await result.current.register({
        email: 'newuser@example.com',
        password: 'password123',
        fullName: 'New User'
      });
    });

    expect(mockSupabase.auth.signUp).toHaveBeenCalledWith({
      email: 'newuser@example.com',
      password: 'password123',
      options: {
        data: {
          full_name: 'New User'
        }
      }
    });
  });

  it('handles register error', async () => {
    mockSupabase.auth.signUp.mockResolvedValueOnce({
      data: { user: null, session: null },
      error: { message: 'Email already registered' }
    });

    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      await result.current.register({
        email: 'existing@example.com',
        password: 'password123',
        fullName: 'Existing User'
      });
    });

    expect(result.current.error).toEqual({ message: 'Email already registered' });
  });

  it('handles logout function call', async () => {
    mockSupabase.auth.signOut.mockResolvedValueOnce({
      error: null
    });

    const { result } = renderHook(() => useAuth(), { wrapper });

    await act(async () => {
      await result.current.logout();
    });

    expect(mockSupabase.auth.signOut).toHaveBeenCalled();
  });

  it('sets loading state during authentication operations', async () => {
    let resolveLogin;
    const loginPromise = new Promise(resolve => {
      resolveLogin = resolve;
    });

    mockSupabase.auth.signInWithPassword.mockReturnValueOnce(loginPromise);

    const { result } = renderHook(() => useAuth(), { wrapper });

    act(() => {
      result.current.login({
        email: 'test@example.com',
        password: 'password123'
      });
    });

    expect(result.current.loading).toBe(true);

    await act(async () => {
      resolveLogin({
        data: { user: { id: 'user-123' }, session: {} },
        error: null
      });
      await loginPromise;
    });

    expect(result.current.loading).toBe(false);
  });

  it('clears error when starting new authentication operation', async () => {
    const { result } = renderHook(() => useAuth(), { wrapper });

    // Set an error first
    act(() => {
      result.current.setError({ message: 'Previous error' });
    });

    expect(result.current.error).toEqual({ message: 'Previous error' });

    // Start login - should clear error
    mockSupabase.auth.signInWithPassword.mockResolvedValueOnce({
      data: { user: { id: 'user-123' }, session: {} },
      error: null
    });

    await act(async () => {
      await result.current.login({
        email: 'test@example.com',
        password: 'password123'
      });
    });

    expect(result.current.error).toBe(null);
  });

  it('provides setUser function for testing', () => {
    const { result } = renderHook(() => useAuth(), { wrapper });

    expect(typeof result.current.setUser).toBe('function');

    const newUser = {
      id: 'new-user-456',
      email: 'newuser@example.com',
      role: 'client'
    };

    act(() => {
      result.current.setUser(newUser);
    });

    expect(result.current.user).toEqual(newUser);
  });

  it('determines client role correctly', () => {
    const { result } = renderHook(() => useAuth(), { wrapper });

    const clientUser = {
      id: 'client-user-123',
      email: 'client@example.com',
      role: 'client'
    };

    act(() => {
      result.current.setUser(clientUser);
    });

    expect(result.current.isAdmin).toBe(false);
  });

  it('handles auth state changes', () => {
    const mockCallback = vi.fn();
    mockSupabase.auth.onAuthStateChange.mockReturnValueOnce({
      data: { subscription: { unsubscribe: vi.fn() } }
    });

    renderHook(() => useAuth(), { wrapper });

    expect(mockSupabase.auth.onAuthStateChange).toHaveBeenCalled();
  });

  it('throws error when used outside provider', () => {
    expect(() => {
      renderHook(() => useAuth());
    }).toThrow('useAuth must be used within an AuthProvider');
  });
});

