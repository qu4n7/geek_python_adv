import pytest
from controllers import send_message

@pytest.fixture
def valid_action_names():
    return {'action': 'send', 'controller': send_message}

def test_valid_names(valid_action_names):
    is_valid = valid_action_names
    assert is_valid