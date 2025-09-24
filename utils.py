# utils.py - Display and formatting utilities

from evaluator import get_hand_name, evaluate_hand

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


def display_results_with_current_hand(predictions, community_cards, stage):
    print("=" * 90)
    print(f"Stage: {stage.upper()}")
    print("Community Cards:", [str(c) for c in community_cards])
    print("=" * 90)
    print("Player   Pocket       Current Hand       Most Likely       Tie %     Win %")
    print("-" * 90)

    # sort by win percentage descending
    sorted_results = sorted(predictions, key=lambda x: x['win_probability'], reverse=True)
    for result in sorted_results:
        player = result['player']
        pocket = result['pocket']

        # --- Current Hand (based on known community cards) ---
        current_rank = evaluate_hand(tuple(pocket + community_cards))
        current_name = get_hand_name(current_rank)

        # --- Most Likely Hand (if simulated results contain info) ---
        most_likely_name = result.get('most_likely_hand', "N/A")

        tie_pct = 0  # Tie percentage not available in current format
        win_pct = result.get('win_probability', 0)

        print(f"{player:<9}{' '.join([str(c) for c in pocket]):<13}"
              f"{current_name:<19}{most_likely_name:<19}"
              f"{tie_pct:<8.2f}{win_pct:.2f}%")

    print("\nSimulations:", predictions[0]['simulations'] if predictions else "N/A")
    print("\n" + "-" * 90)
    print("TOP 3 MOST LIKELY WINNERS:")
    print("-" * 90)

    # Top 3 players
    for i, result in enumerate(sorted_results[:3], 1):
        player = result['player']
        pocket = result['pocket']
        current_rank = evaluate_hand(tuple(pocket + community_cards))
        current_name = get_hand_name(current_rank)
        most_likely_name = result.get('most_likely_hand', "N/A")
        win_pct = result.get('win_probability', 0)

        print(f"{i}. Player {player} ({' '.join([str(c) for c in pocket])}) - {win_pct:.2f}% | "
              f"Current: {current_name} → Likely: {most_likely_name}")

def display_enhanced_results(predictions, community_cards, stage):
    """Enhanced display with hand probability breakdowns and strategic insights"""
    print("=" * 100)
    print(f"ENHANCED TEXAS HOLD'EM PREDICTOR - {stage.upper()} ANALYSIS")
    print("=" * 100)
    
    print(f"\nCurrent Game State:")
    print(f"{stage.upper()}: {' '.join([str(c) for c in community_cards])}")
    print(f"Players: {len(predictions)}")
    print(f"Method: {predictions[0].get('method', 'Exhaustive')}")
    print(f"Simulations: {predictions[0]['simulations']:,}")
    
    # Basic win probability table
    print("\n" + "=" * 100)
    print("WIN PROBABILITY RANKINGS")
    print("=" * 100)
    print("Player   Pocket       Current Hand       Win %      Tie %")
    print("-" * 100)
    
    for result in predictions:
        player = result['player']
        pocket_str = f"{result['pocket'][0]} {result['pocket'][1]}"
        
        # Get current hand name
        if len(community_cards) >= 3:
            current_rank = evaluate_hand(tuple(result['pocket'] + community_cards))
            current_name = get_hand_name(current_rank)
        else:
            current_name = "Pre-flop"
            
        win_pct = result['win_probability']
        tie_pct = result.get('tie_pct', 0)
        
        print(f"Player {player:<2} {pocket_str:<13} {current_name:<19} {win_pct:<8.2f}% {tie_pct:<6.2f}%")
    
    # Hand probability breakdowns
    print("\n" + "=" * 100)
    print("HAND PROBABILITY BREAKDOWNS (What each player might end up with)")
    print("=" * 100)
    
    # Show detailed breakdown for top 3 players and any interesting cases
    players_to_show = predictions[:3]  # Top 3
    
    for i, result in enumerate(players_to_show):
        player = result['player']
        pocket_str = f"{result['pocket'][0]} {result['pocket'][1]}"
        win_pct = result['win_probability']
        
        # Player category emoji
        if i == 0:
            emoji = "🏆"
            category = "LEADER"
        elif win_pct > 15:
            emoji = "🥈"
            category = "CONTENDER"
        elif win_pct > 5:
            emoji = "🎯"
            category = "DARK HORSE"
        else:
            emoji = "⚠️"
            category = "UNDERDOG"
            
        current_rank = evaluate_hand(tuple(result['pocket'] + community_cards))
        current_name = get_hand_name(current_rank)
        
        print(f"\n{emoji} PLAYER {player} ({pocket_str}) - Current: {current_name} [{category}]")
        print("-" * 70)
        print("Most Likely Final Hands:")
        
        # Get hand breakdown
        hand_breakdown = result.get('hand_breakdown', {})
        all_hand_types = result.get('all_hand_types', {})
        
        if all_hand_types:
            # Sort by frequency and show top 5
            sorted_hands = sorted(all_hand_types.items(), key=lambda x: x[1], reverse=True)
            total_sims = result['simulations']
            
            for hand_name, count in sorted_hands[:6]:  # Top 6 hand types
                percentage = (count / total_sims) * 100
                bar_length = int(percentage * 70 / 100)  # Scale to 70 chars max
                bar = "█" * bar_length + "▓"
                
                print(f"  {hand_name:<25} : {percentage:>6.2f}%  {bar}")
        else:
            print("  [Hand breakdown data not available]")
    
    # Strategic insights
    print("\n" + "=" * 100)
    print("KEY INSIGHTS & STRATEGY")
    print("=" * 100)
    
    leader = predictions[0]
    runner_up = predictions[1] if len(predictions) > 1 else None
    
    leader_name = f"Player {leader['player']}"
    leader_win = leader['win_probability']
    
    print(f"🔥 {leader_name} is the heavy favorite ({leader_win:.1f}% win rate)")
    
    if leader_win > 80:
        print(f"   • DOMINANT position - very difficult to overcome")
    elif leader_win > 60:
        print(f"   • STRONG favorite but others still have chances")
    elif leader_win > 40:
        print(f"   • SLIGHT favorite - competitive field")
    else:
        print(f"   • CLOSE race - anyone could win")
        
    if runner_up:
        gap = leader_win - runner_up['win_probability']
        runner_name = f"Player {runner_up['player']}"
        
        if gap > 50:
            print(f"\n💡 {runner_name} needs a miracle (gap: {gap:.1f}%)")
            print(f"   • Must hit premium draws to have a chance")
        elif gap > 20:
            print(f"\n💡 {runner_name} has an uphill battle (gap: {gap:.1f}%)")
            print(f"   • Needs strong improvement on turn/river")
        else:
            print(f"\n💡 {runner_name} is still very much in it (gap: {gap:.1f}%)")
            print(f"   • Could easily take the lead with right cards")
    
    # Cards to watch (simplified version)
    print(f"\n⚡ CARDS TO WATCH FOR:")
    remaining_deck = get_remaining_cards(community_cards, [p['pocket'] for p in predictions])
    
    # High impact cards (simplified)
    high_cards = ['A', 'K', 'Q', 'J', '10']
    remaining_high = [c for c in remaining_deck if str(c).startswith(tuple(high_cards))]
    
    if remaining_high:
        print(f"   • High cards: {', '.join([str(c) for c in remaining_high[:8]])}...")
        print(f"   • These could create straights, improve pairs, or change dynamics")
    
    print("\n" + "=" * 100)

