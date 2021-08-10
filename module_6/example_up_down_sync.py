import time


def count_up(count):
    counter = 0
    while counter < count:
        print("Up", counter)
        counter += 1
        time.sleep(1)


def count_down(count):
    while count > 0:
        print("Down ", count)
        time.sleep(1)
        count -= 1


def main():
    count_up(10)
    count_down(10)


if __name__ == '__main__':
    main()
