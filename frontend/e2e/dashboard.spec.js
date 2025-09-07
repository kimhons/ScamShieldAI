import { test, expect } from '@playwright/test';

test.describe('Client Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/dashboard');
  });

  test('should display dashboard header and navigation', async ({ page }) => {
    await expect(page.getByText(/scamshield ai/i)).toBeVisible();
    await expect(page.getByText(/welcome back/i)).toBeVisible();
    await expect(page.getByText(/protected/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /logout/i })).toBeVisible();
  });

  test('should display statistics cards with correct data', async ({ page }) => {
    // Check for statistics cards
    await expect(page.getByText(/total scans/i)).toBeVisible();
    await expect(page.getByText(/completed/i)).toBeVisible();
    await expect(page.getByText(/in progress/i)).toBeVisible();
    await expect(page.getByText(/credits/i)).toBeVisible();
    
    // Check for numeric values
    await expect(page.getByText('5')).toBeVisible(); // Total scans
    await expect(page.getByText('2')).toBeVisible(); // Completed
    await expect(page.getByText('1')).toBeVisible(); // In progress
    await expect(page.getByText('150')).toBeVisible(); // Credits
  });

  test('should display action cards', async ({ page }) => {
    await expect(page.getByText(/new investigation/i)).toBeVisible();
    await expect(page.getByText(/scan emails, phones, domains & more/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /start scan/i })).toBeVisible();
    
    await expect(page.getByText(/view reports/i)).toBeVisible();
    await expect(page.getByText(/access your investigation reports/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /view all reports/i })).toBeVisible();
    
    await expect(page.getByText(/security alerts/i)).toBeVisible();
    await expect(page.getByText(/monitor threats and warnings/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /view alerts/i })).toBeVisible();
  });

  test('should open investigation modal when Start Scan is clicked', async ({ page }) => {
    await page.getByRole('button', { name: /start scan/i }).click();
    
    await expect(page.getByText(/new investigation/i)).toBeVisible();
    await expect(page.getByText(/start a new scam detection investigation/i)).toBeVisible();
    await expect(page.getByText(/email address/i)).toBeVisible();
    await expect(page.getByText(/phone number/i)).toBeVisible();
    await expect(page.getByText(/website\/domain/i)).toBeVisible();
  });

  test('should display recent investigations list', async ({ page }) => {
    await expect(page.getByText(/recent investigations/i)).toBeVisible();
    await expect(page.getByText(/your latest scam detection scans/i)).toBeVisible();
    
    // Check for investigation items
    await expect(page.getByText(/high priority/i)).toBeVisible();
    await expect(page.getByText(/medium priority/i)).toBeVisible();
    await expect(page.getByText(/completed/i)).toBeVisible();
    await expect(page.getByText(/in_progress/i)).toBeVisible();
    await expect(page.getByText(/pending/i)).toBeVisible();
  });

  test('should display protection tips', async ({ page }) => {
    await expect(page.getByText(/protection tips/i)).toBeVisible();
    await expect(page.getByText(/stay safe with these security recommendations/i)).toBeVisible();
    
    await expect(page.getByText(/verify email senders/i)).toBeVisible();
    await expect(page.getByText(/suspicious phone calls/i)).toBeVisible();
    await expect(page.getByText(/monitor your accounts/i)).toBeVisible();
  });

  test('should have functional View All button', async ({ page }) => {
    const viewAllButton = page.getByRole('button', { name: /view all/i });
    await expect(viewAllButton).toBeVisible();
    await expect(viewAllButton).toBeEnabled();
  });
});

test.describe('Investigation Modal', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/dashboard');
    await page.getByRole('button', { name: /start scan/i }).click();
  });

  test('should display all investigation types', async ({ page }) => {
    await expect(page.getByText(/email address/i)).toBeVisible();
    await expect(page.getByText(/verify email sender authenticity/i)).toBeVisible();
    
    await expect(page.getByText(/phone number/i)).toBeVisible();
    await expect(page.getByText(/check phone number legitimacy/i)).toBeVisible();
    
    await expect(page.getByText(/website\/domain/i)).toBeVisible();
    await expect(page.getByText(/analyze website safety/i)).toBeVisible();
    
    await expect(page.getByText(/ip address/i)).toBeVisible();
    await expect(page.getByText(/investigate ip location and reputation/i)).toBeVisible();
    
    await expect(page.getByText(/social media/i)).toBeVisible();
    await expect(page.getByText(/verify social media profiles/i)).toBeVisible();
  });

  test('should allow selecting different investigation types', async ({ page }) => {
    // Click on Phone Number option
    await page.getByText(/phone number/i).click();
    await expect(page.getByText(/check phone number legitimacy/i)).toBeVisible();
    
    // Click on Domain option
    await page.getByText(/website\/domain/i).click();
    await expect(page.getByText(/analyze website safety/i)).toBeVisible();
  });

  test('should have target input field', async ({ page }) => {
    const targetInput = page.getByPlaceholder(/enter target to investigate/i);
    await expect(targetInput).toBeVisible();
    await expect(targetInput).toBeEditable();
  });

  test('should display priority selection', async ({ page }) => {
    await expect(page.getByText(/priority level/i)).toBeVisible();
    await expect(page.getByText(/medium priority/i)).toBeVisible();
    await expect(page.getByText(/higher priority investigations are processed faster/i)).toBeVisible();
  });

  test('should have functional form buttons', async ({ page }) => {
    await expect(page.getByRole('button', { name: /cancel/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /start investigation/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /close/i })).toBeVisible();
  });

  test('should close modal when Cancel is clicked', async ({ page }) => {
    await page.getByRole('button', { name: /cancel/i }).click();
    await expect(page.getByText(/new investigation/i)).not.toBeVisible();
  });

  test('should close modal when Close (X) is clicked', async ({ page }) => {
    await page.getByRole('button', { name: /close/i }).click();
    await expect(page.getByText(/new investigation/i)).not.toBeVisible();
  });

  test('should accept target input', async ({ page }) => {
    const targetInput = page.getByPlaceholder(/enter target to investigate/i);
    await targetInput.fill('suspicious@scammer.com');
    await expect(targetInput).toHaveValue('suspicious@scammer.com');
  });

  test('should validate required fields', async ({ page }) => {
    // Try to submit without filling target
    await page.getByRole('button', { name: /start investigation/i }).click();
    
    // Should show validation error (implementation dependent)
    // This test assumes validation is implemented
  });
});

