import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Welcome to Agent Marketplace API"


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_register_user():
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_login_user():
    """Test user login"""
    # First register a user
    client.post(
        "/auth/register",
        json={
            "username": "logintest",
            "email": "login@example.com",
            "password": "testpassword123"
        }
    )
    
    # Then login
    response = client.post(
        "/auth/login",
        data={
            "username": "logintest",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_create_agent():
    """Test agent creation"""
    # Register and login
    client.post(
        "/auth/register",
        json={
            "username": "agentcreator",
            "email": "creator@example.com",
            "password": "testpassword123"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": "agentcreator",
            "password": "testpassword123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Create agent
    response = client.post(
        "/agents/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Agent",
            "description": "A test agent",
            "code": "result = 'test'",
            "tags": "test",
            "is_public": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Agent"
    assert data["is_public"] == True


def test_list_agents():
    """Test listing agents"""
    response = client.get("/agents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_unauthorized_create_agent():
    """Test that creating an agent without auth fails"""
    response = client.post(
        "/agents/",
        json={
            "name": "Unauthorized Agent",
            "code": "result = 'test'"
        }
    )
    assert response.status_code == 401


# Cleanup
@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup test database after all tests"""
    def remove_test_db():
        import os
        if os.path.exists("./test.db"):
            os.remove("./test.db")
    request.addfinalizer(remove_test_db)
