#!/usr/bin/env python3
# poker_gui.py - GUI interface for poker predictor

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from card import parse_card, Card
from predictor import predict_hands_with_current
from evaluator import get_hand_name
from utils import print_header

# Color scheme - Refined poker theme
COLORS = {
    "background": "#0F172A",      # Deep navy blue
    "text": "#F8FAFC",            # Almost white
    "header": "#94A3B8",          # Gray blue
    "accent": "#3B82F6",          # Royal blue
    "accent_light": "#60A5FA",    # Lighter blue
    "button": "#2563EB",          # Vibrant blue
    "button_hover": "#1D4ED8",    # Darker blue for hover
    "card_bg": "#1E293B",         # Dark slate blue
    "card_border": "#475569",     # Medium blue-gray
    "win_high": "#10B981",        # Emerald green
    "win_medium": "#F59E0B",      # Amber
    "win_low": "#EF4444",         # Red
    "table": "#047857",           # Poker table green
    "table_border": "#065F46",    # Darker green border
    "suit_heart": "#EF4444",      # Red for hearts
    "suit_diamond": "#EF4444",    # Red for diamonds  
    "suit_club": "#1E293B",       # Black for clubs
    "suit_spade": "#1E293B",      # Black for spades
}

class PokerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Texas Hold'em Predictor")
        self.root.geometry("1000x750")
        self.root.configure(bg=COLORS["background"])
        self.root.minsize(900, 700)  # Set minimum window size
        
        # Load card suit symbols as class variables
        self.suits = {
            'H': '♥',  # Hearts
            'D': '♦',  # Diamonds
            'C': '♣',  # Clubs
            'S': '♠'   # Spades
        }
        
        self.style = ttk.Style()
        self._configure_styles()
        
        self.players = []
        self.community_cards = []
        self.current_stage = "Pre-Flop"  # Pre-Flop, Flop, Turn, River
        
        self._create_widgets()
        self._create_menu()
        
        # Apply theme to root window and all child widgets
        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=COLORS["background"])
            except:
                pass
    
    def _configure_styles(self):
        """Configure ttk styles"""
        # Configure default styles
        self.style.configure("TFrame", background=COLORS["background"])
        self.style.configure("TLabel", 
                             background=COLORS["background"], 
                             foreground=COLORS["text"],
                             font=("Segoe UI", 11))
        
        # Headers and titles
        self.style.configure("Header.TLabel", 
                             background=COLORS["background"], 
                             foreground=COLORS["header"],
                             font=("Segoe UI", 15, "bold"))
        self.style.configure("Title.TLabel", 
                             background=COLORS["background"], 
                             foreground=COLORS["accent"],
                             font=("Segoe UI", 24, "bold"))
        
        # Card styles                     
        self.style.configure("Card.TLabel", 
                             background=COLORS["card_bg"], 
                             foreground=COLORS["text"],
                             font=("Courier New", 14, "bold"),
                             borderwidth=2,
                             relief="raised")
        self.style.configure("CardHeart.TLabel", 
                             background=COLORS["card_bg"], 
                             foreground=COLORS["suit_heart"],
                             font=("Courier New", 14, "bold"))
        self.style.configure("CardDiamond.TLabel", 
                             background=COLORS["card_bg"], 
                             foreground=COLORS["suit_diamond"],
                             font=("Courier New", 14, "bold"))
                             
        # Table styling
        self.style.configure("Table.TFrame", 
                             background=COLORS["table"],
                             relief="raised",
                             borderwidth=3)
        self.style.configure("TableBorder.TFrame", 
                             background=COLORS["table_border"],
                             relief="raised",
                             borderwidth=1)
        
        # Entry field styling
        self.style.configure("TEntry", 
                             fieldbackground=COLORS["card_bg"],
                             foreground=COLORS["text"],
                             insertcolor=COLORS["text"],
                             bordercolor=COLORS["card_border"],
                             lightcolor=COLORS["card_border"],
                             darkcolor=COLORS["card_border"],
                             borderwidth=2,
                             font=("Segoe UI", 11))
        
        # Button styling
        self.style.configure("TButton", 
                             background=COLORS["button"],
                             foreground=COLORS["text"],
                             font=("Segoe UI", 11, "bold"),
                             relief="raised",
                             borderwidth=2)
        self.style.map("TButton",
                       background=[("active", COLORS["button_hover"]),
                                   ("pressed", COLORS["button_hover"])])
                                   
        # Primary action button
        self.style.configure("Primary.TButton", 
                             background=COLORS["accent"],
                             foreground=COLORS["text"],
                             font=("Segoe UI", 12, "bold"))
        self.style.map("Primary.TButton",
                       background=[("active", COLORS["accent_light"]),
                                  ("pressed", COLORS["accent_light"])])
                                  
        # Status message style
        self.style.configure("Status.TLabel",
                             font=("Segoe UI", 10, "italic"))
        
    def _create_widgets(self):
        """Create all GUI widgets"""
        # Main outer frame with padding
        outer_frame = ttk.Frame(self.root)
        outer_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title with poker icon
        title_frame = ttk.Frame(outer_frame)
        title_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Add poker icon and title in the same row
        title_text = "Texas Hold'em Predictor"
        poker_icons = "♠ ♥ ♣ ♦"
        
        title_label = ttk.Label(title_frame, text=title_text, style="Title.TLabel")
        title_label.pack(pady=(0, 5))
        
        # Subtitle with poker icons
        subtitle = ttk.Label(title_frame, text=poker_icons, 
                          font=("Arial", 22, "bold"), 
                          foreground=COLORS["accent"])
        subtitle.pack()
        
        # Create a poker table look for the main content
        table_border = ttk.Frame(outer_frame, style="TableBorder.TFrame")
        table_border.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        
        table_frame = ttk.Frame(table_border, style="Table.TFrame")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        main_frame = ttk.Frame(table_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Top section - Player inputs with card styling
        player_section = ttk.Frame(main_frame)
        player_section.pack(fill=tk.X, pady=10)
        
        ttk.Label(player_section, text="Player Cards", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 10))
        
        # Player inputs grid - 3x2 layout with better spacing
        players_grid = ttk.Frame(player_section)
        players_grid.pack(fill=tk.X)
        
        # Configure grid columns with equal width
        players_grid.columnconfigure(0, weight=1)
        players_grid.columnconfigure(1, weight=1)
        
        # Create styled input fields for 6 players
        self.player_entries = []
        for i in range(6):
            row = i // 2
            col = i % 2
            
            player_frame = ttk.Frame(players_grid)
            player_frame.grid(row=row, column=col, padx=15, pady=8, sticky=tk.W)
            
            # Player number with background
            player_label = ttk.Label(player_frame, 
                               text=f"Player {i+1}", 
                               background=COLORS["accent"],
                               foreground=COLORS["text"],
                               font=("Segoe UI", 11, "bold"))
            player_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky=tk.W)
            
            # Card entry with placeholder
            entry = ttk.Entry(player_frame, width=10)
            entry.grid(row=0, column=1, padx=5, pady=5)
            self.player_entries.append(entry)
            
            # Add placeholder text
            entry.insert(0, "AS KH")
            entry.bind("<FocusIn>", lambda e, i=i: self._clear_placeholder(e, i))
            
            # Add card icon
            card_icon = ttk.Label(player_frame, text="🃏", font=("Segoe UI", 14))
            card_icon.grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Middle section - Community cards with card visuals
        community_section = ttk.Frame(main_frame)
        community_section.pack(fill=tk.X, pady=10)
        
        ttk.Label(community_section, text="Community Cards", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 10))
        
        # Create visual representation of poker table center
        table_center = ttk.Frame(community_section, style="Table.TFrame")
        table_center.pack(fill=tk.X, pady=10, padx=20, ipady=10)
        
        cc_input_frame = ttk.Frame(table_center)
        cc_input_frame.pack(padx=10, pady=10)
        
        # Create flop entries with card styling
        flop_label = ttk.Label(cc_input_frame, text="Flop:", font=("Segoe UI", 12, "bold"), foreground=COLORS["text"])
        flop_label.grid(row=0, column=0, padx=(0, 10), pady=5)
        
        self.flop_entries = []
        for i in range(3):
            entry = ttk.Entry(cc_input_frame, width=4)
            entry.grid(row=0, column=i+1, padx=8, pady=5)
            self.flop_entries.append(entry)
        
        turn_label = ttk.Label(cc_input_frame, text="Turn:", font=("Segoe UI", 12, "bold"), foreground=COLORS["text"])
        turn_label.grid(row=0, column=4, padx=(20, 10), pady=5)
        
        self.turn_entry = ttk.Entry(cc_input_frame, width=4)
        self.turn_entry.grid(row=0, column=5, padx=8, pady=5)
        
        river_label = ttk.Label(cc_input_frame, text="River:", font=("Segoe UI", 12, "bold"), foreground=COLORS["text"])
        river_label.grid(row=0, column=6, padx=(20, 10), pady=5)
        
        self.river_entry = ttk.Entry(cc_input_frame, width=4)
        self.river_entry.grid(row=0, column=7, padx=8, pady=5)
        
        # Add hint text below
        hint_text = "Card format: AH (Ace of Hearts), 10D (Ten of Diamonds), JS (Jack of Spades), etc."
        hint_label = ttk.Label(community_section, text=hint_text, font=("Segoe UI", 9, "italic"))
        hint_label.pack(pady=(10, 0))
        
        # Separator before action area
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=15)
        
        # Action area with prominent buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        # Add a container for buttons to center them
        button_container = ttk.Frame(action_frame)
        button_container.pack(pady=5)
        
        self.calculate_button = ttk.Button(
            button_container, 
            text="Calculate Odds", 
            command=self.calculate_odds,
            style="Primary.TButton",
            width=20
        )
        self.calculate_button.grid(row=0, column=0, padx=10)
        
        self.clear_button = ttk.Button(
            button_container, 
            text="Clear All", 
            command=self.clear_all,
            width=15
        )
        self.clear_button.grid(row=0, column=1, padx=10)
        
        # Status indicator
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar()
        self.status_var.set("Enter player cards to begin")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, style="Status.TLabel")
        self.status_label.pack(anchor=tk.W)
        
        # Results section with better styling
        results_section = ttk.Frame(main_frame)
        results_section.pack(fill=tk.BOTH, expand=True, pady=(15, 0))
        
        results_header = ttk.Frame(results_section)
        results_header.pack(fill=tk.X)
        
        ttk.Label(results_header, text="Results", style="Header.TLabel").pack(side=tk.LEFT)
        
        # Create a styled results view
        results_container = ttk.Frame(results_section, style="TableBorder.TFrame")
        results_container.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.results_text = scrolledtext.ScrolledText(
            results_container, 
            height=12, 
            bg=COLORS["card_bg"], 
            fg=COLORS["text"], 
            wrap=tk.WORD,
            borderwidth=0,
            font=("Consolas", 11)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.results_text.configure(state=tk.DISABLED)
    
    def _create_menu(self):
        """Create the application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear All", command=self.clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Card Format", command=self.show_card_format_help)
        help_menu.add_command(label="About", command=self.show_about)
    
    def show_card_format_help(self):
        """Show help for card formats"""
        messagebox.showinfo(
            "Card Format Help",
            "Cards should be entered in the following format:\n\n"
            "- Value: 2-10, J, Q, K, or A\n"
            "- Suit: H (Hearts), D (Diamonds), C (Clubs), S (Spades)\n\n"
            "Examples:\n"
            "- AH = Ace of Hearts\n"
            "- 10D = Ten of Diamonds\n"
            "- JS = Jack of Spades\n"
            "- 2C = Two of Clubs\n\n"
            "For player cards, enter two cards separated by a space (e.g., 'AS KH')"
        )
    
    def show_about(self):
        """Show about dialog with styled HTML-like content"""
        about_text = (
            "♠ ♥ ♣ ♦   Texas Hold'em Predictor   ♠ ♥ ♣ ♦\n\n"
            "An advanced poker analysis tool for calculating\n"
            "precise win probabilities in Texas Hold'em poker.\n\n"
            "Features:\n"
            "• Calculates exact win probabilities using exhaustive simulation\n"
            "• Supports up to 6 players with precise hand evaluation\n"
            "• Shows current best hand for each player at any stage\n"
            "• Handles split pot scenarios with fractional win percentages\n"
            "• Identifies optimal plays based on mathematical probabilities\n\n"
            "© 2025 Poker Analytics Project"
        )
        
        messagebox.showinfo("About Texas Hold'em Predictor", about_text)
    
    def clear_all(self):
        """Clear all inputs"""
        for entry in self.player_entries:
            entry.delete(0, tk.END)
        
        for entry in self.flop_entries:
            entry.delete(0, tk.END)
        
        self.turn_entry.delete(0, tk.END)
        self.river_entry.delete(0, tk.END)
        
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.configure(state=tk.DISABLED)
        
        self.status_var.set("Enter player cards to begin")
        self.current_stage = "Pre-Flop"
    
    def get_win_color(self, probability):
        """Get color based on win probability"""
        if probability > 50:
            return COLORS["win_high"]
        elif probability > 20:
            return COLORS["win_medium"]
        else:
            return COLORS["win_low"]
    
    def parse_player_cards(self):
        """Parse all player cards from entry fields"""
        players = []
        used_cards = set()
        
        for i, entry in enumerate(self.player_entries):
            try:
                card_str = entry.get().strip()
                if not card_str:  # Skip empty entries
                    continue
                
                card_parts = card_str.split()
                if len(card_parts) != 2:
                    self.status_var.set(f"Error: Player {i+1} needs exactly 2 cards")
                    return None, None
                
                pocket = []
                for card_text in card_parts:
                    try:
                        card = parse_card(card_text)
                        if card in used_cards:
                            self.status_var.set(f"Error: Duplicate card {card} for Player {i+1}")
                            return None, None
                        pocket.append(card)
                        used_cards.add(card)
                    except ValueError as e:
                        self.status_var.set(f"Error: Invalid card format '{card_text}' for Player {i+1}")
                        return None, None
                
                players.append(pocket)
                
            except Exception as e:
                self.status_var.set(f"Error parsing cards for Player {i+1}: {str(e)}")
                return None, None
        
        if not players:
            self.status_var.set("Error: At least one player is required")
            return None, None
        
        return players, used_cards
    
    def parse_community_cards(self, used_cards):
        """Parse community cards from entry fields"""
        community_cards = []
        
        # Parse flop cards
        for i, entry in enumerate(self.flop_entries):
            card_str = entry.get().strip()
            if card_str:
                try:
                    card = parse_card(card_str)
                    if card in used_cards:
                        self.status_var.set(f"Error: Duplicate card {card} in flop")
                        return None
                    community_cards.append(card)
                    used_cards.add(card)
                except ValueError:
                    self.status_var.set(f"Error: Invalid flop card format: {card_str}")
                    return None
        
        # Parse turn card if provided
        turn_str = self.turn_entry.get().strip()
        if turn_str:
            if len(community_cards) < 3:
                self.status_var.set("Error: Can't have turn card without complete flop")
                return None
            
            try:
                turn_card = parse_card(turn_str)
                if turn_card in used_cards:
                    self.status_var.set(f"Error: Duplicate card {turn_card} for turn")
                    return None
                community_cards.append(turn_card)
                used_cards.add(turn_card)
            except ValueError:
                self.status_var.set(f"Error: Invalid turn card format: {turn_str}")
                return None
        
        # Parse river card if provided
        river_str = self.river_entry.get().strip()
        if river_str:
            if len(community_cards) < 4:
                self.status_var.set("Error: Can't have river card without turn card")
                return None
            
            try:
                river_card = parse_card(river_str)
                if river_card in used_cards:
                    self.status_var.set(f"Error: Duplicate card {river_card} for river")
                    return None
                community_cards.append(river_card)
                used_cards.add(river_card)
            except ValueError:
                self.status_var.set(f"Error: Invalid river card format: {river_str}")
                return None
        
        return community_cards
    
    def calculate_odds(self):
        """Calculate odds for the current poker situation"""
        # Disable calculate button during calculation
        self.calculate_button.configure(state=tk.DISABLED)
        self.status_var.set("Calculating probabilities...")
        self.root.update()
        
        # Run calculation in a separate thread to keep UI responsive
        threading.Thread(target=self._perform_calculation, daemon=True).start()
    
    def _perform_calculation(self):
        """Perform the actual calculation in a separate thread"""
        try:
            # Parse player cards
            pocket_hands, used_cards = self.parse_player_cards()
            if not pocket_hands:
                self._calculation_done()
                return
            
            # Parse community cards
            community_cards = self.parse_community_cards(used_cards.copy())
            if community_cards is None:
                self._calculation_done()
                return
            
            # Determine current stage
            if len(community_cards) == 0:
                stage = "Pre-Flop"
            elif len(community_cards) == 3:
                stage = "Flop"
            elif len(community_cards) == 4:
                stage = "Turn"
            elif len(community_cards) == 5:
                stage = "River"
            else:
                self.status_var.set(f"Error: Invalid number of community cards: {len(community_cards)}")
                self._calculation_done()
                return
            
            # Calculate odds
            predictions = predict_hands_with_current(community_cards, pocket_hands)
            
            # Display results
            self.display_results(predictions, community_cards, stage)
            
        except Exception as e:
            self.status_var.set(f"Error during calculation: {str(e)}")
        
        self._calculation_done()
    
    def _calculation_done(self):
        """Re-enable calculate button when calculation is done"""
        self.calculate_button.configure(state=tk.NORMAL)
    
    def display_results(self, predictions, community_cards, stage):
        """Display calculation results in the results area with enhanced styling"""
        # Enable text widget for updating
        self.results_text.configure(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        # Display stage banner with color
        stage_color = {
            "Pre-Flop": "#2563EB",
            "Flop": "#2563EB", 
            "Turn": "#9333EA", 
            "River": "#10B981"
        }.get(stage, "#2563EB")
        
        self.results_text.insert(tk.END, f"\n  POKER ANALYSIS: {stage.upper()} STAGE\n\n", "stage_banner")
        
        # Display community cards with suit symbols
        if community_cards:
            cc_display = ""
            for card in community_cards:
                card_str = str(card)
                value = card_str[:-1]
                suit = card_str[-1]
                
                # Map suit letter to symbol and add with appropriate color tag
                suit_symbol = self.suits.get(suit, suit)
                cc_display += f"{value}{suit_symbol} "
                
            self.results_text.insert(tk.END, f"  COMMUNITY: {cc_display}\n\n", "community")
        else:
            self.results_text.insert(tk.END, "  COMMUNITY: None yet\n\n", "community")
        
        # Create a table-like header with background
        header = f"  {'PLAYER':<8} {'POCKET':<14} {'CURRENT HAND':<22} {'WIN %':<10} {'SIMS':<10}\n"
        self.results_text.insert(tk.END, header, "table_header")
        
        # Create a divider
        self.results_text.insert(tk.END, "  " + "─" * 65 + "\n", "divider")
        
        # Display results for each player with colorized win probabilities
        for i, result in enumerate(predictions):
            # Format pocket cards with suit symbols
            pocket_display = ""
            for card in result['pocket']:
                card_str = str(card)
                value = card_str[:-1]
                suit = card_str[-1]
                suit_symbol = self.suits.get(suit, suit)
                pocket_display += f"{value}{suit_symbol} "
            
            # Get current hand name
            if result['current_hand']:
                hand_name = get_hand_name(result['current_hand'])
            else:
                hand_name = "Waiting for cards"
            
            # Format win probability with appropriate color
            win_prob = result['win_probability']
            win_str = f"{win_prob:.2f}%"
            
            # Format player number
            player_num = f"Player {result['player']}"
            
            # Build the line
            player_line = f"  {player_num:<8} {pocket_display:<14} {hand_name:<22} "
            self.results_text.insert(tk.END, player_line)
            
            # Insert win probability with color based on value
            if win_prob > 50:
                self.results_text.insert(tk.END, f"{win_str:<10}", "win_high")
            elif win_prob > 20:
                self.results_text.insert(tk.END, f"{win_str:<10}", "win_medium")
            else:
                self.results_text.insert(tk.END, f"{win_str:<10}", "win_low")
            
            # Add simulations count
            sims_str = f"{result['simulations']:,}"
            self.results_text.insert(tk.END, f"{sims_str:<10}\n", "normal")
            
            # Add alternating row background
            row_tag = f"row_{i}"
            row_start = f"{i+3}.0"  # +3 for header lines
            row_end = f"{i+4}.0"
            if i % 2 == 0:
                self.results_text.tag_add(row_tag, row_start, row_end)
                self.results_text.tag_configure(row_tag, background="#1E293B")
        
        # Add simulation summary with separator
        self.results_text.insert(tk.END, "\n  " + "─" * 65 + "\n", "divider")
        self.results_text.insert(tk.END, f"  Total simulations run: {predictions[0]['simulations']:,}\n", "info")
        
        # Configure text tags with improved styling
        self.results_text.tag_configure("stage_banner", 
                                        foreground=COLORS["text"], 
                                        background=stage_color,
                                        font=("Segoe UI", 13, "bold"),
                                        justify="center")
        
        self.results_text.tag_configure("community", 
                                        foreground=COLORS["accent_light"],
                                        font=("Consolas", 12, "bold"))
        
        self.results_text.tag_configure("table_header", 
                                        foreground=COLORS["text"],
                                        background=COLORS["accent"],
                                        font=("Consolas", 11, "bold"))
        
        self.results_text.tag_configure("divider", foreground=COLORS["header"])
        self.results_text.tag_configure("normal", foreground=COLORS["text"])
        self.results_text.tag_configure("info", 
                                        foreground=COLORS["header"],
                                        font=("Consolas", 11, "italic"))
        
        # Configure win probability colors
        self.results_text.tag_configure("win_high", 
                                        foreground=COLORS["win_high"],
                                        font=("Consolas", 11, "bold"))
        self.results_text.tag_configure("win_medium", 
                                        foreground=COLORS["win_medium"],
                                        font=("Consolas", 11, "bold"))
        self.results_text.tag_configure("win_low", 
                                        foreground=COLORS["win_low"],
                                        font=("Consolas", 11, "bold"))
        
        # Disable text widget to prevent editing
        self.results_text.configure(state=tk.DISABLED)
        
        # Update status with more detailed message
        self.status_var.set(f"Calculation complete for {stage} stage with {len(predictions)} players")
    
    def _clear_placeholder(self, event, player_index):
        """Clear placeholder text when input field gets focus"""
        if self.player_entries[player_index].get() == "AS KH":
            self.player_entries[player_index].delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerGUI(root)
    root.mainloop()
