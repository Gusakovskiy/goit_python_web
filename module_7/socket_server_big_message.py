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
            all_data = []
            print('Connected by', addr)
            while True:
                data = conn.recv(CHUNK_BYTES)  # blocking syscall
                if data == b'end':
                    break
                elif not data:
                    break
                else:
                    counter += 1
                all_data.append(data)
                print(f'Data received {data}')
                print(f'Counter {counter}')
                # do echo server
            data = b''.join(all_data)
            print(f'Join data {data}')
            if b'server' in data:
                data = data.replace(b'server', b'client')
            conn.sendall(data.title())
            # conn.sendall(b'')
        print(f'Number of calls {counter}')


if __name__ == '__main__':
    # list of open files
    # lsof -i -n | grep Python
    main()
