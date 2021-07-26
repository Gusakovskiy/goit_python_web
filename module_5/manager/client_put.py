from _base import manager

manager.connect()
queue = manager.get_queue()
value = 'hello'
print(f'Put value {value}')
queue.put(value)
