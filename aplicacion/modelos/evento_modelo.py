from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from aplicacion.modelos.base import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)

    vehiculo_id = Column(Integer, ForeignKey("vehiculos.id"), nullable=False)
    ruta_id = Column(Integer, ForeignKey("rutas.id"), nullable=False)

    tipo_evento = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=False)

    fecha_evento = Column("fecha_evento", DateTime, server_default=func.now(), nullable=False)