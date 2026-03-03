from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from aplicacion.base_datos.conexion import get_db
from aplicacion.modelos.vehiculo_modelo import Vehiculo
from aplicacion.esquemas.flota_schema import VehiculoCrearIn
from aplicacion.seguridad.dependencias import get_current_user, require_roles

router = APIRouter(prefix="/vehiculos", tags=["Vehiculos"])

@router.post("/crear", status_code=201)
def crear_vehiculo(
    payload: VehiculoCrearIn,
    db: Session = Depends(get_db),
    _user = Depends(require_roles(1, 2))  # admin/supervisor
):
    try:
        v = Vehiculo(
            placa=payload.placa.strip().upper(),
            modelo=payload.modelo.strip(),
            capacidad_kg=payload.capacidad_kg
        )
        db.add(v)
        db.commit()
        db.refresh(v)
        return {"mensaje": "Vehículo creado", "id": v.id}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Placa duplicada o datos inválidos")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al crear vehículo")

@router.get("/")
def listar_vehiculos(
    db: Session = Depends(get_db),
    _user = Depends(get_current_user)  # cualquier usuario logueado
):
    return db.query(Vehiculo).all()