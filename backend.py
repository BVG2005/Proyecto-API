from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos para Cliente
class Cliente(BaseModel):
    nombre: str
    apellido: str
    telefono: str
    email: str
    id: int

# Modelo de datos para Cita
class Cita(BaseModel):
    id: int
    fecha: str
    cliente_id: int
    motivo: str

# Modelo de datos para Medicamento
class Medicamento(BaseModel):
    nombre: str
    descripcion: str
    stock: int
    precio: float

# Datos de ejemplo
clientes_demo = [
    {
        "nombre": "Juan",
        "apellido": "Pérez",
        "telefono": "555-0101",
        "email": "juan@ejemplo.com",
        "id": 1
    },
    {
        "nombre": "María",
        "apellido": "García",
        "telefono": "555-0102",
        "email": "maria@ejemplo.com",
        "id": 2
    },
    {
        "nombre": "Carlos",
        "apellido": "López",
        "telefono": "555-0103",
        "email": "carlos@ejemplo.com",
        "id": 3
    }
]

citas_demo = [
    {"id": 1, "fecha": "2023-10-01", "cliente_id": 1, "motivo": "Consulta general"},
    {"id": 2, "fecha": "2023-10-02", "cliente_id": 2, "motivo": "Vacunación"},
]

medicamentos_demo = [
    {"nombre": "Antibiótico", "descripcion": "Medicamento para infecciones bacterianas", "stock": 10, "precio": 10.0},
    {"nombre": "Antiinflamatorio", "descripcion": "Medicamento para reducir la inflamación", "stock": 15, "precio": 15.0},
]

@app.get("/clientes/", response_model=List[Cliente])
async def get_clientes(skip: int = 0, limit: int = 100):
    return clientes_demo[skip : skip + limit]

@app.post("/clientes/", response_model=Cliente)
async def create_cliente(cliente: Cliente):
    # Aquí deberías agregar la lógica para guardar el cliente en tu base de datos
    clientes_demo.append(cliente.dict())  # Solo para demostración
    return cliente

@app.post("/mascotas/", response_model=dict)
async def create_mascota(mascota: dict):
    # Aquí deberías agregar la lógica para guardar la mascota en tu base de datos
    # Por simplicidad, solo se devuelve el objeto
    return mascota

@app.get("/citas/", response_model=List[Cita])
async def get_citas(skip: int = 0, limit: int = 100):
    return citas_demo[skip: skip + limit]

@app.get("/medicamentos/", response_model=List[Medicamento])
async def get_medicamentos(skip: int = 0, limit: int = 100):
    return medicamentos_demo[skip: skip + limit]

@app.post("/citas/", response_model=Cita)
async def create_cita(cita: Cita):
    # Aquí deberías agregar la lógica para guardar la cita en tu base de datos
    citas_demo.append(cita.dict())  # Solo para demostración
    return cita

@app.delete("/clientes/{cliente_id}", response_model=dict)
async def delete_cliente(cliente_id: int):
    global clientes_demo  # Asegúrate de que estás usando la lista global
    for cliente in clientes_demo:
        if cliente['id'] == cliente_id:
            clientes_demo.remove(cliente)
            return {"message": "Cliente eliminado exitosamente"}
    return {"error": "Cliente no encontrado"}, 404