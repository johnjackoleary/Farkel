# Farkle Game Modernization Design

## Overview

Modernize the existing Python 2 Farkle game with:
- Python 3 compatibility
- ASCII art dice display
- Complete scoring rules
- Statistical advisor/coach feature
- Configurable AI opponent
- Polished terminal UI

## Project Structure

```
Farkel/
├── farkel/
│   ├── __init__.py
│   ├── dice.py          # Dice class with ASCII art rendering
│   ├── player.py        # Player and AIPlayer classes
│   ├── scoring.py       # All scoring logic
│   ├── advisor.py       # Statistical analysis and recommendations
│   ├── ui.py            # ASCII display functions
│   └── game.py          # Game loop and flow control
├── main.py              # Entry point
└── README.md
```

## ASCII Dice Display

Each die renders as a 3x5 character block:

```
┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐
│   │  │   │  │●  │  │● ●│  │● ●│  │● ●│
│ ● │  │● ●│  │ ● │  │   │  │ ● │  │● ●│
│   │  │   │  │  ●│  │● ●│  │● ●│  │● ●│
└───┘  └───┘  └───┘  └───┘  └───┘  └───┘
  1      2      3      4      5      6
```

During play, dice show their face values below for easy selection:

```
Your roll:
┌───┐  ┌───┐  ┌───┐  ┌───┐
│● ●│  │   │  │●  │  │● ●│
│   │  │ ● │  │ ● │  │ ● │
│● ●│  │   │  │  ●│  │● ●│
└───┘  └───┘  └───┘  └───┘
  4      1      3      5
```

## Scoring Rules

| Combination | Points |
|-------------|--------|
| Single 1 | 100 |
| Single 5 | 50 |
| Three 1s | 300 |
| Three 2s-6s | Face × 100 |
| Four of a kind | 1,000 |
| Five of a kind | 2,000 |
| Six of a kind | 3,000 |
| Straight (1-6) | 1,500 |
| Three pairs | 1,500 |
| Two triplets | 2,500 |
| Four + pair | 1,500 |

**Farkle:** Roll with no scoring dice = lose all points accumulated that turn.

**Hot Dice:** If all six dice are set aside as scoring dice, the player must roll all six again and continue.

**Win condition:** First to 10,000 points triggers final round; everyone gets one more turn, highest score wins.

## Advisor/Coach Feature

Players can type `?` before any decision to see statistical analysis:

```
═══ ADVISOR ═══════════════════════════════════════

  Option              │ Points │ Dice Left │ Farkle % │ EV if Roll
  ────────────────────┼────────┼───────────┼──────────┼───────────
  Keep three 1s       │    300 │     3     │    28%   │    495
  Keep 1, 1           │    200 │     4     │    23%   │    480
  Keep 1              │    100 │     5     │    19%   │    440
  Keep 1, 3, 3        │    400 │     3     │    28%   │    555
  Keep three 1s, 3, 3 │    600 │     1     │    67%   │    655

  ★ Best EV: Keep three 1s, 3, 3 → roll 1 die (expected: 655)

Game context:
  You: 1,250 │ Opponent: 2,400 │ Gap: -1,150
  Risk tolerance suggestion: Aggressive (roll)

════════════════════════════════════════════════════
```

Shows for each option:
- Points locked in
- Dice remaining to roll
- Probability of Farkle on next roll
- Expected value if rolling again (absolute total)
- Best option starred
- Game context and risk suggestion

## AI Opponent

Three difficulty levels selectable at game start:

**Easy (Risk-averse)**
- Banks after reaching 300+ points in a turn
- Always takes the highest-scoring dice combination
- Never pushes luck with fewer than 3 dice

**Medium (Balanced)**
- Uses simple expected value calculations
- Banks when turn total exceeds 400-500 or dice get risky
- Makes reasonable but not optimal choices

**Hard (Optimal)**
- Uses the same EV calculations the advisor shows
- Factors in game state (aggressive when behind, conservative when ahead)
- Plays statistically optimal

## Game Flow

### Main Menu

```
╔═══════════════════════════════════════╗
║            F A R K L E                ║
╚═══════════════════════════════════════╝

  1. Play vs Human
  2. Play vs AI
  3. Rules & Scoring
  4. Quit

Choice:
```

### During a Turn

```
══════════════════════════════════════════════════
 ROUND 3                        Turn total: 450
──────────────────────────────────────────────────
 You: 1,250          Partner: 2,400
══════════════════════════════════════════════════

Your roll:
┌───┐  ┌───┐  ┌───┐  ┌───┐
│● ●│  │   │  │●  │  │● ●│
│   │  │ ● │  │ ● │  │ ● │
│● ●│  │   │  │  ●│  │● ●│
└───┘  └───┘  └───┘  └───┘
  4      1      3      5

Set aside: 1, 1 (200 pts)

Select dice to keep (or ? for advice, b to bank):
```

### End of Round Summary

```
──────────────────────────────────────────────────
 Round 3 Complete
──────────────────────────────────────────────────
 You:      1,250  →  1,700  (+450)
 Partner:  2,400  →  2,400  (Farkle!)
──────────────────────────────────────────────────
```

## Input Commands

During play:
- `1 5` - keep dice by face value (e.g., keep a 1 and a 5)
- `1 1 1` - keep multiple of same value (e.g., keep three 1s)
- `?` - show advisor with statistics
- `b` or `bank` - bank points and end turn
- `r` or `rules` - show scoring rules
- `q` or `quit` - exit game

## Rules Screen

```
═══ FARKLE RULES ════════════════════════════════

GOAL: First to 10,000 points wins (final round for all)

SCORING:
  Single 1 ............. 100    Straight (1-6) .... 1,500
  Single 5 .............. 50    Three pairs ....... 1,500
  Three 1s ............. 300    Two triplets ...... 2,500
  Three 2s-6s ...... Face×100   Four + pair ....... 1,500
  Four of a kind ..... 1,000
  Five of a kind ..... 2,000
  Six of a kind ...... 3,000

FARKLE: Roll no scoring dice = lose turn's points

HOT DICE: Score all 6 dice = must roll all 6 again

Press Enter to continue...
═════════════════════════════════════════════════
```

## Error Handling

- Clear error messages: "Invalid selection - you only rolled one 1"
- Re-prompt without losing game state
- Confirm before quitting mid-game
