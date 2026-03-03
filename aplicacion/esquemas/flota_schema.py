from pydantic import BaseModel, Field

# ---------- Vehículos ----------
class VehiculoCrearIn(BaseModel):
    placa: str = Field(min_length=4, max_length=20)
    modelo: str = Field(min_length=2, max_length=100)
    capacidad_kg: int | None = Field(default=None, ge=0)

# ---------- Rutas ----------
class RutaCrearIn(BaseModel):
    origen: str = Field(min_length=2, max_length=120)
    destino: str = Field(min_length=2, max_length=120)
    distancia_km: float = Field(gt=0)
    riesgo_estimado: str = Field(default="MEDIO", max_length=20)

# ---------- Eventos ----------
class EventoRegistrarIn(BaseModel):
    vehiculo_id: int = Field(gt=0)
    ruta_id: int = Field(gt=0)
    tipo_evento: str = Field(min_length=3, max_length=50)
    descripcion: str = Field(min_length=3, max_length=255)