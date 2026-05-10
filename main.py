from farkel import ui
from farkel.player import Player, AIPlayer
from farkel.game import run_game


def setup_players(mode):
    players = []
    if mode == "1":
        n = 0
        while n < 2:
            try:
                n = int(input("How many human players? (2-6) ").strip())
                if not 2 <= n <= 6:
                    raise ValueError
            except ValueError:
                print("  Please enter a number between 2 and 6.")
        for i in range(n):
            name = input(f"Player {i+1} name: ").strip() or f"Player {i+1}"
            players.append(Player(name))
    else:
        name = input("Your name: ").strip() or "Player"
        players.append(Player(name))
        print("AI difficulty:  1=Easy  2=Medium  3=Hard")
        diff_map = {"1": AIPlayer.DIFFICULTY_EASY,
                    "2": AIPlayer.DIFFICULTY_MEDIUM,
                    "3": AIPlayer.DIFFICULTY_HARD}
        diff = diff_map.get(input("> ").strip(), AIPlayer.DIFFICULTY_MEDIUM)
        players.append(AIPlayer("CPU", diff))
    return players


def main():
    while True:
        ui.main_menu()
        choice = input("Choice: ").strip()

        if choice == "1" or choice == "2":
            players = setup_players(choice)
            run_game(players)
            again = input("Play again? (y/n) ").strip().lower()
            if again != "y":
                break

        elif choice == "3":
            ui.rules_screen()

        elif choice == "4" or choice.lower() == "q":
            break

        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
