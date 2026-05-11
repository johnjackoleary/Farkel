from .scoring import all_scoring_subsets, score_dice
from .player import _farkle_probability, _avg_score

WIDTH = 52


def _ev(turn_total, dice_left, depth=4):
    """Expected value of continuing to roll from this state."""
    if depth == 0 or dice_left == 0:
        return turn_total
    fp = _farkle_probability(dice_left)
    gain = _avg_score(dice_left)
    return (1 - fp) * _ev(turn_total + gain, max(dice_left - 2, 1), depth - 1)


def decide(turn_score, pts, dice_left):
    """Recommend the better of banking now vs rolling after this keep.

    Returns (action, ev) where action is 'bank' or 'roll'. Hot dice
    (dice_left == 0) forces a re-roll per the game rules, so banking is
    not offered in that case.
    """
    bank_ev = turn_score + pts
    if dice_left == 0:
        return "roll", _ev(turn_score + pts, 6)
    roll_ev = _ev(turn_score + pts, dice_left)
    if bank_ev >= roll_ev:
        return "bank", bank_ev
    return "roll", roll_ev


def show_advice(rolled, turn_score):
    """Print the advisor table for a given roll and current turn score."""
    subsets = all_scoring_subsets(rolled)
    if not subsets:
        print("  (Farkle — no scoring options)")
        return

    rows = []
    for subset, pts in subsets.items():
        dice_left = len(rolled) - len(subset)
        action, ev = decide(turn_score, pts, dice_left)
        shown_left = 6 if dice_left == 0 else dice_left
        label = _subset_label(subset)
        rows.append((label, pts, shown_left, action, ev))

    rows.sort(key=lambda r: r[4], reverse=True)
    best_ev = rows[0][4]

    print()
    print("═" * WIDTH)
    print(" ADVISOR ".center(WIDTH, "═"))
    print("═" * WIDTH)
    header = f"  {'Option':<15} {'Pts':>5}  {'Left':>4}  {'Do':>4}  {'Fkl%':>4}  {'EV':>6}"
    print(header)
    print("  " + "─" * (WIDTH - 4))
    for label, pts, shown_left, action, ev in rows:
        star = "★" if ev == best_ev else " "
        if action == "bank":
            fp_str = "  — "
        else:
            fp_str = f"{_farkle_probability(shown_left)*100:>3.0f}%"
        print(f"  {star} {label:<14} {pts:>5}  {shown_left:>4}  {action:>4}  {fp_str:>4}  {ev:>6.0f}")
    print("═" * WIDTH)
    print()


def _subset_label(subset):
    from collections import Counter
    counts = Counter(subset)
    parts = []
    for face in sorted(counts):
        n = counts[face]
        if n == 1:
            parts.append(str(face))
        else:
            parts.append(f"{n}×{face}")
    return ", ".join(parts)
