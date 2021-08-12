# OSI Model
# 7. Application Layer (HTTP, HTTPS, IAMP )
# 6. Presentantion Layer
# 5. Session Layer
# 4. Transport Layer  * you are here
# 3. Network Layer
# 2. Data Link Layer
# 1. Physical Layer

# TCP/IP model (Transmission Control Protocol/ Internet Protocol)
# Application Layer
# Transport Layer  * you are here
# Internet (Network layer)
# Network Acccess Layer (Data Link , Physical Layer)



import socket
# https://docs.python.org/3/library/socket.html
# https://docs.python.org/3/howto/sockets.html#socket-howto
s = socket.socket()  # Transport layer
s.bind(('0.0.0.0', 5000))
s.listen()
s.accept()
s.connect()
s.send()
s.recv()
s.close()
