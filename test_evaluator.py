# test_evaluator.py - Comprehensive test harness for poker hand evaluation

from card import Card, parse_card
from evaluator import rank_hand, get_hand_name

def create_test_hand(hand):
    # Allow both "AS KC" and ["AS", "KC"]
    if isinstance(hand, str):
        hand = hand.split()
    return [parse_card(c) for c in hand]


def test_case(name, hand1_str, hand2_str, expected_winner):
    """Test a single comparison case"""
    hand1 = create_test_hand(hand1_str)
    hand2 = create_test_hand(hand2_str)
    
    rank1 = rank_hand(hand1)
    rank2 = rank_hand(hand2)
    
    if expected_winner == 1:
        result = rank1 > rank2
        expected = "Hand 1 wins"
    elif expected_winner == 2:
        result = rank2 > rank1
        expected = "Hand 2 wins"
    else:  # tie
        result = rank1 == rank2
        expected = "Tie"
    
    status = "✓ PASS" if result else "✗ FAIL"
    
    print(f"{status} | {name}")
    print(f"  Hand 1: {hand1_str} → {get_hand_name(rank1)} {rank1}")
    print(f"  Hand 2: {hand2_str} → {get_hand_name(rank2)} {rank2}")
    print(f"  Expected: {expected} | Actual: {'Correct' if result else 'WRONG'}")
    print()
    
    return result

