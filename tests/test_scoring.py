import unittest

from farkel.scoring import (
    all_dice_score,
    all_scoring_subsets,
    is_farkle,
    score_dice,
    validate_selection,
)


class ScoreDiceTests(unittest.TestCase):
    def test_singles(self):
        self.assertEqual(score_dice([1]), 100)
        self.assertEqual(score_dice([5]), 50)
        self.assertEqual(score_dice([1, 5]), 150)
        self.assertEqual(score_dice([2]), 0)

    def test_three_of_a_kind(self):
        self.assertEqual(score_dice([1, 1, 1]), 300)
        self.assertEqual(score_dice([2, 2, 2]), 200)
        self.assertEqual(score_dice([6, 6, 6]), 600)

    def test_higher_of_a_kind(self):
        self.assertEqual(score_dice([2, 2, 2, 2]), 1000)
        self.assertEqual(score_dice([3, 3, 3, 3, 3]), 2000)
        self.assertEqual(score_dice([4, 4, 4, 4, 4, 4]), 3000)

    def test_six_dice_specials(self):
        self.assertEqual(score_dice([1, 2, 3, 4, 5, 6]), 1500)
        self.assertEqual(score_dice([2, 2, 3, 3, 4, 4]), 1500)
        self.assertEqual(score_dice([2, 2, 2, 3, 3, 3]), 2500)
        self.assertEqual(score_dice([2, 2, 2, 2, 3, 3]), 1500)

    def test_combo_with_singles(self):
        self.assertEqual(score_dice([2, 2, 2, 5]), 250)
        self.assertEqual(score_dice([1, 1, 1, 5]), 350)


class AllDiceScoreTests(unittest.TestCase):
    def test_fully_scoring(self):
        for hand in (
            [1],
            [5],
            [1, 5],
            [2, 2, 2],
            [2, 2, 2, 5],
            [1, 1, 1, 1],
            [1, 2, 3, 4, 5, 6],
            [2, 2, 3, 3, 4, 4],
            [2, 2, 2, 3, 3, 3],
            [2, 2, 2, 2, 3, 3],
            [6, 6, 6, 6, 6, 6],
        ):
            with self.subTest(hand=hand):
                self.assertTrue(all_dice_score(hand))

    def test_partial_scoring_rejected(self):
        # The original bug report: keeping a 5 plus dead dice.
        for hand in (
            [2, 3, 4, 5, 6, 6],
            [1, 2],
            [5, 3],
            [2, 2, 2, 3],
            [5, 5, 2, 2],
            [1, 1, 6],
            [2, 2, 3, 3],  # two pairs is NOT a scoring combo
        ):
            with self.subTest(hand=hand):
                self.assertFalse(all_dice_score(hand))

    def test_empty_is_not_scoring(self):
        self.assertFalse(all_dice_score([]))


class ValidateSelectionTests(unittest.TestCase):
    def test_rejects_dead_dice_in_selection(self):
        # The exact scenario the user hit.
        ok, reason = validate_selection([2, 3, 4, 5, 6, 6], [2, 3, 4, 5, 6, 6])
        self.assertFalse(ok)
        self.assertTrue(reason)

    def test_accepts_only_the_scoring_die(self):
        ok, _ = validate_selection([2, 3, 4, 5, 6, 6], [5])
        self.assertTrue(ok)

    def test_rejects_zero_score(self):
        ok, _ = validate_selection([2, 3], [2, 3])
        self.assertFalse(ok)

    def test_rejects_more_than_rolled(self):
        ok, _ = validate_selection([5], [5, 5])
        self.assertFalse(ok)

    def test_rejects_empty(self):
        ok, _ = validate_selection([1, 2, 3], [])
        self.assertFalse(ok)

    def test_accepts_three_of_a_kind_with_single(self):
        ok, _ = validate_selection([2, 2, 2, 5, 6, 6], [2, 2, 2, 5])
        self.assertTrue(ok)

    def test_rejects_partial_three_of_a_kind(self):
        ok, _ = validate_selection([2, 2, 5, 6, 6, 3], [2, 2, 5])
        self.assertFalse(ok)

    def test_accepts_six_dice_straight(self):
        ok, _ = validate_selection([1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6])
        self.assertTrue(ok)


class AllScoringSubsetsTests(unittest.TestCase):
    def test_only_returns_fully_scoring_subsets(self):
        subsets = all_scoring_subsets([2, 3, 4, 5, 6, 6])
        self.assertEqual(set(subsets.keys()), {(5,)})
        self.assertEqual(subsets[(5,)], 50)

    def test_three_pairs_appears(self):
        subsets = all_scoring_subsets([2, 2, 3, 3, 4, 4])
        self.assertIn((2, 2, 3, 3, 4, 4), subsets)
        self.assertEqual(subsets[(2, 2, 3, 3, 4, 4)], 1500)

    def test_no_dead_dice_in_any_subset(self):
        subsets = all_scoring_subsets([1, 2, 2, 5, 6, 6])
        for subset in subsets:
            self.assertTrue(
                all_dice_score(list(subset)),
                msg=f"{subset} contains non-scoring dice",
            )


class IsFarkleTests(unittest.TestCase):
    def test_true_farkle(self):
        self.assertTrue(is_farkle([2, 3, 4, 6, 6]))
        self.assertTrue(is_farkle([2, 3, 4, 6]))
        self.assertTrue(is_farkle([2, 2, 3, 3]))  # two pairs is not a score

    def test_not_farkle_with_one(self):
        self.assertFalse(is_farkle([1, 2, 3, 4, 6]))

    def test_not_farkle_with_triple(self):
        self.assertFalse(is_farkle([2, 2, 2, 3, 4, 6]))


if __name__ == "__main__":
    unittest.main()
