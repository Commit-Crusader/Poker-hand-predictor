# monte_carlo.py - Monte Carlo simulation for poker hand prediction

import random
from collections import Counter
from card import create_deck
from evaluator import evaluate_hand, get_hand_name

def predict_hands_monte_carlo(community_cards, pocket_hands, num_simulations=25000):
    """
    Monte Carlo simulation - randomly samples future scenarios instead of testing all
    
    Args:
        community_cards: List of cards already on the table
        pocket_hands: List of 6 players' pocket cards
        num_simulations: Number of random scenarios to test (default 10,000)
    
    Returns:
        List of prediction results sorted by win probability
    
    Performance:
        - 10,000 sims ≈ 0.5-1 second (vs 1-2 seconds exhaustive)
        - 50,000 sims ≈ 2-3 seconds (for higher accuracy)
        - Accuracy: ~99.5% compared to exhaustive (within 0.5%)
    """
    
    # Get all used cards
    used_cards = set(community_cards)
    for hand in pocket_hands:
        used_cards.update(hand)
    
    # Get remaining deck
    all_cards = create_deck()
    remaining_deck = [c for c in all_cards if c not in used_cards]
    
    # How many cards left to deal
    num_community = len(community_cards)
    cards_needed = 5 - num_community
    
    results = []
    
    # Simulate for each player
    for i, pocket in enumerate(pocket_hands):
        wins = 0.0
        total_simulations = 0
        hand_type_counts = {}  # Track hand types
        
        # Run Monte Carlo simulations
        for _ in range(num_simulations):
            # Randomly sample future cards (without replacement)
            future_cards = random.sample(remaining_deck, cards_needed)
            full_community = community_cards + future_cards
            
            # Evaluate this player's hand
            cards_tuple = tuple(pocket + full_community)
            player_rank = evaluate_hand(cards_tuple)
            hand_type_name = get_hand_name(player_rank)
            
            # Count this hand type
            if hand_type_name not in hand_type_counts:
                hand_type_counts[hand_type_name] = 0
            hand_type_counts[hand_type_name] += 1
            
            # Evaluate all players for this scenario
            player_ranks = []
            for j, opp_pocket in enumerate(pocket_hands):
                cards_tuple = tuple(opp_pocket + full_community)
                rank = evaluate_hand(cards_tuple)
                player_ranks.append((j, rank))
            
            # Find winners (handle ties)
            best_rank = max(player_ranks, key=lambda x: x[1])[1]
            winners = [j for j, rank in player_ranks if rank == best_rank]
            
            # Split pot on ties
            if i in winners:
                wins += 1.0 / len(winners)
            
            total_simulations += 1
        
        # Get current best hand
        if len(community_cards) >= 5:
            cards_tuple = tuple(pocket + community_cards)
            current_hand_rank = evaluate_hand(cards_tuple)
        elif len(community_cards) == 3 or len(community_cards) == 4:
            from predictor import evaluate_best_partial_hand
            all_cards_now = pocket + community_cards
            current_hand_rank = evaluate_best_partial_hand(all_cards_now)
        else:
            current_hand_rank = None
        
        # Find most common hand type and build breakdown
        most_common_hand = None
        most_common_percentage = 0
        hand_breakdown = {}
        
        if hand_type_counts:
            sorted_hands = sorted(hand_type_counts.items(), key=lambda x: x[1], reverse=True)
            most_common_hand = sorted_hands[0][0]
            most_common_percentage = (sorted_hands[0][1] / total_simulations) * 100
            
            # Build breakdown for top 3
            for hand_name, count in sorted_hands[:3]:
                percentage = (count / total_simulations) * 100
                hand_breakdown[hand_name] = percentage
        
        win_percentage = (wins / total_simulations) * 100
        results.append({
            'player': i + 1,
            'pocket': pocket,
            'win_probability': win_percentage,
            'simulations': total_simulations,
            'current_hand': current_hand_rank,
            'most_likely_hand': most_common_hand,
            'most_likely_percentage': most_common_percentage,
            'hand_breakdown': hand_breakdown,
            'all_hand_types': hand_type_counts,
            'method': 'Monte Carlo'  # Mark as Monte Carlo result
        })
    
    return sorted(results, key=lambda x: x['win_probability'], reverse=True)

