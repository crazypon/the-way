import socket

HEADER_SIZE = 10

sock_serv = socket.socket()
sock_serv.bind(('localhost', 444))
sock_serv.listen(5)

while True:
    conn, addr = sock_serv.accept()
    full_message = ''
    new_message = True
    while True:
        msg = conn.recv(50)
        if new_message:
            msg_len = int(msg[:HEADER_SIZE])
            new_message = False
        print(f'Message\'s length is : {msg_len}')
        full_message += msg.decode('utf-8')

        if len(full_message) - HEADER_SIZE == msg_len:
            conn.send(full_message.encode('utf-8'))
            new_message = True
