import socket

HEADER_SIZE = 10

sock_serv = socket.socket()
sock_serv.connect(('localhost', 444))

while True:
    text = input('>>> ')
    message = f'{len(text):<{HEADER_SIZE}}' + text
    sock_serv.send(message.encode('utf-8'))

    full_message = ''
    new_message = True
    while True:
        msg = sock_serv.recv(50)
        if new_message:
            msg_len = int(msg[:HEADER_SIZE])
            new_message = False
        full_message += msg.decode('utf-8')

        if len(full_message) - HEADER_SIZE == msg_len:
            print(full_message[HEADER_SIZE:])
            new_message = True
