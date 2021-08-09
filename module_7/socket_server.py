#!/usr/bin/env python3

import socket
from time import sleep

from module_7.settings import CHUNK_BYTES

HOST = '127.0.0.1'
PORT = 5000
_MAX_NUMBER_OF_CONNECTIONS = 10


def main():
    # use context manager to close socket properly
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # wgich Internet Address Family and which socket Type
        # set option
        # https://www.gnu.org/software/libc/manual/html_node/Socket_002dLevel-Options.html#Socket_002dLevel-Options
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        print(f'Listen {HOST} {PORT}')
        s.listen(_MAX_NUMBER_OF_CONNECTIONS)  # number of unaccepted connection  before refusing new connections
        print('Accept ')
        conn, addr = s.accept()  # blocking syscall
        counter = 0
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(CHUNK_BYTES)  # blocking syscall
                # sleep(10)
                print(f'Data received {data}')
                print(f'Counter {counter}')
                if not data:  # if empty bytes then EOF
                    break
                else:
                    counter += 1
                # do echo server
            if b'server' in data:
                data = data.replace(b'server', b'client')
            conn.sendall(data.title())
        print(f'Number of calls {counter}')


if __name__ == '__main__':
    # list of open files
    # lsof -i -n | grep Python
    main()
