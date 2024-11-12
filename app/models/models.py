from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.config.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    telefono = Column(String(15))
    email = Column(String(50))
    mascotas = relationship("Mascota", back_populates="cliente")

class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    especie = Column(String(50))
    raza = Column(String(50))
    edad = Column(Integer)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    
    cliente = relationship("Cliente", back_populates="mascotas")
    citas = relationship("Cita", back_populates="mascota")

class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    motivo = Column(String(200))
    mascota_id = Column(Integer, ForeignKey("mascotas.id"))
    hora = Column(String(10))
    
    mascota = relationship("Mascota", back_populates="citas")

class Medicamento(Base):
    __tablename__ = "medicamentos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    descripcion = Column(String(200))
    stock = Column(Integer)
    precio = Column(Integer)