import socket
import select
import queue

server = socket.socket()
server.bind(('localhost', 777))
server.listen(5)

reads = [server]
writes = []

# сюда мы помещаем сообщения которые получили от определенного клиента это помогает нам не ошибится клиентом и случайно
# никому другому не отправить его

message_queues = {}
while True:
    '''
    select.select он смотрит какое соединение готово для чтения, отправки и ошибок. Он когда обслуживает клиента 
    сам временно делает его неблокирующим !
    '''
    readies, writies, excepts = select.select(reads, writes, reads)
    for s in readies:
        if s is server:
            client, address = s.accept()
            reads.append(client)
            message_queues[client] = queue.Queue()
        else:
            # Из тестов я понял что нельзя использовать цикл while так как он блокирует, но также ведь нужно получить
            # все байты поэтому сделал все то же но без бесконечного цикла я отключаю его когда приходит все сообщение
            # дальше если надо select сам еще раз запускает это наш цикл и все  !
            HEADER_SIZE = 10
            full_message = b''
            while True:
                try:
                    data = s.recv(4096)
                except:
                    if s in writes:
                        writes.remove(s)
                    reads.remove(s)
                    s.close()
                    del message_queues[s]
                    break
                full_message += data
                if len(full_message) >= 10:
                    msg_len = HEADER_SIZE + int(full_message[:HEADER_SIZE])
                    if len(full_message) >= msg_len:

                        print(full_message[HEADER_SIZE:msg_len].decode('utf-8'))
                        break

            message_queues[s].put(data)
            if s not in writes:
                writes.append(s)

    for s in writes:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            writes.remove(s)
        else:
            s.send(next_msg)

    for s in excepts:
        # Stop listening for input on the connection
        reads.remove(s)
        if s in writes:
            writes.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]
