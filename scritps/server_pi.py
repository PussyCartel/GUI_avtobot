import socket


server_socket = socket.socket()
server_socket.bind(('', 8585))
server_socket.listen(10)

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(16384)
    print(data)
