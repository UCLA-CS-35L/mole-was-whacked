import pytest
from vending_machine import (
    load_machine, get_price, exact_combination, find_snack
)


@pytest.fixture
def sample_machine(tmp_path):
    """Create a small CSV vending machine and load it."""
    csv_file = tmp_path / "machine.csv"
    csv_file.write_text(
        "row,column,name,price\n"
        "1,A,Chips,120\n"
        "1,B,Soda,150\n"
        "1,C,Candy,80\n"
        "2,A,Gum,50\n"
        "2,B,Cookie,100\n"
        "2,C,Chocolate,200\n"
    )
    return load_machine(str(csv_file))


def test_get_price_chips(sample_machine):
    """Price lookup for Chips."""
    price = get_price(sample_machine, "Chips")
    assert price == 120


def test_get_price_soda(sample_machine):
    """Price lookup for Soda."""
    price = get_price(sample_machine, "Soda")
    assert price == 150


def test_get_price_candy(sample_machine):
    """Price lookup for Candy (works because on first row)."""
    price = get_price(sample_machine, "Candy")
    assert price == 80


def test_get_price_gum(sample_machine):
    """Price lookup for Gum."""
    price = get_price(sample_machine, "Gum")
    assert price == 50


def test_fuzzy_find_chips(sample_machine):
    """Fuzzy search should still suggest closest match."""
    pos = find_snack(sample_machine, "Chpp")
    # The suggestion print is side-effect (not returned); we just check
    # if the coordinates are correct.
    assert pos == (0, 0)


def test_get_price_cookie(sample_machine):
    """Price lookup for Cookie."""
    price = get_price(sample_machine, "Cookie")
    assert price == 100


def test_fuzzy_find_gum(sample_machine, capsys):
    """Fuzzy search should still suggest closest match."""
    pos = find_snack(sample_machine, "Gumm")
    assert pos == (1, 0)
    captured = capsys.readouterr()
    assert "Gum" in captured.out and "$50" in captured.out


def test_exact_combination_exists(sample_machine, capsys):
    """Exact combination that exists (120+150=270)."""
    exact_combination(sample_machine, 270)
    captured = capsys.readouterr()
    assert "No" not in captured.out


def test_exact_combination_not_exist(sample_machine, capsys):
    """Exact combination that does not exist."""
    exact_combination(sample_machine, 999)
    captured = capsys.readouterr()
    assert "No" in captured.out
