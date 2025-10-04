# debug_queen_scenario.py - Debug the Queen scenario

from card import parse_card
from predictor import predict_hands_with_method
from utils import display_enhanced_results
from evaluator import evaluate_hand, get_hand_name

def debug_queen_scenario():
    print("=" * 80)
    print("DEBUGGING QUEEN SCENARIO")
    print("=" * 80)
    
    # Recreate the exact scenario
    pockets = [
        [parse_card("3D"), parse_card("9H")],  # Player 1
        [parse_card("5S"), parse_card("8S")],  # Player 2
        [parse_card("2H"), parse_card("9C")],  # Player 3
        [parse_card("KH"), parse_card("QC")],  # Player 4
        [parse_card("7H"), parse_card("JD")],  # Player 5
        [parse_card("AC"), parse_card("7S")]   # Player 6
    ]
    
    # Board after river with another Queen
    community = [parse_card("QH"), parse_card("7C"), parse_card("4S"), parse_card("10D"), parse_card("QS")]
    
    print("Final Board: QH 7C 4S 10D QS (two Queens)")
    print("=" * 80)
    
    # Manual evaluation of each player
    print("MANUAL HAND EVALUATION:")
    print("-" * 80)
    
    for i, pocket in enumerate(pockets, 1):
        all_cards = pocket + community
        best_hand_rank = evaluate_hand(tuple(all_cards))
        hand_name = get_hand_name(best_hand_rank)
        
        print(f"Player {i} ({pocket[0]} {pocket[1]}): {hand_name}")
        print(f"  Available cards: {' '.join([str(c) for c in all_cards])}")
    
    print("\n" + "=" * 80)
    print("PREDICTOR RESULTS:")
    print("=" * 80)
    
    # Run predictor (should be instant for river)
    results = predict_hands_with_method(community, pockets, "exhaustive")
    
    if results:
        display_enhanced_results(results, community, "RIVER")
    else:
        print("No results returned from predictor!")
    
    # Expected winner
    print("\n" + "=" * 80)
    print("EXPECTED WINNER ANALYSIS:")
    print("=" * 80)
    
    print("Player 4 should win with the best Queen-based hand")
    print("- Has QC in pocket + QH QS on board = Three Queens")
    print("- All others have pair of Queens from the board")
    print("- Player 4's kicker (King) should beat all other kickers")

if __name__ == "__main__":
    debug_queen_scenario()