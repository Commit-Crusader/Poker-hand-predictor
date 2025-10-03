# test_method_selection.py - Test the new flexible method selection

from card import parse_card
from predictor import predict_hands_with_current
from utils import display_results
import time

def test_method_selection():
    print("=" * 70)
    print("TESTING NEW METHOD SELECTION SYSTEM")
    print("=" * 70)
    
    # Sample game
    pockets = [
        [parse_card("AS"), parse_card("AH")],  # Pocket Aces
        [parse_card("KS"), parse_card("KH")],  # Pocket Kings
        [parse_card("QS"), parse_card("QH")],  # Pocket Queens
        [parse_card("JS"), parse_card("JH")],  # Pocket Jacks
        [parse_card("10S"), parse_card("10H")], # Pocket Tens
        [parse_card("7D"), parse_card("2C")]   # Weak hand
    ]
    
    # FLOP scenario
    community = [parse_card("AC"), parse_card("5H"), parse_card("9D")]
    
    print("\nFLOP: AC 5H 9D")
    print("Testing all method options for FLOP analysis:")
    print("-" * 70)
    
    methods = ["exhaustive", "monte_carlo", "auto"]
    
    for method in methods:
        print(f"\n=== Testing {method.upper()} method ===")
        start = time.time()
        results = predict_hands_with_current(community, pockets, method)
        elapsed = time.time() - start
        
        print(f"Time: {elapsed:.3f} seconds")
        if results:
            print(f"Winner: Player {results[0]['player']} - {results[0]['win_probability']:.2f}%")
        else:
            print("No results (method skipped pre-flop)")
    
    # TURN scenario  
    community_turn = community + [parse_card("AD")]
    
    print("\n" + "=" * 70)
    print("TURN: AC 5H 9D AD")
    print("Testing all method options for TURN analysis:")
    print("-" * 70)
    
    for method in methods:
        print(f"\n=== Testing {method.upper()} method ===")
        start = time.time()
        results = predict_hands_with_current(community_turn, pockets, method)
        elapsed = time.time() - start
        
        print(f"Time: {elapsed:.3f} seconds")
        if results:
            print(f"Winner: Player {results[0]['player']} - {results[0]['win_probability']:.2f}%")
        else:
            print("No results")
    
    print("\n" + "=" * 70)
    print("NEW GAME OPTIONS AVAILABLE:")
    print("=" * 70)
    print("1. Always Exhaustive - Forces exhaustive for all stages")
    print("2. Always Monte Carlo - Forces Monte Carlo for all stages") 
    print("3. Auto-selection - Smart method selection per stage")
    print("4. Custom per stage - Choose method for each flop/turn individually")
    print("\nYou can now run: python3 main.py")
    print("=" * 70)

if __name__ == "__main__":
    test_method_selection()