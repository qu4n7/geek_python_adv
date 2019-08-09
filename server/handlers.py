import json
import logging

from actions import resolve
from protocol import validate_request, make_response
from middlewares import compression_middleware, encryption_middleware


@compression_middleware
@encryption_middleware
def handle_default_request(bytes_request):
    request = json.loads(bytes_request.decode())
    
    if validate_request(request):
        actions_name = request.get('action')
        controller = resolve(actions_name)
        if controller:
            try:
                logging.info(f'Client send valid request {request}')
                response = controller(request)
            except Exception as err:
                logging.info(f'Internal server error: {err}')
                response = make_response(request, 500, data='Internal server error')
        else:
            logging.info(f'Controller with action name {actions_name} does not exists')
            response = make_response(request, 404, 'Action not found')
    else:
        logging.info(f'Client send invalid request {request}')
        response = make_response(request, 404, 'Wrong request')

    str_response = json.dumps(response)
    return str_response.encode()