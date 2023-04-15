def periodically_continued(a, b):
    """
    Decorator to create a periodic function in some interval.

    Parameters
    ----------
    a : float
    Lower bound of the interval.

    b : float
    Upper bound of the interval.

    Returns
    -------
    callable
    A function that takes a function and returns a periodic version of it.
    """
    interval = b - a
    return lambda f: lambda x: f((x - a) % interval + a)
