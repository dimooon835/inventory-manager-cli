import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")

if DATABASE_URI is None:
    raise RuntimeError("DATABASE_URI не найден.")

engine = create_engine(
    DATABASE_URI,
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()