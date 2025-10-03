# test_enhanced_display.py - Test the new enhanced display system

from card import parse_card
from predictor import predict_hands_with_method
from utils import display_enhanced_results
import time

def test_enhanced_display():
    print("=" * 100)
    print("TESTING ENHANCED HAND BREAKDOWN DISPLAY")
    print("=" * 100)
    
    # Sample interesting game scenario
    pockets = [
        [parse_card("AS"), parse_card("AH")],  # Pocket Aces (strong)
        [parse_card("KS"), parse_card("KH")],  # Pocket Kings (good)
        [parse_card("QS"), parse_card("QH")],  # Pocket Queens (decent)
        [parse_card("JS"), parse_card("JH")],  # Pocket Jacks (okay)
        [parse_card("10S"), parse_card("9S")], # Suited connectors (draw potential)
        [parse_card("7D"), parse_card("2C")]   # Trash hand (underdog)
    ]
    
    # FLOP that creates interesting dynamics
    community = [parse_card("AC"), parse_card("5H"), parse_card("9D")]
    
    print("\nScenario: Pocket pairs vs suited connectors")
    print("FLOP: AC 5H 9D (gives Player 1 trips, others still in trouble)")
    print("=" * 100)
    
    # Test exhaustive method first
    print("\nTesting with EXHAUSTIVE method...")
    start = time.time()
    results = predict_hands_with_method(community, pockets, "exhaustive")
    elapsed = time.time() - start
    
    print(f"Calculation time: {elapsed:.3f} seconds")
    
    # Display enhanced results
    display_enhanced_results(results, community, "FLOP")
    
    print("\n" + "=" * 100)
    print("TEST COMPLETE - Enhanced display is working!")
    print("=" * 100)
    
    return results

if __name__ == "__main__":
    test_enhanced_display()