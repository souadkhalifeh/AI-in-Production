from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse


router = APIRouter()


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201
)
def create_user(
    request: UserCreate,
    db: Session = Depends(get_db)
):
    user = User(
        name=request.name,
        email=request.email
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="User email already exists."
        )

    return user


@router.get(
    "/users",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    statement = select(User).order_by(User.id)

    return db.scalars(statement).all()