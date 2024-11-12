from app.repositories.repository import Repository
from app.schemas import schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
import re

class Service:
    def __init__(self, repository: Repository):
        self.repository = repository

    # Métodos para Clientes
    def create_cliente(self, cliente: schemas.ClienteCreate):
        return self.repository.create_cliente(cliente)

    def get_clientes(self, skip: int = 0, limit: int = 100):
        return self.repository.get_clientes(skip, limit)

    def get_cliente(self, cliente_id: int):
        return self.repository.get_cliente(cliente_id)

    def update_cliente(self, cliente_id: int, cliente: schemas.ClienteCreate):
        return self.repository.update_cliente(cliente_id, cliente)

    def delete_cliente(self, cliente_id: int):
        return self.repository.delete_cliente(cliente_id)

    def create_multiple_clientes(self, clientes: List[schemas.ClienteCreate]):
        try:
            return self.repository.create_multiple_clientes(clientes)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en el servicio: {str(e)}"
            )

    # Métodos para Mascotas
    def create_mascota(self, mascota: schemas.MascotaCreate):
        try:
            return self.repository.create_mascota(mascota)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error en el servicio al crear mascota: {str(e)}"
            )

    def get_mascotas(self, skip: int = 0, limit: int = 100):
        return self.repository.get_mascotas(skip, limit)

    def get_mascota(self, mascota_id: int):
        mascota = self.repository.get_mascota(mascota_id)
        if not mascota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mascota no encontrada"
            )
        return mascota

    # Métodos para Citas
    def create_cita(self, cita: schemas.CitaCreate):
        try:
            # Verificar si la mascota existe
            mascota = self.repository.get_mascota(cita.mascota_id)
            if not mascota:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Mascota no encontrada"
                )

            # Verificar si ya existe una cita en esa fecha
            cita_existente = self.repository.get_cita_by_fecha(cita.fecha)
            if cita_existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe una cita en esa fecha"
                )

            # Asegúrate de que la hora esté presente y en formato correcto
            if not cita.hora or not re.match(r'^\d{2}:\d{2}$', cita.hora):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La hora debe estar en formato HH:MM"
                )

            return self.repository.create_cita(cita)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear la cita: {str(e)}"
            )

    def get_citas(self, skip: int = 0, limit: int = 100):
        return self.repository.get_citas(skip, limit)

    # Métodos para Medicamentos
    def create_medicamento(self, medicamento: schemas.MedicamentoCreate):
        try:
            return self.repository.create_medicamento(medicamento)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear el medicamento: {str(e)}"
            )

    def get_medicamentos(self, skip: int = 0, limit: int = 100):
        return self.repository.get_medicamentos(skip, limit)

    # ... métodos similares para Medicamentos ...