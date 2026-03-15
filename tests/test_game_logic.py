from logic_utils import check_guess, parse_guess, update_score


# ---------------------------------------------------------------------------
# check_guess — core outcome tests
# ---------------------------------------------------------------------------

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_guess_boundary_low():
    # Boundary: guess equals the lowest valid secret (1)
    assert check_guess(1, 1) == "Win"
    assert check_guess(1, 2) == "Too Low"

def test_guess_boundary_high():
    # Boundary: guess equals the highest valid secret (100)
    assert check_guess(100, 100) == "Win"
    assert check_guess(100, 99) == "Too High"

def test_guess_extremely_large():
    # A very large number is always Too High for any normal secret
    assert check_guess(999999, 50) == "Too High"

def test_guess_negative():
    # A negative number is always Too Low
    assert check_guess(-1, 50) == "Too Low"
    assert check_guess(-999, 1) == "Too Low"


# ---------------------------------------------------------------------------
# parse_guess — validation tests
# ---------------------------------------------------------------------------

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_non_numeric_string():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert "not a number" in err.lower()

def test_parse_negative_number():
    # Negative numbers are out of range (1–100)
    ok, value, err = parse_guess("-5")
    assert ok is False
    assert value is None

def test_parse_too_large():
    ok, value, err = parse_guess("101")
    assert ok is False
    assert value is None
    assert "between 1 and 100" in err

def test_parse_zero():
    ok, value, err = parse_guess("0")
    assert ok is False

def test_parse_float_string():
    # Float input gets truncated to int if within range
    ok, value, err = parse_guess("50.9")
    assert ok is True
    assert value == 50

def test_parse_special_characters():
    ok, value, err = parse_guess("!@#")
    assert ok is False

def test_parse_whitespace_only():
    ok, value, err = parse_guess("   ")
    assert ok is False


# ---------------------------------------------------------------------------
# update_score — scoring tests
# ---------------------------------------------------------------------------

def test_score_win_early():
    # Win on attempt 1 gives maximum points
    result = update_score(0, "Win", 1)
    assert result > 0

def test_score_win_late():
    # Win on a high attempt number still gives at least 10 points
    result = update_score(0, "Win", 20)
    assert result >= 10

def test_score_wrong_guess_deducts():
    result = update_score(50, "Too High", 1)
    assert result == 45

def test_score_never_goes_below_zero():
    # Score should clamp at 0, never go negative
    result = update_score(0, "Too Low", 1)
    assert result == 0

def test_score_clamped_from_small_positive():
    result = update_score(3, "Too High", 2)
    assert result == 0
