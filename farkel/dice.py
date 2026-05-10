import random

# ASCII art face templates — each face is 5 lines of 5 chars (inside the border)
_FACES = {
    1: ["     ", "     ", "  ●  ", "     ", "     "],
    2: ["     ", " ●   ", "     ", "   ● ", "     "],
    3: ["  ●  ", "     ", "  ●  ", "     ", "  ●  "],
    4: [" ● ● ", "     ", "     ", "     ", " ● ● "],
    5: [" ● ● ", "     ", "  ●  ", "     ", " ● ● "],
    6: [" ● ● ", "     ", " ● ● ", "     ", " ● ● "],
}

_TOP    = "┌─────┐"
_BOTTOM = "└─────┘"
_SIDE   = "│"


def dice_art(faces, set_aside_flags=None):
    """
    Render a row of dice as a multi-line string.
    `faces` is a list of int face values.
    `set_aside_flags` is an optional list of bools (True = dim the die).
    Returns a string with newlines.
    """
    if set_aside_flags is None:
        set_aside_flags = [False] * len(faces)

    lines = []
    lines.append("  ".join(_TOP for _ in faces))
    for row in range(5):
        parts = []
        for i, face in enumerate(faces):
            content = _FACES[face][row]
            parts.append(f"{_SIDE}{content}{_SIDE}")
        lines.append("  ".join(parts))
    lines.append("  ".join(_BOTTOM for _ in faces))
    # Index line (1-based position)
    index_row = "  ".join(f"  [{i+1}]  " for i in range(len(faces)))
    lines.append(index_row)
    return "\n".join(lines)


class Dice:
    def __init__(self):
        self.current_side = 1
        self.set_aside = False

    def roll(self):
        self.current_side = random.randint(1, 6)
        return self.current_side
