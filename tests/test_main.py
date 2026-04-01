from main import calc


def test_calc_basic() -> None:
    """
    Tests the calc function with normal integer values.

    Checks positive, negative, and zero values.
    """
    assert calc(2, 3) == 5
    assert calc(0, 0) == 0
    assert calc(-1, 1) == 0
    assert calc(10, 5) == 15


def test_calc_types() -> None:
    """
    Tests that calc returns an integer.

    Ensures that the return type of calc is always int.
    """
    assert isinstance(calc(2, 3), int)
