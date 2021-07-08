import socket
import select

Server = socket.socket()
Server.bind(('localhost', 2222))
Server.listen(5)

ready_for_read = []
ready_for_write = []

while True:
    conn, addr = Server.accept()
    print(f'got connection from {addr}')
    ready_for_read.append(conn)
    ready_for_write.append(conn)

    ready, writy, exy = select.select([ready_for_read], [ready_for_write], [ready_for_read])

    for ser in ready:
        data = ser.recv(1024)
        print(data.decode('utf-8'))

        for server in writy:
            server.send(data.upper())
