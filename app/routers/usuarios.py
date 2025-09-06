from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Crear usuario
@router.post("/", response_model=schemas.UsuarioResponse)
def crear(usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    return crud.crear_usuario(db, usuario)

# Listar usuarios
@router.get("/", response_model=list[schemas.UsuarioResponse])
def listar(db: Session = Depends(database.get_db)):
    return crud.obtener_usuarios(db)

# Modificar usuario
@router.put("/{user_id}", response_model=schemas.UsuarioResponse)
def modificar(user_id: int, datos: schemas.UsuarioBase, db: Session = Depends(database.get_db)):
    return crud.modificar_usuario(db, user_id, datos)

# Dar de baja (inactivo)
@router.delete("/{user_id}", response_model=schemas.UsuarioResponse)
def baja(user_id: int, db: Session = Depends(database.get_db)):
    return crud.baja_usuario(db, user_id)