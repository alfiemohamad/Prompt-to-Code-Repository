from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import CreateUser, UserResponse

def create_user(db: Session, user: CreateUser) -> UserResponse:
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse.from_orm(db_user)

def get_user(db: Session, user_id: int) -> UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    return UserResponse.from_orm(db_user) if db_user else None

def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[UserResponse]:
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserResponse.from_orm(user) for user in users]

def update_user(db: Session, user_id: int, user_data: CreateUser) -> UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        for key, value in user_data.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return UserResponse.from_orm(db_user)
    return None

def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False