"""
=====================================================
Módulo: usuarios.py
Descripción:
    API de gestión de usuarios con autenticación segura.
=====================================================
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from aplicacion.seguridad.configuracion_logs import obtener_logger
from aplicacion.seguridad.autenticacion import crear_token, verificar_password, hash_password
from aplicacion.base_datos.conexion import get_db
from aplicacion.modelos.usuario_modelo import Usuario
from aplicacion.esquemas.usuarios_schema import UsuarioRegistroIn, UsuarioLoginIn, TokenOut

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
logger = obtener_logger()


# ===============================
# REGISTRO DE USUARIO (JSON BODY)
# ===============================
@router.post("/registro", status_code=201)
def registrar_usuario(payload: UsuarioRegistroIn, db: Session = Depends(get_db)):
    try:
        # Normaliza correo (evita duplicados raros por mayúsculas/espacios)
        correo = payload.correo.strip().lower()
        nombre = payload.nombre.strip()

        usuario_existente = db.query(Usuario).filter(Usuario.correo == correo).first()
        if usuario_existente:
            raise HTTPException(status_code=400, detail="El usuario ya existe")

        nuevo_usuario = Usuario(
            nombre=nombre,
            correo=correo,
            password_hash=hash_password(payload.password),
            rol_id=3  # Operador por defecto
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        logger.info(f"Nuevo usuario registrado: {correo}")
        return {"mensaje": "Usuario registrado correctamente", "id": nuevo_usuario.id}

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="No se pudo registrar (posible correo duplicado)")
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error en registro: {e}")
        raise HTTPException(status_code=500, detail="Error interno al registrar usuario")


# ===============================
# LOGIN SEGURO (JSON BODY)
# ===============================
@router.post("/login", response_model=TokenOut)
def login(payload: UsuarioLoginIn, db: Session = Depends(get_db)):
    try:
        correo = payload.correo.strip().lower()
        password = payload.password

        usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
        if not usuario:
            logger.warning(f"Intento login con usuario inexistente: {correo}")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        ahora = datetime.now(timezone.utc)

        # Bloqueo temporal (si existe y sigue vigente)
        if getattr(usuario, "bloqueado_hasta", None) and usuario.bloqueado_hasta > ahora:
            raise HTTPException(status_code=403, detail="Cuenta bloqueada temporalmente. Intenta más tarde.")

        # Si ya pasó el bloqueo temporal, limpia estado
        if getattr(usuario, "bloqueado_hasta", None) and usuario.bloqueado_hasta <= ahora:
            usuario.bloqueado = False
            usuario.bloqueado_hasta = None
            usuario.intentos_fallidos = 0
            db.commit()

        if usuario.bloqueado:
            raise HTTPException(status_code=403, detail="Cuenta bloqueada")

        if not verificar_password(password, usuario.password_hash):
            usuario.intentos_fallidos += 1

            if usuario.intentos_fallidos >= 5:
                usuario.bloqueado = True
                # Requiere que exista la columna bloqueado_hasta en la tabla
                usuario.bloqueado_hasta = ahora + timedelta(minutes=10)
                logger.error(f"Cuenta bloqueada por fuerza bruta: {correo}")

            db.commit()
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        # Login correcto: reset
        usuario.intentos_fallidos = 0
        usuario.bloqueado = False
        if hasattr(usuario, "bloqueado_hasta"):
            usuario.bloqueado_hasta = None
        db.commit()

        token = crear_token({"sub": usuario.correo, "rol": usuario.rol_id})
        logger.info(f"Login exitoso: {correo}")

        return {"access_token": token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.exception(f"Error en login: {e}")
        raise HTTPException(status_code=500, detail="Error interno al iniciar sesión")