def run_all_tests():
    """Run comprehensive test suite"""
    print("="*80)
    print("POKER HAND EVALUATOR TEST HARNESS")
    print("="*80)
    print()
    
    passed = 0
    failed = 0
    
    # ========== BASIC HAND RECOGNITION ==========
    print("--- BASIC HAND RECOGNITION ---")
    
    if test_case(
        "Royal Flush vs Straight Flush",
        ['AH', 'KH', 'QH', 'JH', '10H'],
        ['9H', '8H', '7H', '6H', '5H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Straight Flush vs Four of a Kind",
        ['9H', '8H', '7H', '6H', '5H'],
        ['AS', 'AH', 'AD', 'AC', 'KH'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Four of a Kind vs Full House",
        ['AS', 'AH', 'AD', 'AC', 'KH'],
        ['KS', 'KH', 'KD', '5C', '5H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Full House vs Flush",
        ['KS', 'KH', 'KD', '5C', '5H'],
        ['AH', 'KH', '10H', '7H', '3H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Flush vs Straight",
        ['AH', 'KH', '10H', '7H', '3H'],
        ['9H', '8D', '7C', '6S', '5H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Straight vs Three of a Kind",
        ['9H', '8D', '7C', '6S', '5H'],
        ['QS', 'QH', 'QD', 'AC', 'KH'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Three of a Kind vs Two Pair",
        ['QS', 'QH', 'QD', 'AC', 'KH'],
        ['AS', 'AH', 'KD', 'KC', '5H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Two Pair vs One Pair",
        ['AS', 'AH', 'KD', 'KC', '5H'],
        ['AS', 'AH', 'KD', 'QC', '5H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "One Pair vs High Card",
        ['AS', 'AH', 'KD', 'QC', '5H'],
        ['AS', 'KH', 'QD', 'JC', '9H'],
        1
    ): passed += 1
    else: failed += 1
    
    # ========== STRAIGHT FLUSH TIE-BREAKERS ==========
    print("--- STRAIGHT FLUSH TIE-BREAKERS ---")
    
    if test_case(
        "Higher Straight Flush wins",
        ['9H', '8H', '7H', '6H', '5H'],
        ['8H', '7H', '6H', '5H', '4H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Wheel (A-2-3-4-5) is lowest straight flush",
        ['6H', '5H', '4H', '3H', '2H'],
        ['AH', '2H', '3H', '4H', '5H'],
        1
    ): passed += 1
    else: failed += 1
    
    # ========== FOUR OF A KIND TIE-BREAKERS ==========
    print("--- FOUR OF A KIND TIE-BREAKERS ---")
    
    if test_case(
        "Higher quad wins",
        ['AS', 'AH', 'AD', 'AC', 'KH'],
        ['KS', 'KH', 'KD', 'KC', 'AH'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Same quad, higher kicker wins",
        ['AS', 'AH', 'AD', 'AC', 'KH'],
        ['AS', 'AH', 'AD', 'AC', 'QH'],
        1
    ): passed += 1
    else: failed += 1
    
    # ========== FULL HOUSE TIE-BREAKERS ==========
    print("--- FULL HOUSE TIE-BREAKERS ---")
    
    if test_case(
        "Higher trips wins in full house",
        ['AS', 'AH', 'AD', 'KC', 'KH'],
        ['KS', 'KH', 'KD', 'AC', 'AH'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Same trips, higher pair wins",
        ['AS', 'AH', 'AD', 'KC', 'KH'],
        ['AS', 'AH', 'AD', 'QC', 'QH'],
        1
    ): passed += 1
    else: failed += 1
    
    # ========== FLUSH TIE-BREAKERS ==========
    print("--- FLUSH TIE-BREAKERS ---")
    
    if test_case(
        "Flush: Higher top card wins",
        ['AH', 'KH', '10H', '7H', '3H'],
        ['KH', 'QH', 'JH', '9H', '8H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Flush: Second card breaks tie",
        ['AH', 'KH', '10H', '7H', '3H'],
        ['AH', 'QH', 'JH', '10H', '9H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Flush: Goes to 5th card",
        ['AH', 'KH', 'QH', '7H', '5H'],
        ['AH', 'KH', 'QH', '7H', '4H'],
        1
    ): passed += 1
    else: failed += 1
    
    # ========== STRAIGHT TIE-BREAKERS ==========
    print("--- STRAIGHT TIE-BREAKERS ---")
    
    if test_case(
        "Higher straight wins",
        ['9H', '8D', '7C', '6S', '5H'],
        ['8H', '7D', '6C', '5S', '4H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Wheel (A-2-3-4-5) is lowest straight",
        ['6H', '5D', '4C', '3S', '2H'],
        ['AH', '2D', '3C', '4S', '5H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Same straight is a tie",
        ['9H', '8D', '7C', '6S', '5H'],
        ['9C', '8H', '7D', '6C', '5S'],
        0
    ): passed += 1
    else: failed += 1
    
    # ========== THREE OF A KIND TIE-BREAKERS ==========
    print("--- THREE OF A KIND TIE-BREAKERS ---")
    
    if test_case(
        "Higher trips wins",
        ['AS', 'AH', 'AD', 'KC', '5H'],
        ['KS', 'KH', 'KD', 'AC', 'QH'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Same trips, higher first kicker wins",
        ['AS', 'AH', 'AD', 'KC', '5H'],
        ['AS', 'AH', 'AD', 'QC', 'JH'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Same trips and first kicker, second kicker decides",
        ['AS', 'AH', 'AD', 'KC', '7H'],
        ['AS', 'AH', 'AD', 'KC', '6H'],
        1
    ): passed += 1
    else: failed += 1
    
    # ========== TWO PAIR TIE-BREAKERS ==========
    print("--- TWO PAIR TIE-BREAKERS ---")
    
    if test_case(
        "Higher top pair wins",
        ['AS', 'AH', 'KD', 'KC', '5H'],
        ['KS', 'KH', 'QD', 'QC', 'AH'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Same top pair, higher second pair wins",
        ['AS', 'AH', 'KD', 'KC', '5H'],
        ['AS', 'AH', 'QD', 'QC', 'KH'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Same two pairs, higher kicker wins",
        ['AS', 'AH', 'KD', 'KC', 'QH'],
        ['AS', 'AH', 'KD', 'KC', 'JH'],
        1
    ): passed += 1
    else: failed += 1
    
    # ========== ONE PAIR TIE-BREAKERS ==========
    print("--- ONE PAIR TIE-BREAKERS ---")
    
    if test_case(
        "Higher pair wins",
        ['AS', 'AH', 'KD', 'QC', '5H'],
        ['KS', 'KH', 'AD', 'QC', 'JH'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Same pair, higher first kicker wins",
        ['AS', 'AH', 'KD', 'QC', '5H'],
        ['AS', 'AH', 'QD', 'JC', '10H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Same pair and first kicker, second kicker decides",
        ['AS', 'AH', 'KD', 'QC', '5H'],
        ['AS', 'AH', 'KD', 'JC', '10H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Same pair and two kickers, third kicker decides",
        ['AS', 'AH', 'KD', 'QC', '7H'],
        ['AS', 'AH', 'KD', 'QC', '6H'],
        1
    ): passed += 1
    else: failed += 1
    
    # ========== HIGH CARD TIE-BREAKERS ==========
    print("--- HIGH CARD TIE-BREAKERS ---")
    
    if test_case(
        "Higher top card wins",
        ['AS', 'KH', 'QD', 'JC', '9H'],
        ['KS', 'QH', 'JD', '10C', '9H'],
        2
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Same top card, second card decides",
        ['AS', 'KH', 'QD', 'JC', '9H'],
        ['AS', 'QH', 'JD', '10C', '9H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Goes all the way to 5th card",
        ['AS', 'KH', 'QD', 'JC', '9H'],
        ['AS', 'KH', 'QD', 'JC', '8H'],
        1
    ): passed += 1
    else: failed += 1
    
    if test_case(
        "Identical high cards is a tie",
        ['AS', 'KH', 'QD', 'JC', '9H'],
        ['AS', 'KH', 'QD', 'JC', '9S'],
        0
    ): passed += 1
    else: failed += 1
    
    # ========== RESULTS ==========
    print("="*80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
    if failed == 0:
        print("✓ ALL TESTS PASSED! Your evaluator is working correctly.")
    else:
        print(f"✗ {failed} TEST(S) FAILED - Review the output above.")
    print("="*80)

if __name__ == "__main__":
    run_all_tests()