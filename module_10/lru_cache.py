from collections import deque
# from functools import lru_cache
from inspect import signature


class LruCache:
    def __init__(self, func, max_size):
        self.func = func
        self.max_size = max_size
        self._cache = dict()
        self.queue = deque()

    def __call__(self, *args, **kwargs):
        # to implement
        ...


def lru_cache(max_size=5):
    def wrapper(func):
        cache = LruCache(func, max_size)
        return cache
    return wrapper


@lru_cache()
def foo(value: str, value_1: int):

    return f'result_{value}'


def lruCache(value: str) -> str: # test function
    queue = deque()
    ...
    return "".join([str(ch) for ch in queue])

# LruCache("ABACBDEG") => "GEDBC"

# ("A", "B" , "A", "C", "B", "D", "E", "G")
# lru
# "A"
#     {"A": "result_A"}
#  deque("A")
# B
#  {"A": "result_A", "B": "result_B"}
#  deque("B", "A")
# "A"
#  {"A": "result_A", "B": "result_B"}
#  deque("A", "B")
# C
# #  {"A": "result_A", "B": "result_B", "C": "result_C"}
#  deque("C", "A", "B")
# B
# #  {"A": "result_A", "B": "result_B", "C": "result_C"}
#  deque("B", "C", "A")
# D
# #  {"A": "result_A", "B": "result_B", "C": "result_C", "D": "result_D"}
#  deque("D", "B", "C", "A")
# E
#  {"A": "result_A", "B": "result_B", "C": "result_C", "D": "result_D", "E": "result_E"}
#  deque("E", "D", "B", "C", "A")
# G
# {"G": "result_G", "B": "result_B", "C": "result_C", "D": "result_D", "E": "result_E"}
#  deque("G", "E", "D", "B", "C")
