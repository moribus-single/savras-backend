from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

dbpass = config("DATABASE_PASSWORD")
dbname = config("DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{dbpass}@localhost/{dbname}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
