"""Simple unit test for the greet() function.

Teaching notes:
- Unit tests should be small and fast. They verify the behavior of a single
    function in isolation.
- We import `greet` and assert on its return value.
"""

from myfirstproject.main import greet


def test_greet():
        # Exercise the function and check that the output matches expectation.
        assert greet("Alice") == "Hello, Alice!"
