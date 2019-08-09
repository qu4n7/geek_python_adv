import pytest 
from settings import INSTALLED_APPS

@pytest.fixture
def valid_apps():
    return {
        'echo',
        'messenger'
    }

def test_valid_apps():
    assert INSTALLED_APPS == valid_apps