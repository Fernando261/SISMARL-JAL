from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from aplicacion.base_datos.conexion import get_db
from aplicacion.modelos.usuario_modelo import Usuario

load_dotenv()

security = HTTPBearer()

CLAVE_SECRETA = os.getenv("CLAVE_SECRETA", "CAMBIAR")
ALGORITMO = os.getenv("ALGORITMO", "HS256")

def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    token = cred.credentials
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        correo = payload.get("sub")
        if not correo:
            raise HTTPException(status_code=401, detail="Token inválido (sin sub)")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no existe")

    if getattr(usuario, "bloqueado", False):
        raise HTTPException(status_code=403, detail="Cuenta bloqueada")

    return usuario

def require_roles(*roles_permitidos: int):
    """
    roles_permitidos: ids (ej. 1=admin, 2=supervisor, 3=operador)
    """
    def _check(user: Usuario = Depends(get_current_user)) -> Usuario:
        if user.rol_id not in roles_permitidos:
            raise HTTPException(status_code=403, detail="No autorizado para esta acción")
        return user
    return _check