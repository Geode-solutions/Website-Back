import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'TEST'
    client = app.test_client()
    yield client
