from http import client
from urllib import response
from fastapi.testclient import TestClient
from app import app


client = TestClient(app)

def test_get_main():
    response= client.get('/')
    assert response.status_code == 200