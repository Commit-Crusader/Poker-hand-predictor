# sample_hand_breakdown.py - Demo of enhanced output with hand probability breakdowns

def show_sample_output():
    print("=" * 100)
    print("ENHANCED TEXAS HOLD'EM PREDICTOR - SAMPLE OUTPUT")
    print("=" * 100)
    
    print("\nCurrent Game State:")
    print("FLOP: AC 5H 9D")
    print("Players: 6")
    print("Method: Exhaustive (0.34 seconds)")
    print("\n" + "=" * 100)
    print("WIN PROBABILITY RANKINGS")
    print("=" * 100)
    print("Player   Pocket       Current Hand       Win %      Simulations")
    print("-" * 100)
    print("Player 1 AS AH        Three of a Kind    94.59%     666        ")
    print("Player 6 7D 2C        High Card          4.95%      666        ")
    print("Player 3 QS QH        Pair               0.30%      666        ")
    print("Player 2 KS KH        Pair               0.15%      666        ")
    print("Player 5 10S 10H      Pair               0.00%      666        ")
    print("Player 4 JS JH        Pair               0.00%      666        ")
    
    print("\n" + "=" * 100)
    print("HAND PROBABILITY BREAKDOWNS (What each player might end up with)")
    print("=" * 100)
    
    # Player 1 - Strong hand
    print("\n🏆 PLAYER 1 (AS AH) - Current: Three of a Kind Aces")
    print("-" * 60)
    print("Most Likely Final Hands:")
    print("  Full House (Aces full)     : 18.92%  ██████████████████▓")
    print("  Four of a Kind (Aces)      : 4.50%   ████▓")
    print("  Three of a Kind (Aces)     : 71.17%  ███████████████████████████████████████████████████████████████████████▓")
    print("  Two Pair (Aces over)       : 5.41%   █████▓")
    print("  Other                      : 0.00%   ▓")
    
    # Player 2 - Decent pocket pair
    print("\n🥈 PLAYER 2 (KS KH) - Current: Pair of Kings")  
    print("-" * 60)
    print("Most Likely Final Hands:")
    print("  Two Pair (Kings over)       : 41.44%  █████████████████████████████████████████▓")
    print("  Pair (Kings)               : 31.53%   ███████████████████████████████▓")
    print("  Three of a Kind (Kings)    : 4.50%   ████▓")
    print("  Full House (Kings full)    : 1.80%   █▓")
    print("  Straight                   : 16.22%  ████████████████▓")
    print("  Four of a Kind (Kings)     : 0.45%   ▓")
    print("  Other                      : 4.05%   ████▓")
    
    # Player 6 - Weak hand with potential
    print("\n🎯 PLAYER 6 (7D 2C) - Current: Ace High")
    print("-" * 60) 
    print("Most Likely Final Hands:")
    print("  High Card (Ace high)       : 67.12%  ███████████████████████████████████████████████████████████████████▓")
    print("  Pair (Any pair)            : 28.83%  ████████████████████████████▓")
    print("  Two Pair                   : 3.60%   ███▓")
    print("  Straight                   : 0.45%   ▓")
    print("  Other                      : 0.00%   ▓")
    
    print("\n" + "=" * 100)
    print("KEY INSIGHTS")
    print("=" * 100)
    print("🔥 Player 1 is HEAVILY favored with trip Aces")
    print("   • 18.92% chance of Full House (nearly unbeatable)")
    print("   • 4.50% chance of Four Aces (absolute nuts)")
    print("   • Even with just trips, beats almost everything")
    
    print("\n💡 Player 2 has decent survival chances")
    print("   • 16.22% chance of straight (8-Q or 10-A)")
    print("   • Needs to hit trips/full house to beat Player 1")
    
    print("\n⚠️  Players 3-5 are in danger")
    print("   • All have pocket pairs but Player 1's trips dominate")
    print("   • Need to hit sets (trips) to have fighting chance")
    
    print("\n🎲 Player 6 is the dark horse")
    print("   • Surprising 4.95% win rate despite weak starting hand")
    print("   • Could hit miracle straight or two pair")
    
    print("\n" + "=" * 100)
    print("TURN & RIVER CARDS TO WATCH")
    print("=" * 100)
    print("🚨 DANGER CARDS for Player 1:")
    print("   • Any 5 or 9 (gives others trips)")
    print("   • Q, J, 10, 8 (straight possibilities)")
    
    print("\n🎯 DREAM CARDS for Player 1:")
    print("   • Another Ace (four of a kind - 99.9% win)")
    print("   • Any pair (5,5 or 9,9 - gives full house)")
    
    print("\n⚡ COMEBACK CARDS for others:")
    print("   • K, Q, J, 10, 8, 6 (straight draws)")
    print("   • Matching their pocket pairs (sets)")
    
    print("\n" + "=" * 100)

if __name__ == "__main__":
    show_sample_output()