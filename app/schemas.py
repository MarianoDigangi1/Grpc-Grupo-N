from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

# Enumerado
class RolEnum(str, Enum):
    Presidente = "Presidente"
    Vocal = "Vocal"
    Coordinador = "Coordinador"
    Voluntario = "Voluntario"

#Base usuario
class UsuarioBase(BaseModel):
    nombreUsuario: str
    nombre: str
    apellido: str
    telefono: Optional[str]
    emailUnico: EmailStr
    rol: RolEnum


class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: int
    estaActivo: bool

    class Config:
        orm_mode = True

# Iniciar Sesion
class LoginRequest(BaseModel):
    usuario_o_email: str
    clave: str

class LoginResponse(BaseModel):
    mensaje: str
    nombreUsuario: str | None = None
    emailUnico: str | None = None
    rol: str | None = None