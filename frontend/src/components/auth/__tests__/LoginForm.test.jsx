import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from '../LoginForm';
import { renderWithoutAuth } from '../../../test/test-utils';

// Mock the useAuth hook
const mockLogin = vi.fn();
const mockClearError = vi.fn();

vi.mock('../../../contexts/AuthContext', () => ({
  useAuth: () => ({
    login: mockLogin,
    loading: false,
    error: null,
    clearError: mockClearError
  })
}));

describe('LoginForm', () => {
  let user;

  beforeEach(() => {
    user = userEvent.setup();
    vi.clearAllMocks();
  });

  it('renders login form with all required fields', () => {
    renderWithoutAuth(<LoginForm />);
    
    expect(screen.getByRole('heading', { name: /sign in to scamshield ai/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
    expect(screen.getByText(/don't have an account/i)).toBeInTheDocument();
  });

  it('accepts valid email and password input', async () => {
    renderWithoutAuth(<LoginForm />);
    
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);

    await user.type(emailInput, 'test@scamshield.ai');
    await user.type(passwordInput, 'password123');

    expect(emailInput).toHaveValue('test@scamshield.ai');
    expect(passwordInput).toHaveValue('password123');
  });

  it('has link to registration page', () => {
    renderWithoutAuth(<LoginForm />);
    
    const signUpLink = screen.getByRole('link', { name: /sign up/i });
    expect(signUpLink).toBeInTheDocument();
    expect(signUpLink).toHaveAttribute('href', '/auth/register');
  });

  it('calls clearError when form is submitted', async () => {
    renderWithoutAuth(<LoginForm />);
    
    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    await user.type(emailInput, 'test@scamshield.ai');
    await user.type(passwordInput, 'password123');
    await user.click(submitButton);

    expect(mockClearError).toHaveBeenCalled();
  });
});

