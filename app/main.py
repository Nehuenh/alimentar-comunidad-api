from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import pandas as pd
import os
from app.database import SessionLocal, engine, get_db
from app import models

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