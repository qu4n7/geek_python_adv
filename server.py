import json, socket

class Server(object):
    backlog = 5
    client = None

    def __init__(self, host, port):
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.socket.listen(self.backlog)

    def __del__(self):
        self.close()

    def accept(self):
        # if a client is already connected, disconnect it
        if self.client:
            self.client.close()
        self.client, self.client_addr = self.socket.accept()
        return self

    def send(self, data):
        if not self.client:
            raise Exception('невозможно отправить данные, не подключен клиент')
        _send(self.client, data)
        return self

    def recv(self):
        if not self.client:
            raise Exception('невозможно получить данные, не подключен сервер')
        return _recv(self.client)

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
        if self.socket:
            self.socket.close()
            self.socket = None

def _send(socket, data):
    try:
        serialized = json.dumps(data)
    except (TypeError, ValueError):
        raise Exception('возможна отправка только json форматов')
    socket.send('%d\n' % len(serialized))
    socket.sendall(serialized)

def _recv(socket):
    length_str = ''
    char = socket.recv(1)
    while char != '\n':
        length_str += char
        char = socket.recv(1)
    total = int(length_str)
    view = memoryview(bytearray(total))
    next_offset = 0
    while total - next_offset > 0:
        recv_size = socket.recv_into(view[next_offset:], total - next_offset)
        next_offset += recv_size
    try:
        deserialized = json.loads(view.tobytes())
    except (TypeError, ValueError):
        raise Exception('данные получены не в формате json')
    return deserialized

host = 'localhost'
port = 8080

server = Server(host, port)

while True:
    server.accept()
    data = server.recv()
    server.send({'ответ':data})
    
server.close()