import concurrent.futures
from lib import fibonacci_loop, fibonacci_recursive
from consts import FIBONACCI_TASKS

if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(2) as pool:
        for number, prime in zip(FIBONACCI_TASKS, pool.map(fibonacci_recursive, FIBONACCI_TASKS)):
            print('Task %d fibonacci_number : %s' % (number, prime))
            print('*' * 42)



### REC
### python module_5/fibonacci_multiple_processes.py  100.82s user 0.49s system 99% cpu 1:41.67 total





### LOOP
### python module_5/fibonacci_multiple_processes.py  0.05s user 0.03s system 71% cpu 0.109 total
