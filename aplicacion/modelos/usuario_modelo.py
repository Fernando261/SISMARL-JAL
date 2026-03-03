from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
from aplicacion.modelos.rol_modelo import Rol

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), nullable=False)
    correo = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    rol = relationship(Rol)

    intentos_fallidos = Column(Integer, default=0, nullable=False)
    bloqueado = Column(Boolean, default=False, nullable=False)
    bloqueado_hasta = Column(DateTime, nullable=True)

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())