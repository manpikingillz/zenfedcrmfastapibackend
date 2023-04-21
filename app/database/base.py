from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import databases


# Database configuration
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/zenfed_db"

# create a database instance
database = databases.Database(DATABASE_URL)

# create database engine
engine = create_engine(DATABASE_URL)

# define a base class for SQLAlchemy models
Base = declarative_base()
