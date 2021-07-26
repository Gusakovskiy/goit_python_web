from multiprocessing import Process


def process_data_and_write(file_path, data):
    with open(file_path, 'w') as _f:  #  'a'
        for number in data:
            _f.write(f'{number**2}\n')


if __name__ == '__main__':
    file_path = 'tmp.txt'
    p1 = Process(target=process_data_and_write, args=(file_path, [1, 2, 3]))
    p2 = Process(target=process_data_and_write, args=(file_path, [4, 5, 6]))

    p1.start()
    p2.start()

    print(p1.exitcode, p2.exitcode)  # None, None

    p1.join()
    p2.join()