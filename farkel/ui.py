from .dice import dice_art

WIDTH = 52


def banner():
    print("╔" + "═" * (WIDTH - 2) + "╗")
    print("║" + "  F A R K L E  ".center(WIDTH - 2) + "║")
    print("╚" + "═" * (WIDTH - 2) + "╝")


def main_menu():
    banner()
    print()
    print("  1. Play vs Human")
    print("  2. Play vs AI")
    print("  3. Rules & Scoring")
    print("  4. Quit")
    print()


def rules_screen():
    w = WIDTH
    print("═" * w)
    print(" FARKLE RULES ".center(w, "═"))
    print("═" * w)
    print()
    print("GOAL: First to 10,000 points wins (final round for all)")
    print()
    print("SCORING:")
    print("  Single 1 ............. 100    Straight (1-6) .... 1,500")
    print("  Single 5 ..............  50    Three pairs ....... 1,500")
    print("  Three 1s ............. 300    Two triplets ...... 2,500")
    print("  Three 2s-6s ...... Face×100   Four + pair ....... 1,500")
    print("  Four of a kind ..... 1,000")
    print("  Five of a kind ..... 2,000")
    print("  Six of a kind ...... 3,000")
    print()
    print("FARKLE: Roll no scoring dice = lose turn's points")
    print("HOT DICE: Score all 6 dice = must roll all 6 again")
    print()
    input("Press Enter to continue...")
    print("═" * w)


def turn_header(round_num, turn_total, players):
    print()
    print("═" * WIDTH)
    left = f" ROUND {round_num}"
    right = f"Turn total: {turn_total} "
    print(left + right.rjust(WIDTH - len(left)))
    print("─" * WIDTH)
    scores = "  ".join(f"{p.name}: {p.total_score:,}" for p in players)
    print(" " + scores)
    print("═" * WIDTH)


def show_roll(active_dice_faces, set_aside_faces):
    print()
    if set_aside_faces:
        print("Set aside:")
        print(dice_art(set_aside_faces))
        print()
    print("Your roll:")
    print(dice_art(active_dice_faces))
    print()


def show_ai_roll(player_name, active_dice_faces, set_aside_faces):
    print()
    print(f"{player_name} rolls:")
    if set_aside_faces:
        print("  Set aside:", set_aside_faces)
    print(dice_art(active_dice_faces))


def farkle_message(player_name):
    print()
    print(f"  FARKLE! {player_name} loses all points for this turn.")
    print()


def bank_message(player_name, points_banked, new_total):
    print()
    print(f"  {player_name} banks {points_banked:,} points. Total: {new_total:,}")
    print()


def hot_dice_message():
    print()
    print("  HOT DICE! All dice scored — you must roll all six again!")
    print()


def round_summary(results):
    """results: list of (player_name, old_score, new_score, farkled)"""
    print()
    print("─" * WIDTH)
    print(" Round Complete".ljust(WIDTH))
    print("─" * WIDTH)
    for name, old, new, farkled in results:
        delta = new - old
        tag = "  (Farkle!)" if farkled else f"  (+{delta:,})"
        print(f"  {name:<16} {old:>6,}  →  {new:>6,}{tag}")
    print("─" * WIDTH)
    print()


def winner_screen(player_name, score):
    print()
    print("╔" + "═" * (WIDTH - 2) + "╗")
    msg = f"  {player_name} wins with {score:,} points!  "
    print("║" + msg.center(WIDTH - 2) + "║")
    print("╚" + "═" * (WIDTH - 2) + "╝")
    print()


def prompt_keep():
    print("Select dice to keep by face value (e.g. 1 5  or  1 1 1),")
    print("or: b=bank  ?=advisor  r=rules  q=quit")
    return input("> ").strip()


def prompt_bank_or_roll(turn_total, dice_remaining):
    print(f"  Turn total: {turn_total}.  Dice to roll: {dice_remaining}.")
    while True:
        raw = input("(b)ank or (r)oll? > ").strip().lower()
        if raw in ("b", "bank"):
            return "bank"
        if raw in ("r", "roll"):
            return "roll"
        if raw in ("q", "quit"):
            raise SystemExit
        print("  Please answer 'b' to bank or 'r' to roll.")


def invalid_selection(reason):
    print(f"  ! {reason}")
    print()


def ai_action(player_name, kept, points, banking):
    kept_str = " ".join(str(d) for d in kept)
    action = "banks." if banking else "rolls again."
    print(f"  {player_name} keeps [{kept_str}] (+{points} pts) and {action}")
