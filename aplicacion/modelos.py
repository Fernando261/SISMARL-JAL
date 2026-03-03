"""
Archivo: modelos.py
Define las tablas del sistema.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base_datos import Base

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    hash_contrasena = Column(String(255), nullable=False)
    intentos_fallidos = Column(Integer, default=0)
    bloqueado_hasta = Column(DateTime, nullable=True)

    rol_id = Column(Integer, ForeignKey("roles.id"))
    rol = relationship("Rol")

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())


class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id = Column(Integer, primary_key=True, index=True)
    placa = Column(String(20), unique=True, nullable=False)
    modelo = Column(String(100), nullable=False)
    capacidad_kg = Column(Integer)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
