import React from 'react';
import { render } from '@testing-library/react';
import { AuthProvider } from '../contexts/AuthContext';
import { BrowserRouter } from 'react-router-dom';

// Mock user data for testing
export const mockUser = {
  id: 'test-user-123',
  email: 'test@scamshield.ai',
  full_name: 'Test User',
  role: 'client',
  created_at: new Date().toISOString(),
  subscription_tier: 'premium',
  user_metadata: {
    role: 'client'
  }
};

export const mockAdminUser = {
  id: 'admin-user-123',
  email: 'admin@scamshield.ai',
  full_name: 'Admin User',
  role: 'admin',
  created_at: new Date().toISOString(),
  subscription_tier: 'enterprise',
  user_metadata: {
    role: 'admin'
  }
};

// Custom render function that includes providers
export function renderWithProviders(ui, options = {}) {
  const {
    user = mockUser,
    initialEntries = ['/'],
    ...renderOptions
  } = options;

  function Wrapper({ children }) {
    return (
      <BrowserRouter>
        <AuthProvider initialUser={user}>
          {children}
        </AuthProvider>
      </BrowserRouter>
    );
  }

  return render(ui, { wrapper: Wrapper, ...renderOptions });
}

// Custom render for admin components
export function renderWithAdminUser(ui, options = {}) {
  return renderWithProviders(ui, {
    ...options,
    user: mockAdminUser
  });
}

// Custom render without authentication
export function renderWithoutAuth(ui, options = {}) {
  function Wrapper({ children }) {
    return (
      <BrowserRouter>
        {children}
      </BrowserRouter>
    );
  }

  return render(ui, { wrapper: Wrapper, ...options });
}

// Mock data generators
export const generateMockInvestigation = (overrides = {}) => ({
  id: `inv-${Math.random().toString(36).substr(2, 9)}`,
  target: 'test@example.com',
  type: 'email',
  status: 'pending',
  priority: 'medium',
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  user_id: mockUser.id,
  ...overrides
});

export const generateMockReport = (overrides = {}) => ({
  id: `rep-${Math.random().toString(36).substr(2, 9)}`,
  investigation_id: 'inv-001',
  title: 'Test Investigation Report',
  status: 'completed',
  risk_assessment: 'medium',
  findings: 'Test findings',
  recommendations: 'Test recommendations',
  created_at: new Date().toISOString(),
  ...overrides
});

export const generateMockUser = (overrides = {}) => ({
  id: `user-${Math.random().toString(36).substr(2, 9)}`,
  full_name: 'Test User',
  email: 'test@example.com',
  subscription_tier: 'premium',
  status: 'active',
  investigations_count: 5,
  created_at: new Date().toISOString(),
  last_login: new Date().toISOString(),
  ...overrides
});

// Test data sets
export const mockInvestigations = [
  generateMockInvestigation({ id: 'inv-001', status: 'completed', priority: 'high' }),
  generateMockInvestigation({ id: 'inv-002', status: 'in_progress', priority: 'medium' }),
  generateMockInvestigation({ id: 'inv-003', status: 'pending', priority: 'low' })
];

export const mockReports = [
  generateMockReport({ id: 'rep-001', investigation_id: 'inv-001' }),
  generateMockReport({ id: 'rep-002', investigation_id: 'inv-002' })
];

export const mockUsers = [
  generateMockUser({ id: 'user-001', role: 'client' }),
  generateMockUser({ id: 'user-002', role: 'admin' }),
  generateMockUser({ id: 'user-003', role: 'client' })
];

// Re-export everything from testing-library
export * from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';

