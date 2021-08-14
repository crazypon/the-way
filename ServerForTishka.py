import socket
import threading
import sys


sock_serv = socket.socket()
sock_serv.bind(('localhost', 222))
sock_serv.listen(5)
exit_event = threading.Event()


HEADER_SIZE = 10

def client_handler():
    conn, addr = sock_serv.accept()
    print(f'Got connection from {addr}')
    full_message = b''
    while True:
        try:
            data = conn.recv(4096)
        except:
            print(f'{addr} disconnected')
            global num_of_threads
            num_of_threads -= 1
            conn.close()
            break

        if not data:
            conn.close()
            break
        full_message += data
        if len(full_message) >= 10:
            msg_len = HEADER_SIZE + int(full_message[:HEADER_SIZE])
            if len(full_message) >= msg_len:
                conn.sendall(full_message[:msg_len])
                full_message = full_message[msg_len:]



# Нужно придумать механизм повторного активирования тредов
try:
    num_of_threads = 1
    while True:
        while num_of_threads != 6:
            threading.Thread(target=client_handler).start()
            num_of_threads += 1
except KeyboardInterrupt:
    print('Server is stopping !!!')
    if threading.active_count() == 1:
        sys.exit(1)

