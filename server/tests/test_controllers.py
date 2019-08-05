import pytest 
from datetime import datetime

from controllers import send_message
from protocol import make_response, validate_request

@pytest.fixture 
def expected_code():
    return 200

@pytest.fixture
def valid_request(expected_action, expected_data):
    return {
        'action': expected_action,
        'time': datetime.now().timestamp(),
        'data': expected_data,
    }

def test_send_message(valid_request, valid_code):
    is_valid = send_message(valid_request, valid_code)
    assert is_valid