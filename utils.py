# utils.py - Display and formatting utilities

from evaluator import get_hand_name

def display_results(predictions, community_cards, stage_name):
    """Display formatted prediction results"""
    print(f"\n{'='*70}")
    print(f"Stage: {stage_name}")
    print(f"Community Cards: {community_cards if community_cards else 'None yet'}")
    print(f"{'='*70}")
    print(f"{'Player':<10} {'Pocket':<15} {'Win %':<10} {'Best Possible':<20}")
    print("-" * 70)
    
    for result in predictions:
        pocket_str = f"{result['pocket'][0]} {result['pocket'][1]}"
        win_str = f"{result['win_probability']:.2f}%"
        
        if result['current_hand']:
            hand_name = get_hand_name(result['current_hand'])
        else:
            hand_name = "TBD"
        
        print(f"Player {result['player']:<3} {pocket_str:<15} {win_str:<10} {hand_name:<20}")
    
    print(f"\nSimulations run: {predictions[0]['simulations']:,}")
    print(f"{'='*70}\n")

def display_results_with_current_hand(predictions, community_cards, stage_name):
    """Display formatted prediction results with current hand and most likely hand"""
    
    # Different display format for FLOP vs TURN
    if stage_name == "FLOP":
        # Simple format for FLOP - no most likely hand
        print(f"\n{'='*70}")
        print(f"Stage: {stage_name}")
        print(f"Community Cards: {community_cards}")
        print(f"{'='*70}")
        print(f"{'Player':<8} {'Pocket':<12} {'Current Hand':<18} {'Win %':<10}")
        print("-" * 70)
        
        for result in predictions:
            pocket_str = f"{result['pocket'][0]} {result['pocket'][1]}"
            win_str = f"{result['win_probability']:.2f}%"
            
            # Current hand
            if result['current_hand']:
                current_hand = get_hand_name(result['current_hand'])
            else:
                current_hand = "TBD"
            
            print(f"Player {result['player']:<2} {pocket_str:<12} {current_hand:<18} {win_str:<10}")
        
        print(f"\nSimulations: {predictions[0]['simulations']:,}")
        
        # Show top 3 most likely winners
        print(f"\n{'-'*70}")
        print("TOP 3 MOST LIKELY WINNERS:")
        print(f"{'-'*70}")
        top_3 = predictions[:3]
        for i, result in enumerate(top_3, 1):
            pocket_str = f"{result['pocket'][0]} {result['pocket'][1]}"
            print(f"{i}. Player {result['player']} ({pocket_str}) - {result['win_probability']:.2f}%")
        
        print(f"{'='*70}\n")
    
    else:
        # Full format for TURN - with most likely hand and breakdown
        print(f"\n{'='*90}")
        print(f"Stage: {stage_name}")
        print(f"Community Cards: {community_cards}")
        print(f"{'='*90}")
        print(f"{'Player':<8} {'Pocket':<12} {'Current':<18} {'Most Likely':<18} {'%':<8} {'Win %':<10}")
        print("-" * 90)
        
        for result in predictions:
            pocket_str = f"{result['pocket'][0]} {result['pocket'][1]}"
            win_str = f"{result['win_probability']:.2f}%"
            
            # Current hand
            if result['current_hand']:
                current_hand = get_hand_name(result['current_hand'])
            else:
                current_hand = "TBD"
            
            # Most likely hand
            if result.get('most_likely_hand'):
                likely_hand = result['most_likely_hand']
                likely_pct = f"{result['most_likely_percentage']:.1f}%"
            else:
                likely_hand = "N/A"
                likely_pct = "0%"
            
            print(f"Player {result['player']:<2} {pocket_str:<12} {current_hand:<18} {likely_hand:<18} {likely_pct:<8} {win_str:<10}")
        
        # Show hand breakdown for TURN stage
        if predictions[0].get('hand_breakdown'):
            print(f"\n{'-'*90}")
            print("RIVER POSSIBILITIES (Top 3 outcomes per player):")
            print(f"{'-'*90}")
            
            for result in predictions:
                if result.get('hand_breakdown'):
                    breakdown_str = " | ".join([f"{hand}: {pct:.1f}%" for hand, pct in result['hand_breakdown'].items()])
                    print(f"Player {result['player']}: {breakdown_str}")
        
        print(f"\nSimulations: {predictions[0]['simulations']:,}")
        
        # Show top 3 most likely winners
        print(f"\n{'-'*90}")
        print("TOP 3 MOST LIKELY WINNERS:")
        print(f"{'-'*90}")
        top_3 = predictions[:3]
        for i, result in enumerate(top_3, 1):
            pocket_str = f"{result['pocket'][0]} {result['pocket'][1]}"
            current = get_hand_name(result['current_hand']) if result['current_hand'] else "TBD"
            likely = result.get('most_likely_hand', 'N/A')
            print(f"{i}. Player {result['player']} ({pocket_str}) - {result['win_probability']:.2f}% | Current: {current} → Likely: {likely}")
        
        print(f"{'='*90}\n")

def print_header():
    """Print program header"""
    print("\n" + "="*70)
    print(" "*20 + "TEXAS HOLD'EM PREDICTOR")
    print("="*70)

def print_section(title):
    """Print section separator"""
    print("\n" + "="*70)
    print(title)
    print("="*70)
