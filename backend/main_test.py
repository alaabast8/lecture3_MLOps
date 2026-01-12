import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Import your app and DB setup
from main import app, get_db, Base

# 1. Load Environment Variables
load_dotenv()

# 2. Setup Test Database
TEST_DATABASE_URL = os.getenv("DATABASE_TEST_URL")

if not TEST_DATABASE_URL:
    raise ValueError("DATABASE_TEST_URL not found in .env file")

# Create a specific engine for testing
test_engine = create_engine(TEST_DATABASE_URL)

# Create a specific session for testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# 3. Override the get_db dependency
# This ensures tests use the Test DB, not the Production DB
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# 4. Pytest Fixture to reset DB for every test
@pytest.fixture(autouse=True)
def test_db_setup():
    """
    Creates tables before each test and drops them after.
    This ensures a clean slate for every test function.
    """
    # Create tables in the test database
    Base.metadata.create_all(bind=test_engine)
    yield
    # Drop tables after the test runs
    Base.metadata.drop_all(bind=test_engine)

# --- TESTS ---

# Note: I removed test_read_root because your main.py does not have a "/" endpoint defined.

def test_create_item():
    response = client.post(
        "/api/items", 
        json={"name": "Test Item", "description": "Test Description"}
    )
    assert response.status_code == 200
    data = response.json()
    # main.py returns the item object directly, not wrapped in a message
    assert data["name"] == "Test Item"
    assert "id" in data

def test_get_items():
    # Add an item first
    client.post(
        "/api/items", 
        json={"name": "Test Item", "description": "Test Description"}
    )
    
    response = client.get("/api/items")
    assert response.status_code == 200
    data = response.json()
    
    # main.py returns a list directly: [{}, {}]
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Test Item"

def test_create_and_retrieve_item():
    # Create item
    create_response = client.post(
        "/api/items", 
        json={"name": "Integration Test", "description": "Testing flow"}
    )
    assert create_response.status_code == 200
    
    # Retrieve all items
    get_response = client.get("/api/items")
    assert get_response.status_code == 200
    data = get_response.json()
    
    assert len(data) == 1
    assert data[0]["name"] == "Integration Test"

def test_multiple_items_workflow():
    # Create multiple items
    res1 = client.post("/api/items", json={"name": "Item 1", "description": "First"})
    res2 = client.post("/api/items", json={"name": "Item 2", "description": "Second"})
    
    # Get the ID of the second item specifically (to be safe, don't assume ID is always 2)
    item_2_id = res2.json()["id"]

    # Get specific item
    response = client.get(f"/api/items/{item_2_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Item 2"