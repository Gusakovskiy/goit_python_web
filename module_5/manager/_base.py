from multiprocessing.managers import BaseManager
from queue import Queue


class QueueManager(BaseManager):
    pass

queue = Queue()

QueueManager.register('get_queue', callable=lambda:queue)

manager = QueueManager(address=('127.0.0.1', 50000), authkey=b'abracadabra')