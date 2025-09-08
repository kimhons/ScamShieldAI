import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ClientDashboard } from '../ClientDashboard';
import { renderWithProviders, mockInvestigations } from '../../../test/test-utils';

// Mock the hooks
vi.mock('../../../hooks/useDashboard', () => ({
  useDashboard: () => ({
    dashboardData: {
      stats: {
        totalInvestigations: 5,
        completedInvestigations: 2,
        pendingInvestigations: 1,
        credits: 150
      },
      recentInvestigations: mockInvestigations.slice(0, 3),
      activities: [
        {
          id: 'act-001',
          type: 'investigation_created',
          description: 'New email investigation created',
          timestamp: '2025-01-15T14:30:00Z'
        }
      ]
    },
    loading: false,
    error: null,
    refresh: vi.fn()
  })
}));

vi.mock('../../../hooks/useInvestigations', () => ({
  useInvestigations: () => ({
    investigations: mockInvestigations,
    loading: false,
    error: null,
    createInvestigation: vi.fn(),
    updateInvestigation: vi.fn(),
    deleteInvestigation: vi.fn()
  })
}));

describe('ClientDashboard', () => {
  let user;

  beforeEach(() => {
    user = userEvent.setup();
  });

  it('renders dashboard with welcome message', () => {
    renderWithProviders(<ClientDashboard />);
    
    expect(screen.getByText(/welcome back/i)).toBeInTheDocument();
    expect(screen.getByText(/protected/i)).toBeInTheDocument();
  });

  it('displays statistics cards', () => {
    renderWithProviders(<ClientDashboard />);
    
    expect(screen.getByText(/total scans/i)).toBeInTheDocument();
    expect(screen.getByText(/completed/i)).toBeInTheDocument();
    expect(screen.getByText(/in progress/i)).toBeInTheDocument();
    expect(screen.getByText(/credits/i)).toBeInTheDocument();
  });

  it('displays action cards', () => {
    renderWithProviders(<ClientDashboard />);
    
    expect(screen.getByText(/new investigation/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /start scan/i })).toBeInTheDocument();
    
    expect(screen.getByText(/view reports/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /view all reports/i })).toBeInTheDocument();
  });

  it('has functional logout button', () => {
    renderWithProviders(<ClientDashboard />);
    
    const logoutButton = screen.getByRole('button', { name: /logout/i });
    expect(logoutButton).toBeInTheDocument();
    expect(logoutButton).toBeEnabled();
  });
});

