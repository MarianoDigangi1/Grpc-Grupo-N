from sqlalchemy.orm import Session
from . import models, schemas, utils

########################################################################################################
########################################################################################################
# Crear usuario
########################################################################################################
########################################################################################################
def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    # Verificar si el nombreUsuario ya existe
    if db.query(models.Usuario).filter(models.Usuario.nombreUsuario == usuario.nombreUsuario).first():
        return "Error al crear usuario, el nombre de usuario ya existe"
    
    # Verificar si el email ya existe
    if db.query(models.Usuario).filter(models.Usuario.emailUnico == usuario.emailUnico).first():
        return "Error al crear el usuario, el email ya está registrado"

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
    
    # Enviar email con la clave generada
    utils.enviar_email(usuario.emailUnico, clave)

    return "Usuario creado correctamente"

def obtener_usuarios(db: Session):
    return db.query(models.Usuario).all()

########################################################################################################
########################################################################################################
# Modificar usuario
########################################################################################################
########################################################################################################
def modificar_usuario(db: Session, user_id: int, datos: schemas.UsuarioUpdate):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    print("Usuario a modificar:")
    print(usuario)
    if usuario:
        usuario.nombreUsuario = datos.nombreUsuario
        usuario.nombre = datos.nombre
        usuario.apellido = datos.apellido
        usuario.telefono = datos.telefono
        usuario.emailUnico = datos.emailUnico
        usuario.rol = datos.rol
        usuario.estaActivo = datos.estaActivo
        db.commit()
        db.refresh(usuario)
    return "Usuario modificado correctamente"

########################################################################################################
########################################################################################################
# Baja usuario (Baja lógica)
########################################################################################################
########################################################################################################
def baja_usuario(db: Session, user_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    
    if not usuario:
        return "Usuario no encontrado"
    
    if not usuario.estaActivo:
        return "El usuario ya está inactivo"

    usuario.estaActivo = False
    db.commit()
    db.refresh(usuario)
    return "Usuario dado de baja correctamente"


#Iniciar sesion
def autenticar_usuario(db: Session, identificador: str, clave: str):

    user = db.query(models.Usuario).filter(
        (models.Usuario.nombreUsuario == identificador) |
        (models.Usuario.emailUnico == identificador)
    ).first()

    if not user:
        return schemas.LoginResponse(
            mensaje="Usuario no encontrado",
            nombreUsuario="",
            emailUnico="",
            rol="")

    if not user.estaActivo:
        return schemas.LoginResponse(
            mensaje="Usuario inactivo. Contacte al administrador.",
            nombreUsuario=user.nombreUsuario,
            emailUnico=user.emailUnico,
            rol=user.rol)

    # Verificar clave con bcrypt
    if not utils.verificar_clave(clave, user.clave):
        return schemas.LoginResponse(
            mensaje="Credenciales incorrectas",
            nombreUsuario=user.nombreUsuario,
            emailUnico=user.emailUnico,
            rol=user.rol)

    return schemas.LoginResponse(
        mensaje="Inicio de sesión exitoso",
        nombreUsuario=user.nombreUsuario,
        emailUnico=user.emailUnico,
        rol=user.rol)
