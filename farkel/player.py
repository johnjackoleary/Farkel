from .scoring import score_dice, all_scoring_subsets, is_farkle


class Player:
    def __init__(self, name):
        self.name = name
        self.total_score = 0
        self.is_ai = False

    def choose_keep(self, rolled, turn_score, all_scores):
        """Human players return None — input is handled by the game loop."""
        return None


class AIPlayer(Player):
    DIFFICULTY_EASY   = "easy"
    DIFFICULTY_MEDIUM = "medium"
    DIFFICULTY_HARD   = "hard"

    def __init__(self, name, difficulty=DIFFICULTY_MEDIUM):
        super().__init__(name)
        self.difficulty = difficulty
        self.is_ai = True

    def choose_keep(self, rolled, turn_score, all_scores):
        """
        Return (chosen_faces, should_bank).
        chosen_faces: list of die face values to set aside.
        should_bank: True if the AI wants to bank after keeping.
        """
        subsets = all_scoring_subsets(rolled)
        if not subsets:
            return [], False  # Farkle — no choice

        if self.difficulty == self.DIFFICULTY_EASY:
            return self._easy(rolled, turn_score, subsets)
        elif self.difficulty == self.DIFFICULTY_MEDIUM:
            return self._medium(rolled, turn_score, subsets)
        else:
            return self._hard(rolled, turn_score, subsets, all_scores)

    # ------------------------------------------------------------------
    def _easy(self, rolled, turn_score, subsets):
        best = max(subsets, key=lambda s: subsets[s])
        points = subsets[best]
        dice_left = len(rolled) - len(best)
        if dice_left == 0:
            dice_left = 6  # hot dice
        bank = (turn_score + points) >= 300 or dice_left < 3
        return list(best), bank

    def _medium(self, rolled, turn_score, subsets):
        best = max(subsets, key=lambda s: subsets[s])
        points = subsets[best]
        new_total = turn_score + points
        dice_left = len(rolled) - len(best)
        if dice_left == 0:
            dice_left = 6
        farkle_p = _farkle_probability(dice_left)
        bank = new_total >= 450 or farkle_p > 0.40
        return list(best), bank

    def _hard(self, rolled, turn_score, subsets, all_scores):
        best_keep, best_ev = None, -1
        for subset, pts in subsets.items():
            dice_left = len(rolled) - len(subset)
            if dice_left == 0:
                dice_left = 6
            ev = _expected_value(turn_score + pts, dice_left)
            if ev > best_ev:
                best_ev, best_keep = ev, subset

        points = subsets[best_keep]
        dice_left = len(rolled) - len(best_keep)
        if dice_left == 0:
            dice_left = 6
        bank = (turn_score + points) >= _expected_value(0, dice_left)
        return list(best_keep), bank


# ------------------------------------------------------------------
# Probability helpers
# ------------------------------------------------------------------

def _farkle_probability(num_dice):
    """Approximate probability of farkle with `num_dice` dice."""
    _TABLE = {1: 0.667, 2: 0.444, 3: 0.278, 4: 0.160, 5: 0.077, 6: 0.023}
    return _TABLE.get(num_dice, 0.0)


def _expected_value(banked, num_dice, depth=3):
    """Simple recursive EV estimate for rolling `num_dice` more dice."""
    if depth == 0 or num_dice == 0:
        return banked
    fp = _farkle_probability(num_dice)
    avg_gain = _avg_score(num_dice)
    ev = (1 - fp) * _expected_value(banked + avg_gain, max(num_dice - 2, 1), depth - 1)
    return ev


def _avg_score(num_dice):
    """Very rough average score per roll for `num_dice` dice."""
    _TABLE = {1: 58, 2: 116, 3: 195, 4: 285, 5: 390, 6: 600}
    return _TABLE.get(num_dice, 58)
