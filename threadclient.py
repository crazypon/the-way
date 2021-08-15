import socket

HEADER_SIZE = 10
sock_serv = socket.socket()
sock_serv.connect(('localhost', 777))

full_message = b''

while True:
    while True:
        text = input('>>> ')
        msg = f'{len(text):<10}' + text
        sock_serv.send(msg.encode('utf-8'))
        break
    try:
        data = sock_serv.recv(4096)
    except ConnectionResetError:
        print('Connection has been closed')

    full_message += data
    if len(full_message) >= 10:
        msg_len = HEADER_SIZE + int(full_message[:HEADER_SIZE])
        if len(full_message) >= msg_len:
            payload = full_message[HEADER_SIZE:msg_len]
            print(payload.decode('utf-8'))
            full_message = full_message[msg_len:]
