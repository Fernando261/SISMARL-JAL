from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from aplicacion.base_datos.conexion import get_db
from aplicacion.modelos.ruta_modelo import Ruta
from aplicacion.esquemas.flota_schema import RutaCrearIn
from aplicacion.seguridad.dependencias import get_current_user, require_roles

router = APIRouter(prefix="/rutas", tags=["Rutas"])

@router.post("/crear", status_code=201)
def crear_ruta(
    payload: RutaCrearIn,
    db: Session = Depends(get_db),
    _user = Depends(require_roles(1, 2))  # admin/supervisor
):
    try:
        r = Ruta(
            origen=payload.origen.strip(),
            destino=payload.destino.strip(),
            distancia_km=payload.distancia_km,
            riesgo_estimado=payload.riesgo_estimado.strip().upper()
        )
        db.add(r)
        db.commit()
        db.refresh(r)
        return {"mensaje": "Ruta creada", "id": r.id}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Datos inválidos")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al crear ruta")

@router.get("/")
def listar_rutas(
    db: Session = Depends(get_db),
    _user = Depends(get_current_user)
):
    return db.query(Ruta).all()