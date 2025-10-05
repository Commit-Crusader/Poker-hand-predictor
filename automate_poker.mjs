import { chromium } from 'playwright';

async function runPokerScraper() {
  // 1. Launch browser
  const browser = await chromium.launch({ headless: false }); // false = see browser
  const context = await browser.newContext();
  const page = await context.newPage();

  // 2. Go to SportyBet games page
  console.log("Opening SportyBet...");
  await page.goto('https://www.sportybet.com/gh/games', { waitUntil: 'load' });

  // 3. Click on the Poker tab (you might need to adjust the text selector)
  console.log("Navigating to Poker...");
  await page.waitForSelector('text=Poker', { timeout: 15000 });
  await page.click('text=Poker');

  // 4. Wait for Poker table to load
  console.log("Waiting for table...");
  await page.waitForTimeout(5000); // let dynamic JS load

  // 5. Extract visible info (you’ll adjust these selectors after inspection)
  const cards = await page.$$eval('.card', cards =>
    cards.map(c => c.textContent.trim())
  );
  
  const odds = await page.$$eval('.odds, .win-prob', el =>
    el.map(e => e.textContent.trim())
  );

  const players = await page.$$eval('.player, .table-player', el =>
    el.map(e => e.textContent.trim())
  );

  console.log("\n=== Extracted Poker Info ===");
  console.log("Cards:", cards);
  console.log("Odds:", odds);
  console.log("Players:", players);

  await browser.close();
}

runPokerScraper();

