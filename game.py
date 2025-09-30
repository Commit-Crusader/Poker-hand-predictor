# game.py - Game flow and user interaction

from card import parse_card
from predictor import predict_hands, predict_hands_with_method
from utils import display_results, display_results_with_current_hand, display_enhanced_results, print_header, print_section

def run_game():
    """Main game flow with looping"""
    print_header()

    print("\nChoose prediction method:")
    print("1. Always Exhaustive (most accurate, slower for flop)")
    print("2. Always Monte Carlo (fast, ~99% accurate)")  
    print("3. Auto-selection (smart balance - recommended)")
    print("4. Custom per stage (choose method for each flop/turn)")
    method_choice = input("> ").strip()
    
    print("\nChoose display style:")
    print("1. Basic results (simple win percentages)")
    print("2. Enhanced analysis (hand breakdowns + strategy insights)")
    display_choice = input("> ").strip()
    
    enhanced_display = display_choice == "2"

    if method_choice == "1":
        method = "exhaustive"
    elif method_choice == "2":
        method = "monte_carlo"
    elif method_choice == "3":
        method = "auto"
    else:
        method = "custom"

    
    while True:
        # Always 6 players
        num_players = 6
        
        # Step 1: Get all pocket cards (returns used_cards set)
        pocket_hands, used_cards = get_pocket_cards(num_players)
        
        print_section("All players entered!")
        
        """# PRE-FLOP PREDICTION
        print("\nCalculating pre-flop probabilities...")
        preflop_predictions = predict_hands([], pocket_hands)
        display_results(preflop_predictions, [], "PRE-FLOP")
        
        print_section("Now let's deal the community cards...")
        """
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
        
        # Step 3: Calculate after FLOP with chosen method
        if method == "custom":
            print("\nChoose method for FLOP analysis:")
            print("1. Exhaustive (most accurate, ~1-2 seconds)")
            print("2. Monte Carlo (fast, ~1 second)")  
            print("3. Auto-select (recommended)")
            flop_choice = input("> ").strip()
            
            if flop_choice == "1":
                flop_method = "exhaustive"
            elif flop_choice == "2":
                flop_method = "monte_carlo"
            else:
                flop_method = "auto"
        else:
            flop_method = method
            
        print(f"\nCalculating probabilities after FLOP using {flop_method.upper()} method...")
        predictions = predict_hands_with_method(community_cards, pocket_hands, flop_method)
        
        if enhanced_display:
            display_enhanced_results(predictions, community_cards, "FLOP")
        else:
            display_results_with_current_hand(predictions, community_cards, "FLOP")

        
        # Step 4: Get TURN (4th card)
        turn_card = get_single_card("Enter the TURN card (e.g., 10C):", used_cards)
        used_cards.add(turn_card)
        community_cards.append(turn_card)
        
        # Step 5: Recalculate after TURN
        if method == "custom":
            print("\nChoose method for TURN analysis:")
            print("1. Exhaustive (most accurate, instant)")
            print("2. Monte Carlo (also fast for turn)")  
            print("3. Auto-select (recommended - will pick exhaustive)")
            turn_choice = input("> ").strip()
            
            if turn_choice == "1":
                turn_method = "exhaustive"
            elif turn_choice == "2":
                turn_method = "monte_carlo"
            else:
                turn_method = "auto"
        else:
            turn_method = method
            
        print(f"\nRecalculating probabilities after TURN using {turn_method.upper()} method...")
        predictions = predict_hands_with_method(community_cards, pocket_hands, turn_method)
        
        if enhanced_display:
            display_enhanced_results(predictions, community_cards, "TURN")
        else:
            display_results_with_current_hand(predictions, community_cards, "TURN")

        
        # Step 6: Optional RIVER
        print("Want to see the RIVER? (y/n):")
        continue_river = input("> ").strip().lower()
        
        if continue_river == 'y':
            river_card = get_single_card("\nEnter the RIVER card (e.g., 5D):", used_cards)
            used_cards.add(river_card)
            community_cards.append(river_card)
            
            print("\nFinal results after RIVER...")
            predictions = predict_hands_with_method(community_cards, pocket_hands)
            
            if enhanced_display:
                display_enhanced_results(predictions, community_cards, "RIVER")
            else:
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
