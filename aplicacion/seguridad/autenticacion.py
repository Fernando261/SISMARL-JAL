from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

CLAVE_SECRETA = os.getenv("CLAVE_SECRETA", "CAMBIAR")
ALGORITMO = os.getenv("ALGORITMO", "HS256")
MINUTOS_EXPIRACION = int(os.getenv("MINUTOS_EXPIRACION", "30"))

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(password: str, hash_guardado: str) -> bool:
    return pwd_context.verify(password, hash_guardado)

def crear_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, CLAVE_SECRETA, algorithm=ALGORITMO)