# predictor.py - Win probability calculations

import itertools
from card import create_deck
from evaluator import evaluate_hand, get_hand_name

def predict_hands(community_cards, pocket_hands):
    """Calculate win probabilities for all players"""
    
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
        
        # Try all possible future boards
        for future_cards in itertools.combinations(remaining_deck, cards_needed):
            full_community = community_cards + list(future_cards)
            
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
        
        # Get current best hand if 5+ cards
        if len(community_cards) >= 5:
            cards_tuple = tuple(pocket + community_cards)
            current_hand = evaluate_hand(cards_tuple)
        else:
            current_hand = None
        
        win_percentage = (wins / total_simulations) * 100
        results.append({
            'player': i + 1,
            'pocket': pocket,
            'win_probability': win_percentage,
            'simulations': total_simulations,
            'current_hand': current_hand
        })
    
    return sorted(results, key=lambda x: x['win_probability'], reverse=True)

def predict_hands_with_current(community_cards, pocket_hands):
    """Calculate win probabilities AND show current hand for each player"""
    
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
        
        # Try all possible future boards
        for future_cards in itertools.combinations(remaining_deck, cards_needed):
            full_community = community_cards + list(future_cards)
            
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
        
        # Get CURRENT best hand with available cards
        if len(community_cards) >= 5:
            # If 5 cards available, evaluate best 5-card hand
            cards_tuple = tuple(pocket + community_cards)
            current_hand_rank = evaluate_hand(cards_tuple)
        elif len(community_cards) == 3 or len(community_cards) == 4:
            # If 3 or 4 community cards, show what hand they currently have
            all_cards_now = pocket + community_cards
            current_hand_rank = evaluate_best_partial_hand(all_cards_now)
        else:
            # Pre-flop or no cards
            current_hand_rank = None
        
        win_percentage = (wins / total_simulations) * 100
        results.append({
            'player': i + 1,
            'pocket': pocket,
            'win_probability': win_percentage,
            'simulations': total_simulations,
            'current_hand': current_hand_rank
        })
    
    return sorted(results, key=lambda x: x['win_probability'], reverse=True)

def evaluate_best_partial_hand(cards):
    """Evaluate best possible hand from less than 5 cards"""
    if len(cards) < 5:
        # For partial hands, just check what pairs/trips we have so far
        from collections import Counter
        values = [c.value for c in cards]
        value_counts = Counter(values)
        
        # Sort by count, then by value
        sorted_counts = sorted(value_counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
        
        if sorted_counts[0][1] == 3:
            return (3, [sorted_counts[0][0]], [])  # Three of a kind
        elif sorted_counts[0][1] == 2:
            if len(sorted_counts) > 1 and sorted_counts[1][1] == 2:
                return (2, [sorted_counts[0][0], sorted_counts[1][0]], [])  # Two pair
            else:
                return (1, [sorted_counts[0][0]], [])  # One pair
        else:
            return (0, [], sorted([v for v in values], reverse=True))  # High card
    else:
        # 5+ cards, do normal evaluation
        from evaluator import rank_hand
        best_rank = (0, [], [])
        for combo in itertools.combinations(cards, 5):
            rank = rank_hand(list(combo))
            if rank > best_rank:
                best_rank = rank
        return best_rank
