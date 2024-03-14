from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.env import ENV
from src.db.models import Base


engine = create_engine(str(ENV.db))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()


def create_tables() -> None:
    Base.metadata.create_all(engine)