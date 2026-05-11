from .dice import Dice
from .scoring import score_dice, all_scoring_subsets, is_farkle, validate_selection
from .advisor import show_advice
from . import ui

WIN_SCORE = 10_000


def _roll_active(dice):
    for d in dice:
        if not d.set_aside:
            d.roll()


def _active_faces(dice):
    return [d.current_side for d in dice if not d.set_aside]


def _aside_faces(dice):
    return [d.current_side for d in dice if d.set_aside]


def _reset_dice(dice):
    for d in dice:
        d.set_aside = False


def _apply_kept(dice, kept_faces):
    """Mark dice as set_aside for the chosen face values (greedy match)."""
    remaining = list(kept_faces)
    for d in dice:
        if d.set_aside:
            continue
        if d.current_side in remaining:
            d.set_aside = True
            remaining.remove(d.current_side)


def play_human_turn(player, dice, players, round_num):
    turn_score = 0
    _reset_dice(dice)

    while True:
        _roll_active(dice)
        active = _active_faces(dice)
        aside = _aside_faces(dice)

        ui.turn_header(round_num, turn_score, players)
        ui.show_roll(active, aside)

        if is_farkle(active):
            ui.farkle_message(player.name)
            return 0, True  # (points_earned, farkled)

        # Input loop
        while True:
            raw = ui.prompt_keep()
            cmd = raw.lower()

            if cmd in ("q", "quit"):
                raise SystemExit

            if cmd in ("r", "rules"):
                ui.rules_screen()
                ui.turn_header(round_num, turn_score, players)
                ui.show_roll(active, aside)
                continue

            if cmd == "?":
                show_advice(active, turn_score)
                continue

            if cmd in ("b", "bank"):
                if turn_score == 0:
                    ui.invalid_selection("You haven't scored anything yet — keep some dice first.")
                    continue
                ui.bank_message(player.name, turn_score, player.total_score + turn_score)
                return turn_score, False

            # Parse face values
            try:
                chosen = list(map(int, raw.split()))
            except ValueError:
                ui.invalid_selection("Enter die face values separated by spaces (e.g. 1 5).")
                continue

            valid, reason = validate_selection(active, chosen)
            if not valid:
                ui.invalid_selection(reason)
                continue

            pts = score_dice(chosen)
            _apply_kept(dice, chosen)
            turn_score += pts
            print(f"  Kept {chosen} for {pts} pts. Turn total: {turn_score}")

            # Hot dice: rules force a re-roll of all six.
            if all(d.set_aside for d in dice):
                ui.hot_dice_message()
                _reset_dice(dice)
                break  # outer loop re-rolls all six

            # Otherwise let the player choose: bank now or roll the rest.
            remaining = sum(1 for d in dice if not d.set_aside)
            decision = ui.prompt_bank_or_roll(turn_score, remaining)
            if decision == "bank":
                ui.bank_message(player.name, turn_score, player.total_score + turn_score)
                return turn_score, False
            break  # roll remaining dice


def play_ai_turn(player, dice, players, round_num):
    turn_score = 0
    _reset_dice(dice)
    all_scores = [p.total_score for p in players]

    while True:
        _roll_active(dice)
        active = _active_faces(dice)
        aside = _aside_faces(dice)

        ui.show_ai_roll(player.name, active, aside)

        if is_farkle(active):
            ui.farkle_message(player.name)
            return 0, True

        kept, should_bank = player.choose_keep(active, turn_score, all_scores)
        pts = score_dice(kept)
        _apply_kept(dice, kept)
        turn_score += pts

        ui.ai_action(player.name, kept, pts, should_bank)

        # Hot dice
        if all(d.set_aside for d in dice):
            ui.hot_dice_message()
            _reset_dice(dice)
            should_bank = False  # must roll again

        if should_bank:
            ui.bank_message(player.name, turn_score, player.total_score + turn_score)
            return turn_score, False


def run_game(players):
    dice = [Dice() for _ in range(6)]
    round_num = 1
    final_round = False
    final_player_idx = None

    current_idx = 0
    while True:
        player = players[current_idx]
        round_results_this_turn = []

        old_score = player.total_score

        if player.is_ai:
            earned, farkled = play_ai_turn(player, dice, players, round_num)
        else:
            earned, farkled = play_human_turn(player, dice, players, round_num)

        player.total_score += earned
        round_results_this_turn.append((player.name, old_score, player.total_score, farkled))
        ui.round_summary(round_results_this_turn)

        # Check win trigger
        if not final_round and player.total_score >= WIN_SCORE:
            final_round = True
            final_player_idx = current_idx
            print(f"  {player.name} has reached {WIN_SCORE:,}! Final round begins.")
            print()

        # Advance player
        current_idx = (current_idx + 1) % len(players)
        if current_idx == 0:
            round_num += 1

        # End game when final round completes (everyone had one more turn)
        if final_round and current_idx == (final_player_idx + 1) % len(players):
            break

    winner = max(players, key=lambda p: p.total_score)
    ui.winner_screen(winner.name, winner.total_score)
