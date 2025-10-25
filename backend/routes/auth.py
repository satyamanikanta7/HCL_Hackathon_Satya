from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.db.session import get_db
from backend.models.user import User
from backend.schemas.user import SignupRequest, SigninRequest, TokenResponse, UserRead
from backend.core.security import hash_password, verify_password, create_access_token
from backend.routes.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=TokenResponse)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    exists = db.execute(select(User).where(User.email == req.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=req.email, password_hash=hash_password(req.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(user.id)
    return TokenResponse(access_token=token)

@router.post("/signin", response_model=TokenResponse)
def signin(req: SigninRequest, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == req.email)).scalar_one_or_none()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.id)
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)):
    return user
