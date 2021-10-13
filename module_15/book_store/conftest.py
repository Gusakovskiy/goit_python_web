import pytest
from module_15.book_store.app import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    client = TestClient(app)
    yield client
