import pytest # required to initiate textures

from datetime import datetime
from protocol import make_response

# fixtures required in case you need to link to some external db-s
@pytest.fixture 
def expected_action():
    return 'test'

@pytest.fixture 
def expected_code():
    return 200

@pytest.fixture 
def expected_data():
    return 'some data'

@pytest.fixture
def initial_request(expected_action, expected_data):
    return {
        'action': expected_action,
        'time': datetime.now().timestamp(),
        'data': expected_data,
    }

'''
# in case textures are not ised
ACTION = 'test'
CODE = 200
DATA = 'some data'
REQUEST = {
    'action': ACTION,
    'time': datetime.now().timestamp(),
    'data': DATA,
}
RESPONSE = {
    'action': ACTION,
    'time': datetime.now().timestamp(),
    'code': 200,
    'data': DATA,
}
def test_action_make_reponse():
    actual_response = make_response(REQUEST, CODE, DATA)
    assert actual_response.get('action') == ACTION
def test_code_make_reponse():
    actual_response = make_response(REQUEST, CODE, DATA)
    assert actual_response.get('code') == CODE
def test_data_make_reponse():
    actual_response = make_response(REQUEST, CODE, DATA)
    assert actual_response.get('data') == DATA
'''

def test_action_make_reponse(initial_request, expected_action, expected_code, expected_data):
    actual_response = make_response(
        initial_request, expected_code, expected_data
        )
    assert actual_response.get('action') == expected_action

def test_code_make_reponse(initial_request, expected_action, expected_code, expected_data):
    actual_response = make_response(
        initial_request, expected_code, expected_data
        )
    assert actual_response.get('code') == expected_code

def test_data_make_reponse(initial_request, expected_action, expected_code, expected_data):
    actual_response = make_response(
        initial_request, expected_code, expected_data
        )
    assert actual_response.get('data') == expected_data