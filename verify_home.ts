import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 390, height: 844 }); // iPhone 12 Pro size
  await page.goto('http://localhost:5175/');
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'home_page_final.png', fullPage: true });
  await browser.close();
})();
