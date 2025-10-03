# demo_monte_carlo.py - Quick demo of Monte Carlo integration

from card import parse_card
from monte_carlo import auto_choose_method, predict_hands_monte_carlo
from predictor import predict_hands_with_current
from utils import display_results
import time

def demo_monte_carlo():
    print("=" * 70)
    print("TEXAS HOLD'EM MONTE CARLO DEMO")
    print("=" * 70)
    
    # Sample game setup
    print("\nSample 6-player game:")
    print("Player 1: AS AH (pocket aces)")
    print("Player 2: KS KH (pocket kings)")
    print("Player 3: QS QH (pocket queens)")
    print("Player 4: JS JH (pocket jacks)")
    print("Player 5: 10S 10H (pocket tens)")
    print("Player 6: 7D 2C (weak hand)")
    
    pockets = [
        [parse_card("AS"), parse_card("AH")],
        [parse_card("KS"), parse_card("KH")],
        [parse_card("QS"), parse_card("QH")],
        [parse_card("JS"), parse_card("JH")],
        [parse_card("10S"), parse_card("10H")],
        [parse_card("7D"), parse_card("2C")]
    ]
    
    # FLOP
    print("\n" + "=" * 70)
    print("FLOP: AC 5H 9D")
    print("=" * 70)
    
    community = [parse_card("AC"), parse_card("5H"), parse_card("9D")]
    
    print("\nUsing auto-selection (should pick Monte Carlo)...")
    start = time.time()
    results, method = auto_choose_method(community, pockets, 'balanced')
    elapsed = time.time() - start
    
    print(f"\nMethod used: {method}")
    print(f"Time taken: {elapsed:.2f} seconds")
    
    # Display results
    if results:
        display_results(results, community, "FLOP")
    
    # TURN
    print("\n" + "=" * 70)
    print("TURN: AC 5H 9D AD")
    print("=" * 70)
    
    community.append(parse_card("AD"))
    
    print("\nUsing auto-selection (should pick Exhaustive for turn)...")
    start = time.time()
    results, method = auto_choose_method(community, pockets, 'balanced')
    elapsed = time.time() - start
    
    print(f"\nMethod used: {method}")
    print(f"Time taken: {elapsed:.3f} seconds")
    
    if results:
        display_results(results, community, "TURN")

if __name__ == "__main__":
    demo_monte_carlo()