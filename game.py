# game.py - Game flow and user interaction

from card import parse_card
from predictor import predict_hands, predict_hands_with_current
from utils import display_results, display_results_with_current_hand, print_header, print_section

def run_game():
    """Main game flow with looping"""
    print_header()
    
    while True:
        # Always 6 players
        num_players = 6
        
        # Step 1: Get all pocket cards (returns used_cards set)
        pocket_hands, used_cards = get_pocket_cards(num_players)
        
        print_section("All players entered!")
        
        
        # Step 2: Get FLOP (3 cards one by one)
        community_cards = []
        print("\nEnter FLOP cards one at a time:")
        
        flop1 = get_single_card("FLOP Card 1:", used_cards)
        used_cards.add(flop1)
        community_cards.append(flop1)
        
        flop2 = get_single_card("FLOP Card 2:", used_cards)
        used_cards.add(flop2)
        community_cards.append(flop2)
        
        flop3 = get_single_card("FLOP Card 3:", used_cards)
        used_cards.add(flop3)
        community_cards.append(flop3)
        
        # Step 3: Calculate after FLOP with current hand info
        print("\nCalculating probabilities after FLOP...")
        predictions = predict_hands_with_current(community_cards, pocket_hands)
        display_results_with_current_hand(predictions, community_cards, "FLOP")
        
        # Step 4: Get TURN (4th card)
        turn_card = get_single_card("Enter the TURN card (e.g., 10C):", used_cards)
        used_cards.add(turn_card)
        community_cards.append(turn_card)
        
        # Step 5: Recalculate after TURN with current hand info
        print("\nRecalculating probabilities after TURN...")
        predictions = predict_hands_with_current(community_cards, pocket_hands)
        display_results_with_current_hand(predictions, community_cards, "TURN")
        
        # Step 6: Optional RIVER
        print("Want to see the RIVER? (y/n):")
        continue_river = input("> ").strip().lower()
        
        if continue_river == 'y':
            river_card = get_single_card("\nEnter the RIVER card (e.g., 5D):", used_cards)
            used_cards.add(river_card)
            community_cards.append(river_card)
            
            print("\nFinal results after RIVER...")
            predictions = predict_hands_with_current(community_cards, pocket_hands)
            display_results_with_current_hand(predictions, community_cards, "RIVER")
        
        print("\nThanks for using Texas Hold'em Predictor!")
        
        # Ask to play again
        print("\nPlay another hand? (y/n):")
        play_again = input("> ").strip().lower()
        
        if play_again != 'y':
            print("\nGoodbye!")
            break

def get_pocket_cards(num_players):
    """Get pocket cards from all players with uniqueness check"""
    pocket_hands = []
    used_cards = set()  # Track all cards already dealt
    
    print(f"\nEnter pocket cards for {num_players} players:")
    
    for i in range(num_players):
        while True:
            print(f"Player {i+1} (e.g., AS KC):")
            pocket_input = input("> ").strip().split()
            
            # Validate input
            if len(pocket_input) != 2:
                print("Error: Please enter exactly 2 cards separated by space.")
                continue
            
            try:
                pocket = [parse_card(c) for c in pocket_input]
                
                # Check for duplicate cards in the same hand
                if pocket[0] == pocket[1]:
                    print("Error: Cannot have the same card twice in one hand.")
                    continue
                
                # Check if any card was already used
                duplicate_found = False
                for card in pocket:
                    if card in used_cards:
                        print(f"Error: {card} has already been dealt to another player.")
                        duplicate_found = True
                        break
                
                if duplicate_found:
                    continue
                
                # All checks passed - add cards
                pocket_hands.append(pocket)
                used_cards.update(pocket)
                break
                
            except (ValueError, KeyError, IndexError) as e:
                print(f"Error: Invalid card format. Use format like 'AS KC' or '10H JD'.")
                continue
    
    return pocket_hands, used_cards

def get_single_card(prompt, used_cards):
    """Get and validate a single card input with uniqueness check"""
    while True:
        print(prompt)
        card_input = input("> ").strip()
        
        if not card_input:
            print("Error: Please enter a card.")
            continue
        
        try:
            card = parse_card(card_input)
            
            # Check if card was already used
            if card in used_cards:
                print(f"Error: {card} has already been dealt.")
                continue
            
            return card
            
        except (ValueError, KeyError, IndexError) as e:
            print(f"Error: Invalid card format. Use format like 'AH', 'KD', or '10C'.")
            continue
