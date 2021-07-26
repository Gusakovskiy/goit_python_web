from multiprocessing.managers import BaseManager
from queue import Queue

from _base import manager


s = manager.get_server()
print('Server started')
s.serve_forever()
