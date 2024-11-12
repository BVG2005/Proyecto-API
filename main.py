from fastapi import FastAPI
from app.routes import routes
from app.config.database import engine, Base
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Borrar y recrear las tablas
try:
    Base.metadata.drop_all(bind=engine)  # Elimina todas las tablas
    Base.metadata.create_all(bind=engine)  # Recrea las tablas
    logger.info("Base de datos reinicializada correctamente")
except Exception as e:
    logger.error(f"Error al reinicializar la base de datos: {str(e)}")

app = FastAPI(
    title="Veterinaria San Miguel",
    description="API para gestión de veterinaria",
    version="1.0.0"
)

app.include_router(routes.router) 