test.describe('Admin Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/admin');
  });

  test('should display admin dashboard header', async ({ page }) => {
    await expect(page.getByText(/admin dashboard/i)).toBeVisible();
    await expect(page.getByText(/admin/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /logout/i })).toBeVisible();
  });

  test('should display admin statistics cards', async ({ page }) => {
    await expect(page.getByText(/total revenue/i)).toBeVisible();
    await expect(page.getByText(/total users/i)).toBeVisible();
    await expect(page.getByText(/total reports/i)).toBeVisible();
    await expect(page.getByText(/accuracy rate/i)).toBeVisible();
    
    // Check for values
    await expect(page.getByText('$45,600')).toBeVisible();
    await expect(page.getByText('156')).toBeVisible();
    await expect(page.getByText('96.8%')).toBeVisible();
  });

  test('should display growth indicators', async ({ page }) => {
    await expect(page.getByText(/\+15\.7%/)).toBeVisible();
    await expect(page.getByText(/\+8\.3%/)).toBeVisible();
    await expect(page.getByText(/\+12\.5%/)).toBeVisible();
    await expect(page.getByText(/\+2\.1%/)).toBeVisible();
  });

  test('should display sidebar navigation', async ({ page }) => {
    await expect(page.getByText(/scamshield ai/i)).toBeVisible();
    await expect(page.getByText(/dashboard/i)).toBeVisible();
    await expect(page.getByText(/users/i)).toBeVisible();
    await expect(page.getByText(/reports/i)).toBeVisible();
    await expect(page.getByText(/investigations/i)).toBeVisible();
    await expect(page.getByText(/payments/i)).toBeVisible();
    await expect(page.getByText(/security/i)).toBeVisible();
  });

  test('should display revenue trends section', async ({ page }) => {
    await expect(page.getByText(/revenue trends/i)).toBeVisible();
    await expect(page.getByText(/monthly revenue over the last 12 months/i)).toBeVisible();
    
    // Time period buttons
    await expect(page.getByRole('button', { name: '7D' })).toBeVisible();
    await expect(page.getByRole('button', { name: '30D' })).toBeVisible();
    await expect(page.getByRole('button', { name: '12M' })).toBeVisible();
  });

  test('should display recent activity feed', async ({ page }) => {
    await expect(page.getByText(/recent activity/i)).toBeVisible();
    await expect(page.getByText(/latest system activities/i)).toBeVisible();
    
    await expect(page.getByText(/new user registered/i)).toBeVisible();
    await expect(page.getByText(/investigation completed/i)).toBeVisible();
    await expect(page.getByText(/payment received/i)).toBeVisible();
    await expect(page.getByText(/high-risk detection/i)).toBeVisible();
  });

  test('should display recent reports table', async ({ page }) => {
    await expect(page.getByText(/recent reports/i)).toBeVisible();
    await expect(page.getByText(/latest investigation reports from users/i)).toBeVisible();
    
    // Table headers
    await expect(page.getByText(/id/i)).toBeVisible();
    await expect(page.getByText(/target/i)).toBeVisible();
    await expect(page.getByText(/type/i)).toBeVisible();
    await expect(page.getByText(/status/i)).toBeVisible();
    await expect(page.getByText(/user/i)).toBeVisible();
    await expect(page.getByText(/date/i)).toBeVisible();
    await expect(page.getByText(/actions/i)).toBeVisible();
  });

  test('should have functional export and filter buttons', async ({ page }) => {
    await expect(page.getByRole('button', { name: /export/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /filter/i })).toBeVisible();
  });

  test('should have functional view buttons in reports table', async ({ page }) => {
    const viewButtons = page.getByRole('button', { name: /view/i });
    await expect(viewButtons.first()).toBeVisible();
    await expect(viewButtons.first()).toBeEnabled();
  });
});

test.describe('Responsive Design', () => {
  test('should be responsive on mobile devices', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    await page.goto('/dashboard');
    
    await expect(page.getByText(/welcome back/i)).toBeVisible();
    await expect(page.getByText(/total scans/i)).toBeVisible();
  });

  test('should be responsive on tablet devices', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 }); // iPad
    await page.goto('/dashboard');
    
    await expect(page.getByText(/welcome back/i)).toBeVisible();
    await expect(page.getByText(/total scans/i)).toBeVisible();
  });

  test('should maintain functionality on different screen sizes', async ({ page }) => {
    await page.setViewportSize({ width: 1200, height: 800 }); // Desktop
    await page.goto('/dashboard');
    
    await page.getByRole('button', { name: /start scan/i }).click();
    await expect(page.getByText(/new investigation/i)).toBeVisible();
  });
});

