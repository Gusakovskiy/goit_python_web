from multiprocessing import Pool
import os
import time
import random
import string


def random_string(number_digits):
    return ''.join(random.choice(
        string.ascii_uppercase + string.digits
    ) for _ in range(number_digits))


def random_name():
    names = (
        'Dima', 'Pasha', 'Homer', 'Oleg', 'Viktor',
        'Stepa', 'Morty', 'Vasya', 'Petya',
        'Valera', 'James', 'Meg', 'Orkan', 'Summer',
        'Tom', 'Jerry', 'Ivan', 'Rick', 'Beth', 'Bender',
        'Bart', 'Lisa',
    )
    return random.choice(names)


def send_push_message(tuple_push, *_args):
    receiver, message = tuple_push
    print(f'pid={os.getpid()}, x={receiver}')
    print(f'Message "{message}" to {receiver}')
    print(' ')
    return 'Success' if 'A' not in receiver else 'Fail'


if __name__ == '__main__':
    cpu = 2
    number_of_cpu = os.cpu_count()
    tasks = [
        (random_string(5), f'Hi {random_name()} nice to meet you!')
        for _ in range(10)
    ]
    # number_of_available_cpu = len(os.sched_getaffinity(0))
    with Pool(processes=cpu) as pool:
        print(
            pool.map(
                send_push_message,
                iter(tasks)
            )
        )
        print('')
