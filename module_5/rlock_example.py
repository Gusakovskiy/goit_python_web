from multiprocessing import Process, Value, RLock

import sys


def add_one(name, lock: RLock, val: Value):
    lock.acquire()
    val.value += 1
    print(f'Value in {name} {val.value}')
    lock.release()
    print(f'Done {name}')
    sys.exit(0)


if __name__ == '__main__':
    v = Value('d', 0)
    r = RLock()
    p1 = Process(target=add_one, args=('first', r, v))
    p2 = Process(target=add_one, args=('second', r, v))

    p1.start()
    p2.start()

    print(p1.exitcode, p2.exitcode)  # None, None
    p1.join()
    p2.join()

    print(p1.exitcode, p2.exitcode)  # 0, 0
    print(f'End value {v.value}')  # 2.0