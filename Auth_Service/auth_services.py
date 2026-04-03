
from fastapi import FastAPI, APIRouter
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from schemas import UserRegister, UserLogin
from database import user_collection
from models import user_serializer

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT config
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)


# Verify password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# Generate JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Register User
@router.post("/register")
async def register_user(user: UserRegister):
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)

    result = await user_collection.insert_one(user_dict)
    new_user = await user_collection.find_one({"_id": result.inserted_id})

    return user_serializer(new_user)


# Login User
@router.post("/login")
async def login_user(user: UserLogin):
    db_user = await user_collection.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(db_user["_id"]),
        "email": db_user["email"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }