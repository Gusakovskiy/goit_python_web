import socket
import sys
from time import sleep

from module_7.settings import CHUNK_BYTES


def client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        long_message = b'hello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello serverhello server'
        message = long_message
        try:
            print('Connecting')
            print(f'Sending {sys.getsizeof(message)}')
            s.connect((host, port))
            s.sendall(message)
            sleep(5)
            s.send(b'end')
            while True:
                data = s.recv(CHUNK_BYTES)
                if not data:
                    print(f'Break')
                    break
                print(f'From server: {data}')
        except (ConnectionRefusedError, OSError) as e:
            print('Error {!r}'.format(e))


if __name__ == '__main__':
    client('127.0.0.1', 5000)
