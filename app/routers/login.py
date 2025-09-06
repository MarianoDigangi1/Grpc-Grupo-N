from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    user = crud.autenticar_usuario(db, request.usuario_o_email, request.clave)

    if isinstance(user, dict) and "error" in user:
        return {"mensaje": user["error"]}

    return {
        "mensaje": f"Bienvenido {user.nombre} {user.apellido}",
        "nombreUsuario": user.nombreUsuario,
        "emailUnico": user.emailUnico,
        "rol": user.rol
    }