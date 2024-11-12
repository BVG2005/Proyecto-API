from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas import schemas
from app.services.service import Service
from app.repositories.repository import Repository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Rutas para Clientes
@router.post("/clientes/", response_model=schemas.Cliente, tags=["Clientes"])
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    repository = Repository(db)
    service = Service(repository)
    return service.create_cliente(cliente)

@router.get("/clientes/", response_model=list[schemas.Cliente], tags=["Clientes"])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repository = Repository(db)
    service = Service(repository)
    return service.get_clientes(skip=skip, limit=limit)

@router.get("/clientes/{cliente_id}", response_model=schemas.Cliente, tags=["Clientes"])
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    repository = Repository(db)
    service = Service(repository)
    cliente = service.get_cliente(cliente_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.put("/clientes/{cliente_id}", response_model=schemas.Cliente, tags=["Clientes"])
def actualizar_cliente(cliente_id: int, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    repository = Repository(db)
    service = Service(repository)
    return service.update_cliente(cliente_id, cliente)

@router.delete("/clientes/{cliente_id}", tags=["Clientes"])
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    repository = Repository(db)
    service = Service(repository)
    service.delete_cliente(cliente_id)
    return {"mensaje": "Cliente eliminado"}

@router.post("/clientes/bulk/", 
    response_model=List[schemas.Cliente], 
    tags=["Clientes"],
    status_code=status.HTTP_201_CREATED)
async def crear_multiples_clientes(
    clientes: schemas.ClientesMultiples,
    db: Session = Depends(get_db)
):
    try:
        repository = Repository(db)
        service = Service(repository)
        return service.create_multiple_clientes(clientes.clientes)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear los clientes: {str(e)}"
        )

# Rutas para Mascotas
@router.post("/mascotas/", 
    response_model=schemas.Mascota, 
    tags=["Mascotas"],
    status_code=status.HTTP_201_CREATED)
def crear_mascota(
    mascota: schemas.MascotaCreate,
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Intentando crear mascota: {mascota.nombre}")
        repository = Repository(db)
        service = Service(repository)
        return service.create_mascota(mascota)
    except HTTPException as e:
        logger.error(f"Error HTTP: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la mascota: {str(e)}"
        )

@router.get("/mascotas/", response_model=list[schemas.Mascota], tags=["Mascotas"])
def listar_mascotas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repository = Repository(db)
    service = Service(repository)
    return service.get_mascotas(skip=skip, limit=limit)

# ... rutas similares para actualizar y eliminar mascotas ...

# Rutas para Citas
@router.post("/citas/", response_model=schemas.Cita, tags=["Citas"])
def crear_cita(cita: schemas.CitaCreate, db: Session = Depends(get_db)):
    repository = Repository(db)
    service = Service(repository)
    return service.create_cita(cita)

@router.get("/citas/", response_model=list[schemas.Cita], tags=["Citas"])
def listar_citas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repository = Repository(db)
    service = Service(repository)
    return service.get_citas(skip=skip, limit=limit)

# ... rutas similares para actualizar y eliminar citas ...

# Rutas para Medicamentos
@router.post("/medicamentos/", response_model=schemas.Medicamento, tags=["Medicamentos"])
def crear_medicamento(medicamento: schemas.MedicamentoCreate, db: Session = Depends(get_db)):
    repository = Repository(db)
    service = Service(repository)
    return service.create_medicamento(medicamento)

@router.get("/medicamentos/", response_model=list[schemas.Medicamento], tags=["Medicamentos"])
def listar_medicamentos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repository = Repository(db)
    service = Service(repository)
    return service.get_medicamentos(skip=skip, limit=limit)

# ... rutas similares para actualizar y eliminar medicamentos ...