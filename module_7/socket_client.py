import socket
import sys
from time import sleep


def client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind((host, host + 1))
        message = b'hello server'
        try:
            print('Connecting')
            print(f'Sending {sys.getsizeof(message)}')
            s.connect((host, port))
            s.send(message)
            data = s.recv(1024)
            print(f'From server: {data}')
        except (ConnectionRefusedError, OSError) as e:
            print('Error {!r}'.format(e))


if __name__ == '__main__':
    client('127.0.0.1', 5000)
