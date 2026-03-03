from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

URL_BASE_DATOS = os.getenv("URL_BASE_DATOS")

motor = create_engine(
    URL_BASE_DATOS,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

def get_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()