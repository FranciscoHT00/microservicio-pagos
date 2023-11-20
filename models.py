from sqlalchemy import Column, Integer, String, DateTime, Double, ForeignKey
from datetime import datetime
from database import Base

""" class Usuario(Base):
    __tablename__  = 'Usuario'
    
    idUsuario = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String)
    correo = Column(String, unique=True, index=True)
    contrasenia = Column(String)    
    telefono = Column(String)
    tipo = Column(Integer) """

class Compra(Base):
    __tablename__ = 'Compra'
    
    idCompra = Column(Integer, primary_key=True, autoincrement=True, index=True)
    idUsuario = Column(Integer, index=True)
    fecha = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    total = Column(Double)

class DetallesCompra(Base):
    __tablename__ = 'DetallesCompra'
    
    idCompra = Column(Integer, ForeignKey("Compra.idCompra"), primary_key=True, index=True)
    idProducto = Column(Integer, primary_key=True)
    cantidad = Column(Integer)
    precio = Column(Double)
