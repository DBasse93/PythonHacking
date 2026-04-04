from frontend import app


def calc() -> None:
    """
    Tests the calc function with normal integer values.

    Checks positive, negative, and zero values.
    """
    assert calc(2, 3) == 5
    assert calc(0, 0) == 0
    assert calc(-1, 1) == 0
    assert calc(10, 5) == 15


if __name__ == "__main__":
    app.run(debug=True)
