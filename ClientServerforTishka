import socket
import time

Client_socket =socket.socket()
Client_socket.connect(('localhost', 2222))

while True:
    msg = input('>>> ')
    Client_socket.send(msg.encode('utf-8'))
    # чтобы успеть получить сообщение
    time.sleep(0.5)
    data = Client_socket.recv(1024)
    print(data.decode('utf-8'))
    if msg == '!exit':
        Client_socket.close()


