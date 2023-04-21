from sqlalchemy.orm import sessionmaker
from .base import engine


# Create a SessionLocal class with the database sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Define a dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
