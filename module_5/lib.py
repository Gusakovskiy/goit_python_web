from functools import lru_cache


def fibonacci_recursive(number: int) -> int:
    if number == 0:
        return 0
    elif number == 1:
        return 1
    return fibonacci_recursive(number - 2) + fibonacci_recursive(number - 1)











def fibonacci_loop(n):
    f = [0, 1]
    for i in range(2, n + 1):
        f.append(f[i - 1] + f[i - 2])
    return f[n]
