"""
Archivo: base_datos.py
Configura la conexión segura a MySQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

URL_BASE_DATOS = os.getenv("URL_BASE_DATOS")

motor = create_engine(
    URL_BASE_DATOS,
    pool_pre_ping=True
)

SesionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=motor
)

Base = declarative_base()

def obtener_sesion():
    sesion = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()
