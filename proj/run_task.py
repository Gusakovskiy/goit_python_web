from proj.tasks import add, mul, process_results
from celery import group, chain, chord


def main():
    result = add.delay(1, 3)
    while not result.ready():
        print(f'Waiting for {result}')
    print(result.get(timeout=1))


def signature():
    # add.signature((2, 2), countdown=10)  #  == add.s(2, 2)
    tasks = [add.s(i, i) for i in range(10)]
    print('Group ', group(tasks)().get())
    print('Chain ', chain(add.s(12, 8) | mul.s(8))().get())
    print('Chord', chord((add.s(i, i) for i in range(10)), process_results.s())().get())


if __name__ == '__main__':
    # main()
    signature()
