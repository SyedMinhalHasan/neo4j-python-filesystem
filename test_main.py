import pytest
from fastapi.testclient import TestClient
from main import app, execute_query

client = TestClient(app)

# ############ Add DIRECTORIES  ############
def mock_execute_query_add_directory(query, parameters):
    # Simulate a response from the database
    return [{'d': {'name': parameters['name']}}]

def test_add_directory_with_parent():
    app.dependency_overrides[execute_query] = mock_execute_query_add_directory

    response = client.post("/add_directory/", params={"name": "Test Directory", "parent_directory_id": 4})
    assert response.status_code == 200
    assert response.json() == {'d': {'name': "Test Directory"}}

    # Clean up
    del app.dependency_overrides[execute_query]

def test_add_directory_without_parent():
    app.dependency_overrides[execute_query] = mock_execute_query_add_directory

    response = client.post("/add_directory/", params={"name": "Test Directory"})
    assert response.status_code == 200
    assert response.json() == {'d': {'name': "Test Directory"}}

    # Clean up
    del app.dependency_overrides[execute_query]

def test_add_directory_no_name():
    # Test adding a directory without a name
    response = client.post("/add_directory/", json={})
    assert response.status_code == 422  # Expecting a validation error

############ Add FILES  ############

# Override the execute_query dependency
def mock_execute_query_add_file(query, parameters):
    # Simulate a response from the database
    return [{'f': {'name': parameters['name'], 'content': parameters['content']}}]

def test_add_file_with_parent():
    app.dependency_overrides[execute_query] = mock_execute_query_add_file

    response = client.post("/add_file/", params={"name": "Test File", "content": "File Content", "parent_directory_id": 5})
    assert response.status_code == 200
    assert response.json() == {'f': {'name': "Test File", 'content': "File Content"}}

    # Clean up
    del app.dependency_overrides[execute_query]

def test_add_file_without_parent():
    app.dependency_overrides[execute_query] = mock_execute_query_add_file

    response = client.post("/add_file/", params={"name": "Test File", "content": "File Content"})
    assert response.status_code == 200
    assert response.json() == {'f': {'name': "Test File", 'content': "File Content"}}

    # Clean up
    del app.dependency_overrides[execute_query]


def test_add_file_no_name_or_content():
    # Test adding a file without a name or content
    response = client.post("/add_file/", json={})
    assert response.status_code == 422  # Expecting a validation error

############ Read FILES  ############

def test_read_file():
    # Mock the execute_query function to return File Content
    app.dependency_overrides[execute_query] = lambda query, parameters=None: None

    # Test reading a file that does exist
    response = client.get("/read_file/10")
    assert response.status_code == 200
    assert response.json() == {'content': 'content'}

def test_read_file_not_found():
    # Mock the execute_query function to return None
    app.dependency_overrides[execute_query] = lambda query, parameters=None: None

    # Test reading a file that does not exist
    response = client.get("/read_file/1")
    assert response.status_code == 404

############ Add USERS  ############
    
def test_add_user():
    # Override the execute_query dependency
    def mock_execute_query(query, parameters):
        return [{'u': {'name': parameters['name']}}]

    app.dependency_overrides[execute_query] = mock_execute_query

    response = client.post("/add_user/", params={"name": "MK User"})
    assert response.status_code == 200
    assert response.json() == {'u': {'name': "MK User"}}

    # Clean up / reset the override
    del app.dependency_overrides[execute_query]

def test_add_user_no_name():
    # Test adding a user without a name
    response = client.post("/add_user/", json={})
    assert response.status_code == 422  # Expecting a validation error
