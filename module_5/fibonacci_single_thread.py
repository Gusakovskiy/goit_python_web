from lib import fibonacci_recursive, fibonacci_loop
from consts import FIBONACCI_TASKS

print('Started')
for number in FIBONACCI_TASKS:
    result = fibonacci_recursive(number)
    print(result)
    print('*' * 42)


### REC
# python module_5/fibonacci_single_thread.py  100.92s user 0.49s system 99% cpu 1:42.21 total








### LOOP
# python module_5/fibonacci_single_thread.py  100.11s user 0.47s system 98% cpu 1:41.78 total