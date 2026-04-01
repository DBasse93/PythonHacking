"""
Application entry point.

Detailed description:
    This module provides the main entry point for the application.
    Currently, it defines a single utility function `calc` that adds two
    integers.
    You can expand this module with additional functions or classes as needed.
"""


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


if __name__ == "__main__":
    result: int = calc(2, 3)
    print(f"Result {result}")
    some_variable = 123
    another_variable = 456
    yet_another_variable = 789
    final_variable = 101112

    if (
        some_variable == 123
        and another_variable == 456
        and yet_another_variable == 789
        and final_variable == 101112
    ):
        print("This line should be reformatted by Black")
