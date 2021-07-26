from multiprocessing import Pipe, Process
from time import sleep

_TIME_TO_WAIT = 0.5
_TIME_TO_WAIT_IN_PROCESS = 2.0


def multiply_3(connection, name):
    print(name, 'started..')
    while connection.poll(_TIME_TO_WAIT_IN_PROCESS):
        val = connection.recv()
        val = val ** 2
        print(name, val)


def add_4(connection, name):
    print(name, 'started..')
    while connection.poll(_TIME_TO_WAIT_IN_PROCESS):
        val = connection.recv()
        val = val + 4
        print(name, val)


def main():
    start_1, end_1 = Pipe()
    start_2, end_2 = Pipe()
    w1 = Process(target=multiply_3, args=(end_1, 'first'))
    w2 = Process(target=add_4, args=(end_2, 'second'))
    pipe_starts = (start_1, start_2)

    w1.start()
    w2.start()

    values = (13, 28)
    for value in values:
        print(f'Value {value}')
        for pipe in pipe_starts:
            pipe.send(value)
        sleep(_TIME_TO_WAIT)

    time_to_make_sure_everything_read = _TIME_TO_WAIT_IN_PROCESS * len(pipe_starts) * 1.2
    sleep(time_to_make_sure_everything_read)


if __name__ == '__main__':
    main()