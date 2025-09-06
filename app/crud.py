from sqlalchemy.orm import Session
from . import models, schemas, utils

def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    clave = utils.generar_clave()
    hashed_clave = utils.encriptar_clave(clave)

    db_usuario = models.Usuario(
        nombreUsuario=usuario.nombreUsuario,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        telefono=usuario.telefono,
        clave=hashed_clave,
        emailUnico=usuario.emailUnico,
        rol=usuario.rol,
        estaActivo=True
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    utils.enviar_email(usuario.emailUnico, clave)

    return db_usuario

def obtener_usuarios(db: Session):
    return db.query(models.Usuario).all()

def modificar_usuario(db: Session, user_id: int, datos: schemas.UsuarioBase):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    if usuario:
        usuario.nombreUsuario = datos.nombreUsuario
        usuario.nombre = datos.nombre
        usuario.apellido = datos.apellido
        usuario.telefono = datos.telefono
        usuario.emailUnico = datos.emailUnico
        usuario.rol = datos.rol
        db.commit()
        db.refresh(usuario)
    return usuario

# Baja lógica (marcar inactivo)
def baja_usuario(db: Session, user_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    if usuario:
        usuario.estaActivo = False
        db.commit()
        db.refresh(usuario)
    return usuario


#Iniciar sesion
def autenticar_usuario(db: Session, usuario_o_email: str, clave: str):
    # Buscar por nombreUsuario o email
    user = db.query(models.Usuario).filter(
        (models.Usuario.nombreUsuario == usuario_o_email) |
        (models.Usuario.emailUnico == usuario_o_email)
    ).first()

    if not user:
        return {"error": "Usuario o email inexistente"}

    if not user.estaActivo:
        return {"error": "El usuario está inactivo"}

    # Verificar clave con bcrypt
    if not utils.verificar_clave(clave, user.clave):
        return {"error": "Credenciales incorrectas"}

    return user