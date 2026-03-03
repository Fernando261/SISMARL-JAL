from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .base import Base

class Ruta(Base):
    __tablename__ = "rutas"

    id = Column(Integer, primary_key=True, index=True)
    origen = Column(String(120), nullable=False)
    destino = Column(String(120), nullable=False)
    distancia_km = Column(Float, nullable=False)
    riesgo_estimado = Column(String(20), nullable=False, default="MEDIO")

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())