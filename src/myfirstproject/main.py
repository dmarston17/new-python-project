def greet(name: str) -> str:
    """Return a greeting for name.

    Comments / teaching notes:
    - This is a tiny pure function (no side effects) that's easy to test.
    - Input: `name` (string). Output: greeting string.
    - Keep functions small and deterministic for easy unit testing.
    """
    # Build and return a formatted string. f-strings are the modern way to
    # interpolate variables into strings in Python 3.6+.
    return f"Hello, {name}!"


if __name__ == "__main__":
    # Running this module directly prints a simple greeting. This is handy
    # when you want to sanity-check a module without running the whole app.
    print(greet("world"))
