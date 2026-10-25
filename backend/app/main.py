
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import os
import secrets

from fastapi import Header
from app.models import User
from app.schemas import UserRegister, UserResponse
from app.security import hash_password

from app import models
from app.auth import get_current_user, require_admin
from app.database import Base, engine, get_db
from app.models import User
from app.schemas import (
    LoginRequest,
    RestockRequest,
    TokenResponse,
    UserRegister,
    UserResponse,
    VehicleCreate,
    VehicleResponse,
)
from app.security import (
    create_access_token,
    hash_password,
    verify_password,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Car Dealership Inventory API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ---------------- HEALTH CHECK ----------------

@app.get("/api/health")
def health_check():
    return {"status": "ok"}


# ---------------- AUTHENTICATION ----------------

@app.post(
    "/api/auth/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    data: UserRegister,
    db: Session = Depends(get_db),
):
    user = User(
        username=data.username,
        email=str(data.email).lower(),
        hashed_password=hash_password(data.password),
        role="user",
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    return user


@app.post("/api/auth/login", response_model=TokenResponse)
def login_user(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    email = str(data.email).lower()

    user = db.query(User).filter(User.email == email).first()

    if user is None or not verify_password(
        data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user.id, user.role)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


# ---------------- VEHICLE CREATION ----------------

@app.post(
    "/api/vehicles",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_vehicle = models.Vehicle(**vehicle.model_dump())

    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle


# ---------------- LIST VEHICLES ----------------

@app.get("/api/vehicles", response_model=list[VehicleResponse])
def list_vehicles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(models.Vehicle)
        .order_by(models.Vehicle.id)
        .all()
    )


# ---------------- SEARCH VEHICLES ----------------

@app.get(
    "/api/vehicles/search",
    response_model=list[VehicleResponse],
)
def search_vehicles(
    make: str | None = None,
    model: str | None = None,
    category: str | None = None,
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=422,
            detail="min_price cannot exceed max_price",
        )

    query = db.query(models.Vehicle)

    if make:
        query = query.filter(
            models.Vehicle.make.ilike(f"%{make}%")
        )

    if model:
        query = query.filter(
            models.Vehicle.model.ilike(f"%{model}%")
        )

    if category:
        query = query.filter(
            models.Vehicle.category.ilike(f"%{category}%")
        )

    if min_price is not None:
        query = query.filter(
            models.Vehicle.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            models.Vehicle.price <= max_price
        )

    return query.order_by(models.Vehicle.id).all()


# ---------------- UPDATE VEHICLE ----------------

@app.put(
    "/api/vehicles/{vehicle_id}",
    response_model=VehicleResponse,
)
def update_vehicle(
    vehicle_id: int,
    vehicle: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_vehicle = (
        db.query(models.Vehicle)
        .filter(models.Vehicle.id == vehicle_id)
        .first()
    )

    if db_vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    for field, value in vehicle.model_dump().items():
        setattr(db_vehicle, field, value)

    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle


# ---------------- DELETE VEHICLE: ADMIN ONLY ----------------

@app.delete(
    "/api/vehicles/{vehicle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    db_vehicle = (
        db.query(models.Vehicle)
        .filter(models.Vehicle.id == vehicle_id)
        .first()
    )

    if db_vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    db.delete(db_vehicle)
    db.commit()


# ---------------- PURCHASE VEHICLE ----------------

@app.post(
    "/api/vehicles/{vehicle_id}/purchase",
    response_model=VehicleResponse,
)
def purchase_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_vehicle = (
        db.query(models.Vehicle)
        .filter(models.Vehicle.id == vehicle_id)
        .with_for_update()
        .first()
    )

    if db_vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    if db_vehicle.quantity <= 0:
        raise HTTPException(
            status_code=409,
            detail="Vehicle out of stock",
        )

    db_vehicle.quantity -= 1
    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle


# ---------------- RESTOCK VEHICLE: ADMIN ONLY ----------------

@app.post(
    "/api/vehicles/{vehicle_id}/restock",
    response_model=VehicleResponse,
)
def restock_vehicle(
    vehicle_id: int,
    request: RestockRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    db_vehicle = (
        db.query(models.Vehicle)
        .filter(models.Vehicle.id == vehicle_id)
        .first()
    )

    if db_vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    db_vehicle.quantity += request.quantity
    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle
@app.post("/api/auth/setup-admin", response_model=UserResponse)
def setup_admin(
    data: UserRegister,
    x_setup_key: str = Header(...),
    db: Session = Depends(get_db),
):
    setup_key = os.getenv("ADMIN_SETUP_KEY")

    if not setup_key or not secrets.compare_digest(x_setup_key, setup_key):
        raise HTTPException(status_code=403, detail="Invalid setup key")

    # Allow admin setup only when no administrator exists.
    if db.query(User).filter(User.role == "admin").first():
        raise HTTPException(
            status_code=409,
            detail="An administrator already exists",
        )

    if db.query(User).filter(
        (User.username == data.username) | (User.email == data.email)
    ).first():
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    admin = User(
        username=data.username,
        email=str(data.email),
        hashed_password=hash_password(data.password),
        role="admin",
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin
