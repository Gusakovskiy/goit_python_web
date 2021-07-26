from _base import manager

manager.connect()
queue = manager.get_queue()
print('Waiting for value')
value = queue.get()
print(f'Value {value}')
