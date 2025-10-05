# sportybet_poker_scraper.py - Scraper for SportyBet Poker

from playwright.sync_api import sync_playwright
import subprocess
import time

class SportyBetPokerScraper:
    def __init__(self):
        self.process = None
    
    def identify_suit_from_svg(self, card_element):
        """Identify suit from SVG path"""
        svg = card_element.query_selector('svg')
        if not svg:
            return None
        
        path = svg.query_selector('path')
        if not path:
            return None
        
        path_d = path.get_attribute('d')
        fill_rule = path.get_attribute('fill-rule') or ''
        
        # Spade: "M21.9595 11.8046" - appears in your HTML
        if '21.9595 11.8046' in path_d:
            return 'S'
        
        # Club: "M17.9999 9.94949" with 3-circle pattern
        if '17.9999 9.94949' in path_d and '17.9999 6.27562' in path_d:
            return 'C'
        
        # Heart: "fill-rule='evenodd'" with specific heart path
        if fill_rule == 'evenodd' and '17.9952 1' in path_d:
            return 'H'
        
        # Diamond: "fill-rule='evenodd'" with diamond path
        if fill_rule == 'evenodd' and '8.36742 6.82911' in path_d:
            return 'D'
        
        return None
    
    def extract_card(self, card_element):
        """Extract card rank and suit from element"""
        try:
            # Get rank from span
            rank_element = card_element.query_selector('span.p9p7USKXMQo2_eEm')
            if not rank_element:
                return None
            
            rank = rank_element.inner_text().strip().upper()
            
            # Convert rank if needed
            rank_map = {
                '1': 'A',
                'A': 'A',
                '11': 'J',
                'J': 'J',
                '12': 'Q',
                'Q': 'Q',
                '13': 'K',
                'K': 'K'
            }
            rank = rank_map.get(rank, rank)
            
            # Get suit from SVG
            suit = self.identify_suit_from_svg(card_element)
            if not suit:
                return None
            
            return f"{rank}{suit}"
            
        except Exception as e:
            print(f"Error extracting card: {e}")
            return None
    
    def scrape_game_state(self, page):
        """Scrape all 6 players and community cards"""
        game_data = {
            'pockets': [],
            'flop': [],
            'turn': None,
            'community_cards': []
        }
        
        try:
            # Scrape 6 players' cards
            # Each player is in a div with data-qa="button-screen-odd-446" through "button-screen-odd-451"
            for i in range(446, 452):  # Player 1-6
                player_cards = []
                player_selector = f'[data-qa="button-screen-odd-{i}"]'
                player_element = page.query_selector(player_selector)
                
                if player_element:
                    # Get both cards for this player
                    card_elements = player_element.query_selector_all('[data-qa^="area-card-"]')
                    
                    for card_elem in card_elements[:2]:  # Take first 2 cards
                        card = self.extract_card(card_elem)
                        if card:
                            player_cards.append(card)
                
                # Add to pockets (empty if not found)
                if len(player_cards) == 2:
                    game_data['pockets'].append(player_cards)
                else:
                    game_data['pockets'].append(['', ''])
            
            # Scrape community cards from data-qa="area-table-cards"
            table_cards_container = page.query_selector('[data-qa="area-table-cards"]')
            
            if table_cards_container:
                community_card_elements = table_cards_container.query_selector_all('[data-qa^="area-card-"]')
                
                for card_elem in community_card_elements:
                    card = self.extract_card(card_elem)
                    if card:
                        game_data['community_cards'].append(card)
                
                # Split into flop and turn
                if len(game_data['community_cards']) >= 3:
                    game_data['flop'] = game_data['community_cards'][:3]
                if len(game_data['community_cards']) >= 4:
                    game_data['turn'] = game_data['community_cards'][3]
            
            return game_data
            
        except Exception as e:
            print(f"Error scraping game state: {e}")
            return game_data
    
    def send_to_predictor(self, game_data):
        """Send scraped data to CLI predictor"""
        if not self.process:
            self.process = subprocess.Popen(
                ['python', 'main.py'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
        
        def send_input(text):
            self.process.stdin.write(text + '\n')
            self.process.stdin.flush()
            time.sleep(0.3)
        
        # Send pocket cards
        print("\n=== Sending pocket cards to predictor ===")
        valid_pockets = 0
        for i, pocket in enumerate(game_data['pockets']):
            if pocket[0] and pocket[1]:
                pocket_str = f"{pocket[0]} {pocket[1]}"
                send_input(pocket_str)
                print(f"Player {i+1}: {pocket_str}")
                valid_pockets += 1
            else:
                print(f"Player {i+1}: Cards not visible - skipping")
        
        if valid_pockets < 6:
            print(f"\n⚠️  Warning: Only {valid_pockets}/6 players have visible cards")
            return False
        
        time.sleep(1)
        
        # Send flop cards
        if len(game_data['flop']) == 3:
            print("\n=== Sending flop cards ===")
            for card in game_data['flop']:
                send_input(card)
                print(f"Flop card: {card}")
            time.sleep(2)
        else:
            print(f"\n⚠️  Flop incomplete: {len(game_data['flop'])}/3 cards")
            return False
        
        # Send turn card
        if game_data['turn']:
            print(f"\n=== Sending turn card: {game_data['turn']} ===")
            send_input(game_data['turn'])
            time.sleep(2)
            
            # Read predictor output
            print("\n" + "="*70)
            print("PREDICTOR OUTPUT")
            print("="*70)
            for _ in range(40):
                line = self.process.stdout.readline()
                if line:
                    print(line.strip())
            
            return True
        else:
            print(f"\n⚠️  Turn card not visible yet")
            return False
    
    def monitor_game(self, url):
        """Monitor SportyBet poker game"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            print("="*70)
            print("SPORTYBET POKER SCRAPER")
            print("="*70)
            print(f"\nNavigating to {url}...")
            page.goto(url)
            
            print("\n*** LOGIN INSTRUCTIONS ***")
            print("1. Please login to SportyBet")
            print("2. Navigate to the poker game")
            print("3. Make sure you can see the poker table")
            print("4. Press Enter when ready...")
            input()
            
            print("\n✓ Starting game monitor...")
            print("Waiting for cards to be dealt...\n")
            
            game_count = 0
            
            while True:
                try:
                    # Wait for player cards to appear
                    page.wait_for_selector('[data-qa="button-screen-odd-446"]', timeout=60000)
                    time.sleep(3)  # Let all cards load
                    
                    # Scrape game state
                    game_data = self.scrape_game_state(page)
                    
                    game_count += 1
                    print("\n" + "="*70)
                    print(f"GAME #{game_count}")
                    print("="*70)
                    
                    print("\nScraped Data:")
                    print("-" * 70)
                    for i, pocket in enumerate(game_data['pockets']):
                        if pocket[0] and pocket[1]:
                            print(f"Player {i+1}: {pocket[0]} {pocket[1]}")
                        else:
                            print(f"Player {i+1}: Not visible")
                    
                    print(f"\nCommunity Cards: {game_data['community_cards']}")
                    print(f"Flop: {game_data['flop']}")
                    print(f"Turn: {game_data['turn']}")
                    print("-" * 70)
                    
                    # Check if we have complete data
                    if len(game_data['flop']) == 3 and game_data['turn']:
                        valid_pockets = sum(1 for p in game_data['pockets'] if p[0] and p[1])
                        
                        if valid_pockets == 6:
                            print("\n✓ Complete game state detected!")
                            success = self.send_to_predictor(game_data)
                            
                            if success:
                                print("\n" + "="*70)
                                print("Waiting 20 seconds for next game...")
                                print("="*70)
                                time.sleep(20)
                            else:
                                print("\n⚠️  Failed to send to predictor, retrying...")
                                time.sleep(5)
                        else:
                            print(f"\n⚠️  Only {valid_pockets}/6 players visible, waiting...")
                            time.sleep(3)
                    else:
                        print("\n⏳ Waiting for more cards to be dealt...")
                        time.sleep(3)
                    
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    print("Retrying in 5 seconds...")
                    time.sleep(5)

# Main execution
if __name__ == "__main__":
    scraper = SportyBetPokerScraper()
    
    # SportyBet poker URL
    poker_url = "https://www.sportybet.com/gh/sportygames/live-games/Bet-On-Poker"
    
    scraper.monitor_game(poker_url)
