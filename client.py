import zlib
import yaml
import socket
import json
from datetime import datetime
from argparse import ArgumentParser

WRITE_MODE = 'write'

READ_MODE = 'read'

def make_request(action, data):
    return {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data,
    }

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False,
    help='sets config file path'
)

parser.add_argument(
    '-m', '--mode', type=str, required=True, default=WRITE_MODE,
    help='sets client mode'
)
args = parser.parse_args()

config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        config.update(file_config)

host, port = config.get('host'), config.get('port')


try:
    sock = socket.socket()
    sock.connect((host, port))
    print('client started')

    while True:
        if args.mode == WRITE_MODE:
            action = input('enter action: ')
            data = input('enter data: ')

            request = make_request(action, data)
            str_request = json.dumps(request)
            bytes_request = zlib.compress(str_request.encode())

            sock.send(bytes_request)
            print(f'client sent data { data }')
        elif args.mode == READ_MODE:
            response = sock.recv(config.get('buffersize'))
            bytes_response = zlib.decompress(response)
            print(f'server sent data { bytes_response.decode() }')

except KeyboardInterrupt:
    print('client shutdown')