# evaluator.py - Poker hand evaluation logic

import itertools
from collections import Counter
from functools import lru_cache

@lru_cache(maxsize=10000)
def evaluate_hand(cards_tuple):
    """Find best 5-card hand from 7 cards (cached for performance)"""
    cards = list(cards_tuple)
    best_rank = (0, [], [])
    
    for combo in itertools.combinations(cards, 5):
        rank = rank_hand(list(combo))
        if rank > best_rank:
            best_rank = rank
    
    return best_rank

def rank_hand(five_cards):
    """Rank a 5-card hand - returns tuple structured for proper tie-breaking
    
    Returns: (rank, primary_values, kickers)
    - rank: 0-9 (0=high card, 9=royal flush)
    - primary_values: main combo values sorted desc (pairs, trips, quads, etc.)
    - kickers: remaining cards sorted desc
    
    Python naturally compares tuples element-by-element, so this handles all ties correctly.
    """
    values = sorted([c.value for c in five_cards], reverse=True)
    suits = [c.suit for c in five_cards]
    value_counts = Counter(values)
    
    is_flush = len(set(suits)) == 1
    is_straight = check_straight(values)
    
    # Group cards by count: {count: [values with that count]}
    count_groups = {}
    for val, count in value_counts.items():
        if count not in count_groups:
            count_groups[count] = []
        count_groups[count].append(val)
    
    # Sort each group descending
    for count in count_groups:
        count_groups[count].sort(reverse=True)
    
    # Royal Flush: A-high straight flush
    if is_flush and is_straight and values[0] == [14, 13, 12, 11, 10]:
        return (9, [14], [])
    
    # Straight Flush: any straight + flush
    if is_flush and is_straight:
        # For A-2-3-4-5 (wheel), highest card is 5, not 14
        high_card = 5 if values == [14, 5, 4, 3, 2] else values[0]
        return (8, [high_card], [])
    
    # Four of a Kind
    if 4 in count_groups:
        quads = count_groups[4]  # the quad value
        kicker = count_groups[1]  # the single card
        return (7, quads, kicker)
    
    # Full House
    if 3 in count_groups and 2 in count_groups:
        trips = count_groups[3]
        pair = count_groups[2]
        # If multiple trips (shouldn't happen in 5 cards), take highest
        # If multiple pairs, take highest
        return (6, trips + pair, [])
    
    # Flush
    if is_flush:
        # All 5 cards matter for tie-breaking, in order
        return (5, [], values)
    
    # Straight
    if is_straight:
        # For A-2-3-4-5 (wheel), highest card is 5, not 14
        high_card = 5 if values == [14, 5, 4, 3, 2] else values[0]
        return (4, [high_card], [])
    
    # Three of a Kind
    if 3 in count_groups:
        trips = count_groups[3]
        kickers = sorted(count_groups[1], reverse=True)  # Explicitly sort kickers
        return (3, trips, kickers)
    
    # Two Pair
    if 2 in count_groups and len(count_groups[2]) == 2:
        pairs = count_groups[2]  # already sorted desc
        kicker = sorted(count_groups[1], reverse=True)  # Explicitly sort kickers
        return (2, pairs, kicker)
    
    # One Pair
    if 2 in count_groups:
        pair = count_groups[2]
        kickers = sorted(count_groups[1], reverse=True)  # Explicitly sort kickers
        return (1, pair, kickers)
    
    # High Card - all cards matter
    return (0, [], values)

def check_straight(values):
    """Check if values form a straight"""
    if values == list(range(values[0], values[0]-5, -1)):
        return True
    if values == [14, 5, 4, 3, 2]:  # Ace-low straight
        return True
    return False

def get_hand_name(rank_tuple):
    """Convert rank number to readable hand name"""
    rank = rank_tuple[0]
    hand_names = {
        9: "Royal Flush",
        8: "Straight Flush",
        7: "Four of a Kind",
        6: "Full House",
        5: "Flush",
        4: "Straight",
        3: "Three of a Kind",
        2: "Two Pair",
        1: "Pair",
        0: "High Card"
    }
    return hand_names[rank]
