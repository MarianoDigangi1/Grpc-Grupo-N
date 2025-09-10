from sqlalchemy import Column, Integer, String, Boolean, Enum
from .database import Base
import enum

class RolEnum(str, enum.Enum):
    Presidente = "Presidente"
    Vocal = "Vocal"
    Coordinador = "Coordinador"
    Voluntario = "Voluntario"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombreUsuario = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    telefono = Column(String(20))
    clave = Column(String(255), nullable=False) 
    emailUnico = Column(String(100), unique=True, nullable=False)
    rol = Column(Enum(RolEnum), nullable=False)
    estaActivo = Column(Boolean, default=True, nullable=False)