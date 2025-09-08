import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display login form on homepage', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /sign in to scamshield ai/i })).toBeVisible();
    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel(/password/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /sign in/i })).toBeVisible();
  });

  test('should navigate to registration page', async ({ page }) => {
    await page.getByRole('link', { name: /sign up/i }).click();
    await expect(page).toHaveURL('/auth/register');
    await expect(page.getByRole('heading', { name: /create your scamshield ai account/i })).toBeVisible();
  });

  test('should show validation errors for empty login form', async ({ page }) => {
    await page.getByRole('button', { name: /sign in/i }).click();
    
    await expect(page.getByText(/email is required/i)).toBeVisible();
    await expect(page.getByText(/password is required/i)).toBeVisible();
  });

  test('should show validation error for invalid email', async ({ page }) => {
    await page.getByLabel(/email/i).fill('invalid-email');
    await page.getByRole('button', { name: /sign in/i }).click();
    
    await expect(page.getByText(/please enter a valid email address/i)).toBeVisible();
  });

  test('should toggle password visibility', async ({ page }) => {
    const passwordInput = page.getByLabel(/password/i);
    const toggleButton = page.getByRole('button', { name: /toggle password visibility/i });
    
    await expect(passwordInput).toHaveAttribute('type', 'password');
    
    await toggleButton.click();
    await expect(passwordInput).toHaveAttribute('type', 'text');
    
    await toggleButton.click();
    await expect(passwordInput).toHaveAttribute('type', 'password');
  });

  test('should navigate to client dashboard in test mode', async ({ page }) => {
    // In test mode, we should be automatically logged in
    await page.goto('/dashboard');
    
    await expect(page.getByText(/welcome back/i)).toBeVisible();
    await expect(page.getByText(/total scans/i)).toBeVisible();
    await expect(page.getByText(/completed/i)).toBeVisible();
    await expect(page.getByText(/in progress/i)).toBeVisible();
    await expect(page.getByText(/credits/i)).toBeVisible();
  });

  test('should navigate to admin dashboard in test mode', async ({ page }) => {
    await page.goto('/admin');
    
    await expect(page.getByText(/admin dashboard/i)).toBeVisible();
    await expect(page.getByText(/total revenue/i)).toBeVisible();
    await expect(page.getByText(/total users/i)).toBeVisible();
    await expect(page.getByText(/accuracy rate/i)).toBeVisible();
  });

  test('should display logout button in dashboard', async ({ page }) => {
    await page.goto('/dashboard');
    
    const logoutButton = page.getByRole('button', { name: /logout/i });
    await expect(logoutButton).toBeVisible();
    await expect(logoutButton).toBeEnabled();
  });
});

test.describe('Registration Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/auth/register');
  });

  test('should display registration form', async ({ page }) => {
    await expect(page.getByRole('heading', { name: /create your scamshield ai account/i })).toBeVisible();
    await expect(page.getByLabel(/full name/i)).toBeVisible();
    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel('Password', { exact: true })).toBeVisible();
    await expect(page.getByLabel(/confirm password/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /create account/i })).toBeVisible();
  });

  test('should show validation errors for empty registration form', async ({ page }) => {
    await page.getByRole('button', { name: /create account/i }).click();
    
    await expect(page.getByText(/full name is required/i)).toBeVisible();
    await expect(page.getByText(/email is required/i)).toBeVisible();
    await expect(page.getByText(/password is required/i)).toBeVisible();
  });

  test('should validate password confirmation', async ({ page }) => {
    await page.getByLabel(/full name/i).fill('Test User');
    await page.getByLabel(/email/i).fill('test@example.com');
    await page.getByLabel('Password', { exact: true }).fill('password123');
    await page.getByLabel(/confirm password/i).fill('different-password');
    
    await page.getByRole('button', { name: /create account/i }).click();
    
    await expect(page.getByText(/passwords do not match/i)).toBeVisible();
  });

  test('should validate password strength', async ({ page }) => {
    await page.getByLabel(/full name/i).fill('Test User');
    await page.getByLabel(/email/i).fill('test@example.com');
    await page.getByLabel('Password', { exact: true }).fill('123');
    
    await page.getByRole('button', { name: /create account/i }).click();
    
    await expect(page.getByText(/password must be at least 8 characters/i)).toBeVisible();
  });

  test('should have link back to login page', async ({ page }) => {
    const loginLink = page.getByRole('link', { name: /sign in/i });
    await expect(loginLink).toBeVisible();
    await expect(loginLink).toHaveAttribute('href', '/auth/login');
  });

  test('should accept valid registration data', async ({ page }) => {
    await page.getByLabel(/full name/i).fill('Test User');
    await page.getByLabel(/email/i).fill('test@scamshield.ai');
    await page.getByLabel('Password', { exact: true }).fill('password123');
    await page.getByLabel(/confirm password/i).fill('password123');
    
    // Form should be valid (no validation errors)
    await page.getByRole('button', { name: /create account/i }).click();
    
    // Should not show validation errors
    await expect(page.getByText(/full name is required/i)).not.toBeVisible();
    await expect(page.getByText(/email is required/i)).not.toBeVisible();
    await expect(page.getByText(/password is required/i)).not.toBeVisible();
  });
});

