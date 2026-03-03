from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .base import Base

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(20), unique=True, nullable=False, index=True)
    modelo = Column(String(100), nullable=False)
    capacidad_kg = Column(Integer, nullable=True)

    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())