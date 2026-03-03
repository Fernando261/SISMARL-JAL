from fastapi import FastAPI
from aplicacion.base_datos.conexion import motor
from aplicacion.modelos.base import Base

from aplicacion.rutas.usuarios import router as usuarios_router
from aplicacion.rutas.rutas_logisticas import router as rutas_router
from aplicacion.rutas.eventos import router as eventos_router
from aplicacion.rutas.vehiculos import router as vehiculos_router

app = FastAPI(title="SISMARL-JAL")

Base.metadata.create_all(bind=motor)

app.include_router(usuarios_router)
app.include_router(rutas_router)
app.include_router(eventos_router)
app.include_router(vehiculos_router)

@app.get("/")
def inicio():
    return {"mensaje": "Sistema SISMARL-JAL funcionando correctamente"}