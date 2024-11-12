from typing import List
from datetime import date
from pydantic import BaseModel

class CitaBase(BaseModel):
    fecha: date
    motivo: str
    mascota_id: int
    hora: str 

class CitaCreate(CitaBase):
    hora: str

class Cita(CitaBase):
    id: int
    hora: str
     

    class Config:
        orm_mode = True
# Medicamento Schemas
class MedicamentoBase(BaseModel):
    nombre: str
    descripcion: str
    stock: int
    precio: float

class MedicamentoCreate(MedicamentoBase):
    pass

class Medicamento(MedicamentoBase):
    id: int
    
    class Config:
        orm_mode = True

# Cliente Schemas
class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    email: str

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int
    
    class Config:
        orm_mode = True

# Clientes Multiples
class ClientesMultiples(BaseModel):
    clientes: list[ClienteCreate]

# Mascota Schemas
class MascotaBase(BaseModel):
    nombre: str
    especie: str
    raza: str
    edad: int
    cliente_id: int

class MascotaCreate(MascotaBase):
    pass

class Mascota(MascotaBase):
    id: int
    
    class Config:
        orm_mode = True
