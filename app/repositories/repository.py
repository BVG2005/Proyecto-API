from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from app.models import models
from app.schemas import schemas
import logging
from datetime import date

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Repository:
    def __init__(self, db: Session):
        self.db = db

    def get_cliente(self, cliente_id: int):
        return self.db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

    def get_clientes(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.Cliente).offset(skip).limit(limit).all()

    def create_cliente(self, cliente: schemas.ClienteCreate):
        db_cliente = models.Cliente(**cliente.dict())
        self.db.add(db_cliente)
        self.db.commit()
        self.db.refresh(db_cliente)
        return db_cliente

    def update_cliente(self, cliente_id: int, cliente: schemas.ClienteCreate):
        db_cliente = self.get_cliente(cliente_id)
        if db_cliente:
            for key, value in cliente.dict().items():
                setattr(db_cliente, key, value)
            self.db.commit()
            self.db.refresh(db_cliente)
        return db_cliente

    def delete_cliente(self, cliente_id: int):
        db_cliente = self.get_cliente(cliente_id)
        if db_cliente:
            self.db.delete(db_cliente)
            self.db.commit()
        return db_cliente

    def create_multiple_clientes(self, clientes: List[schemas.ClienteCreate]):
        try:
            db_clientes = []
            for cliente in clientes:
                db_cliente = models.Cliente(
                    nombre=cliente.nombre,
                    apellido=cliente.apellido,
                    telefono=cliente.telefono,
                    email=cliente.email
                )
                self.db.add(db_cliente)
                db_clientes.append(db_cliente)
            
            self.db.commit()
            
            for cliente in db_clientes:
                self.db.refresh(cliente)
            
            return db_clientes
            
        except Exception as e:
            self.db.rollback()  # Revertir cambios en caso de error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en la base de datos: {str(e)}"
            )

    def create_mascota(self, mascota: schemas.MascotaCreate):
        try:
            # Primero verificamos si el cliente existe
            cliente = self.db.query(models.Cliente).filter(
                models.Cliente.id == mascota.cliente_id
            ).first()
            
            if not cliente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cliente con id {mascota.cliente_id} no encontrado"
                )

            # Creamos la mascota
            db_mascota = models.Mascota(
                nombre=mascota.nombre,
                especie=mascota.especie,
                raza=mascota.raza,
                edad=mascota.edad,
                cliente_id=mascota.cliente_id
            )
            
            self.db.add(db_mascota)
            self.db.commit()
            self.db.refresh(db_mascota)
            
            logger.info(f"Mascota creada exitosamente: {db_mascota.nombre}")
            return db_mascota
            
        except HTTPException as e:
            logger.error(f"Error HTTP: {str(e.detail)}")
            raise e
        except Exception as e:
            logger.error(f"Error al crear mascota: {str(e)}")
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear la mascota: {str(e)}"
            )

    def get_mascotas(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.Mascota).offset(skip).limit(limit).all()

    def get_mascota(self, mascota_id: int):
        return self.db.query(models.Mascota).filter(models.Mascota.id == mascota_id).first()

    def create_cita(self, cita: schemas.CitaCreate):
        db_cita = models.Cita(
            fecha=cita.fecha,
            motivo=cita.motivo,
            mascota_id=cita.mascota_id,
            hora=cita.hora
        )
        self.db.add(db_cita)
        self.db.commit()
        self.db.refresh(db_cita)
        return db_cita

    def get_cita_by_fecha(self, fecha: date):
        return self.db.query(models.Cita).filter(
            models.Cita.fecha == fecha
        ).first()

    def get_citas(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.Cita).offset(skip).limit(limit).all()

    def create_medicamento(self, medicamento: schemas.MedicamentoCreate):
        db_medicamento = models.Medicamento(
            nombre=medicamento.nombre,
            descripcion=medicamento.descripcion,
            stock=medicamento.stock,
            precio=medicamento.precio
        )
        self.db.add(db_medicamento)
        self.db.commit()
        self.db.refresh(db_medicamento)
        return db_medicamento

    def get_medicamentos(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.Medicamento).offset(skip).limit(limit).all()

    # Métodos similares para Mascota, Cita y Medicamento 