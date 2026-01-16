import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://mlops:mlops@db:5432/mlopsdb")
DISABLE_DB = os.getenv("DISABLE_DB", "false").lower() == "true"

engine = None
SessionLocal = None
Base = declarative_base()

def init_db():
    global engine, SessionLocal
    if DISABLE_DB:
        return
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Import models to create tables
    from app.models import PredictionLog  # noqa: F401
    Base.metadata.create_all(bind=engine)

def get_session():
    if DISABLE_DB:
        yield None
        return
    global SessionLocal, engine
    if engine is None or SessionLocal is None:
        try:
            init_db()
        except OperationalError:
            yield None
            return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
