import unittest

from farkel.advisor import decide


class DecideTests(unittest.TestCase):
    def test_banks_when_turn_score_is_high(self):
        # 1 die left, already have 550: rolling has tiny EV vs. banking.
        action, ev = decide(turn_score=500, pts=50, dice_left=1)
        self.assertEqual(action, "bank")
        self.assertEqual(ev, 550)

    def test_rolls_on_fresh_six_dice(self):
        # turn_score=0, keep one 5 from 6, dice_left=5: rolling is clearly better.
        action, _ = decide(turn_score=0, pts=50, dice_left=5)
        self.assertEqual(action, "roll")

    def test_hot_dice_forces_roll(self):
        # dice_left == 0 → hot dice. Rules force a re-roll of all six;
        # the advisor must not recommend banking here.
        action, _ = decide(turn_score=0, pts=1500, dice_left=0)
        self.assertEqual(action, "roll")

    def test_banks_when_one_die_left(self):
        # With only 1 die left and meaningful turn_score, banking dominates.
        action, _ = decide(turn_score=300, pts=100, dice_left=1)
        self.assertEqual(action, "bank")


if __name__ == "__main__":
    unittest.main()
