from sqlalchemy.orm import Session
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.models import User
from app.schemas.schemas import UserCreate


def register_user(db: Session, data: UserCreate):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ValueError("Email already registered")
    user = User(email=data.email, hashed_password=get_password_hash(data.password), full_name=data.full_name)
    db.add(user)
    db.commit()
    return user


def login_user(db: Session, email: str, password: str) -> str:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid email or password")
    return create_access_token(str(user.id))
