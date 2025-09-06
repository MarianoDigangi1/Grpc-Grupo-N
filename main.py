from fastapi import FastAPI
from app.routers import usuarios, login
from app.database import Base, engine

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestión de Usuarios")

app.include_router(usuarios.router)

app.include_router(login.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a la API de Gestión de Usuarios"}