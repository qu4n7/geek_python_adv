import yaml
import socket
import json
from datetime import datetime
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str, required=False,
    help='sets config file path'
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
    
    action = input('enter action: ')
    data = input('enter data: ')

    request = {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data,
    }

    str_request = json.dumps(request)

    sock.send(str_request.encode())
    print(f'client sends data { data }')

    b_response = sock.recv(config.get('buffersize'))
    print(f'server send data { b_response.decode() }')

except KeyboardInterrupt:
    print('client shutdown')