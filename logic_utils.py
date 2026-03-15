"""Utility functions for the Game Glitch Investigator guessing game."""

import json
import os

HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "highscore.json")


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) number range for a given difficulty.

    Parameters
    ----------
    difficulty : str
        One of ``"Easy"``, ``"Normal"``, or ``"Hard"``.

    Returns
    -------
    tuple[int, int]
        A ``(low, high)`` pair representing the inclusive guess range.
        Defaults to ``(1, 100)`` for any unrecognised difficulty value.

    Examples
    --------
    >>> get_range_for_difficulty("Easy")
    (1, 20)
    >>> get_range_for_difficulty("Hard")
    (1, 50)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse and validate a raw text guess from the user.

    Accepts whole numbers or decimal strings (decimal part is truncated).
    Rejects empty input, non-numeric strings, and values outside 1–100.

    Parameters
    ----------
    raw : str
        The raw string entered by the user.

    Returns
    -------
    ok : bool
        ``True`` if the input is a valid integer in the range [1, 100].
    guess_int : int or None
        The parsed integer value, or ``None`` when ``ok`` is ``False``.
    error_message : str or None
        A human-readable error description, or ``None`` when ``ok`` is ``True``.

    Examples
    --------
    >>> parse_guess("42")
    (True, 42, None)
    >>> parse_guess("abc")
    (False, None, 'That is not a number.')
    >>> parse_guess("150")
    (False, None, 'Guess must be between 1 and 100.')
    """
    if raw is None or raw == "" or not raw.strip():
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < 1 or value > 100:
        return False, None, "Guess must be between 1 and 100."

    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """Compare the player's guess to the secret number.

    Parameters
    ----------
    guess : int
        The number submitted by the player.
    secret : int
        The hidden target number.

    Returns
    -------
    str
        ``"Win"`` if the guess matches the secret,
        ``"Too High"`` if the guess exceeds the secret, or
        ``"Too Low"`` if the guess is below the secret.

    Examples
    --------
    >>> check_guess(50, 50)
    'Win'
    >>> check_guess(70, 50)
    'Too High'
    >>> check_guess(30, 50)
    'Too Low'
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate the new score after a guess.

    A correct guess awards points scaled by how quickly the player won.
    An incorrect guess deducts 5 points. The score is always clamped to a
    minimum of zero.

    Parameters
    ----------
    current_score : int
        The player's score before this guess.
    outcome : str
        The result of the guess: ``"Win"``, ``"Too High"``, or ``"Too Low"``.
    attempt_number : int
        The 1-based attempt count for the current game.

    Returns
    -------
    int
        The updated score, guaranteed to be >= 0.

    Examples
    --------
    >>> update_score(0, "Win", 1)
    80
    >>> update_score(50, "Too High", 3)
    45
    >>> update_score(0, "Too Low", 1)
    0
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    return max(0, current_score - 5)


def load_high_score() -> int:
    """Load the all-time high score from ``highscore.json``.

    If the file does not exist or cannot be read, returns ``0``.

    Returns
    -------
    int
        The stored high score, or ``0`` if no record exists.
    """
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            data = json.load(f)
            return int(data.get("high_score", 0))
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return 0


def save_high_score(score: int) -> None:
    """Persist *score* to ``highscore.json`` if it exceeds the stored record.

    Parameters
    ----------
    score : int
        The score to compare against and potentially save.
    """
    current_best = load_high_score()
    if score > current_best:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump({"high_score": score}, f)
