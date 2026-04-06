"""
Application entry point.

Detailed description:
    This module provides the main entry point for the application.
    Currently, it defines a single utility function `calc` that adds two
    integers.
    You can expand this module with additional functions or classes as needed.
"""

from backend import create_app


def calc(x: int, y: int) -> int:
    """
    Calculate the sum of two integers.

    This function takes two integer inputs and returns their sum.
    It does not perform any type conversion or error handling.

    Args:
        x (int): The first number to add.
        y (int): The second number to add.

    Returns:
        int: The sum of x and y.
    """
    return x + y


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