def get_remaining_cards(community_cards, pocket_hands):
    """Get list of remaining cards in deck"""
    from card import create_deck
    used_cards = set(community_cards)
    for hand in pocket_hands:
        used_cards.update(hand)
    
    all_cards = create_deck()
    return [c for c in all_cards if c not in used_cards]

def explain_winning_hand_simple(winner, stage):
    """Explain why the winning hand is winning in simple terms a kid can understand"""
    print(f"\n{'='*70}")
    print("🎯 WHY IS THIS HAND WINNING? (Simple Explanation)")
    print(f"{'='*70}")

    current_hand = winner.get('current_hand')
    if not current_hand:
        print("Not enough cards yet to explain!")
        return

    hand_rank = current_hand[0]
    hand_name = get_hand_name(current_hand)
    win_pct = winner['win_probability']

    # Get simple explanation based on hand type
    explanations = {
        9: "🏆 ROYAL FLUSH - The BEST hand in poker! They have A-K-Q-J-10 all the same suit. Like finding a unicorn!",
        8: "🌊 STRAIGHT FLUSH - Five cards in a row, all the same suit. Super rare and super strong!",
        7: "4️⃣ FOUR OF A KIND - They have FOUR cards of the same number! Like having four Aces. Very hard to beat!",
        6: "🏠 FULL HOUSE - They have three of one card AND two of another. Like three Kings and two 5s. Really strong!",
        5: "💎 FLUSH - All five cards are the same suit (all hearts, all spades, etc). Pretty rare!",
        4: "📊 STRAIGHT - Five cards in a row (like 5-6-7-8-9). Doesn't matter what suit. Solid hand!",
        3: "3️⃣ THREE OF A KIND - They have three cards that match! Like three Queens. Good hand!",
        2: "👥 TWO PAIR - They have two pairs of matching cards. Like two 8s and two Kings. Decent!",
        1: "👫 ONE PAIR - They have two cards that match. Like two Jacks. Better than nothing!",
        0: "🎴 HIGH CARD - No matches yet, but they have the highest card. Weakest hand type."
    }

    explanation = explanations.get(hand_rank, "Unknown hand type")
    print(f"\n{explanation}")

    # Add context about winning chances
    print(f"\n💡 Why they're winning:")
    if win_pct > 90:
        print(f"   → They have a {win_pct:.1f}% chance to win!")
        print(f"   → That's like flipping a coin and getting heads 9 out of 10 times.")
        print(f"   → Their hand is MUCH better than everyone else's!")
    elif win_pct > 70:
        print(f"   → They have a {win_pct:.1f}% chance to win.")
        print(f"   → That's like getting a question right on a test most of the time.")
        print(f"   → Their hand is clearly the best right now!")
    elif win_pct > 50:
        print(f"   → They have a {win_pct:.1f}% chance to win.")
        print(f"   → That's like winning more than half the time if you played 100 games.")
        print(f"   → They're the favorite, but it's not guaranteed!")
    else:
        print(f"   → They have a {win_pct:.1f}% chance to win.")
        print(f"   → It's close! Other players have good hands too.")
        print(f"   → They're slightly ahead but need to be careful!")

    # Stage-specific advice
    if stage == "FLOP":
        print(f"\n📌 What's next:")
        print(f"   → Two more cards are coming (Turn and River)")
        print(f"   → Other players might catch up or fall behind")
        print(f"   → Stay tuned to see what happens!")
    else:  # TURN
        print(f"\n📌 What's next:")
        print(f"   → Only ONE more card is coming (the River)")
        likely = winner.get('most_likely_hand')
        if likely:
            print(f"   → They'll probably end with: {likely}")
        print(f"   → This is the final chance for anyone to improve!")

    print(f"{'='*70}")

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
