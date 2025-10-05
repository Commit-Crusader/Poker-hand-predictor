# card.py - Card representation and parsing

class Card:
    """Represents a single playing card"""
    
    def __init__(self, value, suit):
        self.value = value  # 2-14 (14=Ace)
        self.suit = suit    # H/D/C/S
    
    def __repr__(self):
        value_names = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        display_value = value_names.get(self.value, str(self.value))
        return f"{display_value}{self.suit}"
    
    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.value, self.suit))

def parse_card(card_string):
    """Convert string like 'AH' or '10D' to Card object"""
    card_string = card_string.upper()
    
    # Minimum length check
    if len(card_string) < 2:
        raise ValueError("Card must have at least 2 characters (value + suit).")
    
    suit = card_string[-1]
    value_part = card_string[:-1]
    
    # Validate suit
    valid_suits = ['S', 'H', 'D', 'C']
    if suit not in valid_suits:
        raise ValueError(f"Invalid suit '{suit}'. Must be S, H, D, or C.")
    
    value_map = {'A': 14, 'K': 13, 'Q': 12, 'J': 11}
    
    # Check if it's a face card first, then convert to int
    if value_part in value_map:
        value = value_map[value_part]
    else:
        # Validate numeric rank
        try:
            value = int(value_part)
        except ValueError:
            raise ValueError(f"Invalid rank '{value_part}'. Must be 2-10, J, Q, K, or A.")
        
        # Check rank range (2-10 only for numeric cards)
        if value < 2 or value > 10:
            raise ValueError(f"Invalid rank '{value}'. Numeric ranks must be 2-10.")
    
    return Card(value, suit)

def create_deck():
    """Create a full 52-card deck"""
    return [Card(v, s) for v in range(2, 15) for s in ['H', 'D', 'C', 'S']]
