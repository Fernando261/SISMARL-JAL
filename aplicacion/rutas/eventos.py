from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from aplicacion.base_datos.conexion import get_db
from aplicacion.modelos.evento_modelo import Evento
from aplicacion.modelos.vehiculo_modelo import Vehiculo
from aplicacion.modelos.ruta_modelo import Ruta
from aplicacion.esquemas.flota_schema import EventoRegistrarIn
from aplicacion.inteligencia.motor_inferencia import evaluar_evento
from aplicacion.seguridad.dependencias import get_current_user

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.post("/registrar", status_code=201)
def registrar_evento(
    payload: EventoRegistrarIn,
    db: Session = Depends(get_db),
    _user = Depends(get_current_user)  # cualquier usuario logueado
):
    try:
        # Validaciones básicas: existen vehiculo y ruta
        if not db.query(Vehiculo).filter(Vehiculo.id == payload.vehiculo_id).first():
            raise HTTPException(status_code=404, detail="Vehículo no existe")
        if not db.query(Ruta).filter(Ruta.id == payload.ruta_id).first():
            raise HTTPException(status_code=404, detail="Ruta no existe")

        ev = Evento(
            vehiculo_id=payload.vehiculo_id,
            ruta_id=payload.ruta_id,
            tipo_evento=payload.tipo_evento.strip().upper(),
            descripcion=payload.descripcion.strip(),
        )
        db.add(ev)
        db.commit()
        db.refresh(ev)

        evaluacion = evaluar_evento(ev.tipo_evento)

        return {
            "mensaje": "Evento registrado",
            "id": ev.id,
            "evaluacion_ia": evaluacion
        }

    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Datos inválidos para registrar evento")
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error interno al registrar evento")

@router.get("/")
def listar_eventos(
    db: Session = Depends(get_db),
    _user = Depends(get_current_user)
):
    return db.query(Evento).all()