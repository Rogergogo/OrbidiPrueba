from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: MOVE TO .env
DATABASE_URL = "sqlite:///./db_local.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Get DB Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
