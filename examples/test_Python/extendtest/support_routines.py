def interface_repeater(func):
    """Supporting decorator. It allows repeat command request if enter invalid value."""
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                raise KeyboardInterrupt("It's time to close!")
            except Exception:
                print("\nIncorrect input! Try again.")
    return wrapper
