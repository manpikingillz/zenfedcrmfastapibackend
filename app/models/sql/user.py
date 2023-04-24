from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Boolean
from app.database.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    disabled = Column(Boolean)


def get_user(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()
