const { Builder, By, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');

describe('E2E Tests', () => {
  let driver;

  beforeAll(async () => {
    const options = new chrome.Options();
    options.addArguments('--headless');
    options.addArguments('--no-sandbox');
    options.addArguments('--disable-dev-shm-usage');
    
    driver = await new Builder()
      .forBrowser('chrome')
      .setChromeOptions(options)
      .build();
  }, 30000);

  afterAll(async () => {
    await driver.quit();
  });

  test('Full user flow - add item and verify', async () => {
    // Navigate to app
    await driver.get('http://localhost:3000');
    
    // Wait for environment badge
    await driver.wait(until.elementLocated(By.css('[data-testid="environment-badge"]')), 10000);
    
    // Fill form
    const nameInput = await driver.findElement(By.css('[data-testid="item-name-input"]'));
    await nameInput.sendKeys('E2E Test Item');
    
    const descInput = await driver.findElement(By.css('[data-testid="item-description-input"]'));
    await descInput.sendKeys('E2E Description');
    
    // Submit form
    const submitBtn = await driver.findElement(By.css('[data-testid="submit-button"]'));
    await submitBtn.click();
    
    // Verify item appears in list
    await driver.wait(until.elementLocated(By.css('[data-testid="items-list"]')), 10000);
    const itemsList = await driver.findElement(By.css('[data-testid="items-list"]'));
    const text = await itemsList.getText();
    
    expect(text).toContain('E2E Test Item');
  }, 30000);
});