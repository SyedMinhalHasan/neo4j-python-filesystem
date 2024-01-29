import pytest
from fastapi.testclient import TestClient
from main import app, execute_query

client = TestClient(app)

def test_add_directory_no_name():
    # Test adding a directory without a name
    response = client.post("/add_directory/", json={})
    assert response.status_code == 422  # Expecting a validation error

def test_add_file_no_name_or_content():
    # Test adding a file without a name or content
    response = client.post("/add_file/", json={})
    assert response.status_code == 422  # Expecting a validation error


def test_read_file_not_found():
    # Mock the execute_query function to return None
    app.dependency_overrides[execute_query] = lambda query, parameters=None: None

    # Test reading a file that does not exist
    response = client.get("/read_file/1")
    assert response.status_code == 404
