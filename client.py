import json, socket
import time

class Client(object):
    socket = None

    def __del__(self):
        self.close()

    def connect(self, host, port):
        self.socket = socket.socket()
        self.socket.connect((host, port))
        return self

    def send(self, data):
        if not self.socket:
            raise Exception('необходимо подключиться перед отправкой')
        _send(self.socket, data)
        return self

    def recv(self):
        if not self.socket:
            raise Exception('необходимо подключиться перед получением')
        return _recv(self.socket)

    def recv_and_close(self):
        data = self.recv()
        self.close()
        return data

    def close(self):
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

i=1
while True:
	client = Client()
	client.connect(host, port).send({'test':i})
	i+=1
	response = client.recv()
	print(response)
	client.close()
	time.sleep(1)