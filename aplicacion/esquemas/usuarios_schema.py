from pydantic import BaseModel, EmailStr, Field

class UsuarioRegistroIn(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    correo: EmailStr
    password: str = Field(min_length=6, max_length=128)

class UsuarioLoginIn(BaseModel):
    correo: EmailStr
    password: str = Field(min_length=6, max_length=128)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"