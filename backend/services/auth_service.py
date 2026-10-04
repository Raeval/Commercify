from datetime import datetime, timedelta, timezone
import os
from sqlalchemy.orm import Session

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from passlib.context import CryptContext
import models

import jwt

from database import get_db

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 48

# Global variables
security = HTTPBearer(auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing authentication token")
    
    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.get(models.User, int(user_id))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def create_access_token(
        user_id: int,
    ):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(
            hours=ACCESS_TOKEN_EXPIRE_HOURS
        ),
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

def register(email, username, gender, password, db: Session):
    existing_user = (db.query(models.User)
                            .filter(models.User.email == email)
                            .first()
        )
    
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    new_user = models.User(
        username=username,
        email=email,
        gender=gender,
        hashed_password=pwd_context.hash(password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(new_user.user_id)

    return new_user, access_token

def sign_in(username, password, db: Session):
    user = (
        db.query(models.User)
            .filter(models.User.username == username)
            .first()
    )
    
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    access_token = create_access_token(user.user_id)
    return user, access_token