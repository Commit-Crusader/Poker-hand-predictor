# 🃏 Texas Hold'em Hand Predictor

A powerful Python-based poker hand prediction tool that calculates real-time win probabilities for 6 players in Texas Hold'em poker. Perfect for analyzing poker games and understanding probability distributions at each betting round.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🌟 Features

- **Real-time Probability Calculations** - Get exact win percentages after Flop and Turn
- **6-Player Support** - Analyze games with exactly 6 players
- **Tie Handling** - Accurate fractional win calculations for split pots
- **Optimized Performance** - LRU caching for lightning-fast hand evaluations
- **Proper Hand Ranking** - Complete tie-breaking logic following Texas Hold'em rules
- **Interactive CLI** - Clean, user-friendly command-line interface
- **Auto-Loop** - Continuous gameplay mode with 20-second intervals
- **Web Scraper** - Experimental scraper for SportyBet Poker (manual mode)
- **Comprehensive Testing** - 33+ test cases covering all poker scenarios

## 🎯 How It Works

The predictor uses **exhaustive simulation** to calculate exact probabilities:
- **After Flop (3 cards)**: Tests all possible Turn + River combinations (~1,000 simulations)
- **After Turn (4 cards)**: Tests all possible River cards (~40-50 simulations)

Results are displayed instantly with current hand rankings and win percentages for each player.

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Testing](#testing)
- [Web Scraper](#web-scraper)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Basic Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/poker-hand-predictor.git
cd poker-hand-predictor

# No external dependencies needed for basic CLI!
# Uses only Python standard library
```

### Optional: Web Scraper Setup

For the SportyBet poker scraper (optional):

```bash
# Install Playwright
pip install playwright
playwright install chromium
```

## 💻 Usage

### Running the Predictor

```bash
python main.py
```

### Step-by-Step Flow

1. **Enter Pocket Cards** for all 6 players
   ```
   Player 1 (e.g., AS KC):
   > AS AH
   Player 2 (e.g., AS KC):
   > KD KH
   ...
   ```

2. **Enter Flop Cards** (one at a time)
   ```
   FLOP Card 1:
   > AC
   FLOP Card 2:
   > 5H
   FLOP Card 3:
   > 9D
   ```

3. **View Flop Predictions**
   ```
   ================================================================================
   Stage: FLOP
   Community Cards: [AC, 5H, 9D]
   ================================================================================
   Player   Pocket       Current Hand       Win %      Sims      
   --------------------------------------------------------------------------------
   Player 1 AS AH        Three of a Kind    85.23%     1,081     
   Player 2 KD KH        Pair               8.45%      1,081     
   ...
   ```

4. **Enter Turn Card**
   ```
   Enter the TURN card (e.g., 10C):
   > AD
   ```

5. **View Turn Predictions** and results

6. **Auto-restart** - Game automatically restarts after 20 seconds

### Card Format

Cards use the format: **Value + Suit**

**Values:** `2-10`, `J` (Jack), `Q` (Queen), `K` (King), `A` (Ace)  
**Suits:** `S` (Spades), `H` (Hearts), `D` (Diamonds), `C` (Clubs)

**Examples:**
- `AS` = Ace of Spades
- `10H` = 10 of Hearts
- `KD` = King of Diamonds
- `2C` = 2 of Clubs

## 📁 Project Structure

```
poker_predictor/
│
├── main.py                      # Entry point
├── game.py                      # Game flow and user interaction
├── card.py                      # Card class and deck creation
├── evaluator.py                 # Hand evaluation and ranking
├── predictor.py                 # Win probability calculator
├── utils.py                     # Display formatting utilities
├── test_evaluator.py            # Comprehensive test suite
├── sportybet_poker_scraper.py   # Web scraper for SportyBet (optional)
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `main.py` | Entry point - launches the game |
| `game.py` | Manages game flow, user input, and loop control |
| `card.py` | Card representation and deck management |
| `evaluator.py` | Hand ranking with proper tie-breaking |
| `predictor.py` | Probability calculations and simulations |
| `utils.py` | Display formatting and output utilities |
| `test_evaluator.py` | Unit tests for hand evaluation |

## 🔧 Technical Details

### Algorithm

- **Exhaustive Simulation**: Tests every possible future card combination (not Monte Carlo)
- **Exact Probabilities**: Calculates true mathematical odds
- **Tie-Breaking**: Proper kicker evaluation following official Texas Hold'em rules

### Performance

- **LRU Cache**: Hand evaluations are cached for repeated combinations
- **Flop Calculations**: ~1,000 simulations (instant)
- **Turn Calculations**: ~40-50 simulations (instant)

### Hand Rankings

From highest to lowest:

1. **Royal Flush** - A♥ K♥ Q♥ J♥ 10♥
2. **Straight Flush** - Five consecutive cards, same suit
3. **Four of a Kind** - Four cards of same rank
4. **Full House** - Three of a kind + Pair
5. **Flush** - Five cards of same suit
6. **Straight** - Five consecutive cards
7. **Three of a Kind** - Three cards of same rank
8. **Two Pair** - Two different pairs
9. **Pair** - Two cards of same rank
10. **High Card** - Highest card wins

### Code Quality

- **Modular Design**: Separated concerns across multiple files
- **Docstrings**: All functions documented
- **Input Validation**: Robust error handling and sanitization
- **Uniqueness Checks**: Prevents duplicate cards
- **Type Safety**: Ready for type hints

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_evaluator.py
```

**Test Coverage:**
- 33+ test cases
- All hand rankings tested
- Tie-breaker scenarios
- Edge cases (wheel straight, ace-low, etc.)

**Expected Output:**
```
================================================================================
POKER HAND EVALUATOR TEST HARNESS
================================================================================
✓ PASS | Royal Flush vs Straight Flush
✓ PASS | Straight Flush vs Four of a Kind
...
================================================================================
RESULTS: 33 passed, 0 failed out of 33 tests
✓ ALL TESTS PASSED! Your evaluator is working correctly.
================================================================================
```

## 🌐 Web Scraper

**Experimental feature** for scraping live poker games from SportyBet.

### Manual Mode (Recommended)

```bash
python sportybet_poker_scraper.py
```

1. Browser opens to SportyBet
2. Login and navigate to poker game
3. Manually enter cards when prompted
4. Predictor runs automatically
5. Results displayed
6. Auto-loops for next game

### Features

- Screenshot capture for reference
- Automatic data feeding to predictor
- 20-second auto-restart
- Validation and error handling

## 📊 Examples

### Example Output

```
================================================================================
Stage: TURN
Community Cards: [AC, 5H, 9D, AD]
================================================================================
Player   Pocket       Current Hand       Win %      Sims      
--------------------------------------------------------------------------------
Player 1 AS AH        Four of a Kind     97.73%     44        
Player 2 KD KH        Two Pair           0.00%      44        
Player 3 QS QC        Two Pair           0.00%      44        
Player 4 JD JH        Two Pair           0.00%      44        
Player 5 10S 10C      Full House         2.27%      44        
Player 6 7D 2H        Pair               0.00%      44        
================================================================================
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Ideas for Contribution

- [ ] Add pre-flop probability calculations (with optimization)
- [ ] Implement Monte Carlo sampling option
- [ ] Create GUI version with card visuals
- [ ] Add hand strength indicators
- [ ] Export results to CSV/JSON
- [ ] Multi-table tournament mode
- [ ] Improve web scraper with OCR
- [ ] Add more poker site scrapers

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python's standard library (no external dependencies for core functionality)
- Inspired by the need for accurate poker probability analysis
- Designed as a learning tool for understanding poker mathematics

## 📧 Contact

Your Name - [@Commit-Crusader](https://github.com/Commit-Crusader)

Project Link: [https://github.com/Commit-Crusader/poker-hand-predictor](https://github.com/Commit-Crusader/poker-hand-predictor)

---

**⭐ If you found this project helpful, please give it a star!**

---

## 🎓 Educational Use

This tool is designed for:
- Learning poker probability theory
- Understanding hand rankings and tie-breakers
- Analyzing poker strategy
- Educational purposes only

**Not intended for:**
- Real-money gambling
- Cheating in online poker
- Violating poker site terms of service

---

Made with ❤️ and Python
