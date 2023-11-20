from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from typing import Annotated
from schemas import CompraBase
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import uvicorn

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", include_in_schema=False)
async def documentacion():
    return RedirectResponse(url="/docs")

@app.post("/crear_compra")
async def crear_compra(compra: CompraBase, db: db_dependency):
    
    precios_productos = {
        1: 1000,
        2: 2000,
        3: 3000,
        4: 4000,
        5: 5000
    }
    
    totalProductos = sum(precios_productos[producto.idProducto]*producto.cantidad for producto in compra.productos)
    
    nueva_compra = models.Compra(
        idUsuario = compra.idUsuario,
        total = totalProductos
    )
    
    db.add(nueva_compra)
    db.commit()
    db.refresh(nueva_compra)
    
    for producto in compra.productos:
        item_compra = models.DetallesCompra(
            idCompra = nueva_compra.idCompra,
            idProducto = producto.idProducto,
            cantidad = producto.cantidad,
            precio = precios_productos[producto.idProducto]
        )
        db.add(item_compra)
    
    db.commit()
    
    return {"respuesta": "Compra registrada correctamente.",
            "idCompra": nueva_compra.idCompra}

@app.get("/listar_compras")
async def listar_compras(db: db_dependency):
    result = db.query(models.Compra).all()
    return result

@app.get("/compras_usuario/{idUsuario}")
async def compras_por_usuario(id_usuario: int, db: db_dependency):
    compras = db.query(models.Compra).filter(models.Compra.idUsuario == id_usuario).all()
    if not compras:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o no tiene compras.")
    return compras

@app.get("/detalles_compra/{idCompra}")
async def detalles_compra(id_compra: int, db: db_dependency):
    items = db.query(models.DetallesCompra).filter(models.DetallesCompra.idCompra == id_compra).all()
    if not items:
        raise HTTPException(status_code=404, detail="Compra no registrada.")
    return items

