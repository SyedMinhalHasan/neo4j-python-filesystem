import pytest
from fastapi.testclient import TestClient
from main import app, execute_query

client = TestClient(app)

############ Add OWNERS  ############

def test_add_directory():
    # Mock the execute_query function to return a predictable result
    app.dependency_overrides[execute_query] = lambda query, parameters=None: [{'name': parameters['name']}]

    # Test adding a directory without a parent directory id
    response = client.post("/add_directory/", json={'name': 'Test Directory', 'parent_directory_id': ''})
    print(response)
    assert response.status_code == 200
    assert response.json() == {'name': 'Test Directory'}

    # Test adding a directory with a parent directory id
    response = client.post("/add_directory/", json={'name': 'Test Directory', 'parent_directory_id': 1})
    assert response.status_code == 200
    assert response.json() == {'name': 'Test Directory'}

def test_add_directory_no_name():
    # Test adding a directory without a name
    response = client.post("/add_directory/", json={})
    assert response.status_code == 422  # Expecting a validation error

# ############ Add FILES  ############

def test_add_file():
    # Mock the execute_query function to return a predictable result
    app.dependency_overrides[execute_query] = lambda query, parameters=None: [{'name': parameters['name'], 'content': parameters['content']}]

    # Test adding a file without a parent directory id
    response = client.post("/add_file/", json={'name': 'Test File', 'content': 'Test Content'})
    assert response.status_code == 200
    assert response.json() == {'name': 'Test File', 'content': 'Test Content'}

    # Test adding a file with a parent directory id
    response = client.post("/add_file/", json={'name': 'Test File', 'content': 'Test Content', 'parent_directory_id': 1})
    assert response.status_code == 200
    assert response.json() == {'name': 'Test File', 'content': 'Test Content'}

def test_add_file_no_name_or_content():
    # Test adding a file without a name or content
    response = client.post("/add_file/", json={})
    assert response.status_code == 422  # Expecting a validation error


############ Add USERS  ############
    
# def test_add_user():
    # Mock the execute_query function to return a predictable result
    app.dependency_overrides[execute_query] = lambda query, parameters=None: [{'name': parameters['name']}]

    # Test adding a user
    response = client.post("/add_user/", json={'name': 'Test User'})
    assert response.status_code == 200
    assert response.json() == {'name': 'Test User'}

# def test_add_user_no_name():
    # Test adding a user without a name
    response = client.post("/add_user/", json={})
    assert response.status_code == 422  # Expecting a validation error


########### Read FILES  ############

def test_read_file():
    # Mock the execute_query function to return a predictable result
    app.dependency_overrides[execute_query] = lambda query, parameters=None: [{'content': 'Test Content'}]

    # Test reading a file
    response = client.get("/read_file/1")
    assert response.status_code == 200
    assert response.json() == {'content': 'Test Content'}

def test_read_file_not_found():
    # Mock the execute_query function to return None
    app.dependency_overrides[execute_query] = lambda query, parameters=None: None

    # Test reading a file that does not exist
    response = client.get("/read_file/1")
    assert response.status_code == 404

############ Add OWNERS  ############

def test_add_owner():
    # Mock the execute_query function to return a predictable result
    app.dependency_overrides[execute_query] = lambda query, parameters=None: [{'node': {'id': parameters['node_id']}, 'user': {'id': parameters['user_id']}}]

    # Test adding an owner to a node
    response = client.post("/add_owner/1", json={'user_id': 1})
    assert response.status_code == 200
    assert response.json() == {'node': {'id': 1}, 'user': {'id': 1}}

def test_remove_file_owner():
    # Mock the execute_query function to return a predictable result
    app.dependency_overrides[execute_query] = lambda query, parameters=None: [{'file': {'id': parameters['file_id']}, 'user': {'id': parameters['user_id']}}]

    # Test removing an owner from a file
    response = client.delete("/remove_file_owner/1", json={'user_id': 1})
    assert response.status_code == 200
    assert response.json() == {'file': {'id': 1}, 'user': {'id': 1}}

############ List DIRECTORIES  ############

def test_list_directory():
    # Mock the execute_query function to return a predictable result
    app.dependency_overrides[execute_query] = lambda query, parameters=None: [{'child': {'id': 1}}]

    # Test listing a directory
    response = client.get("/list_directory/1")
    assert response.status_code == 200
    assert response.json() == [{'child': {'id': 1}}]

############ List DIRECTORIES Recursive  ############

def test_list_directory_recursive():
    # Mock the execute_query function to return a predictable result
    app.dependency_overrides[execute_query] = lambda query, parameters=None: [{'child': {'id': 1}}]

    # Test listing a directory recursively
    response = client.get("/list_directory_recursive/1")
    assert response.status_code == 200
    assert response.json() == [{'child': {'id': 1}}]

############ Delete NODES  ############

def test_delete_node():
    # Mock the execute_query function to return a predictable result
    app.dependency_overrides[execute_query] = lambda query, parameters=None: [{'node': {'id': parameters['node_id']}}]

#     # Test deleting a node
    response = client.delete("/delete_node/1")
    assert response.status_code == 200
    assert response.json() == [{'node': {'id': 1}}]