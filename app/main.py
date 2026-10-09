from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import pandas as pd
import os
from app.database import SessionLocal, engine, get_db
from app import models

from pydantic import BaseModel, field_validator, model_validator
from typing import Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Alimentar Comunidad API - Nehuen Herrero")

def cargar_datos_iniciales():
    db = SessionLocal()
    if db.query(models.Comedor).count() == 0:
        ruta_clean = "data/clean.csv"
        ruta_sample = "data/sample_anonimo.csv"
        ruta = ruta_clean if os.path.exists(ruta_clean) else ruta_sample
        df = pd.read_csv(ruta)
        df = df[df["ratio"] <= 1000]
        for _, row in df.iterrows():
            c = models.Comedor(
                provincia=row["provincia"],
                barrio_anonimo=row["barrio_anonimo"],
                tipo_comedor=row["tipo_comedor"],
                capacidad_viandas=int(row["capacidad_viandas"]),
                voluntarios=int(row["voluntarios"]),
                ratio=int(row["ratio"]),
                estado="activo"
            )
            db.add(c)
        db.commit()
        print(f"Cargados {len(df)} comedores desde {ruta}")
    db.close()

cargar_datos_iniciales()

@app.get("/")
def hola():
    return {"mensaje": "API Alimentar Comunidad con DB SQL", "registros": "cargados desde CSV anonimizado"}

@app.get("/comedores")
def listar_comedores(db: Session = Depends(get_db)):
    return db.query(models.Comedor).filter(models.Comedor.activo == True).all()

@app.get("/comedores/{provincia}")
def filtrar_por_provincia(provincia: str, db: Session = Depends(get_db)):
    return db.query(models.Comedor).filter(models.Comedor.provincia == provincia, models.Comedor.activo == True).all()

@app.delete("/comedores/{id}")
def soft_delete(id: int, db: Session = Depends(get_db)):
    comedor = db.query(models.Comedor).filter(models.Comedor.id == id).first()
    if not comedor:
        return {"error": "No encontrado"}
    comedor.activo = False
    db.commit()
    return {"mensaje": f"Comedor {id} desactivado (soft delete)", "trazabilidad": "preservada como en RENACOM"}



class ComedorCreate(BaseModel):
    provincia: str
    barrio_anonimo: str
    tipo_comedor: str = "Comunitario"
    capacidad_viandas: int
    voluntarios: int
    direccion: Optional[str] = None # campo extra para compatibilidad, no se guarda


    @model_validator(mode='after')
    def validar_ratio(self):
        if self.voluntarios > 0 and self.capacidad_viandas / self.voluntarios > 1000:
            raise ValueError('Ratio viandas/voluntarios > 1000 inconsistente - validacion RENACOM')
        return self

@app.post("/comedores", status_code=201)
def crear_comedor(comedor: ComedorCreate, db: Session = Depends(get_db)):
    ratio = comedor.capacidad_viandas // max(comedor.voluntarios, 1)
    nuevo = models.Comedor(
        provincia=comedor.provincia,
        barrio_anonimo=comedor.barrio_anonimo,
        tipo_comedor=comedor.tipo_comedor,
        capacidad_viandas=comedor.capacidad_viandas,
        voluntarios=comedor.voluntarios,
        ratio=ratio,
        estado="activo",
        activo=True
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo