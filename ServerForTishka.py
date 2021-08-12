import socket
import threading


HEADER_SIZE = 10

sock_serv = socket.socket()
sock_serv.bind(('localhost', 337))
sock_serv.listen(5)
exit_event = threading.Event()

def client_handler(conn, addr):
    print(f'Got connection from {addr}')
    full_message = b''
    while True:
        data = conn.recv(4096)
        full_message += data
        if len(full_message) >= 10:
            msg_len = HEADER_SIZE + int(full_message[:HEADER_SIZE])
            if full_message[HEADER_SIZE:msg_len] == '!stopserver'.encode('utf-8'):
                print(f'Connection {addr} has closed !')
                conn.send(full_message[:msg_len])
                conn.close()
                break
            if len(full_message) >= msg_len:
                conn.sendall(full_message[:msg_len])
                full_message = full_message[msg_len:]


while True:
    connection, address = sock_serv.accept()
    if connection:
        threading.Thread(target=client_handler, args=(connection,address,)).start()
