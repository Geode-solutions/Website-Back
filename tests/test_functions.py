import os
import pytest
from app import app
from flask import url_for


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'TEST'
    client = app.test_client()
    with app.app_context():
        pass
    app.app_context().push()
    yield client


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200