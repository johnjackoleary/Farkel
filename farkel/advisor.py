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


def show_advice(rolled, turn_score):
    """Print the advisor table for a given roll and current turn score."""
    subsets = all_scoring_subsets(rolled)
    if not subsets:
        print("  (Farkle — no scoring options)")
        return

    rows = []
    for subset, pts in subsets.items():
        dice_left = len(rolled) - len(subset)
        if dice_left == 0:
            dice_left = 6  # hot dice
        fp = _farkle_probability(dice_left)
        ev = _ev(turn_score + pts, dice_left)
        label = _subset_label(subset)
        rows.append((label, pts, dice_left, fp, ev, subset))

    rows.sort(key=lambda r: r[4], reverse=True)
    best_ev = rows[0][4]

    print()
    print("═" * WIDTH)
    print(" ADVISOR ".center(WIDTH, "═"))
    print("═" * WIDTH)
    header = f"  {'Option':<22} {'Pts':>5}  {'Left':>4}  {'Fkl%':>5}  {'EV':>6}"
    print(header)
    print("  " + "─" * (WIDTH - 4))
    for label, pts, dice_left, fp, ev, _ in rows:
        star = "★" if ev == best_ev else " "
        print(f"  {star} {label:<21} {pts:>5}  {dice_left:>4}  {fp*100:>4.0f}%  {ev:>6.0f}")
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
