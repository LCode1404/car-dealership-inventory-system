
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.models import User
from app.security import create_access_token, hash_password

from app.database import Base, get_db
from app.main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        db = TestingSessionLocal()

        admin = User(
            username="testadmin",
            email="admin@test.com",
            hashed_password=hash_password("TestAdmin123!"),
            role="admin",
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        token = create_access_token(admin.id, admin.role)
        test_client.headers.update(
            {"Authorization": f"Bearer {token}"}
        )
        db.close()

        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_vehicle(client):
    vehicle = {
        "make": "Toyota",
        "model": "Camry",
        "category": "Sedan",
        "price": 25000,
        "quantity": 5,
    }

    response = client.post("/api/vehicles", json=vehicle)

    assert response.status_code == 201
    data = response.json()
    assert data["make"] == "Toyota"
    assert data["model"] == "Camry"
    assert data["quantity"] == 5
    assert "id" in data


def test_list_vehicles(client):
    client.post(
        "/api/vehicles",
        json={
            "make": "Honda",
            "model": "Civic",
            "category": "Sedan",
            "price": 22000,
            "quantity": 3,
        },
    )

    response = client.get("/api/vehicles")

    assert response.status_code == 200
    vehicles = response.json()
    assert len(vehicles) == 1
    assert vehicles[0]["make"] == "Honda"


def test_search_vehicles_by_make(client):
    client.post(
        "/api/vehicles",
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 25000,
            "quantity": 5,
        },
    )

    client.post(
        "/api/vehicles",
        json={
            "make": "Honda",
            "model": "Civic",
            "category": "Sedan",
            "price": 22000,
            "quantity": 3,
        },
    )

    response = client.get(
        "/api/vehicles/search",
        params={"make": "Toyota"},
    )

    assert response.status_code == 200
    vehicles = response.json()
    assert len(vehicles) == 1
    assert vehicles[0]["make"] == "Toyota"


def test_search_vehicles_by_price_range(client):
    for vehicle in [
        {
            "make": "Toyota",
            "model": "Corolla",
            "category": "Sedan",
            "price": 20000,
            "quantity": 4,
        },
        {
            "make": "BMW",
            "model": "X5",
            "category": "SUV",
            "price": 60000,
            "quantity": 2,
        },
    ]:
        client.post("/api/vehicles", json=vehicle)

    response = client.get(
        "/api/vehicles/search",
        params={"min_price": 15000, "max_price": 30000},
    )

    assert response.status_code == 200
    vehicles = response.json()
    assert len(vehicles) == 1
    assert vehicles[0]["model"] == "Corolla"


def test_update_vehicle(client):
    created = client.post(
        "/api/vehicles",
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 25000,
            "quantity": 5,
        },
    )
    vehicle_id = created.json()["id"]

    response = client.put(
        f"/api/vehicles/{vehicle_id}",
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 27000,
            "quantity": 5,
        },
    )

    assert response.status_code == 200
    assert response.json()["price"] == 27000


def test_delete_vehicle(client):
    created = client.post(
        "/api/vehicles",
        json={
            "make": "Honda",
            "model": "Civic",
            "category": "Sedan",
            "price": 22000,
            "quantity": 3,
        },
    )
    vehicle_id = created.json()["id"]

    response = client.delete(f"/api/vehicles/{vehicle_id}")

    assert response.status_code == 204
    assert client.get("/api/vehicles").json() == []


def test_purchase_vehicle_decreases_quantity(client):
    created = client.post(
        "/api/vehicles",
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 25000,
            "quantity": 5,
        },
    )
    vehicle_id = created.json()["id"]

    response = client.post(f"/api/vehicles/{vehicle_id}/purchase")

    assert response.status_code == 200
    assert response.json()["quantity"] == 4


def test_cannot_purchase_vehicle_with_zero_stock(client):
    created = client.post(
        "/api/vehicles",
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 25000,
            "quantity": 0,
        },
    )
    vehicle_id = created.json()["id"]

    response = client.post(f"/api/vehicles/{vehicle_id}/purchase")

    assert response.status_code == 409


def test_restock_vehicle(client):
    created = client.post(
        "/api/vehicles",
        json={
            "make": "Toyota",
            "model": "Camry",
            "category": "Sedan",
            "price": 25000,
            "quantity": 2,
        },
    )
    vehicle_id = created.json()["id"]

    response = client.post(
        f"/api/vehicles/{vehicle_id}/restock",
        json={"quantity": 3},
    )

    assert response.status_code == 200
    assert response.json()["quantity"] == 5


from fastapi.testclient import TestClient
from app.main import app


def test_register_new_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "SecurePass123!",
        },
    )

    assert response.status_code in (200, 201)
    assert response.json()["email"] == "newuser@example.com"
    assert "hashed_password" not in response.json()


def test_register_duplicate_email(client):
    user_data = {
        "username": "duplicateuser",
        "email": "duplicate@example.com",
        "password": "SecurePass123!",
    }

    first_response = client.post("/api/auth/register", json=user_data)
    second_response = client.post("/api/auth/register", json=user_data)

    assert first_response.status_code in (200, 201)
    assert second_response.status_code == 409


def test_login_with_valid_credentials(client):
    user_data = {
        "username": "loginuser",
        "email": "loginuser@example.com",
        "password": "SecurePass123!",
    }

    registration = client.post("/api/auth/register", json=user_data)
    assert registration.status_code in (200, 201)

    response = client.post(
        "/api/auth/login",
        json={
            "email": user_data["email"],
            "password": user_data["password"],
        },
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_login_with_wrong_password(client):
    user_data = {
        "username": "wrongpassuser",
        "email": "wrongpass@example.com",
        "password": "SecurePass123!",
    }

    registration = client.post("/api/auth/register", json=user_data)
    assert registration.status_code in (200, 201)

    response = client.post(
        "/api/auth/login",
        json={
            "email": user_data["email"],
            "password": "IncorrectPassword123!",
        },
    )

    assert response.status_code == 401


def test_protected_endpoint_without_token():
    unauthenticated_client = TestClient(app)

    response = unauthenticated_client.get("/api/vehicles")

    assert response.status_code == 401