def compare_monte_carlo_accuracy(community_cards, pocket_hands, num_simulations=10000):
    """
    Compare Monte Carlo results vs Exhaustive simulation
    Useful for testing accuracy
    """
    from predictor import predict_hands_with_current
    
    print("="*70)
    print("MONTE CARLO vs EXHAUSTIVE COMPARISON")
    print("="*70)
    
    # Run exhaustive
    print("\nRunning exhaustive simulation...")
    import time
    start = time.time()
    exhaustive_results = predict_hands_with_current(community_cards, pocket_hands)
    exhaustive_time = time.time() - start
    
    # Run Monte Carlo
    print(f"Running Monte Carlo ({num_simulations:,} simulations)...")
    start = time.time()
    mc_results = predict_hands_monte_carlo(community_cards, pocket_hands, num_simulations)
    mc_time = time.time() - start
    
    # Compare
    print("\n" + "-"*70)
    print(f"{'Method':<15} {'Time (sec)':<12} {'Simulations':<15}")
    print("-"*70)
    print(f"{'Exhaustive':<15} {exhaustive_time:<12.3f} {exhaustive_results[0]['simulations']:,}")
    print(f"{'Monte Carlo':<15} {mc_time:<12.3f} {num_simulations:,}")
    print(f"\nSpeedup: {exhaustive_time/mc_time:.2f}x faster")
    
    # Compare accuracy
    print("\n" + "-"*70)
    print(f"{'Player':<8} {'Exhaustive %':<15} {'Monte Carlo %':<15} {'Difference':<12}")
    print("-"*70)
    
    max_diff = 0
    for ex, mc in zip(exhaustive_results, mc_results):
        diff = abs(ex['win_probability'] - mc['win_probability'])
        max_diff = max(max_diff, diff)
        print(f"Player {ex['player']:<2} {ex['win_probability']:<15.2f} {mc['win_probability']:<15.2f} {diff:<12.2f}")
    
    print("-"*70)
    print(f"Maximum difference: {max_diff:.2f}%")
    print(f"Accuracy: {100 - max_diff:.2f}%")
    print("="*70)
    
    return exhaustive_results, mc_results

def auto_choose_method(community_cards, pocket_hands, speed_preference='balanced'):
    """
    Automatically choose between exhaustive and Monte Carlo based on scenario
    
    Args:
        speed_preference: 'fast', 'balanced', or 'accurate'
    """
    num_community = len(community_cards)
    cards_needed = 5 - num_community
    
    # Calculate number of possible combinations
    from card import create_deck
    used_cards = set(community_cards)
    for hand in pocket_hands:
        used_cards.update(hand)
    remaining = len(create_deck()) - len(used_cards)
    
    # Calculate combinations using factorial approximation
    if cards_needed == 1:
        total_combos = remaining
    elif cards_needed == 2:
        total_combos = remaining * (remaining - 1) // 2
    else:
        # Approximate for larger numbers
        total_combos = remaining ** cards_needed // (cards_needed ** cards_needed)
    
    print(f"\nAnalyzing scenario: {cards_needed} cards to deal, ~{total_combos:,} combinations")
    
    # Decision logic
    if cards_needed == 1:  # Turn stage
        print("→ Using EXHAUSTIVE (Turn stage is already fast)")
        from predictor import predict_hands_with_current
        return predict_hands_with_current(community_cards, pocket_hands), 'Exhaustive'
    
    elif cards_needed == 2:  # Flop stage
        if speed_preference == 'fast':
            print("→ Using MONTE CARLO (Fast mode: 10,000 simulations)")
            return predict_hands_monte_carlo(community_cards, pocket_hands, 10000), 'Monte Carlo'
        elif speed_preference == 'accurate':
            print("→ Using EXHAUSTIVE (Accurate mode)")
            from predictor import predict_hands_with_current
            return predict_hands_with_current(community_cards, pocket_hands), 'Exhaustive'
        else:  # balanced
            print("→ Using MONTE CARLO (Balanced mode: 25,000 simulations)")
            return predict_hands_monte_carlo(community_cards, pocket_hands, 25000), 'Monte Carlo'
    
    else:  # Pre-flop - skip analysis
        print("→ SKIPPING PRE-FLOP ANALYSIS (Start after flop for optimal performance)")
        print("  Pre-flop decisions should be based on starting hand charts")
        return None, 'Skipped'

# Example usage and testing
if __name__ == "__main__":
    from card import parse_card
    
    print("="*70)
    print("MONTE CARLO SIMULATION TESTER")
    print("="*70)
    
    # Example game
    community = [parse_card(c) for c in ["AH", "KH", "QH"]]
    pockets = [
        [parse_card("JH"), parse_card("10H")],
        [parse_card("AS"), parse_card("AC")],
        [parse_card("7C"), parse_card("7D")],
        [parse_card("KD"), parse_card("KS")],
        [parse_card("9S"), parse_card("8S")],
        [parse_card("3H"), parse_card("3C")]
    ]
    
    print("\nTest 1: Basic Monte Carlo (10,000 simulations)")
    print("-"*70)
    results = predict_hands_monte_carlo(community, pockets, 25000)
    for result in results[:3]:
        print(f"Player {result['player']}: {result['win_probability']:.2f}%")
    
    print("\n\nTest 2: Accuracy Comparison")
    print("-"*70)
    compare_monte_carlo_accuracy(community, pockets, 25000)
    
    print("\n\nTest 3: Auto-choose method")
    print("-"*70)
    results, method = auto_choose_method(community, pockets, 'balanced')
    print(f"\nSelected method: {method}")
    print(f"Top winner: Player {results[0]['player']} - {results[0]['win_probability']:.2f}%")
