from collections import Counter
from itertools import combinations


SCORE_TABLE = {
    "single_1":     100,
    "single_5":     50,
    "three_1s":     300,
    "three_of":     lambda face: face * 100,  # face 2-6
    "four_of":      1000,
    "five_of":      2000,
    "six_of":       3000,
    "straight":     1500,
    "three_pairs":  1500,
    "two_triplets": 2500,
    "four_pair":    1500,
}


def score_dice(dice):
    """Return the score for a given list of die face values (1-6)."""
    if not dice:
        return 0
    counts = Counter(dice)
    return _score_counts(counts)


def _score_counts(counts):
    values = sorted(counts.keys())
    total_dice = sum(counts.values())

    # --- Six-dice combos (only valid when all 6 dice used) ---
    if total_dice == 6:
        # Straight 1-2-3-4-5-6
        if set(values) == {1, 2, 3, 4, 5, 6}:
            return SCORE_TABLE["straight"]

        # Three pairs
        if len(values) == 3 and all(counts[v] == 2 for v in values):
            return SCORE_TABLE["three_pairs"]

        # Two triplets
        if len(values) == 2 and all(counts[v] == 3 for v in values):
            return SCORE_TABLE["two_triplets"]

        # Four of a kind + a pair
        for v in values:
            if counts[v] == 4:
                others = [x for x in values if x != v]
                if len(others) == 1 and counts[others[0]] == 2:
                    return SCORE_TABLE["four_pair"]

    score = 0
    remaining = dict(counts)

    for face in sorted(remaining.keys()):
        n = remaining[face]
        if n >= 6:
            score += SCORE_TABLE["six_of"]
            remaining[face] = 0
            continue
        if n >= 5:
            score += SCORE_TABLE["five_of"]
            remaining[face] -= 5
            n = remaining[face]
        if n >= 4:
            score += SCORE_TABLE["four_of"]
            remaining[face] -= 4
            n = remaining[face]
        if n >= 3:
            if face == 1:
                score += SCORE_TABLE["three_1s"]
            else:
                score += SCORE_TABLE["three_of"](face)
            remaining[face] -= 3
            n = remaining[face]
        if face == 1:
            score += n * SCORE_TABLE["single_1"]
        elif face == 5:
            score += n * SCORE_TABLE["single_5"]

    return score


def all_scoring_subsets(dice):
    """
    Return all unique subsets of dice (as sorted tuples) that score > 0,
    along with their scores. Each subset must keep only scorable dice.
    """
    results = {}
    for size in range(1, len(dice) + 1):
        for combo in combinations(range(len(dice)), size):
            subset = tuple(sorted(dice[i] for i in combo))
            if subset in results:
                continue
            s = score_dice(list(subset))
            if s > 0:
                results[subset] = s
    return results  # {subset_tuple: score}


def is_farkle(dice):
    """True if no subset of dice scores."""
    return len(all_scoring_subsets(dice)) == 0


def validate_selection(rolled, chosen):
    """
    Check that `chosen` is a legal scorable selection from `rolled`.
    Both are lists of face values (may contain duplicates).
    Returns (valid: bool, reason: str).
    """
    if not chosen:
        return False, "You must choose at least one die."

    rolled_counts = Counter(rolled)
    chosen_counts = Counter(chosen)

    for face, n in chosen_counts.items():
        if n > rolled_counts.get(face, 0):
            return False, f"You only rolled {rolled_counts.get(face, 0)} die/dice showing {face}."

    if score_dice(list(chosen)) == 0:
        return False, "That selection scores zero points — choose scoring dice."

    return True, ""
