import concurrent.futures
from lib import fibonacci_recursive, fibonacci_loop
from consts import FIBONACCI_TASKS


print('Started')
with concurrent.futures.ThreadPoolExecutor(2) as executor:
    for number in FIBONACCI_TASKS:
        future = executor.submit(fibonacci_recursive, number)
        return_value = future.result()
        print(return_value)
        print('*' * 42)
print('Join')


# python module_5/fibonacci_multiple_threads.py  99.48s user 0.23s system 99% cpu 1:40.13 total