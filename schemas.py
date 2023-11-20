from pydantic import BaseModel
from datetime import datetime
from typing import List, Tuple

""" class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    contrasenia: str
    telefono: str
    tipo: int

class UsuarioActualizado(BaseModel):
    nombre: str = None
    correo: str = None
    contrasenia: str = None
    telefono: str = None
    tipo: int = None """

class ItemCompra(BaseModel):
    idProducto: int
    cantidad: int

class CompraBase(BaseModel):
    idUsuario: int
    fecha: datetime = datetime.now
    productos: List[ItemCompra]