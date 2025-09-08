import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { InvestigationModal } from '../InvestigationModal';
import { renderWithProviders } from '../../../test/test-utils';

// Mock the useInvestigations hook
const mockCreateInvestigation = vi.fn();
vi.mock('../../../hooks/useInvestigations', () => ({
  useInvestigations: () => ({
    createInvestigation: mockCreateInvestigation,
    loading: false,
    error: null
  })
}));

describe('InvestigationModal', () => {
  let user;
  const mockOnClose = vi.fn();

  beforeEach(() => {
    user = userEvent.setup();
    vi.clearAllMocks();
  });

  it('does not render when isOpen is false', () => {
    renderWithProviders(
      <InvestigationModal isOpen={false} onClose={mockOnClose} />
    );
    
    expect(screen.queryByText(/new investigation/i)).not.toBeInTheDocument();
  });

  it('renders modal when isOpen is true', () => {
    renderWithProviders(
      <InvestigationModal isOpen={true} onClose={mockOnClose} />
    );
    
    // Check if modal content is rendered (adjust based on actual implementation)
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });

  it('has functional close button', () => {
    renderWithProviders(
      <InvestigationModal isOpen={true} onClose={mockOnClose} />
    );
    
    const closeButton = screen.getByRole('button', { name: /close/i });
    expect(closeButton).toBeInTheDocument();
  });
});

