from src.clean_data import normalize_text


def test_normalize_text():
    assert normalize_text(" BATTERY ") == "battery"


def test_normalize_text_none():
    assert normalize_text(None) == "unknown"