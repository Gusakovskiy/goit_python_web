from multiprocessing import Queue, Process
from time import sleep


def reader(queue: Queue, name: str):
    print(name, 'started..')
    while not queue.empty():
        val = queue.get(timeout=0.5)
        print(f'Process {name}, read: "{val}"')
    print(name, 'ended..')


def writer(queue: Queue, name: str):
    print(name, 'started..')
    val = f'Hello from process {name}'
    queue.put(val)
    print(name, 'ended..')
    print(' ')


def main():
    q = Queue()
    w1 = Process(target=writer, args=(q, 'writer'))
    w2 = Process(target=reader, args=(q, 'reader'))

    q.put('Hello from main thread')
    w1.start()
    # sleep(1.0)
    w2.start()
    # wait to end
    w1.join()
    w2.join()


if __name__ == '__main__':
    main()