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
    """Display formatted prediction results with current hand"""
    print(f"\n{'='*80}")
    print(f"Stage: {stage_name}")
    print(f"Community Cards: {community_cards}")
    print(f"{'='*80}")
    print(f"{'Player':<8} {'Pocket':<12} {'Current Hand':<18} {'Win %':<10} {'Sims':<10}")
    print("-" * 80)
    
    for result in predictions:
        pocket_str = f"{result['pocket'][0]} {result['pocket'][1]}"
        win_str = f"{result['win_probability']:.2f}%"
        sims_str = f"{result['simulations']:,}"
        
        if result['current_hand']:
            hand_name = get_hand_name(result['current_hand'])
        else:
            hand_name = "TBD"
        
        print(f"Player {result['player']:<2} {pocket_str:<12} {hand_name:<18} {win_str:<10} {sims_str:<10}")
    
    print(f"{'='*80}\n")

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
