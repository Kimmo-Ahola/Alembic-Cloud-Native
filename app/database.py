import os
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+psycopg2://tasks:tasks@localhost:5432/tasks" 
    # tasks:tasks = user:password. 
    # /tasks = namnet på databasen
)

engine = create_engine(url=DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

NAMING_CONVENTION = { 
    "ix": "ix_%(column_0_label)s", 
    "uq": "uq_%(table_name)s_%(column_0_name)s", 
    "ck": "ck_%(table_name)s_%(constraint_name)s", 
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s", 
    "pk": "pk_%(table_name)s", 
} 

class Base(DeclarativeBase): 
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()