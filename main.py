from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase
from typing import Optional

app = FastAPI()

# Establishing connection parameters for Neo4j database
uri = "neo4j://localhost:7687"  # Update with your Neo4j server URI
username = "neo4j"
password = "Cipher$1357"  # Update with your Neo4j password

# Creating a database driver instance for Neo4j
driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to execute a given Cypher query against the Neo4j database
def execute_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record.data() for record in result]

# Endpoint to add a new directory node
@app.post("/add_directory/")
def add_directory(name: str, parent_directory_id: Optional[int] = None):
    if parent_directory_id is not None:
        query = """
        CREATE (d:Directory {name: $name})
        WITH d
        MATCH (pd:Directory) WHERE ID(pd) = $parent_directory_id
        CREATE (d)-[:HAS_PARENT]->(pd)
        RETURN d
        """
        result = execute_query(query, {'name': name, 'parent_directory_id': parent_directory_id})
    else:
        query = """
        CREATE (d:Directory {name: $name})
        RETURN d
        """
        result = execute_query(query, {'name': name})
    return result[0] if result else {}

# Endpoint to add a new file node (separate or inside any directory)
@app.post("/add_file/")
def add_file(name: str, content: str, parent_directory_id: Optional[int] = None):
    if parent_directory_id is not None:
        query = """
        CREATE (f:File {name: $name, content: $content})
        WITH f
        MATCH (d:Directory) WHERE ID(d) = $parent_directory_id
        CREATE (f)-[:HAS_PARENT]->(d)
        RETURN f
        """
        result = execute_query(query, {'name': name, 'content': content, 'parent_directory_id': parent_directory_id})
    else:
        query = """
        CREATE (f:File {name: $name, content: $content})
        RETURN f
        """
        result = execute_query(query, {'name': name, 'content': content})
    return result[0] if result else {}

# Endpoint to add a new user node
@app.post("/add_user/")
def add_user(name: str):
    query = """
    CREATE (u:User {name: $name})
    RETURN u
    """
    result = execute_query(query, {'name': name})
    return result[0] if result else {}

# Endpoint to read content of a file node by ID
@app.get("/read_file/{file_id}")
def read_file(file_id: int):
    query = """
    MATCH (f:File) WHERE ID(f)=$file_id
    RETURN f.content AS content
    """
    result = execute_query(query, {'file_id': file_id})
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="File not found")

# Endpoint to associate a node (file or directory) with a user as owner
@app.post("/add_owner/{node_id}")
def add_owner(node_id: int, user_id: int):
    query = """
    MATCH (u:User) WHERE ID(u) = $user_id
    OPTIONAL MATCH (f:File) WHERE ID(f) = $node_id
    OPTIONAL MATCH (d:Directory) WHERE ID(d) = $node_id
    WITH u, COALESCE(f, d) AS node
    WHERE node IS NOT NULL
    CREATE (node)-[:OWNED_BY]->(u)
    RETURN node, u
    """
    return execute_query(query, {'node_id': node_id, 'user_id': user_id})

# Endpoint to remove ownership of a file from a user
@app.delete("/remove_file_owner/{file_id}")
def remove_file_owner(file_id: int, user_id: int):
    query = """
    MATCH (f:File)-[r:OWNED_BY]->(u:User) 
    WHERE ID(f) = $file_id AND ID(u) = $user_id
    DELETE r
    RETURN f, u
    """
    return execute_query(query, {'file_id': file_id, 'user_id': user_id})

# Endpoint to list direct children of a directory
@app.get("/list_directory/{directory_id}")
def list_directory(directory_id: int):
    query ="""
    MATCH (parent:Directory) 
    WHERE ID(parent) = $directory_id
    MATCH (f:File)-[:HAS_PARENT]->(parent)
    RETURN f AS child
    UNION
    MATCH (parent:Directory)
    WHERE ID(parent) = $directory_id
    MATCH (d:Directory)-[:HAS_PARENT]->(parent)
    RETURN d AS child
    """
    return execute_query(query, {'directory_id': directory_id})

# Endpoint to recursively list all descendants of a directory
@app.get("/list_directory_recursive/{directory_id}")
def list_directory_recursive(directory_id: int):
    query ="""
    MATCH (parent:Directory) WHERE ID(parent) = $directory_id
    MATCH (child)-[:HAS_PARENT*0..]->(parent)
    WHERE (child:File OR child:Directory)
    RETURN DISTINCT child
    """
    return execute_query(query, {'directory_id': directory_id})

# Endpoint to delete a node (file, directory, or user) and its relationships
@app.delete("/delete_node/{node_id}")
def delete_node(node_id: int):
    query = """
    MATCH (n)
    WHERE ID(n) = $node_id AND (n:Directory OR n:User OR n:File)
    OPTIONAL MATCH (n)<-[r:HAS_PARENT*]-(child)
    OPTIONAL MATCH (n)<-[o:OWNED_BY*]-(child)
    DETACH DELETE n, child
    """
    return execute_query(query, {'node_id': node_id})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)