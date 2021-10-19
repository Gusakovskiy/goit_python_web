"""Module docs"""
import doctest


class MyClass:
    """Class docs
    Docs of MyClass
    """

    def __init__(self, value):
        """Constructor for MyClass

        :param value: stored value
        """
        self._value = value


def special_add_func(a, b):
    """Add two numbers

    Special function to add to numbers but only if first one is not 42
    >>> special_add_func(4, 3)
    7
    >>> special_add_func(42, 7)
    Traceback (most recent call last):
    ...
    ValueError: Nothing should be added to 42
    >>> special_add_func(8, 5)
    13


    :raises ValueError: if first argument is 42
    :param a: int. first value to add
    :param b: int. second value to add
    :return: int. result of addition of a and b
    """
    if a == 42:
        raise ValueError('Nothing should be added to 42')
    return a + b


if __name__ == "__main__":
    doctest.testmod()
    # or with pytest
    # pytest --doctest-modules
