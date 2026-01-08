import pytest
from fastapi.testclient import TestClient
from main import app, items_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_items():
    """Clear items before each test"""
    items_db.clear()
    yield
    items_db.clear()

# Unit Test 1: Test root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "environment" in response.json()

# Unit Test 2: Test create item
def test_create_item():
    response = client.post("/api/items", json={"name": "Test Item", "description": "Test Description"})
    assert response.status_code == 200
    assert response.json()["message"] == "Item created"
    assert response.json()["item"]["name"] == "Test Item"

# Unit Test 3: Test get items
def test_get_items():
    # Add an item first
    client.post("/api/items", json={"name": "Test Item", "description": "Test Description"})
    response = client.get("/api/items")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1
    

# Integration Test 1: Create and retrieve item
def test_create_and_retrieve_item():
    # Create item
    create_response = client.post("/api/items", json={"name": "Integration Test", "description": "Testing flow"})
    assert create_response.status_code == 200
    
    # Retrieve all items
    get_response = client.get("/api/items")
    assert get_response.status_code == 200
    assert len(get_response.json()["items"]) == 1
    assert get_response.json()["items"][0]["name"] == "Integration Test"

# Integration Test 2: Create multiple items and retrieve specific one
def test_multiple_items_workflow():
    # Create multiple items
    client.post("/api/items", json={"name": "Item 1", "description": "First"})
    client.post("/api/items", json={"name": "Item 2", "description": "Second"})
    
    # Get specific item
    response = client.get("/api/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Item 2"